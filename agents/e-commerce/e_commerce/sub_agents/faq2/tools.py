from typing import Optional
import time
import os
import google.auth
import google.auth.transport.requests

DEFAULT_AGENT_IDS = {
    1: "63e53e79-74dd-4aa9-b414-4222f5f290b7",  # 小三美日
    2: "1958cdad-1e19-4c11-8360-54281f7e7b97",  # 莎莎
}

# 使用正確的 Dialogflow CX SDK 導入語句
try:
    credentials, project = google.auth.default()
    # print(f"成功獲取默認憑證！專案 ID: {project}")
    # print(f"憑證類型: {type(credentials).__name__}")
    # print(f"憑證是否有效: {credentials.valid}")

    from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
    from google.cloud.dialogflowcx_v3.types import (
        DetectIntentRequest,
        DetectIntentResponse,
        QueryInput, TextInput,
        QueryParameters
    )
except ImportError as e:
    print(f"[重要警告] 無法導入 Dialogflow CX SDK: {e}")
    print("poetry add google-cloud-dialogflow-cx")
    raise

def get_agent_id(shop_id: int) -> int:
    """
    根據商店 ID 獲取對應的 Dialogflow Agent ID
    
    Returns:
        對應的 Dialogflow Agent ID 字符串
    """
    if shop_id is None:
        shop_id = get_shop_id()
    
    # 根據商店 ID 獲取對應的 Agent ID
    agent_id = DEFAULT_AGENT_IDS.get(shop_id, DEFAULT_AGENT_IDS[1])
    print(f"agent_id: {agent_id}")

    return agent_id

class DialogflowSDKTools:
    """使用 Google Cloud Dialogflow CX SDK 與 Dialogflow 服務通訊"""

    def __init__(
        self,
        project_id: str = "arch-qa-454806",
        location: str = "global",
        agent_id: str = "63e53e79-74dd-4aa9-b414-4222f5f290b7"
    ):
        """
        Args:
            project_id: GCP 專案 ID
            location: 代理位置
        """
        self.project_id = project_id
        self.location = location
        
        googleCredentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") 
        print(f"googleCredentials: {googleCredentials}")

        # 檢查環境變數
        # if googleCredentials is None:
        #     raise Exception("未設定 GOOGLE_APPLICATION_CREDENTIALS 環境變數")
        
        # 建立 SessionsClient，SDK 會自動讀取環境變數 GOOGLE_APPLICATION_CREDENTIALS
        print("[資訊] 初始化 Dialogflow CX SDK")
        self.client = SessionsClient()

    def detect_intent(
        self,
        agent_id: str,
        session_id: str,
        text: str,
        language_code: str = "zh-TW",
        time_zone: str = "Asia/Hong_Kong",
        max_retries: int = 3,
    ) -> Optional[DetectIntentResponse]:
        """
        使用 Dialogflow CX SDK 偵測使用者意圖

        Args:
            session_id: 對話工作階段 ID
            text: 使用者輸入文字
            language_code: 語言代碼（預設繁體中文）
            time_zone: 時區（預設亞洲／香港）
        Returns:
            DetectIntentResponse 物件；若失敗則回傳 None
        """
        try:
            # 建立完整的 session 路徑
            session_path = f"projects/{self.project_id}/locations/{self.location}/agents/{agent_id}/sessions/{session_id}"
            
            # 設定查詢文字輸入
            text_input = TextInput(text=text)
            query_input = QueryInput(text=text_input, language_code=language_code)
            
            # 調整查詢參數，優化知識庫匹配
            query_params = QueryParameters(
                time_zone=time_zone,
                parameters={
                    # 提高知識庫檢索的優先級
                    "knowledgeBaseQuerySource": "knowledge",
                    "enableKnowledgeConnectors": True,
                    "disableWebhook": False,  # 確保 webhook 可用於知識庫查詢
                    "knowledgeAnswer": {
                        "enabled": True,
                        "confidence_threshold": 0.3,  # 降低閾值以增加匹配機會
                        "max_answers": 3  # 增加返回答案數量
                    }
                }
            )
            
            # 編寫請求
            request = DetectIntentRequest(
                session=session_path,
                query_input=query_input,
                query_params=query_params
            )
            
            # 向 Dialogflow CX 發送請求
            print(f"[Dialogflow CX] 發送請求: {text}")
            
            retry_count = 0
            while retry_count <= max_retries:  # 允許初始嘗試 + max_retries 次重試
                start_time = time.time()
                response = self.client.detect_intent(request)
                end_time = time.time()
                print(f"回應時間: {end_time - start_time:.2f} 秒")
                
                # 檢查 match_type 是否為 8 (KNOWLEDGE)
                if (response and response.query_result and 
                    response.query_result.match and 
                    response.query_result.match.match_type == 8):
                    return response
                
                # 如果不是 KNOWLEDGE，且還有重試次數，則重試
                if retry_count < max_retries:
                    retry_count += 1
                    print(f"[重試] match_type 不是 8 (KNOWLEDGE)，目前為 {response.query_result.match.match_type if response.query_result.match else 'None'}，第 {retry_count} 次重試...")
                    time.sleep(0.5)  # 短暫延遲，避免過快重試
                else:
                    # 已用完所有重試次數，返回最後一次嘗試的結果
                    print(f"[警告] 已重試 {max_retries} 次，仍未獲得 KNOWLEDGE 匹配結果")
                    return response
            
            return response
            
        except Exception as e:
            print(f"[錯誤] 呼叫 Dialogflow CX detect_intent 失敗：{e}")
            return None