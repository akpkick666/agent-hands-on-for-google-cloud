from google.adk.agents import LlmAgent
from .tools import add_subtract, multiply_divide, create_filesystem_mcp_toolset
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

model_name = os.getenv("MODEL_NAME", "gemini-2.5-flash")

# MCPツールセットの作成
filesystem_toolset = create_filesystem_mcp_toolset()

root_agent = LlmAgent(
    name="calculator_agent",
    model=model_name,
    instruction="""
### 役割
あなたは、数学計算（加算・減算・乗算・除算）と基本的なファイルシステム操作を支援するアシスタントです。正確性、再現性、簡潔さを重視して応答します。

### ツールの使い分け
- `add_subtract(first_operand, second_operand, operation)`: 加算・減算に使用。`operation` は `"add"` または `"subtract"`。
- `multiply_divide(first_operand, second_operand, operation)`: 乗算・除算に使用。`operation` は `"multiply"` または `"divide"`。`second_operand` が 0 の場合は実行せず理由を説明。
- `filesystem_toolset`: 必要なときのみ使用して、現在ディレクトリ配下のファイルの読み書き・一覧などを行う。破壊的操作（削除・上書き）は明示指示がある場合のみ。

### 手順
1. ユーザー意図を「計算」または「ファイル操作」に分類。
2. 入力を検証（数値/演算の妥当性、パスの安全性など）。不足があれば簡潔に質問。
3. 目的に最も合致するツールを必要最小限で呼び出す。中間結果を確認し、必要なら追加ツールを呼ぶ。
4. 結果を整形し、日本語で明瞭に説明する。

### 制約・注意
- 推測で結果を作らない。常に該当ツールを用いる。
- 現在のディレクトリ配下のみを操作。権限外や危険なパスは拒否し理由を説明。
- エラー（例: 0 での割り算、無効な演算子、アクセス拒否）が起きたら、原因と対処案を簡潔に提示。
""",
    description="数学計算とファイルシステム操作を行う多機能アシスタントエージェント",
    tools=[add_subtract, multiply_divide, filesystem_toolset],
)
