"""投訴處理代理的工具函數。"""
from google.adk.tools import ToolContext

async def categorize_complaint(
    complaint_text: str,
    tool_context: ToolContext,
):
    """
    分析並分類客戶投訴。
    
    Args:
        complaint_text: 客戶投訴的文字描述
        tool_context: 工具上下文
        
    Returns:
        包含投訴分類和嚴重程度的字典
    """
    # 這裡是簡化的分類邏輯，實際應用中可能需要更複雜的分析
    categories = ["產品質量", "服務態度", "物流延誤", "價格爭議", "其他"]
    severities = ["輕微", "中等", "嚴重", "極為嚴重"]
    
    # 模擬分類過程
    # 在實際實現中，這裡可以使用更複雜的分類演算法
    keywords = {
        "產品質量": ["壞了", "損壞", "不良", "品質", "瑕疵", "故障"],
        "服務態度": ["態度", "服務", "客服", "禮貌", "粗魯"],
        "物流延誤": ["物流", "快遞", "延遲", "送貨", "等待"],
        "價格爭議": ["價格", "退款", "贵", "便宜", "促銷"],
    }
    
    complaint_lower = complaint_text.lower()
    detected_category = "其他"
    
    for category, words in keywords.items():
        if any(word in complaint_lower for word in words):
            detected_category = category
            break
    
    # 確定嚴重程度
    severity = "中等"  # 默認中等
    if "非常" in complaint_lower or "極為" in complaint_lower or "極其" in complaint_lower:
        severity = "嚴重"
    if "要求賠償" in complaint_lower or "投訴" in complaint_lower or "舉報" in complaint_lower:
        severity = "極為嚴重"
        
    result = {
        "category": detected_category,
        "severity": severity,
        "analysis": f"根據內容分析，這是一個關於{detected_category}的{severity}投訴。"
    }
    
    # 保存分類結果到狀態中
    tool_context.state["complaint_category"] = result
    
    return result

async def suggest_resolution(
    complaint_category: str,
    severity: str,
    tool_context: ToolContext,
):
    """
    根據投訴類型和嚴重程度提供解決方案建議。
    
    Args:
        complaint_category: 投訴類別
        severity: 嚴重程度
        tool_context: 工具上下文
        
    Returns:
        包含建議解決方案的字典
    """
    resolutions = {
        "產品質量": {
            "輕微": "提供產品使用指導或故障排除步驟",
            "中等": "提供產品維修或部分退款",
            "嚴重": "提供產品更換或全額退款",
            "極為嚴重": "提供產品更換、全額退款並額外賠償",
        },
        "服務態度": {
            "輕微": "道歉並重新培訓相關人員",
            "中等": "道歉、提供小額優惠券作為補償",
            "嚴重": "道歉、提供大額優惠券或折扣",
            "極為嚴重": "道歉、提供重要補償並進行內部調查",
        },
        "物流延誤": {
            "輕微": "道歉並提供物流更新",
            "中等": "道歉並提供小額優惠券",
            "嚴重": "道歉、退還運費並提供優惠券",
            "極為嚴重": "道歉、退還運費、提供額外補償",
        },
        "價格爭議": {
            "輕微": "解釋價格政策",
            "中等": "提供小額折扣或優惠券",
            "嚴重": "提供價格調整或部分退款",
            "極為嚴重": "提供全額退款或大幅度降價",
        },
        "其他": {
            "輕微": "提供一般性解決方案",
            "中等": "提供特定解決方案和小額補償",
            "嚴重": "提供全面解決方案和合理補償",
            "極為嚴重": "提供完整解決方案和豐厚補償",
        }
    }
    
    # 獲取對應的解決方案
    resolution = resolutions.get(complaint_category, {}).get(severity, "進行個案分析並提供客制化解決方案")
    
    # 生成具體步驟
    steps = []
    if complaint_category == "產品質量":
        steps = [
            "聯繫客戶了解詳細的產品問題",
            "要求提供產品損壞或問題的照片或視頻證據",
            "安排技術人員評估問題",
            f"根據評估結果提供{resolution.lower()}",
            "跟進客戶滿意度"
        ]
    elif complaint_category == "服務態度":
        steps = [
            "向客戶表達誠摯的歉意",
            "記錄涉及的員工和具體情況",
            f"{resolution}",
            "確保相關員工得到適當培訓",
            "跟進客戶滿意度"
        ]
    else:
        steps = [
            "詳細了解客戶的具體問題",
            "記錄投訴詳情以便後續追蹤",
            f"提供解決方案：{resolution}",
            "跟進解決情況",
            "確認客戶滿意度"
        ]
    
    result = {
        "recommended_resolution": resolution,
        "steps": steps,
        "note": "請根據具體情況調整解決方案"
    }
    
    return result

async def get_previous_complaints(
    customer_id: str,
    tool_context: ToolContext,
):
    """
    查詢客戶的歷史投訴記錄。
    
    Args:
        customer_id: 客戶ID
        tool_context: 工具上下文
        
    Returns:
        包含歷史投訴記錄的字典
    """
    # 模擬歷史投訴數據
    # 實際應用中，這裡會連接到資料庫或API
    mock_complaints = {
        "C001": [
            {"date": "2025-01-15", "category": "產品質量", "status": "已解決"},
            {"date": "2024-11-20", "category": "物流延誤", "status": "已解決"}
        ],
        "C002": [
            {"date": "2025-03-10", "category": "價格爭議", "status": "處理中"}
        ],
        "C003": []
    }
    
    # 獲取客戶歷史投訴
    complaints = mock_complaints.get(customer_id, [])
    
    result = {
        "customer_id": customer_id,
        "complaint_count": len(complaints),
        "complaints": complaints,
        "is_repeat_complainer": len(complaints) > 1
    }
    
    return result