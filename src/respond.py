#!/usr/bin/env python3

"""
NL Forward - Response Handler

Finds relevant gov_posts with drafted responses and sends
approval requests to Telegram.

Intended to be run after monitor.py finishes a scan, or on a
schedule (e.g., every 2 hours in GitHub Actions).
"""

import asyncio
from textwrap import shorten

from supabase import Client

from utils import get_supabase, send_telegram_async, build_inline_keyboard, log


def fetch_pending_responses(supabase: Client) -> list[dict]:
    resp = (
        supabase.table("gov_posts")
        .select("*")
        .eq("response_status", "pending")
        .not_.is_("our_response", "null")
        .order("detected_at", asc=True)
        .limit(10)
        .execute()
    )
    return resp.data or []


async def send_approval_message(supabase: Client, post: dict):
    post_id = post["id"]
    text = post.get("post_text") or ""
    url = post.get("post_url") or ""
    suggestion = post.get("our_response") or ""
    score = post.get("relevance_score")

    preview = shorten(text, width=280, placeholder="…")
    suggestion_preview = shorten(suggestion, width=280, placeholder="…")

    score_str = f"{score:.2f}" if score is not None else "n/a"

    msg = (
        "🔔 <b>New government post detected</b>\n\n"
        f"<b>Source:</b> {post.get('account')} ({post.get('platform')})\n"
        f"<b>Relevance:</b> {score_str}\n\n"
        f"<b>Post:</b>\n{preview}\n\n"
        f"<b>Link:</b> {url}\n\n"
        "<b>Suggested response:</b>\n"
        f"{suggestion_preview}\n\n"
        "Choose:\n"
        "✅ Approve and post\n"
        "✏️ Approve (you will edit manually on platform)\n"
        "❌ Skip this one\n"
        "⏰ Save for later"
    )

    keyboard = build_inline_keyboard(
        [
            ("✅ Approve", f"resp:approve:{post_id}"),
            ("✏️ Approve (manual)", f"resp:manual:{post_id}"),
            ("❌ Skip", f"resp:skip:{post_id}"),
            ("⏰ Later", f"resp:later:{post_id}"),
        ]
    )

    await send_telegram_async(msg, reply_markup=keyboard)

    # Mark that we've requested approval, to avoid re-sending
    supabase.table("gov_posts").update(
        {"response_status": "pending"}
    ).eq("id", post_id).execute()


async def main_async():
    supabase = get_supabase()
    posts = fetch_pending_responses(supabase)

    if not posts:
        log("No pending responses to approve.")
        return 0

    log(f"Sending approval messages for {len(posts)} posts...")
    for post in posts:
        await send_approval_message(supabase, post)

    log("Done sending approvals.")
    return len(posts)


def main():
    return asyncio.run(main_async())


if __name__ == "__main__":
    main()
