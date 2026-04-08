---
date: '2026-04-09'
title: GitHub App の秘密鍵を AWS KMS に閉じ込める
url: https://zenn.dev/aws_japan/articles/b311c3710826a6
---

はじめに
こんにちは konippi です。
2026 年 3 月、脆弱性スキャナーのTrivy が侵害されたことは大きなニュースとなりました。攻撃者は GitHub Actions ワークフローの設定 pull_request_target を悪用して PAT を窃取し、Trivy の公式リリースにクレデンシャルスティーラーを注入。数千の CI/CD パイプラインに影響を与えました。同時期に axios の npm パッケージ侵害や、 prt-scan キャンペーンも発生しています。
これらに共通するのは、信頼されたソフトウェアサプライチェーンの一部が侵害され、ソフトウェアの配布チ...
