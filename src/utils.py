#!/usr/bin/env python3

"""
NL Forward - Shared utilities

- Supabase client factory
- Telegram send helper
- Simple logging + time helpers
"""

import os
import sys
import json
from datetime import datetime, timezone

from supabase import create_client
import httpx

# --- Environment / config -------------------------------------------------


def require_env(name: str) -> str:
    """Read a required environment variable or exit with a clear error."""
    value = os.getenv(name)
    if not value:
        print(f"❌ Missing required environment variable: {name}", file=sys.stderr)
        sys.exit(1)
    return value


SUPABASE_URL = require_env("SUPABASE_URL")
SUPABASE_KEY = require_env("SUPABASE_KEY")

TELEGRAM_BOT_TOKEN = require_env("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = require_env("TELEGRAM_CHAT_ID")

# Optional Buffer config – used by queue_buffer.py
BUFFER_ACCESS_TOKEN = os.getenv("BUFFER_ACCESS_TOKEN")
BUFFER_TWITTER_PROFILE_ID = os.getenv("BUFFER_TWITTER_PROFILE_ID")
BUFFER_FACEBOOK_PROFILE_ID = os.getenv("BUFFER_FACEBOOK_PROFILE_ID")
BUFFER_INSTAGRAM_PROFILE_ID = os.getenv("BUFFER_INSTAGRAM_PROFILE_ID")


# --- Supabase --------------------------------------------------------------


def get_supabase():
    """Return a Supabase client singleton."""
    # In Actions this is cheap to re-create, but keep as function for clarity.
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# --- Time helpers ----------------------------------------------------------


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat()


# --- Telegram helpers ------------------------------------------------------


async def send_telegram_async(
    text: str,
    parse_mode: str = "HTML",
    reply_markup: dict | None = None,
) -> None:
    """Send a Telegram message asynchronously."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload: dict = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": parse_mode,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, json=payload)
        if r.status_code != 200:
            print(f"❌ Telegram send failed: {r.status_code} {r.text}", file=sys.stderr)


def build_inline_keyboard(buttons: list[tuple[str, str]]) -> dict:
    """
    Build Telegram inline keyboard structure.

    buttons: list of (label, callback_data)
    """
    return {
        "inline_keyboard": [
            [{"text": label, "callback_data": data} for label, data in buttons]
        ]
    }


# --- Simple logging --------------------------------------------------------


def log(msg: str) -> None:
    ts = iso_now()
    print(f"[{ts}] {msg}")
    sys.stdout.flush()


if __name__ == "__main__":
    # Quick self-check for local debugging
    print("Supabase URL:", SUPABASE_URL)
    print("Telegram chat:", TELEGRAM_CHAT_ID)
