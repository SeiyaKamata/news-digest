#!/usr/bin/env python3
"""
先月（1日〜末日）の個人GitHubリポジトリのコミットと作成したNotionページを
DWMデータベースの月次ページに書き込む。
"""

import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(__file__))

from github.repos import get_commits_in_range
from notion.pages import append_blocks, build_report_blocks, get_or_create_page, get_pages_in_range

NOTION_DWM_DATABASE_ID = os.environ["NOTION_DWM_DATABASE_ID"]
JST = timezone(timedelta(hours=9))


def get_last_month_range() -> tuple[str, str, str, str]:
    """先月1日〜末日の範囲を返す。実行日（1日）の前月。"""
    today = datetime.now(JST)
    first_of_this_month = today.replace(day=1)
    last_of_last_month = first_of_this_month - timedelta(days=1)
    first_of_last_month = last_of_last_month.replace(day=1)

    since = first_of_last_month.strftime("%Y-%m-%dT00:00:00+09:00")
    until = last_of_last_month.strftime("%Y-%m-%dT23:59:59+09:00")
    month_label = first_of_last_month.strftime("%Y-%m")
    start_date = first_of_last_month.strftime("%Y-%m-%d")
    return month_label, since, until, start_date


def main() -> None:
    month_label, since, until, start_date = get_last_month_range()
    print(f"対象月: {month_label} ({since[:10]} 〜 {until[:10]})")

    print("GitHubコミットを取得中...")
    commits = get_commits_in_range(since, until)
    print(f"  {len(commits)}件のコミット")

    print("Notionページを取得中...")
    pages = get_pages_in_range(since, until)
    print(f"  {len(pages)}件のページ")

    print("月次ページを取得/作成中...")
    page_id = get_or_create_page(NOTION_DWM_DATABASE_ID, month_label, start_date, "Monthly")
    print(f"  page_id: {page_id}")

    print("ブロックを追記中...")
    append_blocks(page_id, build_report_blocks(commits, pages))

    print("完了！")


if __name__ == "__main__":
    main()
