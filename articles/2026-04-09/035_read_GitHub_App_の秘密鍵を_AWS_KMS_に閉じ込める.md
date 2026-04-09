---
title: GitHub App の秘密鍵を AWS KMS に閉じ込める
url: https://zenn.dev/aws_japan/articles/b311c3710826a6
date: 2026-04-09
---

## 要約
- こんにちは konippi です
- 2026 年 3 月、脆弱性スキャナーのTrivy が侵害されたことは大きなニュースとなりました
- 攻撃者は GitHub Actions ワークフローの設定 pull_request_target を悪用して PAT を窃取し、Trivy の公式リリースにクレデンシャルスティーラーを注入
- なぜ重要か: GitHub AppのRSA秘密鍵をAWS KMSに安全に閉じ込める実装例

## メモ
（ここに感想を書く）
