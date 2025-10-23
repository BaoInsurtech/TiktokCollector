import time
import requests
import os
from db.client import prisma

from model.common_model import APIResponse
from model.auth_model import AuthTokenResponse, ShopDataResponse
from utils.sign import generate_sign

APP_KEY = os.getenv("APP_KEY", "")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "")

async def shop_authorize_handler(access_token: str):
    base_url = 'https://open-api.tiktokglobalshop.com'
    uri_path = '/authorization/202309/shops'
    timestamp = int(time.time())
    qs = {
        'app_key': APP_KEY,
        'timestamp': str(timestamp),
    }
    headers = {
        'x-tts-access-token': access_token,
        'content-type': 'application/json'
    }
    request_option = {
        'qs': qs,
        'uri': uri_path,
        'headers': headers
    }
    sign = generate_sign(request_option, APP_SECRET_KEY)
    qs['sign'] = sign
    return requests.get(f"{base_url}{uri_path}", params=qs, headers=headers)

async def auth_callback_handler(app_key: str = None, code: str = None) -> APIResponse:
    print(f"Auth callback received with app_key: {app_key}, code: {code}")
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
        data: AuthTokenResponse = response.json().get("data")
        print(f"Received auth tokens: {response.json()}")
        if (data is None):
            return APIResponse(code=500, message=response.json().get("message", "Failed to get auth tokens"))
        await prisma.tiktokshoptokens.create(data=data)
        response = await shop_authorize_handler(data.access_token)
        response.raise_for_status()
        data: ShopDataResponse = response.json().get("data")
        if (data is None):
            return APIResponse(code=500, message=response.json().get("message", "Failed to get shop data"))
        print(f"Authorized shop data: {data}")
        await prisma.tiktokshopdata.create(data=data)
    except Exception as e:
        print(f"Error in auth_callback_handler: {e}")
        return APIResponse(code=500, message="Internal server error")
    return APIResponse(code=200, message="Authorization successful")

async def refresh_token_handler():
    refresh_token = None
    try:
        tmp = await prisma.tiktokshoptokens.find_unique(
            where={"customer_id": 1}
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
            "grant_type": "refresh_token"
        }
        response = requests.get("https://auth.tiktok-shops.com/api/v2/token/refresh", params=params)
        response.raise_for_status()
        
        print(f"Refreshed auth tokens: {response.json()}")
        data = AuthTokenResponse(**(response.json().get("data")))
        if (data is None):
            return APIResponse(code=500, message=response.json().get("message", "Failed to refresh tokens"))
        await prisma.tiktokshoptokens.update(
            where={"customer_id": 1},
            data=data.model_dump()
        )
        return APIResponse(code=200, message="Authorization successful")
    except Exception as e:
        print(f"Error in auth_callback_handler: {e}")
        return APIResponse(code=500, message="Internal server error")
