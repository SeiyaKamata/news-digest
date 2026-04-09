---
title: 脆弱性対応と minimumReleaseAge を両立しながら依存管理をクリーンに保つ
url: https://zenn.dev/pksha/articles/audit-override-auto-sync
date: 2026-04-09
---

## 要約
- PKSHA Technology で SWE をしている須藤です
- npm エコシステムを標的としたサプライチェーン攻撃はすでに現実のリスクです
- 2026 年 3 月には、週間 8,000 万ダウンロードを超える axios のメンテナーアカウントが乗っ取られ、悪意ある依存パッケージを通じてクロスプラットフォーム対応の RAT（遠隔操作ツール）を配布される事件も起きています
- なぜ重要か: pnpmのminimumReleaseAgeで脆弱性対応と依存管理を両立する方法

## メモ
（ここに感想を書く）
