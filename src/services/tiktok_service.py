import os 
import asyncio
import time
import requests
from typing import Optional, Dict, Any
import httpx
import urllib.parse
from ..utils.sign import generate_sign

TIKTOK_API_BASE = "https://open-api.tiktokglobalshop.com"
APP_KEY = os.getenv("APP_KEY", "")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "")

TIKTOK_API_ENDPOINTS = [
    ("/order/202309/orders/search", "order_search"),

]

async def call_tiktok_api(access_token: str, 
                          api_path: str, 
                          params: dict | None = None,
                          body: dict | None = None,
                          shop_cipher: str | None = None):
    
    timestamp = int(time.time())
    qs = {
        "app_key": APP_KEY,
        "timestamp": str(timestamp),
        "shop_cipher": shop_cipher or "",
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

    sign = generate_sign(request_option, APP_SECRET_KEY)
    qs["sign"] = sign

    async with httpx.AsyncClient(timeout=30.0) as client:
        if body:
            resp = await client.post(request_option["uri"], headers=headers, params=qs, json=body)
        else:
            resp = await client.get(request_option["uri"], headers=headers, params=qs)

        try:
            data = resp.json()
        except Exception:
            data = {"raw_text": resp.text}

        return {
            "url": str(resp.url),
            "status_code": resp.status_code,
            "elapsed": resp.elapsed.total_seconds(),
            "data": data,
        }