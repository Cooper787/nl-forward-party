#!/usr/bin/env python3

"""
NL Forward - Telegram Bot

Long-polling bot that handles callback buttons from respond.py.
Updates gov_posts status and queues approved responses.
"""

import asyncio
import os
from datetime import datetime, timedelta, timezone
from typing import Tuple

import httpx
from supabase import Client

from utils import (
    get_supabase,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    log,
    iso_now,
)

API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def parse_callback_data(data: str) -> Tuple[str, str]:
    """Parse callback data of form 'resp:ACTION:POST_ID'."""
    try:
        prefix, action, post_id = data.split(":", 2)
        if prefix != "resp":
            return "", ""
        return action, post_id
    except ValueError:
        return "", ""


async def telegram_get_updates(offset: int | None = None) -> list[dict]:
    params = {"timeout": 30}
    if offset is not None:
        params["offset"] = offset

    async with httpx.AsyncClient(timeout=35) as client:
        r = await client.get(f"{API_BASE}/getUpdates", params=params)
        if r.status_code != 200:
            log(f"❌ getUpdates error {r.status_code}: {r.text}")
            return []
        body = r.json()
        return body.get("result", [])


async def telegram_answer_callback_query(callback_query_id: str, text: str):
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(
            f"{API_BASE}/answerCallbackQuery",
            json={"callback_query_id": callback_query_id, "text": text},
        )


def approve_post(supabase: Client, post_id: str, mode: str = "auto") -> bool:
    """Mark gov_posts row approved, optionally enqueue the response for posting."""
    resp = (
        supabase.table("gov_posts")
        .select("*")
        .eq("id", post_id)
        .limit(1)
        .execute()
    )
    rows = resp.data or []
    if not rows:
        log(f"⚠️ approve_post: gov_posts id {post_id} not found")
        return False

    post = rows[0]
    suggested = post.get("our_response") or ""
    if not suggested.strip():
        log(f"⚠️ approve_post: no our_response text for {post_id}")
        return False

    update = {
        "response_status": "approved" if mode == "manual" else "queued",
        "responded_at": iso_now(),
    }
    supabase.table("gov_posts").update(update).eq("id", post_id).execute()

    if mode == "manual":
        return True

    # Auto: enqueue into content_queue for near-future posting
    scheduled_for = datetime.now(timezone.utc) + timedelta(minutes=10)
    queue_row = {
        "content_type": "gov_response",
        "twitter_text": suggested,
        "facebook_text": suggested,
        "instagram_text": suggested,
        "scheduled_for": scheduled_for.isoformat(),
        "posted": False,
        "created_at": iso_now(),
    }
    supabase.table("content_queue").insert(queue_row).execute()
    log(f"✅ Enqueued gov response from gov_posts {post_id}")
    return True


def update_status(supabase: Client, post_id: str, status: str):
    supabase.table("gov_posts").update(
        {"response_status": status, "responded_at": iso_now()}
    ).eq("id", post_id).execute()


async def handle_callback_query(supabase: Client, cq: dict):
    data = cq.get("data") or ""
    cq_id = cq.get("id")
    action, post_id = parse_callback_data(data)

    if not action or not post_id:
        log(f"⚠️ Unknown callback data: {data}")
        await telegram_answer_callback_query(cq_id, "Unknown action.")
        return

    log(f"Callback: {action} for post {post_id}")

    if action == "approve":
        ok = approve_post(supabase, post_id, mode="auto")
        text = "Approved and queued for posting." if ok else "Failed to approve."
        await telegram_answer_callback_query(cq_id, text)
    elif action == "manual":
        ok = approve_post(supabase, post_id, mode="manual")
        text = "Marked approved. Please post manually." if ok else "Failed to update."
        await telegram_answer_callback_query(cq_id, text)
    elif action == "skip":
        update_status(supabase, post_id, "skipped")
        await telegram_answer_callback_query(cq_id, "Skipped.")
    elif action == "later":
        update_status(supabase, post_id, "pending_later")
        await telegram_answer_callback_query(cq_id, "Saved for later.")
    else:
        await telegram_answer_callback_query(cq_id, "Unknown action.")


async def poll_updates():
    supabase = get_supabase()
    log("🤖 Telegram bot started (long polling).")

    offset = None
    while True:
        try:
            updates = await telegram_get_updates(offset)
        except Exception as e:
            log(f"❌ Error in getUpdates: {e}")
            await asyncio.sleep(5)
            continue

        for upd in updates:
            offset = upd["update_id"] + 1
            if "callback_query" in upd:
                await handle_callback_query(supabase, upd["callback_query"])

        await asyncio.sleep(1)


def main():
    asyncio.run(poll_updates())


if __name__ == "__main__":
    main()
