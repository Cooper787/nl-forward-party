#!/usr/bin/env python3

"""
NL Forward - Buffer Queue

Reads upcoming posts from Supabase `content_queue` and creates
scheduled updates in Buffer for the next 7 days.

Assumptions:
- DB schema matches ARCHITECTURE.md (content_queue table).
- Env vars:
  - BUFFER_ACCESS_TOKEN
  - BUFFER_TWITTER_PROFILE_ID
  - BUFFER_FACEBOOK_PROFILE_ID
  - BUFFER_INSTAGRAM_PROFILE_ID
"""

import os
import sys
from datetime import datetime, timedelta, timezone

import httpx
from supabase import Client

from utils import (
    get_supabase,
    BUFFER_ACCESS_TOKEN,
    BUFFER_TWITTER_PROFILE_ID,
    BUFFER_FACEBOOK_PROFILE_ID,
    BUFFER_INSTAGRAM_PROFILE_ID,
    log,
    iso_now,
)


BUFFER_API_BASE = "https://api.bufferapp.com/1"


def require_buffer_config():
    if not BUFFER_ACCESS_TOKEN:
        print("❌ BUFFER_ACCESS_TOKEN is not set.", file=sys.stderr)
        sys.exit(1)
    if not any(
        [BUFFER_TWITTER_PROFILE_ID, BUFFER_FACEBOOK_PROFILE_ID, BUFFER_INSTAGRAM_PROFILE_ID]
    ):
        print("❌ At least one BUFFER_*_PROFILE_ID must be set.", file=sys.stderr)
        sys.exit(1)


def get_pending_posts(supabase: Client, days_ahead: int = 7) -> list[dict]:
    """Fetch posts scheduled in the next N days that are not yet marked posted."""
    now = datetime.now(timezone.utc)
    upper = now + timedelta(days=days_ahead)

    resp = (
        supabase.table("content_queue")
        .select("*")
        .eq("posted", False)
        .gte("scheduled_for", now.isoformat())
        .lte("scheduled_for", upper.isoformat())
        .order("scheduled_for", asc=True)
        .execute()
    )
    return resp.data or []


def buffer_create_update(
    profile_id: str,
    text: str,
    scheduled_for: datetime,
) -> bool:
    """Create a scheduled update in Buffer."""
    if not text or not text.strip():
        return False

    payload = {
        "profile_ids[]": profile_id,
        "text": text,
        "scheduled_at": scheduled_for.replace(tzinfo=timezone.utc).isoformat(),
        "now": False,
        "shorten": False,
        "access_token": BUFFER_ACCESS_TOKEN,
    }

    try:
        with httpx.Client(timeout=10) as client:
            r = client.post(f"{BUFFER_API_BASE}/updates/create.json", data=payload)
        if r.status_code != 200:
            log(f"❌ Buffer API error {r.status_code}: {r.text}")
            return False
        body = r.json()
        if not body.get("success"):
            log(f"❌ Buffer reported failure: {body}")
            return False
        return True
    except Exception as e:
        log(f"❌ Exception calling Buffer: {e}")
        return False


def queue_posts(supabase: Client, posts: list[dict]) -> int:
    """Queue posts for all configured profiles; mark as posted once queued."""
    queued_count = 0
    for post in posts:
        scheduled_for = datetime.fromisoformat(post["scheduled_for"])
        twitter_text = post.get("twitter_text") or ""
        facebook_text = post.get("facebook_text") or ""
        instagram_text = post.get("instagram_text") or twitter_text

        success_any = False

        # Twitter
        if BUFFER_TWITTER_PROFILE_ID and twitter_text:
            if buffer_create_update(BUFFER_TWITTER_PROFILE_ID, twitter_text, scheduled_for):
                success_any = True

        # Facebook
        if BUFFER_FACEBOOK_PROFILE_ID and facebook_text:
            if buffer_create_update(BUFFER_FACEBOOK_PROFILE_ID, facebook_text, scheduled_for):
                success_any = True

        # Instagram
        if BUFFER_INSTAGRAM_PROFILE_ID and instagram_text:
            if buffer_create_update(BUFFER_INSTAGRAM_PROFILE_ID, instagram_text, scheduled_for):
                success_any = True

        if success_any:
            # For now, treat "queued in Buffer" as "posted = TRUE" with posted_at ~ queue time.
            supabase.table("content_queue").update(
                {"posted": True, "posted_at": iso_now()}
            ).eq("id", post["id"]).execute()
            queued_count += 1
            log(f"✅ Queued post {post['id']} for {scheduled_for.isoformat()}")
        else:
            log(f"⚠️ Failed to queue post {post['id']}")

    return queued_count


def main():
    require_buffer_config()
    supabase = get_supabase()

    log("🔁 Fetching pending posts from Supabase...")
    posts = get_pending_posts(supabase)
    log(f"Found {len(posts)} posts to queue in Buffer")

    if not posts:
        return 0

    queued = queue_posts(supabase, posts)
    log(f"✅ Finished queuing. Total posts queued: {queued}")
    return queued


if __name__ == "__main__":
    sys.exit(0 if main() is not None else 1)
