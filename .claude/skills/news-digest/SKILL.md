---
name: news-digest
description: Notionのnewsデータベースから今日の記事を取得して精読/流し読みに分類し、日報ページにニュースダイジェストを追記するskill。「今日のニュースをまとめて」「ニュースダイジェストを日報に書いて」などと言われたときに使う。
---

# ニュースダイジェストを日報に書く

## 振り分け基準

### 精読
以下のいずれかに該当するもの：
- エンジニアリング・セキュリティに直接関係する重要な技術情報
- 政治・経済の大きな動向（市場・政策に影響するもの）
- 自分の業務・学習に実用的に役立つ情報

### 流し読み
- 上記に該当しない一般的なニュース
- トレンド情報・話題

---

## 手順

### Step 1: 今日のニュース記事を取得

以下のコマンドを実行する：

```bash
NOTION_TOKEN=<token> NOTION_NEWS_DATABASE_ID=<db_id> \
  python3 /Users/kamata_seiya/.claude-p/skills/news-digest/scripts/fetch_news.py
```

JSON形式で記事一覧が出力される：
```json
[
  {
    "page_id": "...",
    "title": "記事タイトル",
    "url": "https://...",
    "summary": "要約テキスト"
  }
]
```

記事が0件の場合は処理を終了する。

### Step 2: 各記事を精読/流し読みに分類

Step 1で取得したsummaryをもとに、上記の振り分け基準に従って各記事を分類する。

- **精読**: summaryを1〜2文に圧縮して保持する
- **流し読み**: titleとurlのみ保持（summaryは不要）

### Step 3: 今日の日報ページIDを取得

`write-daily`スキルの手順に従い、今日の日報ページIDを取得する：

```bash
NOTION_TOKEN=<token> NOTION_DWM_DATABASE_ID=<dwm_db_id> \
  python3 /Users/kamata_seiya/.claude-p/skills/write-daily/scripts/find_daily.py
```

出力されたURLの末尾の文字列がページID。

### Step 4: 日報ページにダイジェストを追記

以下の形式のJSONをstdinに渡してスクリプトを実行する：

```bash
echo '{
  "read": [
    {"title": "タイトル", "url": "https://...", "summary": "要約1〜2文"}
  ],
  "skim": [
    {"title": "タイトル", "url": "https://..."}
  ]
}' | NOTION_TOKEN=<token> python3 /Users/kamata_seiya/.claude-p/skills/news-digest/scripts/append_digest.py <page_id>
```

### Step 5: 完了報告

精読N件・流し読みM件を日報に追記した旨をユーザーに伝える。
