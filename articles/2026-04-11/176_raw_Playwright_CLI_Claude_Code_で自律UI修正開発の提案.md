---
date: '2026-04-11'
title: Playwright CLI + Claude Code で自律UI修正開発の提案
url: https://zenn.dev/catatsumuri/articles/22227c79a94a86
---

はじめに — コーディングエージェント に「目」を与える
Claude Code や Codex CLI は非常に強力なコーディングエージェントであるが、UI の問題に関しては必ずしも万能ではない。
特に以下のようなケースは苦手である。

Markdown のレンダリング崩れ
CSS の微妙なズレ
レスポンシブのレイアウト崩れ
スクロール後に発生する UI 問題

これらはコードを読んだだけでは判断しづらく、実際の画面を確認しないと分からないケースが多い。つまりAI開発エージェントは「コードは読めるが、画面は見えない」という制約がある。
ここではLaravel Boost +  Pl...
