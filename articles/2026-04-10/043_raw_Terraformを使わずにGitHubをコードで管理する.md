---
date: '2026-04-10'
title: Terraformを使わずにGitHubをコードで管理する
url: https://zenn.dev/babarot/articles/github-as-code-with-gh-infra
---

GitHubのリポジトリをどう管理するか
GitHubのリポジトリが増えてくると、設定の管理が地味に厄介になります。OSSを複数持っていると、merge strategyやRuleset、Actionsの許可設定など、毎回似たような設定をしていくことになります。また、新しい設定を入れていくときも古いリポジトリでは漏れがちで、久しぶりに開いたら古い設定だった、みたいなこともよくあります。
例えば、Goで新しいCLIツールを書いて公開するとします。visibilityをpublicにして、squash mergeだけ有効にして、auto delete head branchesをオンにす...
