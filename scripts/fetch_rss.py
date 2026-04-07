#!/usr/bin/env python3
"""
RSSフィードを取得して articles/YYYY-MM-DD/ にmarkdownとして保存する。
"""

import os
import re
import sys
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml
import feedparser

JST = timezone(timedelta(hours=9))


def slugify(text: str) -> str:
    """タイトルをファイル名用スラッグに変換する。"""
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    text = text.strip("_")
    return text[:50]


def url_hash(url: str) -> str:
    """URLの短縮ハッシュを返す（重複チェック用）。"""
    return hashlib.md5(url.encode()).hexdigest()[:8]


def load_feeds(feeds_path: Path) -> list[str]:
    with feeds_path.open() as f:
        data = yaml.safe_load(f)
    return data.get("feeds", [])


def load_existing_urls(date_dir: Path) -> set[str]:
    """既存記事のURLセットを返す（重複スキップ用）。"""
    existing = set()
    for md_file in date_dir.glob("*.md"):
        content = md_file.read_text()
        for line in content.splitlines():
            if line.startswith("url:"):
                url = line.replace("url:", "").strip()
                existing.add(url)
    return existing


def make_raw_markdown(title: str, url: str, date: str, description: str) -> str:
    return f"""---
title: {title}
url: {url}
date: {date}
---

{description}
"""


def fetch_all_feeds(feed_urls: list[str], date_dir: Path, today: str) -> int:
    existing_urls = load_existing_urls(date_dir)
    counter_file = date_dir / ".counter"
    start = int(counter_file.read_text()) if counter_file.exists() else 1

    count = start
    saved = 0

    for feed_url in feed_urls:
        print(f"Fetching: {feed_url}")
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)
            continue

        for entry in feed.entries:
            url = entry.get("link", "")
            title = entry.get("title", "no title")
            description = entry.get("summary", "")

            if not url:
                continue
            if url in existing_urls:
                print(f"  SKIP (duplicate): {title}")
                continue

            slug = slugify(title)
            filename = f"{count:03d}_raw_{slug}.md"
            filepath = date_dir / filename

            filepath.write_text(make_raw_markdown(title, url, today, description))
            existing_urls.add(url)
            print(f"  SAVED: {filename}")
            count += 1
            saved += 1

    counter_file.write_text(str(count))
    return saved


def main():
    repo_root = Path(__file__).parent.parent
    feeds_path = repo_root / "feeds.yaml"

    today = datetime.now(JST).strftime("%Y-%m-%d")
    date_dir = repo_root / "articles" / today
    date_dir.mkdir(parents=True, exist_ok=True)

    feed_urls = load_feeds(feeds_path)
    saved = fetch_all_feeds(feed_urls, date_dir, today)
    print(f"\nDone. {saved} new articles saved to articles/{today}/")


if __name__ == "__main__":
    main()
