---
title: Running out of disk space in production
url: https://alt-romes.github.io/posts/2026-04-01-running-out-of-disk-space-on-launch.html
date: 2026-04-08
---

## 要約
- プロダクション環境でリリース直後にディスク容量不足が発生した事例の解析記
- デバッグビルド・ログ・キャッシュファイルなどが静かに蓄積する問題が根本原因
- 容量監視・アラート設定の事前実施と、デプロイ時のディスク使用量チェックの重要性を学んだ
- 小規模サービスでも番本番運用では事前のリソース設計が不可欠

## メモ
