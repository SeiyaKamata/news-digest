#!/usr/bin/env python3
"""
_raw_ ファイルの記事をGemini Flash APIで要約し、フロントマターにai_summaryを追記する。
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml
from google import genai

JST = timezone(timedelta(hours=9))

PROMPT_TEMPLATE = """\
以下のニュース記事を日本語で5〜6行で要約してください。

タイトル: {title}
内容: {description}"""


def parse_raw_file(path: Path) -> tuple[dict, str] | None:
    """フロントマターと本文を返す。解析失敗時はNone。"""
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
    body = "\n".join(lines[end + 1 :]).strip()
    return fm, body


def write_with_summary(path: Path, fm: dict, body: str) -> None:
    """ai_summary付きのフロントマターでファイルを上書きする。"""
    frontmatter = yaml.dump(
        fm,
        allow_unicode=True,
        default_flow_style=False,
    ).rstrip()
    path.write_text(f"---\n{frontmatter}\n---\n\n{body}\n")


def summarize(client: genai.Client, title: str, description: str) -> str:
    prompt = PROMPT_TEMPLATE.format(title=title, description=description)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text.strip()


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    repo_root = Path(__file__).parent.parent
    today = datetime.now(JST).strftime("%Y-%m-%d")
    date_dir = repo_root / "articles" / today

    if not date_dir.exists():
        print(f"No articles directory: {date_dir}")
        return

    raw_files = sorted(
        f for f in date_dir.glob("*.md") if f.name != "README.md"
    )
    if not raw_files:
        print("No _raw_ files found.")
        return

    done, skipped, errors = 0, 0, 0
    for path in raw_files:
        parsed = parse_raw_file(path)
        if parsed is None:
            print(f"  SKIP (parse error): {path.name}", file=sys.stderr)
            skipped += 1
            continue

        fm, body = parsed
        if "ai_summary" in fm:
            print(f"  SKIP (already summarized): {path.name}")
            skipped += 1
            continue

        title = fm.get("title", "")
        try:
            summary = summarize(client, title, body)
        except Exception as e:
            print(f"  ERROR: {path.name}: {e}", file=sys.stderr)
            errors += 1
            continue

        fm["ai_summary"] = summary
        write_with_summary(path, fm, body)
        print(f"  DONE: {path.name}")
        done += 1

    print(f"\nSummary: {done} done, {skipped} skipped, {errors} errors")


if __name__ == "__main__":
    main()
