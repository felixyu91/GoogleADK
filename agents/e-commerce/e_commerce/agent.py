import os

from google.genai import types
from google.adk.agents import LlmAgent

from dotenv import load_dotenv
from .sub_agents import complaint_agent, order_agent, faq2_agent
from .prompts import (
return_instructions_root,
return_global_instructions_root
)

# 根據 ADK 文檔，修改環境變量加載方式
# 在開發環境使用 dotenv，在 Agent Engine 使用環境變量
try:
    load_dotenv()
except:
    pass

root_agent = LlmAgent(
    model=os.getenv("ROOT_AGENT_MODEL", "gemini-2.0-flash-001"),
    name="root_agent",
    instruction=return_instructions_root(),
    global_instruction=return_global_instructions_root(),
    sub_agents=[complaint_agent, order_agent, faq2_agent],
    tools=[],
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)