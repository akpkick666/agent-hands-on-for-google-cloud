## LLM Agent（calculator_agent / search_agent）ハンズオン

本セクションは、ADK (Agent Development Kit) のコアである `LlmAgent` がツールを使用して動作するハンズオンです。
関数ツール、組み込みツール、MCP ツールの具体例として以下の 2 つのエージェントを紹介します。

- calculator_agent: 関数ツール + MCP ツール（ファイルシステム）
- search_agent: 組み込みツール（Google 検索）


### 前提条件
- ルートの [`README.md`](../../../README.md) に記載のセットアップが完了していること
- Vertex AI User ロールが実行者に付与されていること
```bash
# IAM ロール付与
gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/aiplatform.user"
```

### エージェント構成
- calculator_agent（[`calculator_agent/agent.py`](calculator_agent/agent.py)）
  - 役割: 四則演算（加減乗除）と基本的なファイルシステム操作の支援
  - ツール:
    - 関数ツール: `add_subtract(first_operand, second_operand, operation)` / `multiply_divide(first_operand, second_operand, operation)`（[参考](https://google.github.io/adk-docs/tools/function-tools/)）
    - MCP ツール: Filesystem MCP Toolset（カレントディレクトリ配下の安全なファイル操作、[参考](https://google.github.io/adk-docs/tools/mcp-tools/)）

- search_agent（[`search_agent/agent.py`](search_agent/agent.py)）
  - 役割: 必要に応じて Google 検索を使用し、情報源（出典）を明記して回答
  - ツール: 組み込みツール `google_search`

### ポイント

- 関数ツール（Function tools）: Python 関数を `tools` に渡すだけで `FunctionTool` として利用できます。LLM はシステム指示、会話履歴、およびユーザー要求を分析し、関数名・docstring・パラメータ（型ヒント/デフォルト値含む）に基づいて「どの場面で」「どの引数で」呼び出すかを判断します。<br>
戻り値は JSON 化可能な構造（例: 辞書）を推奨。（[参考1](https://google.github.io/adk-docs/tools/function-tools/)）（[参考2](https://google.github.io/adk-docs/tools/#how-agents-use-tools)）
- 組み込みツール（Built-in tools）: ADK 提供の標準ツール群（例: `google_search`、Code Execution、Vertex AI RAG/Search、BigQuery、Spanner など）。（[参考](https://google.github.io/adk-docs/tools/built-in-tools/)）
  - 制約（2025-09 時点）: **1 エージェントにつき 1 個のみ使用可能。サブエージェントでは使用不可。**
  - 複数の Built-in を使いたい場合は、Built-in ごとに別エージェントを作成し、親エージェントから `AgentTool` として呼び出します（[参考](https://google.github.io/adk-docs/tools/built-in-tools/#use-built-in-tools-with-other-tools)）。
- MCP ツール（MCP tools）: Model Context Protocol 経由で外部 MCP サーバーと接続し、`MCPToolset` がツール列挙（list_tools）と呼び出し（call_tool）を仲介します。（[参考](https://google.github.io/adk-docs/tools/mcp-tools/)）


### 動作確認

```bash
cd ~/agent-hands-on-for-google-cloud/server/agents/llm_agent
adk web
```

- ブラウザが起動します。画面から `calculator_agent` / `google_search_agent` を選んで対話してください。

