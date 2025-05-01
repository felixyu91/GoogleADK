"""測試 Dialogflow CX SDK 整合功能"""
import os
import sys
from pathlib import Path

# 添加父目錄到 Python 路徑以便導入 faq2.tools
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from e_commerce.sub_agents.faq2.tools import DialogflowSDKTools

def main():
    """主函數，測試 Dialogflow CX 整合"""

    googleCredentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    # 檢查環境變數是否已設定
    if googleCredentials is None:
        print("[錯誤] 環境變數 GOOGLE_APPLICATION_CREDENTIALS 未設定")
        return
    
    print(f"GOOGLE_APPLICATION_CREDENTIALS: {googleCredentials}")

    # 創建 DialogflowSDKTools 實例
    dialogflow_tools = DialogflowSDKTools()
    
    # 設定會話 ID
    session_id="cc-87e66248-ec5b-468a-bfc0-a864593574a9"
    
    # 測試查詢
    test_queries = [
        "請問你是哪間商店的客服?",
        "可以開發票嗎?",
        "有支援哪些付款方式",
        "多久會出貨?",
        "有支援哪些配送方式?"
    ]
    
    # 執行測試
    print("===== 測試 Dialogflow CX SDK =====")
    print(f"專案 ID: {dialogflow_tools.project_id}")
    print(f"位置: {dialogflow_tools.location}")
    print(f"客服 ID: {dialogflow_tools.agent_id}")
    print(f"會話 ID: {session_id}")
    print("-" * 50)
    
    for i, query in enumerate(test_queries):
        print(f"\題目 {i+1}: '{query}'")
        response = dialogflow_tools.detect_intent(
            session_id=session_id,
            text=query
        )
        
        if response:
            # 提取關鍵資訊
            query_result = response.query_result
            response_text = query_result.response_messages[0].text.text[0] if query_result.response_messages else "無回應文字"
            confidence = query_result.intent_detection_confidence
            
            # 印出更多有用的資訊
            print(f"意圖: {query_result.intent.display_name if query_result.intent else '無意圖'}")
            print(f"置信度: {confidence:.2%}")
            print(f"回應: {response_text}")

            # 印出匹配條件
            if query_result.match and query_result.match.confidence > 0:
                print(f"匹配類型: {query_result.match.match_type}")
                print(f"匹配置信度: {query_result.match.confidence:.2%}")

        else:
            print("請求失敗，沒有收到回應")
        
        print("-" * 50)
    
    print("\n測試完成！")

if __name__ == "__main__":
    main()