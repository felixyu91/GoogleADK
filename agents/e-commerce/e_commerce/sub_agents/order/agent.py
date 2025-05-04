"""訂單處理代理：處理訂單查詢、訂單狀態追蹤等功能。"""
import os
from datetime import datetime

from google.genai import types
from google.adk.agents import LlmAgent 
from google.adk.agents.callback_context import CallbackContext

from dotenv import load_dotenv
from .tools import (
    get_order_details,
)
from .prompts import return_instructions, return_global_instructions
from e_commerce.base_tools import get_shop_id, get_shop_name

load_dotenv()

shop_id = get_shop_id()
shop_name = get_shop_name(shop_id)

def setup_before_agent_call(callback_context: CallbackContext):
    """設置代理調用前的準備工作。"""
    # 記錄代理調用時間
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    callback_context.state["call_time"] = current_time
    
    # 如果有活動訂單，添加到指令中
    if "active_order_id" in callback_context.state:
        order_id = callback_context.state["active_order_id"]
        callback_context._invocation_context.agent.instruction = (
            return_instructions()
            + f"""
    
    --------- 目前正在處理的訂單 ---------
    訂單編號: {order_id}
    
    """
        )

root_agent = LlmAgent(
    model="gemini-2.0-flash-001",
    name="order_agent",
    instruction=return_instructions(),
    global_instruction=return_global_instructions(shop_name),
    before_agent_callback=setup_before_agent_call,
    tools=[
        get_order_details
    ],
    generate_content_config=types.GenerateContentConfig(temperature=0.2),
)