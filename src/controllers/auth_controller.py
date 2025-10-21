import requests
import os
from prisma import Prisma

from model.common_model import APIResponse
from model.auth_model import AuthTokenResponse

APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "")

async def auth_callback_handler(app_key: str = None, code: str = None) -> APIResponse:
    if app_key == None or code == None:
        return APIResponse(code=400, message="Invalid parameters")
    try:
        params = {
            "app_key": app_key,
            "app_secret": APP_SECRET_KEY,
            "auth_code": code,
            "grant_type": "authorized_code"
        }
        response = requests.get("https://auth.tiktok-shops.com/api/v2/token/get", params=params)
        response.raise_for_status()
        data: AuthTokenResponse = response.json().get("data", {})
        await Prisma.TiktokShopTokens.create(data=data.model_dump())

    except Exception as e:
        print(f"Error in auth_callback_handler: {e}")
        return APIResponse(code=500, message="Internal server error")
    return APIResponse(code=200, message="Authorization successful")

