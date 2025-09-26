## LLM Agent ツールデモ（calculator_agent / search_agent）

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
  - Python 関数をツール化して LLM から呼び出します。
  - 参照: https://google.github.io/adk-docs/tools/function-tools/

- 組み込みツール（Built-in tools）
  - ADK 提供の標準ツール群（`google_search`、コード実行など）
  - **制限（2025-09 時点）**  
   1. ルートエージェントまたは単一エージェントごとに、**1 つの組み込みツールのみ**がサポートされている。<br>
   同一エージェント内での他ツールの使用は不可。  
   2. 組み込みツールは **サブエージェント（ネストされたエージェント）では使用できません**。  
  - 詳細: https://google.github.io/adk-docs/tools/built-in-tools/

- MCP ツール（MCP tools）
  - Model Context Protocol 経由で外部サーバーと連携
  - 本デモ: Filesystem MCP サーバー（Node.js/npx 必要）
  - 参照: https://google.github.io/adk-docs/tools/mcp-tools/

### エージェントがツールを選択する条件（方針）
- `instruction` に基づいてユーザー意図を分類し、最小限のツールを選択します。
- 例（calculator_agent）:
  - 入力が数値計算なら関数ツールを使用。
  - ファイル操作指示が明確で安全なら MCP ファイルシステムツールを使用。危険/不明瞭な場合は質問または拒否。
- 例（search_agent）:
  - 出典が必要な外部知識が含まれる質問では `google_search` を使用し、出典URLを明記。
- LLM Agent の基本: https://google.github.io/adk-docs/agents/llm-agents/

### 起動と動作確認
#### 1) ブラウザで確認（adk web）

```bash
cd server/agents/llm_agent
adk web
```

- ブラウザが起動（ポートは環境によって異なる場合があります）。画面から `calculator_agent` / `google_search_agent` を選んで対話します。
- モデルや API 設定が必要な場合は事前に環境変数/設定を行ってください。起動やセットアップの詳細は Quickstart を参照: https://google.github.io/adk-docs/get-started/quickstart/

#### 2) API サーバーで確認（adk api_server + curl）

```bash
cd server/agents/llm_agent
adk api_server
```

- 既定ポートは実行環境の設定に依存します（一般的には 8000 または 8080）。サーバーログの表示ポートを確認してください。
 - APIサーバー起動・テストの流れは Quickstart/Testing を参照: https://google.github.io/adk-docs/get-started/quickstart/ / https://google.github.io/adk-docs/get-started/testing/

代表的な `curl` 例（エンドポイントは実行時のサーバーログに合わせて調整してください）:

計算（calculator_agent）
```bash
curl -s -X POST \
  http://localhost:8000/api/v1/agent \
  -H "Content-Type: application/json" \
  -d '{"agent": "calculator_agent", "input": "2 と 3 を足して"}'
```

検索（search_agent）
```bash
curl -s -X POST \
  http://localhost:8000/api/v1/agent \
  -H "Content-Type: application/json" \
  -d '{"agent": "google_search_agent", "input": "Gemini 2.0 の発表情報の出典を教えて"}'
```

### 注意
- 実際のエンドポイントパスやボディ形式は ADK のバージョン/設定で変わる可能性があります。`adk api_server` 起動時のログ/ドキュメントに従ってください（Quickstart: https://google.github.io/adk-docs/get-started/quickstart/）。
- `google_search` などの組み込みツールは、ネットワーク/認証要件により失敗する場合があります。必要な環境変数や API キー設定を行ってください。
- MCP ファイルシステムはカレント配下のみを対象とし、破壊的操作は明示指示がある場合に限定してください。



