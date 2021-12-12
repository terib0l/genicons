# To-Do

* ~~バックエンドのベースを書いておく~~
* ~~処理のプログレスを実装（画像生成に時間がかかる場合を想定）~~
* ~~SQLの実装~~
* => TDD(:Test Driven Development)に変更したい (11/26)
  * TDDでDevOpsのDev部分はできる(plan -> code -> build -> test)
  * Linter
  * Test
* Dockerが使える環境に以降
  ~~* gunicornの起動テスト~~
  ~~* DB操作関連のAPIを作成~~
  * MySQLとの通信テスト
* フロントエンドのベースを実装
  * BackendをDockerで起動して通信テスト
  * 画像生成時の表示
  * 画像生成途中の表示
  * 画像生成後の表示
  * 作成物の展示部分を作成
* ML実装
  * TensorflowのDockerの起動テスト
  * DockerのTensorflowでStyleTransferのテンプレを作成
  * StyleTransferの実装テスト
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
