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
"請問你是誰呢?",
"怎麼看我領過哪些折價券?",
"假日也會配送嗎?",
"退貨後還會收到通知嗎?",
"折價券要怎麼使用?",
"能不能補寄紙本發票嗎?",
"我填錯地址要怎麼辦?",
"可以存電子載具嗎?",
"我要怎麼修改我的電話或地址?",
"下單會收到 email 嗎?",
"能不能存電子載具嗎?",
"退貨流程要怎麼申請?",
"怎麼看訂單什麼時候送達?",
"收件人可以換人嗎?",
"退貨要自己出運費嗎?",
"我能不能查之前的發票記錄嗎?",
"可以自己選物流公司嗎?",
"訂單成立後會收到什麼通知?",
"要怎麼查包裹現在送到哪?",
"要登入才能查訂單嗎?",
"付款沒跳成功怎麼辦?",
"退貨後還會收到通知嗎?",
"怎麼開統編發票?",
"用街口支付可以嗎?",
"我可以選配送時間嗎?",
"信用卡付款會很安全嗎?",
"付款完成會通知我嗎?",
"地址填錯可以改嗎?",
"退貨會影響優惠嗎?",
"你們有真人客服嗎?",
"出貨會通知我嗎?",
"取消後什麼時候會退款?",
"訂單成立後會收到什麼通知?",
"信用卡付款會很安全嗎?",
"出貨會發簡訊嗎?",
"假日也會配送嗎?",
"什麼時候會出貨?",
"可以補寄紙本發票嗎?",
"訂單能不能修改嗎?",
"退貨後折價券還會退回嗎?",
"我可以指定送到超商嗎?",
"發票填錯可以改嗎?",
"我填錯地址怎麼辦?",
"退貨地址在哪裡看?",
"折價券有期限嗎?",
"下單會收到 email 嗎?",
"出貨會通知我嗎?",
"收件人能不能換人嗎?",
"我可以查之前的發票記錄嗎?",
"可以填英文地址嗎?",
"你們有真人客服嗎?",
"客服幾點上班?",
"退款多久會入帳?",
"能不能自己選物流公司嗎?",
"怎麼看我的退款進度?",
"能不能寄送到外島嗎?",
"我能不能選配送時間嗎?",
"有哪些付款方式可以選?",
"退款會發通知提醒嗎?",
"要登入才能查訂單嗎?",
"什麼情況不能退貨?",
"我會收到物流追蹤嗎?",
"地址填錯能不能改嗎?",
"可以用 Apple Pay 結帳嗎?",
"要怎麼看訂單什麼時候送達?",
"能不能指定朋友代收嗎?",
"可以同時用多張折價券嗎?",
"退貨一定要原包裝嗎?",
"退貨流程怎麼申請?",
"忘記密碼怎麼辦?",
"退款會退到原本的卡嗎?",
"我可以在哪查到訂單明細?",
"我會收到物流追蹤嗎?",
"我能不能在哪查到訂單明細?",
"發票會一起寄來嗎?",
"出貨會發簡訊嗎?",
"能不能取消訂單嗎?",
"可以寄送到外島嗎?",
"付款沒跳成功要怎麼辦?",
"可以取消訂單嗎?",
"退貨後折價券還會退回嗎?",
"退貨要自己出運費嗎?",
"退貨一定要原包裝嗎?",
"折價券怎麼使用?",
"退貨會影響優惠嗎?",
"我能不能指定送到超商嗎?",
"要怎麼看我的退款進度?",
"發票會一起寄來嗎?",
"可以指定朋友代收嗎?",
"送到公司地址可以嗎?",
"有哪些付款方式能不能選?",
"訂單可以修改嗎?",
"退款多久會入帳?",
"要怎麼看我領過哪些折價券?",
"可以刷分期嗎?",
"怎麼查包裹現在送到哪?",
"付款完成會通知我嗎?",
"忘記密碼要怎麼辦?",
"折價券有期限嗎?",
"什麼時候會出貨?",
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
        print(f"題目{i + 1}")
        response = dialogflow_tools.detect_intent(
            agent_id=agent_id,
            session_id=session_id,
            text=query
        )
        
        if response:
            # 提取關鍵資訊
            query_result = response.query_result
            response_text = query_result.response_messages[0].text.text[0].replace('\n', ' ').replace('\r', ' ')
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
    file_path = os.path.join(current_script_dir, f"result_{shop_id}.csv")
    
    print(f"\n將 {len(all_responses)} 個回應保存到 {file_path}...")
    
    try:
        # 如果文件已存在，先刪除
        if os.path.exists(file_path):
            os.remove(file_path)
            print("文件刪除成功")
        
        # 引入 csv 模塊
        import csv
        
        # 寫入新 CSV 文件
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # 寫入標題行
            # writer.writerow(['問題', '回應'])
            
            for i, response_text in enumerate(all_responses):
                writer.writerow([response_text])
        
        print(f"成功將回應保存到 {file_path}")
    except Exception as e:
        print(f"保存文件時發生錯誤: {e}")

if __name__ == "__main__":
    main()