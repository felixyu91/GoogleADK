"""faq Agent: 透過 Dialogflow SDK 檢索小三美日網店的常見問題。"""
import os

from google.genai import types
from google.adk.agents import LlmAgent

from dotenv import load_dotenv
from .prompts import return_instructions_faq2, return_global_instructions_faq2
from .tools import DialogflowSDKTools

load_dotenv()

# 初始化 Dialogflow SDK 工具
dialogflow_tools = DialogflowSDKTools()

def query_dialogflow(text: str) -> str:
    """
    將使用者的問題傳送到 Dialogflow CX 使用 SDK 獲取回應
    
    Args:
        text: 使用者輸入的文字
    
    Returns:
        Dialogflow 回傳的回應內容
    """
    # 產生一個唯一的對話 ID
    session_id = f"cc-87e66248-ec5b-468a-bfc0-a864593574a9"
    
    # 使用 SDK 向 Dialogflow CX 查詢意圖
    response = dialogflow_tools.detect_intent(
        session_id=session_id,
        text=text,
    )
    
    # 解析回應
    if response:
        # 取得 QueryResult
        query_result = response.query_result
        
        # 提取意圖資訊（若有）
        intent = "未識別意圖"
        if query_result.intent and query_result.intent.display_name:
            intent = query_result.intent.display_name
            
        # 首先嘗試從回應訊息中獲取文字
        if query_result.response_messages:
            for msg in query_result.response_messages:
                if hasattr(msg, "text") and msg.text and msg.text.text:
                    return msg.text.text[0] if msg.text.text else f"我理解你想詢問: {intent}"
        
        # 如果回應訊息中沒有文字，嘗試從 fulfillment_text 獲取
        if query_result.fulfillment_text:
            return query_result.fulfillment_text
        
        # 最後回傳識別的意圖
        return f"我理解你想詢問關於「{intent}」的問題，但目前沒有特定回應。"
    
    # 如果完全無法獲取回應
    return "抱歉，我目前無法回應您的問題，請稍後再試。"

root_agent = LlmAgent(
    model=os.getenv("FAQ_AGENT_MODEL", "gemini-2.0-flash-001"),
    name='faq2_agent',
    instruction=return_instructions_faq2(),
    global_instruction=return_global_instructions_faq2(),
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