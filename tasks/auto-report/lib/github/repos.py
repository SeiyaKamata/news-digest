import os

from .client import github_request


def get_personal_repos() -> list[dict]:
    repos = []
    page = 1
    while True:
        batch = github_request(f"/user/repos?type=owner&per_page=100&page={page}")
        if not isinstance(batch, list) or not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def get_commits(repo_full_name: str, since: str, until: str) -> list[dict]:
    username = os.environ["GH_USERNAME"]
    results = []
    page = 1
    while True:
        batch = github_request(
            f"/repos/{repo_full_name}/commits"
            f"?author={username}&since={since}&until={until}&per_page=100&page={page}"
        )
        if not isinstance(batch, list) or not batch:
            break
        results.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return results


def get_commits_in_range(since: str, until: str) -> list[dict]:
    """全個人リポジトリ(forkを除く)から指定期間のコミットを取得する。"""
    repos = get_personal_repos()
    results = []
    for repo in repos:
        if repo.get("fork"):
            continue
        for commit in get_commits(repo["full_name"], since, until):
            raw_message = commit.get("commit", {}).get("message", "")
            subject = raw_message.splitlines()[0] if raw_message else "(no message)"
            results.append({
                "repo": repo["name"],
                "message": subject,
                "url": commit["html_url"],
            })
    return results
