from .client import notion_request


def get_pages_in_range(since: str, until: str) -> list[dict]:
    """指定期間（since/until は ISO8601日付文字列）に作成されたNotionページを取得する。"""
    since_date = since[:10]
    until_date = until[:10]

    pages = []
    has_more = True
    cursor = None

    while has_more:
        payload: dict = {
            "filter": {"value": "page", "property": "object"},
            "sort": {"direction": "descending", "timestamp": "created_time"},
            "page_size": 100,
        }
        if cursor:
            payload["start_cursor"] = cursor

        data = notion_request("POST", "/search", payload)
        has_more = data.get("has_more", False)
        cursor = data.get("next_cursor")

        for page in data.get("results", []):
            created = page.get("created_time", "")[:10]
            if created < since_date:
                has_more = False
                break
            if created > until_date:
                continue
            title = _extract_title(page)
            pages.append({"title": title, "url": page.get("url", "")})

    return pages


def get_or_create_page(
    database_id: str,
    title: str,
    date: str,
    period: str,
) -> str:
    """DWMデータベースから指定条件のページを取得、なければ作成してページIDを返す。"""
    data = notion_request(
        "POST",
        f"/databases/{database_id}/query",
        {
            "filter": {
                "and": [
                    {"property": "Date", "date": {"equals": date}},
                    {"property": "Period", "select": {"equals": period}},
                ]
            }
        },
    )
    results = data.get("results", [])
    if results:
        return results[0]["id"]

    page = notion_request(
        "POST",
        "/pages",
        {
            "parent": {"database_id": database_id},
            "properties": {
                "Name": {"title": [{"text": {"content": title}}]},
                "Date": {"date": {"start": date}},
                "Period": {"select": {"name": period}},
            },
        },
    )
    return page["id"]


def append_blocks(page_id: str, blocks: list[dict]) -> None:
    notion_request("PATCH", f"/blocks/{page_id}/children", {"children": blocks})


def build_report_blocks(commits: list[dict], pages: list[dict]) -> list[dict]:
    blocks: list[dict] = []

    blocks.append(_heading("📝 コミット"))
    if commits:
        for c in commits:
            blocks.append(_commit_item(c))
    else:
        blocks.append(_paragraph("コミットなし"))

    blocks.append(_heading("📚 作成したNotionページ"))
    if pages:
        for p in pages:
            blocks.append(_link_item(p["title"], p["url"]))
    else:
        blocks.append(_paragraph("作成したページなし"))

    return blocks


# --- helpers ---

def _extract_title(page: dict) -> str:
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            rich_text = prop.get("title", [])
            if rich_text:
                return rich_text[0].get("plain_text", "")
    return "(無題)"


def _heading(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def _paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def _commit_item(commit: dict) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {"type": "text", "text": {"content": f"[{commit['repo']}] "}},
                {"type": "text", "text": {
                    "content": commit["message"], "link": {"url": commit["url"]},
                }},
            ]
        },
    }


def _link_item(title: str, url: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {"type": "text", "text": {"content": title, "link": {"url": url}}}
            ]
        },
    }
