---
date: '2026-04-12'
title: Claude Code Skillsは作って終わりじゃない — 事後ログで改善サイクルを回す
url: https://zenn.dev/tre_conigli/articles/claude-code-skill-improvement-cycle
---

Claude Code の Custom Skills を使い込んでいると、ある問題に気づく。作った直後は快適に動くのに、数週間後に微妙にズレた出力が出始める。ユーザーがチャット上で修正を入れても、その修正は会話が終われば消える。
この記事では、その「作って終わり」問題に対して、事後ログ収集という仕組みで改善サイクルを回すアプローチを解説する。具体的には、自作した capturing-run-update-logs というSkillの設計思想と仕組みを紹介する。
対象読者: Claude Code の Skills を自作している、または自作を検討しているエンジニア。

 Skillはな...
