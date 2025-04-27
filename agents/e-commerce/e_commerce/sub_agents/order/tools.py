"""訂單處理代理的工具函數。"""
from google.adk.tools import ToolContext

async def get_order_details(
    order_id: str,
    tool_context: ToolContext,
):
    """
    獲取訂單詳細信息。
    
    Args:
        order_id: 訂單編號
        tool_context: 工具上下文
        
    Returns:
        包含訂單詳細信息的字典
    """
    # 模擬訂單數據
    mock_orders = {
        "TG123": {
            "order_id": "TG123",
            "order_time": "2025-04-20T10:30:00Z",
            "amount": 1999.0,
            "status": "已出貨",
            "carrier": "7-11超商付款取貨",
            "items": [
                {"name": "高級精品茶壺", "quantity": 1, "price": 1999.0}
            ],
            "shipping_address": "台北市松山門市",
            "payment_method": "信用卡",
            "estimated_delivery": "2025-04-27"
        },
        "TG456": {
            "order_id": "TG456",
            "order_time": "2025-04-21T14:45:00Z",
            "amount": 4000.0,
            "status": "配送中",
            "carrier": "宅配",
            "items": [
                {"name": "時尚運動手錶", "quantity": 1, "price": 2500.0},
                {"name": "運動鞋", "quantity": 1, "price": 1500.0}  
            ],
            "shipping_address": "台北市",
            "payment_method": "LINE Pay",
            "estimated_delivery": "2025-04-29"
        },
        "TG789": {
            "order_id": "TG789",
            "order_time": "2025-04-22T09:15:00Z",
            "amount": 3200.0,
            "status": "未付款",
            "carrier": "待出貨",
            "items": [
                {"name": "無線藍牙耳機", "quantity": 1, "price": 3200.0}
            ],
            "shipping_address": "台中市",
            "payment_method": "ATM轉帳",
            "estimated_delivery": "2025-04-30"
        }
    }
    
    # 將當前查詢的訂單ID保存到狀態
    tool_context.state["active_order_id"] = order_id
    
    order = mock_orders.get(order_id)
    if not order:
        return {"error": f"找不到訂單 {order_id}"}
    
    return order