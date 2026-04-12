#!/usr/bin/env python3
"""
要約済み記事をNotionのnewsデータベースに一記事一ページで保存する。
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

JST = timezone(timedelta(hours=9))

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
NOTION_NEWS_DATABASE_ID = os.environ["NOTION_NEWS_DATABASE_ID"]
NOTION_API_VERSION = "2022-06-28"


def notion_request(method: str, path: str, payload: dict | None = None) -> dict:
    url = f"https://api.notion.com/v1{path}"
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"ERROR: Notion API {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def parse_article(path: Path) -> dict | None:
    text = path.read_text()
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    try:
        fm = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    return fm


def create_news_page(title: str, url: str, summary: str) -> None:
    # ページ本文にsummaryを入れる（2000文字制限対応）
    summary_chunks = [summary[i:i+2000] for i in range(0, len(summary), 2000)]
    children = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": chunk}}]
            },
        }
        for chunk in summary_chunks
    ]

    payload = {
        "parent": {"database_id": NOTION_NEWS_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title[:2000]}}]},
            "URL": {"url": url},
        },
        "children": children,
    }
    notion_request("POST", "/pages", payload)


def main():
    today = datetime.now(JST).strftime("%Y-%m-%d")
    repo_root = Path(__file__).parent.parent
    date_dir = repo_root / "articles" / today

    if not date_dir.exists():
        print(f"No articles directory: {date_dir}")
        return

    article_files = sorted(
        f for f in date_dir.glob("*.md") if f.name != "README.md"
    )
    if not article_files:
        print("No articles found.")
        return

    done, skipped, errors = 0, 0, 0
    for path in article_files:
        fm = parse_article(path)
        if not fm:
            print(f"  SKIP (parse error): {path.name}", file=sys.stderr)
            skipped += 1
            continue

        title = fm.get("title", "")
        url = fm.get("url", "")
        summary = fm.get("ai_summary", "")

        if not summary:
            print(f"  SKIP (no ai_summary): {path.name}")
            skipped += 1
            continue

        try:
            create_news_page(title, url, summary)
            print(f"  SAVED: {title[:60]}")
            done += 1
        except Exception as e:
            print(f"  ERROR: {path.name}: {e}", file=sys.stderr)
            errors += 1

    # 成功した記事ファイルのみ削除（エラー分は再送できるよう残す）
    if errors == 0:
        for path in article_files:
            path.unlink()
    else:
        print(f"WARNING: {errors} errors occurred. Article files not deleted.", file=sys.stderr)

    print(f"\nDone. {done} saved, {skipped} skipped, {errors} errors")


if __name__ == "__main__":
    main()
