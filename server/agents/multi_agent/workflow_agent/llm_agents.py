from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from pydantic import BaseModel, Field
from typing import List, Literal
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

model_name = os.getenv("MODEL_NAME", "gemini-2.5-flash")

# 書き込み先ファイルパスの定義
OUTPUT_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "workflow_response.md"
)


# Pydanticモデル定義
class MarkdownResponse(BaseModel):
    """マークダウン回答生成エージェントの出力形式"""

    markdown_content: str = Field(
        description="ユーザーの問い合わせに対するマークダウン形式の回答"
    )


class EvaluationResult(BaseModel):
    """評価エージェントの出力形式"""

    strengths: List[str] = Field(description="回答の優れている点")
    weaknesses: List[str] = Field(description="改善が必要な点")
    specific_improvements: List[str] = Field(description="具体的な改善提案")
    needs_revision: bool = Field(description="修正が必要かどうか")


class FileWriteResult(BaseModel):
    """ファイル書き込みエージェントの出力形式"""

    action_taken: Literal["revision_applied", "original_saved", "error_occurred"] = (
        Field(description="実行したアクション")
    )
    file_path: str = Field(description="保存先ファイルパス")


def create_filesystem_mcp_toolset():
    """
    Creates an MCP toolset for basic filesystem operations.

    Returns:
        MCPToolset: Filesystem MCP toolset rooted at the current directory.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))

    return MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    current_directory,
                ],
            )
        )
    )


# 1. ユーザーからの問い合わせに対し、最適な回答をマークダウン形式で生成するエージェント
markdown_generator_agent = LlmAgent(
    name="MarkdownGeneratorAgent",
    model=model_name,
    instruction="""
### 役割
あなたは、ユーザーの問い合わせに対してマークダウン形式で最適な回答を生成する専門エージェントです。

### 実行手順
1. ユーザーの問い合わせを詳細に分析
2. 問い合わせのトピックと必要な情報を特定
3. 適切な構成とセクションを計画
4. マークダウン記法を活用して読みやすい回答を生成
5. 見出し、リスト、強調、コードブロックなどを適切に使用

### マークダウン記法要件
- 適切な見出し階層（#, ##, ###など）を使用
- 箇条書きや番号付きリストを効果的に活用
- 重要な部分は**太字**や*斜体*で強調
- 必要に応じてコードブロック（```）を使用
- 表組みが適切な場合は表を使用
- 引用が必要な場合は > を使用

### 出力要件
- マークダウン形式の回答のみを出力
- 論理的で読みやすい構成
- 日本語での明瞭な説明
""",
    description="ユーザーの問い合わせに対してマークダウン形式で最適な回答を生成するエージェント",
    output_key="markdown_response",
    output_schema=MarkdownResponse,
)

# 2. 生成内容を評価するエージェント
content_evaluation_agent = LlmAgent(
    name="ContentEvaluationAgent",
    model=model_name,
    instruction="""
### 役割
あなたは、マークダウン形式で生成された回答の品質を評価し、改善点を特定する専門エージェントです。

### 評価対象
**生成されたマークダウン回答:**
{markdown_response}

### 評価基準
1. **内容の関連性**: ユーザーの問い合わせに対する回答の適切性
2. **マークダウン形式**: マークダウン記法の正確性と効果的な使用
3. **読みやすさ**: 構成の論理性と理解しやすさ
4. **内容の完全性**: 問い合わせに対する回答の網羅性
5. **構造**: 見出し、セクション分けの適切性

### 評価手順
1. 生成されたマークダウン内容を詳細に分析
2. 回答の優れている点を特定
3. 改善が必要な点を特定
4. 具体的な改善提案を生成
5. 修正が必要かどうかを判定

### 出力要件
- 優れている点、改善が必要な点、具体的な改善提案、修正必要性を出力
- 客観的で建設的な評価
- 具体的で実行可能な改善提案
- 明確な修正必要性の判断
""",
    description="生成されたマークダウン回答の品質を評価するエージェント",
    output_key="evaluation_result",
    output_schema=EvaluationResult,
)

# 3. 評価結果に基づき修正を行い、ファイルに書き込むエージェント
file_writer_agent = LlmAgent(
    name="FileWriterAgent",
    model=model_name,
    instruction=f"""
### 役割
あなたは、評価結果に基づいてマークダウン内容を修正し、ファイルに保存する専門エージェントです。

### 入力データ
**生成されたマークダウン回答:**
{{markdown_response}}

**評価結果:**
{{evaluation_result}}

### 実行手順
1. 評価結果の`needs_revision`フィールドを確認
2. 修正が必要な場合（needs_revision: true）：
   - `specific_improvements`に基づいてマークダウン内容を改善
   - マークダウン記法の修正
   - 構成や内容の改善
   - 読みやすさの向上
3. 修正が不要な場合（needs_revision: false）：
   - 元のマークダウン内容をそのまま使用
4. 最終的なマークダウン内容をファイルに保存

### セキュリティ/制約
- 使用可能なMCPツールは`write_file`のみ。他のツール（例: `read_file`, `list_directory` など）は使用しない。
- 操作対象は次のファイルに限定: {OUTPUT_FILE_PATH}
- `write_file`呼び出し時のパスは必ず上記と一致させる。

### ファイル保存
- ファイルパス: {OUTPUT_FILE_PATH}
- ファイル名: workflow_response.md
- MCPツール`write_file`のみを使用してファイルに書き込み

### 出力要件
- 実行したアクションと保存先ファイルパスのみを出力
- 簡潔で明確なアクション報告
""",
    description="評価結果に基づいて修正を行い、ファイルに書き込むエージェント",
    tools=[create_filesystem_mcp_toolset()],
    output_key="file_write_result",
    output_schema=FileWriteResult,
)
