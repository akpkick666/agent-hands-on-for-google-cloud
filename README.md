## プロジェクト概要

本リポジトリは、Google Cloud 環境で動作するエージェント開発ハンズオン用の教材です。
各コマンドは Cloud Shell 上での実行を想定しています。


## Cloud Shell のセットアップ

### 1) Cloud Shell の許可（セッションごと）
Cloud Shell を開いた直後に表示される **Authorize Cloud Shell** ダイアログで **Authorize** をクリックしてください。許可はセッションごとに必要です（再接続時は再度許可が必要）。

### 2) gcloud のアカウント・プロジェクト設定
```bash
# 認証済みアカウントの一覧
gcloud auth list

# gcloud が現在使用するアカウント
gcloud config get-value account

# 現在のプロジェクト ID
gcloud config get-value project
```

値が違う / 未設定の場合は以下を実行します。
```bash
# 使いたいアカウントに切替
gcloud config set account <YOUR_ACCOUNT>

# 対象プロジェクトに切替
gcloud config set project <YOUR_PROJECT_ID>
```

### 3) 環境変数の設定
環境変数を設定しておきます。
```bash
# プロジェクト ID
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)

# ロケーション
export GOOGLE_CLOUD_LOCATION=us-central1
```

### 4) リポジトリを取得
```bash
git clone https://github.com/akpkick666/agent-hands-on-for-google-cloud.git
```

### 5) Python 3.12 + venv のセットアップ
```bash
cd agent-hands-on-for-google-cloud/server
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```
## Next.js クライアントの起動

ADK API サーバーと併せて Next.js 製のチャットクライアントを起動できます。

1. 依存パッケージをインストールします。
   ```bash
   cd client
   pnpm install
   ```
2. `.env.local` を作成し、ADK API サーバーの URL を設定します。
   ```bash
   cp .env.local.example .env.local
   # NEXT_PUBLIC_ADK_BASE_URL に ADK サーバーのエンドポイントを設定
   ```
3. サーバー側の API を起動します。
   ```bash
   cd ../server
   uvicorn main:app --reload
   ```
4. 別ターミナルで Next.js クライアントを開発モードで起動します。
   ```bash
   cd ../client
   pnpm dev
   ```

`pnpm build` と `pnpm start` を使用すると本番ビルドを生成・起動できます。
