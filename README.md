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
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
export PROJECT_NUMBER="$(gcloud projects describe "$GOOGLE_CLOUD_PROJECT" --format='value(projectNumber)')"
export REGION="asia-northeast1"
export MODEL_NAME="gemini-2.5-flash"
export GOOGLE_GENAI_USE_VERTEXAI="True"
export GOOGLE_CLOUD_LOCATION="global"
```

### 4) リポジトリを取得
```bash
git clone https://github.com/ak-ten6/agent-hands-on-for-google-cloud.git
```

### 5) Python + venv のセットアップ
```bash
cd ~/agent-hands-on-for-google-cloud/server
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```


## エージェントハンズオン

### 1) LLM Agent（`server/agents/llm_agent`）

- **概要**: ADK の `LlmAgent` がツールを使って動作する基本ハンズオン。
  - `calculator_agent`: 関数ツール + MCP（Filesystem）
  - `search_agent`: 組み込みツール `google_search`
- **学べること**: Function tools / Built-in tools / MCP tools の使い分け
- **リンク**:
  - **ディレクトリ**: [server/agents/llm_agent](server/agents/llm_agent/)
  - **ハンズオン詳細**: [server/agents/llm_agent/README.md](server/agents/llm_agent/README.md)


### 2) マルチエージェント（`server/agents/multi_agent`）

- **概要**: 複数エージェントの協調実行。以下の 3 構成を体験できます。
  - Workflow Agent（順次実行）
  - Coordinator/Dispatcher（LLM による担当移譲）
  - Agent-as-a-Tool（他エージェントをツールとして呼び出し）
- **ポイント**: 構造化出力（`output_schema`/`output_key`）、LLM-Driven Delegation、専門エージェントの分担
- **リンク**:
  - **ディレクトリ**: [server/agents/multi_agent](server/agents/multi_agent/)
  - **ハンズオン詳細**: [server/agents/multi_agent/README.md](server/agents/multi_agent/README.md)


### 3) マルチエージェントのデプロイ（`server/agents/multi_agent/deploy`）

- **概要**: マルチエージェント構成を Cloud Run にデプロイし、プロキシ/IAP 等でのアクセス方法を解説
- **主な内容**: 必要 IAM ロール、`gcloud run deploy` によるソースデプロイ、Cloud Run プロキシ、IAP の有効化
- **リンク**:
  - **ディレクトリ**: [server/agents/multi_agent/deploy](server/agents/multi_agent/deploy/)
  - **デプロイ手順**: [server/agents/multi_agent/deploy/README.md](server/agents/multi_agent/deploy/README.md)
