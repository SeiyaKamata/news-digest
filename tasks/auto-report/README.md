# auto-report

GitHubのコミット履歴とNotionの作成ページをDWMデータベースの日報/週次/月次ページに書き込む。

## フロー

```
GitHub Actions
  daily  (cron: JST 1:00)    → 前日のコミット・Notionページを日報に追記
  weekly (cron: JST 月6:00)  → 先週のコミット・Notionページを週次ページに追記
  monthly(cron: JST 1日6:00) → 先月のコミット・Notionページを月次ページに追記
```

## ファイル構成

```
auto-report/
├── scripts/
│   ├── daily_report.py     # 日次レポート
│   ├── weekly_report.py    # 週次レポート
│   └── monthly_report.py   # 月次レポート
└── lib/
    ├── notion/             # Notion APIクライアント
    └── github/             # GitHub APIクライアント
```

## 必要なSecrets

| Secret名 | 内容 |
|---|---|
| `NOTION_TOKEN` | Notion Integration Token |
| `NOTION_DWM_DATABASE_ID` | NotionのDWMデータベースID（日報/週次/月次） |
| `GH_PAT` | GitHub Personal Access Token |
| `GH_USERNAME` | GitHubユーザー名 |
