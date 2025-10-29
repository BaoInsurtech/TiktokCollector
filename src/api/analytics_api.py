import requests
import utils.sign as generate_sign
import time
import os
import httpx
from model.common_model import APIResponse

from typing import Optional, Dict, Any

TIKTOK_API_BASE = "https://open-api.tiktokglobalshop.com"
APP_KEY = os.getenv("APP_KEY", "")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "")

async def get_shop_performance(access_token: str,
                         shop_cipher: str,
                        start_date_ge: str | None = None,
                            end_date_lt: str | None = None,
                         body: dict | None = None,
                         params: dict | None = None):
    """
    Gọi API lấy danh sách đơn hàng từ TikTok Shop
    """
    api_path = "/analytics/202405/shop/performance"
    timestamp = int(time.time())
    qs = {
        "app_key": APP_KEY,
        "timestamp": str(timestamp),
        "shop_cipher": shop_cipher or "",
        "start_date_ge": start_date_ge or "",
        "end_date_lt": end_date_lt or "",
    }
    if params:
        qs.update(params)

    url = f"{TIKTOK_API_BASE}{api_path}"
    headers = {
        "x-tts-access-token": access_token,
        "content-type": "application/json",
        "Accept": "application/json"
    }

    request_option = {
        "uri": url,
        "qs": qs,
        "headers": headers,
        "body": body or {},
    }

   # Generate signature
    sign = generate_sign.generate_sign(request_option, APP_SECRET_KEY)
    qs["sign"] = sign

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url, headers=headers, params=qs)
        
        # ✅ Parse JSON từ httpx.Response
        try:
            body = resp.json()
        except Exception as e:
            body = {
                "code": resp.status_code,
                "message": resp.text,
                "data": None
            }
        
        # Extract fields
        code = int(body.get("code", resp.status_code))
        message = body.get("message", "")
        data = body.get("data")
        
        print(f"✅ Response code: {code}, message: {message}")
        
        return {
            "code": code,
            "message": message,
            "data": data,
        }
    
async def get_shop_product_performance_list(access_token: str,
                         shop_cipher: str,
                        start_date_ge: str | None = None,
                            end_date_lt: str | None = None,
                         body: dict | None = None,
                         params: dict | None = None):
    """
    Gọi API lấy danh sách đơn hàng từ TikTok Shop
    """
    api_path = "/analytics/202405/shop_products/performance"
    timestamp = int(time.time())
    qs = {
        "app_key": APP_KEY,
        "timestamp": str(timestamp),
        "shop_cipher": shop_cipher or "",
        "start_date_ge": start_date_ge or "",
        "end_date_lt": end_date_lt or "",
    }
    if params:
        qs.update(params)

    url = f"{TIKTOK_API_BASE}{api_path}"
    headers = {
        "x-tts-access-token": access_token,
        "content-type": "application/json",
        "Accept": "application/json"
    }

    request_option = {
        "uri": url,
        "qs": qs,
        "headers": headers,
        "body": body or {},
    }

   # Generate signature
    sign = generate_sign.generate_sign(request_option, APP_SECRET_KEY)
    qs["sign"] = sign

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url, headers=headers, params=qs)
        
        # ✅ Parse JSON từ httpx.Response
        try:
            body = resp.json()
        except Exception as e:
            body = {
                "code": resp.status_code,
                "message": resp.text,
                "data": None
            }
        
        # Extract fields
        code = int(body.get("code", resp.status_code))
        message = body.get("message", "")
        data = body.get("data")
        
        print(f"✅ Response code: {code}, message: {message}")
        
        return {
            "code": code,
            "message": message,
            "data": data,
        }