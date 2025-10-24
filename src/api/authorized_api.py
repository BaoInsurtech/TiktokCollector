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

print("APP_KEY:", APP_KEY)
print("APP_SECRET_KEY:", APP_SECRET_KEY)
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

async def get_authorized_categories_set(access_token: str,
                         shop_cipher: str,
                         pageSize: int | None = 20,
                         body: dict | None = None,
                         params: dict | None = None):
    """
    Gọi API lấy danh sách đơn hàng từ TikTok Shop
    """
    api_path = "/authorization/202405/category_assets"
    timestamp = int(time.time())
    qs = {
        "app_key": APP_KEY,
        "timestamp": str(timestamp),
        # "shop_cipher": shop_cipher or "",
        # "page_size": str(pageSize),
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