# genicons

##### Ongoing
##### The project is expected to be completed by March 2022.

## Description

This is generating icons app.  
By uploading an image of your choice, you can generate an icon-like image.  
The generated images are assumed to be rounded squares and circles.  
The reason for this is that the former is often used as an icon for desktop applications, and the latter is often used for profiles.

## Motivation

The aim of developing this application is to learn about these technologies.  
***[SQL, ML, AWS, DevSecOps, Docker + IaC, (and TDD)]***  
I'll Create Web API using FastAPI with SQL and ML and dockerize it.  
For the front end, I'll use Vue.js as it is easy to develop SPA.  
Then deploy this app on AWS.  
To study DevSecOps, I'll also use GihubActions to create a workflow that incorporates security checks.

## Contents

```
.
├── app/
└── README.md
```

## Setup

```
$ 
```

## License

[MIT](https://github.com/terib0l/genicons/blob/main/LICENSE)

## Memo

#### To-Do

* ~~バックエンドのベースを書いておく~~
* ~~処理のプログレスを実装（画像生成に時間がかかる場合を想定）~~
* ~~SQLの実装~~
* => TDD(:Test Driven Development)に変更したい (11/26)
  * TDDでDevOpsのDev部分はできる(plan -> code -> build -> test)
* Dockerが使える環境に以降
  * MySQLとの通信テスト
  * DB操作関連のAPIを作成
  * TensorflowのDockerの起動テスト
  * DockerのTensorflowでStyleTransferのテンプレを作成
  * StyleTransferの実装テスト
  * gunicornの起動テスト
* フロントエンドのベースを実装
  * BackendをDockerで起動して通信テスト
  * 画像生成時の表示
  * 画像生成途中の表示
  * 画像生成後の表示
  * 作成物の展示部分を作成
* => ここで大体の実装が終わっている予定
  * Ops部分を作ってみる(release -> deploy -> operate -> monitor)
    * AWSの準備とデプロイの自動化
    * ウェブログとシステムログの収集と監視(Prometeus, Elasticsearch)
* その他細かいこと
  * どこの工程からSecを入れていくか？
    * Pre-Commit Hooks
    * Secret Management
    * SCA / SAST
    * DAST
    * Security in IaC
  * AWSサーバのIaC化(terraform, Ansible)
  * MLとDBとFastAPIのサーバを分けてKubernetesで管理

#### Technical-Elements

* Backend (それぞれDockerを利用する)
  * FastAPI
  * MySQL
  * Tensorflow (for StyleTransfer)
* Frontend
  * Vue.js
* Environment
  * AWS
* CI/CD
  * GithubActions
