"""faq Agent: 透過 Dialogflow SDK 檢索常見問題。"""
import os

from google.genai import types
from google.adk.agents import LlmAgent
from .prompts import return_instructions, return_global_instructions
from .tools import DialogflowSDKTools, get_agent_id
from e_commerce.base_tools import load_env, get_shop_id, get_shop_name

load_env()

shop_id = get_shop_id()
shop_name = get_shop_name(shop_id)
dialogflow_tools = DialogflowSDKTools()

def query_dialogflow(text: str) -> str:
    """
    將使用者的問題傳送到 Dialogflow CX 使用 SDK 獲取回應
    
    Args:
        text: 使用者輸入的文字
    
    Returns:
        Dialogflow 回傳的回應內容
    """
    agent_id = get_agent_id(shop_id)

    session_id = f"cc-87e66248-ec5b-468a-bfc0-a864593574a9"
    
    # 使用 SDK 向 Dialogflow CX 查詢意圖
    response = dialogflow_tools.detect_intent(
        agent_id=agent_id,
        session_id=session_id,
        text=text,
    )
    
    # 解析回應
    if response:
        # 取得 QueryResult
        query_result = response.query_result

        # 首先嘗試從回應訊息中獲取文字
        if query_result.response_messages:
            for msg in query_result.response_messages:
                if hasattr(msg, "text") and msg.text and msg.text.text:
                    return msg.text.text[0]
        
        # 如果回應訊息中沒有文字，嘗試從 fulfillment_text 獲取
        if query_result.fulfillment_text:
            return query_result.fulfillment_text
    
    # 如果完全無法獲取回應
    return "抱歉，我目前無法回應您的問題，請稍後再試。"

root_agent = LlmAgent(
    model=os.getenv("FAQ_AGENT_MODEL"),
    name='faq2_agent',
    instruction=return_instructions(),
    global_instruction=return_global_instructions(shop_name),
    tools=[
        query_dialogflow,
    ],
    # 添加生成設定，提高回答的穩定性和準確性
    generate_content_config=types.GenerateContentConfig(
        temperature=0.15,  # 進一步降低溫度，提高電商政策回答的一致性
        top_p=0.92,
        top_k=40,
        candidate_count=1,  # 只生成一個回答版本，確保政策回答一致性
    ),
)