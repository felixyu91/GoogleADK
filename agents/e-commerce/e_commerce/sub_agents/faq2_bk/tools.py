import requests
from typing import Dict, Any, Optional

class DialogflowTools:
    """對話流工具集，提供與 Dialogflow API 相關的功能"""
    
    def __init__(self, project_id: str = "arch-qa-454806", 
                 location: str = "global", 
                 agent_id: str = "63e53e79-74dd-4aa9-b414-4222f5f290b7"):
        """初始化對話流工具集
        
        Args:
            project_id: Google Cloud 專案 ID
            location: 代理程式所在位置
            agent_id: 代理程式 ID
        """
        self.project_id = project_id
        self.location = location
        self.agent_id = agent_id
        self.base_url = f"https://global-dialogflow.googleapis.com/v3/projects/{project_id}/locations/{location}/agents/{agent_id}"
    
    def detect_intent(self, session_id: str, text: str, access_token: str) -> Optional[Dict[str, Any]]:
        """使用 Dialogflow 偵測使用者意圖
        
        Args:
            session_id: 對話工作階段 ID
            text: 使用者輸入文字
            access_token: Google OAuth 存取權杖
            
        Returns:
            Dialogflow 回應，若請求失敗則回傳 None
        """
        try:
            url = f"{self.base_url}/sessions/{session_id}:detectIntent"
            
            headers = {
                "X-Goog-User-Project": self.project_id,
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            
            payload = {
                "queryInput": {
                    "text": {
                        "text": text
                    },
                    "languageCode": "zh-tw"
                },
                "queryParams": {
                    "timeZone": "Asia/Hong_Kong"
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"呼叫 Dialogflow API 時發生錯誤: {str(e)}")
            return None