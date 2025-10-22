import requests
import os
from prisma import Prisma

from model.common_model import APIResponse
from model.auth_model import AuthTokenResponse

APP_KEY = os.getenv("APP_KEY", "")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "")

async def auth_callback_handler(app_key: str = None, code: str = None) -> APIResponse:
    if code == None:
        return APIResponse(code=400, message="Invalid parameters")
    try:
        params = {
            "app_key": APP_KEY,
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

async def refresh_token_handler():
    refresh_token = None
    try:
        tmp = await Prisma.TiktokShopTokens.get(
            where={
                "id": 1
            },
            select={
                "refresh_token": True
            }
        )
        refresh_token = tmp.refresh_token
    except Exception as e:
        print(f"Error fetching refresh token: {e}")
        return APIResponse(code=500, message="Internal server error")

    if refresh_token is None:
        return APIResponse(code=400, message="No refresh token found")
    
    try:
        params = {
            "app_key": APP_KEY,
            "app_secret": APP_SECRET_KEY,
            "refresh_token": refresh_token,
            "grant_type": "authorized_code"
        }
        response = requests.get("https://auth.tiktok-shops.com/api/v2/token/refresh", params=params)
        response.raise_for_status()
        data: AuthTokenResponse = response.json().get("data", {})
        await Prisma.TiktokShopTokens.update({
            "where": {
                "id": 1
            },
            "data": data.model_dump()
        })
        return APIResponse(code=200, message="Authorization successful")
    except Exception as e:
        print(f"Error in auth_callback_handler: {e}")
        return APIResponse(code=500, message="Internal server error")