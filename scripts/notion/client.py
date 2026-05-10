import json
import os
import urllib.error
import urllib.request

NOTION_API_VERSION = "2022-06-28"


def notion_request(method: str, path: str, payload: dict | None = None) -> dict:
    token = os.environ["NOTION_TOKEN"]
    url = f"https://api.notion.com/v1{path}"
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.loads(res.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"Notion API {e.code}: {body}") from e
