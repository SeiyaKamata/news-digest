#!/usr/bin/env python3
"""
先週（月曜〜日曜）の個人GitHubリポジトリのコミットと作成したNotionページを
DWMデータベースの週次ページに書き込む。
"""

import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(__file__))

from github.repos import get_commits_in_range
from notion.pages import append_blocks, build_report_blocks, get_or_create_page, get_pages_in_range

NOTION_DWM_DATABASE_ID = os.environ["NOTION_DWM_DATABASE_ID"]
JST = timezone(timedelta(hours=9))


def get_last_week_range() -> tuple[str, str, str, str]:
    """先週月曜〜日曜の範囲を返す。手動実行日に依存せず、暦上の先週を返す。"""
    today = datetime.now(JST).date()
    this_monday = today - timedelta(days=today.weekday())
    last_monday = this_monday - timedelta(days=7)
    last_sunday = this_monday - timedelta(days=1)
    since = last_monday.strftime("%Y-%m-%dT00:00:00+09:00")
    until = last_sunday.strftime("%Y-%m-%dT23:59:59+09:00")
    week_label = last_monday.strftime("%G-W%V")
    start_date = last_monday.strftime("%Y-%m-%d")
    return week_label, since, until, start_date


def main() -> None:
    week_label, since, until, start_date = get_last_week_range()
    print(f"対象週: {week_label} ({since[:10]} 〜 {until[:10]})")

    print("GitHubコミットを取得中...")
    commits = get_commits_in_range(since, until)
    print(f"  {len(commits)}件のコミット")

    print("Notionページを取得中...")
    pages = get_pages_in_range(since, until)
    print(f"  {len(pages)}件のページ")

    print("週次ページを取得/作成中...")
    page_id = get_or_create_page(NOTION_DWM_DATABASE_ID, week_label, start_date, "Weekly")
    print(f"  page_id: {page_id}")

    print("ブロックを追記中...")
    append_blocks(page_id, build_report_blocks(commits, pages))

    print("完了！")


if __name__ == "__main__":
    main()
