import os
from datetime import date

from google.genai import types
from google.adk.agents import LlmAgent

from dotenv import load_dotenv
from .sub_agents import complaint_agent, order_agent, faq_agent
from .prompts import (
return_instructions_root,
return_global_instructions_root
)

load_dotenv()

date_today = date.today()

root_agent = LlmAgent(
    model=os.getenv("ROOT_AGENT_MODEL"),
    name="root_agent",
    instruction=return_instructions_root(),
    global_instruction=return_global_instructions_root(),
 sub_agents=[complaint_agent, order_agent, faq_agent],
    tools=[],
generate_content_config=types.GenerateContentConfig(temperature=0.01),
)