"""faq Agent: 透過 Dialogflow API 檢索小三美日網店的常見問題。"""
import os

from google.genai import types
from google.adk.agents import LlmAgent

from dotenv import load_dotenv
from .prompts import return_instructions_faq2, return_global_instructions_faq2
from .tools import DialogflowTools

load_dotenv()

dialogflow_tools = DialogflowTools()

def query_dialogflow(text: str) -> str:
    """
    將使用者的問題傳送到 Dialogflow API 獲取回應
    
    Args:
        text: 使用者輸入的文字
    
    Returns:
        Dialogflow 回傳的回應內容
    """

    access_token = os.getenv("DIALOGFLOW_ACCESS_TOKEN")
    session_id = f"cc-87e66248-ec5b-468a-bfc0-a864593574a9"
    
    # 呼叫 Dialogflow API
    response = dialogflow_tools.detect_intent(
        session_id=session_id,
        text=text,
        access_token=access_token
    )
    
    # 解析回應並返回相關內容
    if response and 'queryResult' in response:
        response_messages = response['queryResult'].get('responseMessages', [])
        if response_messages and len(response_messages) > 0:
            text_obj = response_messages[0].get('text', {})
            if text_obj and 'text' in text_obj and len(text_obj['text']) > 0:
                return text_obj['text'][0]
        return "無法理解您的問題"
    else:
        return "抱歉，我目前無法回應您的問題，請稍後再試。"

root_agent = LlmAgent(
    model=os.getenv("FAQ_AGENT_MODEL"),
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