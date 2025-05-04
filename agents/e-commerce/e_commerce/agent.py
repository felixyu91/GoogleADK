import os

from google.genai import types
from google.adk.agents import LlmAgent
from dotenv import load_dotenv
from .sub_agents import complaint_agent, order_agent, faq2_agent
from .prompts import return_instructions, return_global_instructions
from e_commerce.base_tools import get_shop_id, get_shop_name

load_dotenv()

shop_id = get_shop_id()
shop_name = get_shop_name(shop_id)

root_agent = LlmAgent(
    model=os.getenv("ROOT_AGENT_MODEL", "gemini-2.0-flash-001"),
    name="root_agent",
    instruction=return_instructions(),
    global_instruction=return_global_instructions(shop_name),
    sub_agents=[complaint_agent, order_agent, faq2_agent],
    tools=[],
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)