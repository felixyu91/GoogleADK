"""Complaint Agent: 處理客戶投訴和問題反饋。"""
import os
from datetime import datetime

from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext

from .prompts import return_instructions, return_global_instructions
from e_commerce.base_tools import load_env, get_shop_id, get_shop_name

load_env()

shop_id = get_shop_id()
shop_name = get_shop_name(shop_id)

def setup_before_agent_call(callback_context: CallbackContext):
    """設置代理調用前的準備工作。"""
    # 記錄代理調用時間
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    callback_context.state["call_time"] = current_time
    
    # 根據需要動態更新指令
    if "complaint_category" in callback_context.state:
        category = callback_context.state["complaint_category"]
        callback_context._invocation_context.agent.instruction = (
            return_instructions_complaint()
            + f"""
    
    --------- 目前識別的投訴類別 ---------
    {category}
    
    """
        )

root_agent = LlmAgent(
    model="gemini-2.0-flash-001",
    name="complaint_agent",
    instruction=return_instructions(),
    global_instruction=return_global_instructions(shop_name),
    before_agent_callback=setup_before_agent_call,
    tools=[
    ],
    generate_content_config=types.GenerateContentConfig(temperature=0.2),
)