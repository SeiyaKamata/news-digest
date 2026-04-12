# ニュース自動要約システム

RSSで収集したニュース記事をGemini APIで自動要約し、NotionのNewsデータベースに保存するシステム。

## システム構成

```
GitHub Actions (cron: JST 6:00)
  → feeds.yaml からRSSを取得
  → Gemini APIで各記事を要約
  → Notionのnewsデータベースに一記事一ページで保存

Claude Code Remote Tasks
  → newsデータベースから今日の記事を取得
  → 精読/流し読みに分類
  → 日報ページにニュースダイジェストを追記
```

## リポジトリ構造

```
/
├── feeds.yaml                              # RSSフィードリスト
├── CLAUDE.md                               # Claude Code Remote Tasks の指示書
├── requirements.txt                        # Python依存パッケージ
├── scripts/
│   ├── fetch_rss.py                        # RSSフェッチスクリプト
│   ├── summarize.py                        # Gemini APIで記事を要約
│   └── save_to_notion.py                   # NotionのNewsデータベースに保存
├── skills/news-digest/scripts/
│   ├── fetch_news.py                       # newsDBから今日の記事取得
│   ├── append_digest.py                    # 日報ページにダイジェストを追記
│   └── find_daily.py                       # 日報ページID取得
└── .github/
    └── workflows/
        └── fetch-rss.yml                   # GitHub Actionsワークフロー
```

## セットアップ

### 1. GitHub Secrets を設定

リポジトリの Settings → Secrets and variables → Actions に以下を追加：

| Secret名 | 内容 |
|---|---|
| `GEMINI_API_KEY` | Google AI Studio のAPIキー |
| `NOTION_TOKEN` | Notion Integration Token |
| `NOTION_NEWS_DATABASE_ID` | NotionのNewsデータベースID |

### 2. Claude Code Remote Tasks の設定

Remote Tasksに以下の環境変数（Secrets）を追加：

| Secret名 | 内容 |
|---|---|
| `NOTION_TOKEN` | Notion Integration Token |
| `NOTION_NEWS_DATABASE_ID` | NotionのNewsデータベースID |
| `NOTION_DWM_DATABASE_ID` | NotionのDWMデータベースID（日報） |

### 3. Notion Integration の設定

1. [notion.so/my-integrations](https://www.notion.so/my-integrations) でIntegrationを作成
2. 以下のデータベースにIntegrationを接続：
   - Newsデータベース
   - DWMデータベース（日報）

### 4. RSSフィードのカスタマイズ

`feeds.yaml` を編集してフィードを追加・削除する。

```yaml
feeds:
  - https://example.com/feed.rss
```
