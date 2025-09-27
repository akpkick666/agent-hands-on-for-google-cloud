from google.adk.agents import SequentialAgent
from .llm_agents import (
    markdown_generator_agent,
    content_evaluation_agent,
    file_writer_agent,
)

# SequentialAgentを使用してワークフローを構築
# 1. マークダウン生成エージェント → 2. 評価エージェント → 3. ファイル書き込みエージェント の順で実行
workflow_agent = SequentialAgent(
    name="MarkdownWorkflowAgent",
    sub_agents=[markdown_generator_agent, content_evaluation_agent, file_writer_agent],
    description="ユーザーの問い合わせに対してマークダウン形式の回答を生成し、評価・修正を行い、ファイルに保存するワークフローエージェント",
)

root_agent = workflow_agent
