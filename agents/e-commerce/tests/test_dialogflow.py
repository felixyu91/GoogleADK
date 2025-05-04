"""測試 Dialogflow CX SDK 整合功能"""
import os
import sys
import argparse
from pathlib import Path
from e_commerce.sub_agents.faq2.tools import DialogflowSDKTools
from google.cloud.dialogflowcx_v3.types import Match

# 添加父目錄到 Python 路徑以便導入 faq2.tools
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))


def main():
    """主函數，測試 Dialogflow CX 整合"""
    # 創建命令行參數解析器
    parser = argparse.ArgumentParser(description='測試 Dialogflow CX SDK 整合')
    # 添加 shop_id 參數
    parser.add_argument('--shop_id', type=int, default=1, 
                        help='商店 ID (1=小三美日, 2=莎莎)')

    googleCredentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    # 檢查環境變數是否已設定
    if googleCredentials is None:
        print("[錯誤] 環境變數 GOOGLE_APPLICATION_CREDENTIALS 未設定")
        return
    
    print(f"GOOGLE_APPLICATION_CREDENTIALS: {googleCredentials}")

    # 創建 DialogflowSDKTools 實例
    dialogflow_tools = DialogflowSDKTools()
    
    # 解析命令行參數
    args = parser.parse_args()

    shop_id = args.shop_id

    # 根據 shop_id 選擇 agent_id
    # 小三美日:63e53e79-74dd-4aa9-b414-4222f5f290b7
    # 莎莎:1958cdad-1e19-4c11-8360-54281f7e7b97
    if shop_id == 1:
        agent_id = "63e53e79-74dd-4aa9-b414-4222f5f290b7"
        print(f"使用商店 1 (小三美日) 的 agent_id: {agent_id}")
    else:
        agent_id = "1958cdad-1e19-4c11-8360-54281f7e7b97"
        print(f"使用商店 2 (莎莎) 的 agent_id: {agent_id}")

    # 設定會話 ID
    session_id="cc-87e66248-ec5b-468a-bfc0-a864593574a9"
    
    # 測試查詢
    test_queries = [
"請問你的身分是誰?",
"可以用哪些付款方式?",
"可以用 Apple Pay 嗎?",
"付款會有加密保障嗎?",
"什麼時候會出貨?",
"付款後多久可以收到商品?",
"出貨時間包含假日嗎?",
"要去哪裡查詢我的訂單?",
"可以查歷史訂單嗎?",
"訂單成立後會有通知嗎?",
"出貨後會有追蹤碼嗎?",
"可以追蹤我的包裹嗎?",
"海外地區有哪些配送服務?",
"海外運費怎麼算?",
"下單後還能取消嗎?",
"取消訂單後會退款嗎?",
"取消後多久會收到退款?",
"退貨需要保留原包裝嗎?",
"退貨需要填表嗎?",
"怎麼收到退款?",
"信用卡退款怎麼處理?",
"退款需要填身分證嗎?",
"退貨要自己出運費嗎?",
"退貨的運費會退還嗎?",
"怎麼用折價券?",
"折價券可以退嗎?",
"退貨會影響折價券嗎?",
"怎麼查電子發票?",
"發票可以捐贈嗎?",
"開立發票會寄給我嗎?",
"怎麼聯絡客服最快?",
"客服回覆時間要多久?",
"出貨會有通知嗎?",
"送達前會提前通知嗎?",
"退款大概要幾天?",
"退貨完成後多久退款?",
"付款失敗怎麼辦?",
"付款沒跳成功會怎樣?",
"地址填錯怎麼辦?",
"可以改收件地址嗎?",
"可以用 Apple Pay 是怎麼處理的?",
"退貨完成後多久退款?是怎樣的流程?",
"可以用哪些付款方式?是怎樣的流程?",
"怎麼聯絡客服最快?是怎樣的流程?",
"出貨會有通知是怎麼處理的?",
"出貨會有通知是怎麼處理的?",
"出貨時間包含假日是怎麼處理的?",
"下單後還能取消是怎麼處理的?",
"取消後多久會收到退款?是怎樣的流程?",
"取消後多久會收到退款?是怎樣的流程?",
"怎麼聯絡客服最快?是怎樣的流程?",
"取消後多久會收到退款?是怎樣的流程?",
"海外運費怎麼算?是怎樣的流程?",
"海外運費怎麼算?是怎樣的流程?",
"可以追蹤我的包裹是怎麼處理的?",
"怎麼查電子發票?是怎樣的流程?",
"信用卡退款怎麼處理?是怎樣的流程?",
"可以用哪些付款方式?是怎樣的流程?",
"退款大概要幾天?是怎樣的流程?",
"取消後多久會收到退款?是怎樣的流程?",
"可以改收件地址是怎麼處理的?",
"發票可以捐贈是怎麼處理的?",
"付款失敗怎麼辦?是怎樣的流程?",
"怎麼收到退款?是怎樣的流程?",
"可以追蹤我的包裹是怎麼處理的?",
"付款失敗怎麼辦?是怎樣的流程?",
"可以用 Apple Pay 是怎麼處理的?",
"開立發票會寄給我是怎麼處理的?",
"要去哪裡查詢我的訂單?是怎樣的流程?",
"怎麼查電子發票?是怎樣的流程?",
"付款沒跳成功會怎樣?是怎樣的流程?",
"可以追蹤我的包裹是怎麼處理的?",
"訂單成立後會有通知是怎麼處理的?",
"怎麼聯絡客服最快?是怎樣的流程?",
"怎麼用折價券?是怎樣的流程?",
"訂單成立後會有通知是怎麼處理的?",
"發票可以捐贈是怎麼處理的?",
"取消後多久會收到退款?是怎樣的流程?",
"信用卡退款怎麼處理?是怎樣的流程?",
"海外地區有哪些配送服務?是怎樣的流程?",
"下單後還能取消是怎麼處理的?",
"退貨要自己出運費是怎麼處理的?",
"海外地區有哪些配送服務?是怎樣的流程?",
"開立發票會寄給我是怎麼處理的?",
"退款需要填身分證是怎麼處理的?",
"什麼時候會出貨?是怎樣的流程?",
"付款失敗怎麼辦?是怎樣的流程?",
"出貨會有通知是怎麼處理的?",
"訂單成立後會有通知是怎麼處理的?",
"出貨後會有追蹤碼是怎麼處理的?",
"退貨會影響折價券是怎麼處理的?",
"退貨要自己出運費是怎麼處理的?",
"付款後可以改成其他付款方式嗎?",
"可以同時使用折價券和免運優惠嗎?",
"退貨後多久會收到退款通知?",
"Apple Pay 付款會有交易記錄嗎?",
"訂單取消後會收到簡訊或信件通知嗎?",
"查詢訂單需要登入會員嗎?",
"怎麼查詢我的退款處理狀態?",
"發票如果填錯了可以修改嗎?",
    ]

    all_responses = []
    
    # 執行測試
    print("===== 測試 Dialogflow CX SDK =====")
    print(f"專案 ID: {dialogflow_tools.project_id}")
    print(f"位置: {dialogflow_tools.location}")
    print(f"客服 ID: {agent_id}")
    print(f"會話 ID: {session_id}")
    print("-" * 50)
    
    for i, query in enumerate(test_queries):
        print(f"\題目 {i + 1}")
        response = dialogflow_tools.detect_intent(
            agent_id=agent_id,
            session_id=session_id,
            text=query
        )
        
        if response:
            # 提取關鍵資訊
            query_result = response.query_result
            response_text = query_result.response_messages[0].text.text[0] if query_result.response_messages else "無回應文字"
            confidence = query_result.intent_detection_confidence

            all_responses.append(response_text)
            
            # 印出更多有用的資訊
            print(f"intent: {query_result.intent}")
            print(f"置信度: {confidence:.4f}")
            print(f"回應: {response_text}")

            # 印出匹配條件，使用枚舉類型
            if query_result.match and query_result.match.confidence > 0:
                # 使用枚舉類型轉換數字為名稱
                mt_value = query_result.match.match_type
                try:
                    mt_enum = Match.MatchType(mt_value)    # 轉成 enum 物件
                    print(f"匹配類型: {mt_enum.name} (原值: {mt_value})")
                except ValueError:
                    print(f"匹配類型: 未知類型 (原值: {mt_value})")
                print(f"匹配置信度: {query_result.match.confidence:.4f}")

        else:
            print("請求失敗，沒有收到回應")
        
        print("-" * 50)
    
    print("\n測試完成！")

    # 將所有回應保存到文件
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_script_dir, f"result_{agent_id}.txt")
    
    print(f"\n將 {len(all_responses)} 個回應保存到 {file_path}...")
    
    try:
        # 如果文件已存在，先刪除
        if os.path.exists(file_path):
            os.remove(file_path)
            print("文件刪除成功")
        
        # 寫入新文件
        with open(file_path, 'w', encoding='utf-8') as f:
            for i, response_text in enumerate(all_responses):
                # 寫入序號、問題和回應
                f.write(f"{response_text}\n")
    except Exception as e:
        print(f"保存文件時發生錯誤: {e}")

if __name__ == "__main__":
    main()