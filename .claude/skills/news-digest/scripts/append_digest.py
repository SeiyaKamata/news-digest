#!/usr/bin/env python3
"""
日報ページにニュースダイジェストを追記する。
引数としてページIDと分類済み記事のJSONを受け取る。

使い方:
  echo '<json>' | python append_digest.py <page_id>

JSONの形式:
  {
    "read": [{"title": "...", "url": "...", "summary": "..."}],
    "skim": [{"title": "...", "url": "..."}]
  }
"""

import json
import os
import sys
import urllib.error
import urllib.request

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
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


def build_blocks(read_articles: list[dict], skim_articles: list[dict]) -> list[dict]:
    blocks = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📰 ニュースダイジェスト"}}]
            },
        },
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "🔴 精読"}}]
            },
        },
    ]

    if read_articles:
        for article in read_articles:
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": article["title"],
                                "link": {"url": article["url"]},
                            },
                        },
                        {
                            "type": "text",
                            "text": {"content": f" — {article.get('summary', '')}"},
                        },
                    ]
                },
            })
    else:
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "なし"}}]},
        })

    blocks.append({
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "⚪ 流し読み"}}]
        },
    })

    if skim_articles:
        for article in skim_articles:
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": article["title"],
                                "link": {"url": article["url"]},
                            },
                        }
                    ]
                },
            })
    else:
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "なし"}}]},
        })

    return blocks


def append_blocks(page_id: str, blocks: list[dict]) -> None:
    for i in range(0, len(blocks), 100):
        notion_request(
            "PATCH",
            f"/blocks/{page_id}/children",
            {"children": blocks[i:i + 100]},
        )


def main():
    if not NOTION_TOKEN:
        print("ERROR: NOTION_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: echo '<json>' | python append_digest.py <page_id>", file=sys.stderr)
        sys.exit(1)

    page_id = sys.argv[1]
    digest = json.loads(sys.stdin.read())

    read_articles = digest.get("read", [])
    skim_articles = digest.get("skim", [])

    blocks = build_blocks(read_articles, skim_articles)
    append_blocks(page_id, blocks)
    print(f"Done. 精読:{len(read_articles)}件, 流し読み:{len(skim_articles)}件 を追記しました。")


if __name__ == "__main__":
    main()
