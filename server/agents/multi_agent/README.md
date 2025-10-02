## マルチエージェントシステム

マルチエージェントシステムは、目的の異なる複数のエージェントを連携させ、単体のエージェントでは難しい複雑なタスクを分担・協調して解決するアーキテクチャです。<br>
各エージェントが固有の指示やツール、入出力スキーマを持ち、会話コンテキストや中間成果物を共有することで、より正確かつ再現性の高い応答が得られます。<br>
詳細は [ADK ドキュメントの Multi Agents 章](https://google.github.io/adk-docs/agents/multi-agents/) を参照してください。

本セクションでは、以下 3 つのマルチエージェント構成のハンズオンを行います。
- [**Workflow Agent (Sequential agent)**](https://google.github.io/adk-docs/agents/workflow-agents/)
- [**Coordinator/Dispatcher Pattern (LLM-Driven Delegation)**](https://google.github.io/adk-docs/agents/multi-agents/#coordinatordispatcher-pattern)
- [**Agent-as-a-Tool**](https://google.github.io/adk-docs/tools/function-tools/#agent-tool)


## 前提条件
- ルートの [`README.md`](../../../README.md) に記載のセットアップが完了していること
- Vertex AI User ロールが実行者に付与されていること
```bash
# IAM ロール付与
gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/aiplatform.user"
```


## Workflow Agent (Sequential agent) ハンズオン

### エージェントの流れ
`SequentialAgent` は複数のサブエージェントを順番に実行し、中間結果を次のステップへ受け渡します。<br>
今回は、以下のサブエージェントを使用します。

1. **MarkdownGeneratorAgent**
   - 役割: ユーザーから指定されたテーマについて Markdown 形式の回答を生成。
   - 出力: `markdown_response` フィールドを持つ構造化出力。

2. **ContentEvaluationAgent**
   - 役割: 回答を評価し、改善点を提示。
   - 出力: `evaluation_result` フィールドに評価コメントを格納。

3. **FileWriterAgent**
   - 役割: Filesystem MCP ツールを用いて、評価をもとに修正した最終回答を `workflow_response.md` に書き込み。


### ポイント
- LLM Agent で **output_schema** を指定し、意図した出力がより確実に取得できるようにしています。
  - output_schema、tools の同時利用が [v1.11.0](https://github.com/google/adk-python/releases/tag/v1.11.0) でサポートされました！！
- LLM Agent で **output_key** を指定することで、Session の State に出力結果を保存できます。（[参考](https://google.github.io/adk-docs/agents/llm-agents/#structuring-data-input_schema-output_schema-output_key)）
  - 保存した値は、プレースホルダー ({}) で参照できます。（[参考](https://google.github.io/adk-docs/sessions/state/)）


### 動作確認

```bash
cd ~/agent-hands-on-for-google-cloud/server/agents/multi_agent
adk web
```

 - ブラウザ起動後、`workflow_agent` を選択して対話を開始できます。
 - **注意**: プルダウンに `deploy` も表示されますが、これは実行できません。必ず `workflow_agent` を選択してください。


## Coordinator/Dispatcher Pattern (LLM-Driven Delegation) ハンズオン

### エージェントの流れ
本パターンでは、各エージェントがユーザー質問の意図を判断し、最適なエージェントへと会話主体を切り替えながら回答します。<br>
今回は、以下のエージェントを使用します。

- 親エージェント: `InformationCounterAgent`（モール全般の案内）
- サブエージェント: `UlukuloShopGuideAgent`（衣料品店「ユルクロ」）
- サブエージェント: `SaizeriyaShopGuideAgent`（レストラン「サイゼリ屋」）
- サブエージェント: `TofuCinemasGuideAgent`（映画館「TOFUシネマズ」）

会話主体となっているエージェントの Instruction には、内部的に以下のシステムインストラクションが挿入され、他エージェントへの移譲判断が可能になります。（[参考](https://github.com/google/adk-python/blob/main/src/google/adk/flows/llm_flows/agent_transfer.py)）

```
You have a list of other agents to transfer to:

Agent name: {AGENT_NAME}
Agent description: {AGENT_DESCRIPTION}

If you are the best to answer the question according to your description, you
can answer it.

If another agent is better for answering the question according to its
description, call `transfer_to_agent` function to transfer the
question to that agent. When transferring, do not generate any text other than
the function call.
```

エージェントが「自分より適したエージェントがいる」と判断した場合、`transfer_to_agent` を呼び出して会話主体を切り替えます。<br>
以降の応答は切り替え先のエージェント内容に従って生成されます。


### ポイント
- **LLM-Driven Delegation（Agent Transfer）**: アクティブエージェントが `transfer_to_agent` を用いて最適な担当へ移譲します。[（参考）](https://google.github.io/adk-docs/agents/multi-agents/#b-llm-driven-delegation-agent-transfer)
- **会話主体の動的切替**: 移譲が行われると、以降の回答は移譲先が主体となって行います。
- **サブエージェントの専門性**:
  - 各サブエージェントは担当領域に特化した対応を行います。各自ツールを保持しています。
    - `UlukuloShopGuideAgent`: `get_ulukulo_top_sales` ツールで 2025 年 1–9 月の月別売上上位 3 件を提供可能。
    - `SaizeriyaShopGuideAgent`: `get_saizeriya_top_sales` ツールで 2025 年 1–9 月の月別売上上位 3 件を提供可能。
    - `TofuCinemasGuideAgent`: `get_tofu_cinemas_schedule` ツールで指定日の上映スケジュールを提供可能。
- **親エージェントの役割**: `InformationCounterAgent` はモール全般の基本情報を回答しつつ、必要に応じて専門エージェントへ移譲します。


### 動作確認

```bash
cd ~/agent-hands-on-for-google-cloud/server/agents/multi_agent/deploy
adk web
```

- ブラウザ起動後、`coordinator` を選択して対話を開始できます。
- 例（想定ルーティング）:
  - 「ユルクロの7月の売上上位は？」→ `UlukuloShopGuideAgent` へ移譲
  - 「サイゼリ屋の3月の売上上位は？」→ `SaizeriyaShopGuideAgent` へ移譲
  - 「9月15日のTOFUシネマズの上映は？」→ `TofuCinemasGuideAgent` へ移譲
  - 「駐車場の料金は？」→ `InformationCounterAgent` が回答


## Agent-as-a-Tool ハンズオン

### エージェントの流れ
本パターンでは、ルートエージェントが会話主体のまま、他エージェントを**ツールとして**呼び出します。<br>
今回の構成では、ルートエージェント `InformationCounterAgent` が以下のエージェントを `AgentTool` として保持します。

- `UlukuloShopGuideAgent`（衣料品店「ユルクロ」）
- `SaizeriyaShopGuideAgent`（レストラン「サイゼリ屋」）
- `TofuCinemasGuideAgent`（映画館「TOFUシネマズ」）

ユーザーの質問内容に応じて、`InformationCounterAgent` は適切なエージェントツールを呼び出し、その結果を受け取って最終回答を作成します。<br>
この間、会話主体の移譲は発生せず、常に `InformationCounterAgent` がユーザーに応答します。


### ポイント
- **会話主体は固定**: エージェントはあくまでツールとして実行されるため、会話主体の遷移は行われません。常にルートエージェント（`InformationCounterAgent`）が回答します。（[参考](https://google.github.io/adk-docs/agents/multi-agents/#c-explicit-invocation-agenttool)）
- **ツール使用判断の根拠**: システム指示、会話履歴、ユーザー要求をもとに、各エージェントツールの「name」「description」「スキーマ」を参照して、どのエージェントを呼ぶべきかを判断します。（[参考](https://google.github.io/adk-docs/tools/#how-agents-use-tools)）
- **応答の最終編集**: ツールからの応答は `InformationCounterAgent` に戻り、必要に応じて要約・整形したうえでユーザーへ返答します。


### 動作確認

```bash
cd ~/agent-hands-on-for-google-cloud/server/agents/multi_agent/deploy
adk web
```

- ブラウザ起動後、`agent_as_tool` を選択して対話を開始できます。
- 例（想定動作）:
  - 「ユルクロの7月の売上上位は？」→ `UlukuloShopGuideAgent` をツールとして呼び出し、ルートエージェントが最終返答
  - 「サイゼリ屋の3月の売上上位は？」→ `SaizeriyaShopGuideAgent` をツールとして呼び出し、ルートエージェントが最終返答
  - 「9月15日のTOFUシネマズの上映は？」→ `TofuCinemasGuideAgent` をツールとして呼び出し、ルートエージェントが最終返答
  - 「駐車場の料金は？」→ ルートエージェントが自分の知識で直接回答


