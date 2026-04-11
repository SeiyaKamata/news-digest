---
date: '2026-04-12'
title: S3 Filesで消えるアーキテクチャ層、生まれるアーキテクチャ
url: https://zenn.dev/genda_jp/articles/b6ff5ea33c7a71
---

2026年4月7日、AWSがAmazon S3 Filesを一般提供（GA）しました。S3バケットをNFS v4.1/v4.2のファイルシステムとしてマウントできる機能です。EC2、EKS、ECS、Lambdaのいずれからでも利用できます。
https://aws.amazon.com/blogs/aws/launching-s3-files-making-s3-buckets-accessible-as-file-systems/
発表直後から多くのセットアップ記事や速報が出ていますので、この記事では「何が設定できるか」ではなく「何が不要になり、何が可能になるか」を整理します。
対象読...
