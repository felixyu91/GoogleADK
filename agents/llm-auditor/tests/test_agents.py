"""
測試已部署的 Vertex AI Agent Engine 代理

這個腳本用於測試已部署到 Vertex AI Agent Engine 的代理。
可以使用命令行參數指定測試參數，包括代理 ID、項目 ID、位置和測試消息。

用法示例:
    python test_remote_agent.py --agent_id 6043698758535872512 --message "小三美日有哪些付款方式?" --agent_type e-commerce
    python test_remote_agent.py --agent_id 5339096523084922880 --message "Can you audit this code for security?" --agent_type llm-auditor
"""

import argparse
import os
from typing import Optional, Dict, Any, List
import time
import vertexai

# 確保導入正確的 agent_engines 模組
try:
    # 新版本導入方式
from vertexai import agent_engines
except ImportError:
    # 備選導入方式
    try:
        from vertexai.preview import agent_engines
    except ImportError:
        # 如果兩種方式都無法導入，建議更新 vertexai 庫
        print("錯誤: 無法導入 agent_engines 模組。請更新 vertexai 庫:")
        print("pip install --upgrade google-cloud-aiplatform[agent_engines]")
        exit(1)

# 嘗試導入必要的類型
try:
    # 新版 ADK 導入路徑
    from google.adk.public.agent.model import Content, Part
    from google.adk.sessions import VertexAiSessionService
    from google.adk.events import Event
except ImportError:
    try:
        # 較舊版本或替代導入路徑
        from google.adk.public import Content, Part
        from google.adk.sessions import VertexAiSessionService
        from google.adk.events import Event
    except ImportError:
        print("無法導入 Google ADK 必要模塊，請檢查安裝版本")
        print("您當前安裝的 ADK 版本可能不兼容")
        print("嘗試執行: pip install --upgrade google-adk")
        exit(1)

from google import adk


def parse_args() -> argparse.Namespace:
    """解析命令行參數"""
    parser = argparse.ArgumentParser(description="測試已部署的 Agent Engine 代理")
    
    parser.add_argument(
        "--agent_id",
        required=True,
        help="代理 ID (例如: 6043698758535872512)",
    )
    parser.add_argument(
        "--project_id",
        default=os.getenv("GOOGLE_CLOUD_PROJECT", "arch-qa-454806"),
        help="GCP 項目 ID (默認使用環境變量)",
    )
    parser.add_argument(
        "--location",
        default=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        help="GCP 位置 (默認使用環境變量)",
    )
    parser.add_argument(
        "--message",
        default=None,
        help="要發送給代理的測試消息",
    )
    parser.add_argument(
        "--agent_type",
        choices=["e-commerce", "llm-auditor"],
        default="e-commerce",
        help="代理類型，決定默認測試消息",
    )
    
    return parser.parse_args()


def get_default_test_messages(agent_type: str) -> List[str]:
    """根據代理類型獲取默認測試消息"""
    messages = {
        "e-commerce": [
            "小三美日有哪些付款方式?",
            "如果我要退貨該怎麼做?",
            "發票可以開立統編嗎?",
            "折價券怎麼使用?"
        ],
        "llm-auditor": [
            "Can you audit this code for security vulnerabilities? function authenticate(username, password) { if(username === 'admin' && password === 'password123') return true; return false; }",
            "Is storing passwords in plaintext a security risk?",
            "What are common security vulnerabilities in web applications?"
        ]
    }
    return messages.get(agent_type, ["Hello!"])


def get_resource_name(project_id: str, location: str, agent_id: str) -> str:
    """構建完整的代理資源名稱"""
    return f"projects/{project_id}/locations/{location}/reasoningEngines/{agent_id}"


def test_agent_with_messages(
    resource_name: str,
    messages: List[str],
    user_id: str = "test_user_123"
) -> None:
    """使用多個測試消息測試代理"""
    # 獲取已部署的代理
    print(f"連接到代理: {resource_name}")
    remote_agent = agent_engines.get(resource_name)
    
    # 創建會話
    print(f"創建與代理 {remote_agent.display_name or '(未命名)'} 的測試會話")
    session = remote_agent.create_session(user_id=user_id)
    session_id = session["id"]
    print(f"會話 ID: {session_id}")
    
    # 逐個發送測試消息
    for i, message in enumerate(messages):
        print(f"\n{'='*80}")
        print(f"測試消息 {i+1}: {message}")
        print(f"{'='*80}")
        print("代理回應:")
        
        # 使用流式響應獲取代理回應
        for event in remote_agent.stream_query(
            user_id=user_id,
            session_id=session_id,
            message=message,
        ):
            if event.get("content", None):
                print(event.get("content"), end="")
                
        print("\n")  # 在回應後添加空行


def main() -> None:
    """主函數"""
    args = parse_args()
    
    # 設置測試消息
    if args.message:
        test_messages = [args.message]
    else:
        test_messages = get_default_test_messages(args.agent_type)
    
    # 初始化 Vertex AI
    vertexai.init(
        project=args.project_id,
        location=args.location,
    )
    
    # 獲取完整的資源名稱
    resource_name = get_resource_name(args.project_id, args.location, args.agent_id)
    
    # 測試代理
    try:
        test_agent_with_messages(resource_name, test_messages)
    except Exception as e:
        print(f"測試代理時發生錯誤: {str(e)}")


if __name__ == "__main__":
    main()