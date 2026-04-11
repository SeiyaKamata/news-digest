---
date: '2026-04-12'
title: Unityメモリ＆GCの完全理解
url: https://qiita.com/nekoya404/items/1ba7c598ef69b5595de5?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items
---

Unityでこいう疑問、ありませんか？

なぜGCが実行された後でも、マネージドヒープ／仮想メモリの使用量が減らないのか？
GC.Collect()を何回も実行すれば常駐メモリが減るというのは本当なのか？

1. OSメモリ構造

1-1. 物理メモリ vs 仮想メモ...
