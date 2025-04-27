from google.adk.tools import ToolContext
from google.adk.tools.agent_tool import AgentTool
# from google.adk.rag.vertexai import VertexAiRagRetriever  # 取消註釋，啟用 RAG 導入

# 移除對不存在子代理的導入
# from .sub_agents import order_agent

async def call_order_agent(
    question: str,
    tool_context: ToolContext,
):
"""
    訂單代理：回傳 3 筆假訂單資料
    欄位：order_id, order_time, amount
    """
    # print("call_order_agent")

# 不再使用不存在的子代理
    # agent_tool = AgentTool(agent=order_agent)
    orders = [
        {"order_id": "TG12345678", "order_time": "2025-04-20T10:30:00Z", "amount": 150.0},
        {"order_id": "TG66666666", "order_time": "2025-04-21T14:45:00Z", "amount": 250.0},
        {"order_id": "TG77777777", "order_time": "2025-04-22T09:15:00Z", "amount": 100.0},
    ]

    tool_context.state["order_agent_output"] = orders
    return orders

async def call_product_agent(
    question: str,
    tool_context: ToolContext,
):
    """
    商品代理：回傳 3 筆假商品資料
    欄位：name, description, price
    """
    products = [
        {"name": "高級精品茶壺", "description": "手工製作的精品茶壺，採用優質陶瓷", "price": 1999},
        {"name": "時尚運動手錶", "description": "防水運動手錶，具有心率監測功能", "price": 2500},
        {"name": "無線藍牙耳機", "description": "高音質無線藍牙耳機，具有降噪功能", "price": 3200},
    ]

    tool_context.state["product_agent_output"] = products
    return products

# 服務條款代理：使用 Vertex AI RAG Retriever
# call_service_agent = VertexAiRagRetriever(  # 取消註釋，啟用 RAG 功能
#     name="service_terms",
#     corpus_name="projects/392953038090/locations/us-central1/ragCorpora/2305843009213693952",
#     description="查詢服務條款與退換貨政策"
# ) 