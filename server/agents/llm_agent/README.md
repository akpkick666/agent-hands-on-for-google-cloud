## LLM Agent（calculator_agent / search_agent）

本セクションは、ADK (Agent Development Kit) のコアである `LlmAgent` がツールを使用して動作するハンズオンです。<br>
関数ツール、組み込みツール、MCPツールの具体例として以下の2つのエージェントを紹介します。

- calculator_agent: 関数ツール + MCPツール（ファイルシステム）
- search_agent: 組み込みツール（Google 検索）


### 前提条件
- ルートの [`README.md`](../../../README.md) に記載のセットアップが完了していること

### エージェント構成
- calculator_agent ([`calculator_agent/agent.py`](calculator_agent/agent.py))
  - 役割: 四則演算（加減乗除）と基本的なファイルシステム操作の支援
  - ツール:
    - 関数ツール: `add_subtract(first_operand, second_operand, operation)` / `multiply_divide(first_operand, second_operand, operation)`
      - Function tools: https://google.github.io/adk-docs/tools/function-tools/
    - MCPツール: Filesystem MCP Toolset（カレントディレクトリ配下の安全なファイル操作）
      - MCP tools: https://google.github.io/adk-docs/tools/mcp-tools/

- search_agent ([`search_agent/agent.py`](search_agent/agent.py))
  - 役割: 必要に応じて Google 検索を使用し、情報源（出典）を明記して回答
  - ツール: 組み込みツール `google_search`

### ツールの種類とポイント
- 関数ツール（Function tools）
  - Python 関数を `tools` に渡すだけで `FunctionTool` として利用できます。LLM は関数名・docstring・パラメータ（型ヒント/デフォルト値含む）を解析し、「どの場面で」「どの引数で」呼び出すかを判断します。戻り値は JSON 化可能な構造（例: 辞書）を推奨。<br>参照: https://google.github.io/adk-docs/tools/function-tools/

- 組み込みツール（Built-in tools）
  - ADK 提供の標準ツール群（例: `google_search`、Code Execution、Vertex AI RAG/Search、BigQuery、Spanner など）。<br>参照: https://google.github.io/adk-docs/tools/built-in-tools/
  - 制約（2025-09 時点）: 
    - **1エージェントにつき Built-in は1個のみ。**
    - **サブエージェントでは使用不可。**
  <br>参照: https://google.github.io/adk-docs/tools/built-in-tools/#limitations
  - 複数の Built-in を使いたい場合は、Built-in ごとに別エージェントを作成し、親エージェントから `AgentTool` として呼び出します。
  <br>参照: https://google.github.io/adk-docs/tools/built-in-tools/#use-built-in-tools-with-other-tools

- MCP ツール（MCP tools）
  - Model Context Protocol 経由で外部 MCP サーバーと接続し、`MCPToolset` がツール列挙（list_tools）と呼び出し（call_tool）を仲介します。<br>参照: https://google.github.io/adk-docs/tools/mcp-tools/

### エージェントがツールを選択する条件（方針）
- LLM は、各ツールの docstring・関数名・型情報と、エージェント `instruction` を総合して最小限のツールを選択します。<br>参照: https://google.github.io/adk-docs/tools/function-tools/
- Tips: ツールの docstring に「使うべき/使わない場面」「前提条件」「例外（例: 0除算不可）」を明記すると誤用が減ります。<br>参照: https://google.github.io/adk-docs/tools/function-tools/
- （注意）`output_schema` を設定した LlmAgent はツールを併用できません（構造化出力とのトレードオフ）。<br>参照: https://google.github.io/adk-docs/agents/llm-agents/

### 起動と動作確認
#### 1) ブラウザで確認（adk web）

```bash
cd server/agents/llm_agent
adk web
```

- ブラウザが起動。画面から `calculator_agent` / `google_search_agent` を選んで対話します。

#### 2) API サーバーで確認（adk api_server + curl）

```bash
cd server/agents/llm_agent
adk api_server
```

- 最初の問い合わせ前にセッションを作成してください（新規 `session_id` を発行）。<br>参照: https://google.github.io/adk-docs/get-started/testing/

セッション作成（calculator_agent の例）
```bash
curl -s -X POST \
  http://localhost:8000/apps/calculator_agent/users/u_1/sessions/s_calc \
  -H "Content-Type: application/json" \
  -d '{"state": {}}'
```

セッション作成（search_agent の例）
```bash
curl -s -X POST \
  http://localhost:8000/apps/search_agent/users/u_1/sessions/s_search \
  -H "Content-Type: application/json" \
  -d '{"state": {}}'
```

- API サーバーの実行リクエストは `/run`（同期）または `/run_sse`（SSE）を使用します。<br>参照: https://google.github.io/adk-docs/api-reference/rest/


リクエスト（calculator_agent の例）
```bash
curl -s -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "calculator_agent",
    "user_id": "u_1",
    "session_id": "s_calc",
    "new_message": {
      "role": "user",
      "parts": [{"text": "2 と 3 を足して"}]
    }
  }'
```

リクエスト（search_agent の例）
```bash
curl -s -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "search_agent",
    "user_id": "u_1",
    "session_id": "s_search",
    "new_message": {
      "role": "user",
      "parts": [{"text": "nanobanana ってなにがすごいの？"}]
    }
  }'
```

