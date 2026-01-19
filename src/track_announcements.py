#!/usr/bin/env python3

"""
NL Forward - Budget / Policy Announcements Tracker

Runs daily (via GitHub Actions) to scan key RSS feeds and
insert new budget/policy announcements into `gov_announcements`.
"""

from datetime import datetime, timedelta
from typing import List, Dict

import feedparser

from utils import get_supabase, log


GOV_RSS_FEEDS: List[Dict[str, str]] = [
    {
        "name": "NL Government News",
        "url": "https://www.gov.nl.ca/releases/feed/",
        "category": "official",
    },
    {
        "name": "CBC NL",
        "url": "https://www.cbc.ca/cmlink/rss-canada-newfoundland",
        "category": "news",
    },
    {
        "name": "VOCM News",
        "url": "https://vocm.com/feed/",
        "category": "news",
    },
    {
        "name": "NTV News",
        "url": "https://ntv.ca/feed/",
        "category": "news",
    },
]


BUDGET_KEYWORDS = [
    "budget",
    "spending",
    "tax",
    "taxes",
    "healthcare",
    "health care",
    "MRI",
    "wait time",
    "youth",
    "retention",
    "municipal",
    "crown land",
    "childcare",
    "sovereign wealth",
    "digital government",
]


def is_potential_announcement(title: str, summary: str) -> bool:
    text = (title or "") + " " + (summary or "")
    text = text.lower()
    return any(kw in text for kw in BUDGET_KEYWORDS)


def parse_published(entry) -> datetime:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6])
    return datetime.utcnow()


def main():
    supabase = get_supabase()
    cutoff = datetime.utcnow() - timedelta(days=2)

    total_new = 0

    for feed_cfg in GOV_RSS_FEEDS:
        log(f"🔍 Checking {feed_cfg['name']} for announcements...")
        try:
            feed = feedparser.parse(feed_cfg["url"])
        except Exception as e:
            log(f"❌ Error parsing {feed_cfg['name']}: {e}")
            continue

        for entry in feed.entries[:20]:
            published = parse_published(entry)
            if published < cutoff:
                continue

            title = getattr(entry, "title", "")
            summary = getattr(entry, "summary", "")
            link = getattr(entry, "link", "")

            if not is_potential_announcement(title, summary):
                continue

            # Skip if already in gov_announcements
            existing = (
                supabase.table("gov_announcements")
                .select("id")
                .eq("source_url", link)
                .execute()
            )
            if existing.data:
                continue

            row = {
                "title": title,
                "source_url": link,
                "announcement_date": published.date().isoformat(),
                "category": feed_cfg["category"],
                "amount_mentioned": None,
                "our_analysis": None,
                "related_policy": None,
                "detected_at": datetime.utcnow().isoformat(),
            }

            supabase.table("gov_announcements").insert(row).execute()
            log(f"✅ Tracked announcement: {title} ({link})")
            total_new += 1

    log(f"📊 New announcements stored: {total_new}")
    return total_new


if __name__ == "__main__":
    main()
