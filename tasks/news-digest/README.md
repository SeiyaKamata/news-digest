# news-digest

RSSで収集したニュース記事をGemini APIで自動要約し、NotionのNewsデータベースに保存する。
その後Claude Codeが精読/流し読みに分類して日報ページにダイジェストを追記する。

## フロー

```
GitHub Actions (cron: JST 6:00)
  → feeds.yaml からRSSを取得
  → Gemini APIで各記事を要約（失敗した場合はdescriptionをそのまま保存）
  → Notionのnewsデータベースに一記事一ページで保存

Claude Code
  → newsデータベースから今日の記事を取得
  → 精読/流し読みに分類
  → 日報ページにニュースダイジェストを追記
```

## ファイル構成

```
news-digest/
├── feeds.yaml          # 購読するRSSフィードリスト
└── scripts/
    ├── fetch_rss.py    # RSSフェッチ・記事をarticles/YYYY-MM-DD/に保存
    ├── summarize.py    # Gemini APIで記事を要約しai_summaryをフロントマターに追記
    └── save_to_notion.py  # 記事をNotionのNewsデータベースに保存
```

## 必要なSecrets

| Secret名 | 内容 |
|---|---|
| `GEMINI_API_KEY` | Google AI Studio のAPIキー |
| `NOTION_TOKEN` | Notion Integration Token |
| `NOTION_NEWS_DATABASE_ID` | NotionのNewsデータベースID |

## RSSフィードのカスタマイズ

`feeds.yaml` を編集する。

```yaml
feeds:
  - https://example.com/feed.rss
```
