from google.adk.agents import LlmAgent
from google.adk.tools import google_search
import os

model_name = os.getenv("MODEL_NAME", "gemini-2.5-flash")

root_agent = LlmAgent(
    name="google_search_agent",
    model=model_name,
    instruction="必要に応じてGoogle検索を使用して質問に回答してください。必ず情報源を明記してください。",
    description="Google検索機能を備えたプロフェッショナルな検索アシスタント",
    tools=[google_search],
)
