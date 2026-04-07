# ニュース自動要約システム

RSSで収集したニュース記事をClaude Codeが自動要約し、Obsidianで閲覧できるようにするシステム。

## システム構成

```
GitHub Actions (cron: JST 6:00)
  → feeds.yaml からRSSを取得
  → articles/YYYY-MM-DD/ にmarkdownとしてコミット

Claude Code Remote Tasks (JST 7:00)
  → articles/YYYY-MM-DD/ の未処理記事を取得
  → 各記事URLをfetchして要約
  → read_ / skim_ プレフィックスで振り分け
  → articles/YYYY-MM-DD/README.md に日次ダイジェストを作成
  → コミット

Obsidian + Obsidian Git plugin
  → GitHubリポジトリをvaultとして同期
  → 記事を読む・感想・メモを書く
```

## リポジトリ構造

```
/
├── feeds.yaml                          # RSSフィードリスト
├── CLAUDE.md                           # Claude Codeへの指示
├── scripts/
│   └── fetch_rss.py                    # RSSフェッチスクリプト
├── .github/
│   └── workflows/
│       └── fetch-rss.yml              # GitHub Actionsワークフロー
└── articles/
    └── 2026-04-08/
        ├── README.md                   # 日次ダイジェスト
        ├── 001_read_タイトル.md        # 精読記事
        └── 002_skim_タイトル.md        # 流し読み記事
```

## セットアップ

### 1. リポジトリをプライベートで作成

このリポジトリをGitHubにpushする。

### 2. Claude Code Remote Tasks を設定

1. [claude.ai/code](https://claude.ai/code) にアクセス
2. Remote Tasks を新規作成
3. GitHubリポジトリを接続
4. スケジュール: `0 22 * * *`（UTC）= JST 7:00
5. 指示: `CLAUDE.md の指示に従って今日の記事を処理してください`

### 3. Obsidian を設定

1. Obsidian Git プラグインをインストール
2. このGitHubリポジトリをvaultとして設定
3. 自動pull間隔: 5分

### 4. RSSフィードのカスタマイズ

`feeds.yaml` を編集してフィードを追加・削除する。

```yaml
feeds:
  - https://example.com/feed.rss
```
