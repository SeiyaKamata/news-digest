---
date: '2026-04-10'
title: Amazon S3 Files vs Amazon FSx for Lustre：性能比較をしてみた
url: https://zenn.dev/nix/articles/74ccf846643edb
---

1. はじめに
X で大活躍中の @___nix___ です。
今回、GAされたばかりの Amazon S3 Files について早速 Amazon FSx for Lustre との性能比較をしてみました。
難しい内容は余り嬉しく無い人向けにザックリ結果だけを先に記載しておきます。



何したい？
おすすめ
理由




S3 のデータを普通にファイルとして読み書きしたい
S3 Files
設定が簡単。容量の事前確保も不要


大きいファイルを高速に読み書きしたい (1つずつ順番に)
Lustre
1つの処理が速い。S3 Files は1つずつだと遅い


大きいファイルを高速に...
