#!/usr/bin/env python3
"""
Notionのnewsデータベースから今日作成された記事を取得してJSON出力する。
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
NOTION_NEWS_DATABASE_ID = os.environ.get("NOTION_NEWS_DATABASE_ID", "")
NOTION_API_VERSION = "2022-06-28"

JST = timezone(timedelta(hours=9))


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


def get_page_content(page_id: str) -> str:
    """ページ本文のテキストを取得する。"""
    data = notion_request("GET", f"/blocks/{page_id}/children")
    texts = []
    for block in data.get("results", []):
        block_type = block.get("type")
        if block_type in ("paragraph", "bulleted_list_item", "numbered_list_item"):
            rich_text = block.get(block_type, {}).get("rich_text", [])
            text = "".join(t.get("plain_text", "") for t in rich_text)
            if text:
                texts.append(text)
    return "\n".join(texts)


def main():
    if not NOTION_TOKEN:
        print("ERROR: NOTION_TOKEN not set", file=sys.stderr)
        sys.exit(1)
    if not NOTION_NEWS_DATABASE_ID:
        print("ERROR: NOTION_NEWS_DATABASE_ID not set", file=sys.stderr)
        sys.exit(1)

    today = datetime.now(JST).strftime("%Y-%m-%d")
    tomorrow = (datetime.now(JST) + timedelta(days=1)).strftime("%Y-%m-%d")

    # created_timeでフィルタリング（Notion APIのfilterはcreated_timeを直接サポートしないため
    # 最近のページを取得して日付で絞り込む）
    payload = {
        "filter": {
            "timestamp": "created_time",
            "created_time": {
                "on_or_after": f"{today}T00:00:00+09:00",
            },
        },
        "sorts": [{"timestamp": "created_time", "direction": "ascending"}],
        "page_size": 100,
    }

    results = []
    cursor = None
    while True:
        if cursor:
            payload["start_cursor"] = cursor
        data = notion_request("POST", f"/databases/{NOTION_NEWS_DATABASE_ID}/query", payload)
        results.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")

    articles = []
    for page in results:
        # created_timeが今日かチェック
        created = page.get("created_time", "")
        if not created.startswith(today):
            continue

        props = page.get("properties", {})

        # タイトル取得
        title = ""
        name_prop = props.get("Name", {})
        if name_prop.get("type") == "title":
            rich_text = name_prop.get("title", [])
            title = "".join(t.get("plain_text", "") for t in rich_text)

        # URL取得
        url = props.get("URL", {}).get("url", "")

        # ページ本文（ai_summary）取得
        page_id = page["id"]
        summary = get_page_content(page_id)

        articles.append({
            "page_id": page_id,
            "title": title,
            "url": url,
            "summary": summary,
        })

    print(json.dumps(articles, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
