import time
import requests
import os
from db.client import prisma

from model.common_model import APIResponse
from utils.sign import generate_sign
from db.mongo_client import connect_mongo, disconnect_mongo  # import từ file bạn đã viết
from pymongo.errors import BulkWriteError


APP_KEY = os.getenv("APP_KEY", "")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "")

async def shop_info_handler() -> APIResponse:
    # Lấy access token từ database
    access_token = None
    try:
        tmp = await prisma.tiktokshoptokens.find_unique(
            where={"id": 1}
        )
        access_token = tmp.access_token
    except Exception as e:
        print(f"Error fetching access token: {e}")
        return APIResponse(code=500, message="Internal server error")
    if access_token is None:
        return APIResponse(code=400, message="No access token found")
    # Query parameters
    base_url = 'https://open-api.tiktokglobalshop.com'
    uri_path = '/seller/202309/shops'
    timestamp = int(time.time())
    qs = {
        'app_key': APP_KEY,
        'timestamp': str(timestamp),
    }
    # Headers
    headers = {
        'x-tts-access-token': access_token,
        'content-type': 'application/json'
    }

    # No body for GET
    request_option = {
        'qs': qs,
        'uri': uri_path,
        'headers': headers,
        'body': None
    }

    # Tính chữ ký
    sign = generate_sign(request_option, APP_SECRET_KEY)

    # Gửi request GET
    full_url = f"{base_url}{uri_path}"
    qs['sign'] = sign
    try:
        response = requests.get(full_url, params=qs, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error in get_shop_info_handler: {e}")
        return APIResponse(code=500, message="Internal server error")
    # Hiển thị kết quả
    print("Request URL:", response.url)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    data = response.json().get("data", {})
    return APIResponse(code=200, message="Success", data=data)
