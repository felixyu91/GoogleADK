"""
基底工具模組
包含多個 agent 共享的基礎功能
"""
import os

# 定義預設值
DEFAULT_SHOP_ID = 1  # 1=小三美日, 2=莎莎

def get_shop_id() -> int:
    """
    從環境變數取得商店 ID

    Returns:
        商店 ID (1=小三美日, 2=莎莎網店)
    """
    shop_id = os.environ.get('SHOP_ID')
    print(f"shop_id: {shop_id}")
    return int(shop_id)

def get_shop_name(shop_id: int) -> str:
    """
    根據商店 ID 取得商店名稱
    
    Returns:
        商店名稱（小三美日或莎莎）
    """

    shop_name =  "小三美日" if shop_id == 1 else "莎莎網店"
    print(f"shop_name: {shop_name}")

    return shop_name