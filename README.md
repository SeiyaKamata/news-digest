# daily-automations

Notionを中心とした日次自動化タスクをまとめたリポジトリ。

## タスク一覧

| タスク | 概要 |
|---|---|
| [news-digest](tasks/news-digest/README.md) | RSSニュースを要約してNotionに保存し、日報にダイジェストを追記 |
| [auto-report](tasks/auto-report/README.md) | GitHubコミットとNotionページを日報/週次/月次レポートに書き込む |

## セットアップ

### GitHub Secrets

| Secret名 | 用途 |
|---|---|
| `GEMINI_API_KEY` | Google AI Studio のAPIキー（news-digest） |
| `NOTION_TOKEN` | Notion Integration Token |
| `NOTION_NEWS_DATABASE_ID` | NotionのNewsデータベースID |
| `NOTION_DWM_DATABASE_ID` | NotionのDWMデータベースID |
| `GH_PAT` | GitHub Personal Access Token（auto-report） |
| `GH_USERNAME` | GitHubユーザー名（auto-report） |

### Notion Integration の設定

1. [notion.so/my-integrations](https://www.notion.so/my-integrations) でIntegrationを作成
2. 以下のデータベースにIntegrationを接続：
   - Newsデータベース
   - DWMデータベース（日報/週次/月次）
