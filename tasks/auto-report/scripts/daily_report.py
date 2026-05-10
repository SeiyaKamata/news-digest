#!/usr/bin/env python3
"""
昨日の個人GitHubリポジトリのコミットと作成したNotionページを
DWMデータベースの日報ページに書き込む。
"""

import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from github.repos import get_commits_in_range
from notion.pages import append_blocks, build_report_blocks, get_or_create_page, get_pages_in_range

NOTION_DWM_DATABASE_ID = os.environ["NOTION_DWM_DATABASE_ID"]
JST = timezone(timedelta(hours=9))


def get_yesterday_range() -> tuple[str, str, str]:
    yesterday = datetime.now(JST) - timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")
    since = yesterday.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    until = yesterday.replace(hour=23, minute=59, second=59, microsecond=0).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return date_str, since, until


def main() -> None:
    date_str, since, until = get_yesterday_range()
    print(f"対象日: {date_str}")

    print("GitHubコミットを取得中...")
    commits = get_commits_in_range(since, until)
    print(f"  {len(commits)}件のコミット")

    print("Notionページを取得中...")
    pages = get_pages_in_range(since, until)
    print(f"  {len(pages)}件のページ")

    print("日報ページを取得/作成中...")
    page_id = get_or_create_page(NOTION_DWM_DATABASE_ID, date_str, date_str, "Daily")
    print(f"  page_id: {page_id}")

    print("ブロックを追記中...")
    append_blocks(page_id, build_report_blocks(commits, pages))

    print("完了！")


if __name__ == "__main__":
    main()
