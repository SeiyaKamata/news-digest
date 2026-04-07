#!/usr/bin/env python3
"""
RSSフィードを取得して articles/YYYY-MM-DD/ にmarkdownとして保存する。
"""

import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml
import feedparser

JST = timezone(timedelta(hours=9))


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text.strip("_")[:50]


def load_feeds(feeds_path: Path) -> list[str]:
    with feeds_path.open() as f:
        data = yaml.safe_load(f)
    return data.get("feeds", [])


def load_existing_urls(date_dir: Path) -> set[str]:
    """既存記事のURLセットを返す（重複スキップ用）。フロントマターのみ読む。"""
    existing = set()
    for md_file in date_dir.glob("*.md"):
        lines = md_file.read_text().splitlines()
        # フロントマターブロック（--- から次の --- まで）だけをパース
        if lines and lines[0].strip() == "---":
            try:
                end = lines.index("---", 1)
                fm = yaml.safe_load("\n".join(lines[1:end]))
                if fm and "url" in fm:
                    existing.add(fm["url"])
            except (ValueError, yaml.YAMLError):
                pass
    return existing


def make_raw_markdown(title: str, url: str, date: str, description: str) -> str:
    frontmatter = yaml.dump(
        {"title": title, "url": url, "date": date},
        allow_unicode=True,
        default_flow_style=False,
    ).rstrip()
    return f"---\n{frontmatter}\n---\n\n{description}\n"


def fetch_feed(feed_url: str) -> tuple[str, feedparser.FeedParserDict | None]:
    feed = feedparser.parse(feed_url)
    if feed.bozo and not feed.entries:
        return feed_url, None
    return feed_url, feed


def fetch_all_feeds(feed_urls: list[str], date_dir: Path, today: str) -> int:
    existing_urls = load_existing_urls(date_dir)
    counter_file = date_dir / ".counter"
    try:
        count = int(counter_file.read_text())
    except FileNotFoundError:
        count = 1

    start = count
    try:
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(fetch_feed, url): url for url in feed_urls}
            for future in as_completed(futures):
                feed_url, feed = future.result()
                if feed is None:
                    print(f"  ERROR: {feed_url}", file=sys.stderr)
                    continue

                print(f"Fetched: {feed_url} ({len(feed.entries)} entries)")
                for entry in feed.entries:
                    url = entry.get("link", "")
                    title = entry.get("title", "no title")
                    description = entry.get("summary", "")

                    if not url or url in existing_urls:
                        continue

                    slug = slugify(title)
                    filename = f"{count:03d}_raw_{slug}.md"
                    (date_dir / filename).write_text(
                        make_raw_markdown(title, url, today, description)
                    )
                    existing_urls.add(url)
                    print(f"  SAVED: {filename}")
                    count += 1
    finally:
        counter_file.write_text(str(count))

    return count - start


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
