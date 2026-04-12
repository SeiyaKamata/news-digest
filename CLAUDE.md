# ニュース自動要約システム - Claude Code指示書

## あなたの役割

Notionのnewsデータベースから今日の記事を取得し、精読/流し読みに分類して日報ページにニュースダイジェストを追記する。

## 処理手順

### Step 1: 今日の記事を取得

以下のスクリプトを実行して今日の記事をJSON形式で取得する：

```bash
python skills/news-digest/scripts/fetch_news.py
```

記事が0件の場合は処理を終了する。

### Step 2: 精読/流し読みに分類

取得した各記事のsummaryをもとに以下の基準で分類する。

**精読：**
- エンジニアリング・セキュリティに直接関係する重要な技術情報
- 政治・経済の大きな動向（市場・政策に影響するもの）
- 自分の業務・学習に実用的に役立つ情報

**流し読み：**
- 上記に該当しない一般的なニュース
- トレンド情報・話題

精読記事のsummaryは1〜2文に圧縮する。流し読み記事はtitleとurlのみ保持する。

### Step 3: 今日の日報ページIDを取得

```bash
python skills/news-digest/scripts/find_daily.py
```

出力されたURLの末尾がページID（ハイフンなし32文字）。

### Step 4: 日報ページにダイジェストを追記

以下の形式のJSONをstdinに渡してスクリプトを実行する：

```bash
echo '<json>' | python skills/news-digest/scripts/append_digest.py <page_id>
```

JSONの形式：
```json
{
  "read": [
    {"title": "タイトル", "url": "https://...", "summary": "要約1〜2文"}
  ],
  "skim": [
    {"title": "タイトル", "url": "https://..."}
  ]
}
```

## 環境変数

以下の環境変数が必要（GitHub Secretsから渡される）：

- `NOTION_TOKEN` - Notion Integration Token
- `NOTION_NEWS_DATABASE_ID` - newsデータベースID
- `NOTION_DWM_DATABASE_ID` - DWMデータベースID
