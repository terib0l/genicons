# genicons

##### Ongoing
##### The project is expected to be completed by March 2022.

## Description

The aim of developing this application is to learn about these technologies.  
***[SQL, ML, AWS, DevSecOps, Docker + IaC]***  
I'll Create Web API using FastAPI with SQL and ML and dockerize it.  
For the front end, I'll use Vue.js as it is easy to develop SPA.  
Then deploy this app on AWS.  
To study DevSecOps, I'll also use GihubActions to create a workflow that incorporates security checks.

This is generating icons app.  
By uploading an image of your choice, you can generate an icon-like image.  
The generated images are assumed to be rounded squares and circles.  
The reason for this is that the former is often used as an icon for desktop applications, and the latter is often used for profiles.

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
* SQLの実装
* フロントエンドのベースを実装（FastAPIとの連携を含む）
* フロントエンドの細かい部分を実装
* アプリをDocker化(Dockerfileとdocker-composeを記述)
* AWSに移行
* ローカルでMLモデルのサンプルを実装
* AWSのMLサービスを検討しつつ、MLモデルを実装
* AWS上でのアプリの動作検証
* DevSecOpsのワークフローについて考える
  * Githubからの自動デプロイの方法
  * IaCについて考える
  * etc

#### Technical-Elements

* FastAPI
  * Docker
  * MySQL
* Vue.js
* AWS
  * EC2
  * ~~Amazon SageMaker~~
  * ~~Amazon Deep Learning Container~~
* GithubActions
