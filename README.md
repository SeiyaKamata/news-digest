# daily-automations

Notionを中心とした日次自動化タスクをまとめたリポジトリ。

## タスク一覧

### news-digest

RSSで収集したニュース記事をGemini APIで自動要約し、NotionのNewsデータベースに保存する。

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

### auto-report

GitHubのコミット履歴とNotionの作成ページをDWMデータベースの日報/週次/月次ページに書き込む。

```
GitHub Actions
  daily  (cron: JST 1:00)   → 前日のコミット・Notionページを日報に追記
  weekly (cron: JST 月6:00) → 先週のコミット・Notionページを週次ページに追記
  monthly(cron: JST 1日6:00)→ 先月のコミット・Notionページを月次ページに追記
```

## リポジトリ構造

```
/
├── tasks/
│   ├── news-digest/
│   │   ├── feeds.yaml                  # RSSフィードリスト
│   │   └── scripts/
│   │       ├── fetch_rss.py            # RSSフェッチ
│   │       ├── summarize.py            # Gemini APIで記事を要約
│   │       └── save_to_notion.py       # NotionのNewsデータベースに保存
│   └── auto-report/
│       ├── scripts/
│       │   ├── daily_report.py
│       │   ├── weekly_report.py
│       │   └── monthly_report.py
│       └── lib/
│           ├── notion/                 # Notion APIクライアント
│           └── github/                 # GitHub APIクライアント
├── .claude/skills/news-digest/         # Claude Code スキル
├── requirements.txt
└── .github/workflows/
    ├── fetch-rss.yml
    ├── daily-report.yml
    ├── weekly-report.yml
    └── monthly-report.yml
```

## セットアップ

### GitHub Secrets

| Secret名 | 用途 |
|---|---|
| `GEMINI_API_KEY` | Google AI Studio のAPIキー（news-digest） |
| `NOTION_TOKEN` | Notion Integration Token |
| `NOTION_NEWS_DATABASE_ID` | NotionのNewsデータベースID |
| `NOTION_DWM_DATABASE_ID` | NotionのDWMデータベースID（日報/週次/月次） |
| `GH_PAT` | GitHub Personal Access Token（auto-report） |
| `GH_USERNAME` | GitHubユーザー名（auto-report） |

### Notion Integration の設定

1. [notion.so/my-integrations](https://www.notion.so/my-integrations) でIntegrationを作成
2. 以下のデータベースにIntegrationを接続：
   - Newsデータベース
   - DWMデータベース（日報/週次/月次）

### RSSフィードのカスタマイズ

`tasks/news-digest/feeds.yaml` を編集する。

```yaml
feeds:
  - https://example.com/feed.rss
```
