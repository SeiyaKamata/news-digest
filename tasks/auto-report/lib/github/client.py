import json
import os
import urllib.error
import urllib.request


def github_request(path: str) -> list | dict:
    token = os.environ["GH_TOKEN"]
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.loads(res.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"GitHub API {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"GitHub API request failed: {e}") from e
