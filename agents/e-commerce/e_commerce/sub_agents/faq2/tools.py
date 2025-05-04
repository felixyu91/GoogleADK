from typing import Optional
import time
import os
import google.auth
import google.auth.transport.requests

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
        if googleCredentials is None:
            print("環境變數 GOOGLE_APPLICATION_CREDENTIALS 未設定")
        
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
            
            # 設定查詢參數
            query_params = QueryParameters(time_zone=time_zone)
            
            # 編寫請求
            request = DetectIntentRequest(
                session=session_path,
                query_input=query_input,
                query_params=query_params
            )
            
            # 向 Dialogflow CX 發送請求
            print(f"[開始] 發送請求到 Dialogflow CX: {text}")
            start_time = time.time()
            response = self.client.detect_intent(request)
            end_time = time.time()
            print(f"[完成] Dialogflow CX 回應時間: {end_time - start_time:.2f} 秒")
            
            return response
            
        except Exception as e:
            print(f"[錯誤] 呼叫 Dialogflow CX detect_intent 失敗：{e}")
            return None