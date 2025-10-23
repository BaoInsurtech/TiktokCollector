from fastapi import APIRouter
from controllers.auth_controller import *
from utils.sign import generate_sign
router = APIRouter()

APP_KEY = os.getenv("APP_KEY", "")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "")

async def shop_products_handler() -> APIResponse:
    access_token = None
    try:
        tmp = await prisma.tiktokshoptokens.find_unique(
            where={"customer_id": 1}
        )
        access_token = tmp.access_token
    except Exception as e:
        print(f"Error fetching access token: {e}")
        return APIResponse(code=500, message="Internal server error")
    if access_token is None:
        return APIResponse(code=400, message="No access token found")
    # Query parameters
    base_url = 'https://open-api.tiktokglobalshop.com'
    uri_path = '/product/202312/global_products/search'
    timestamp = int(time.time())
    qs = {
        'app_key': APP_KEY,
        'timestamp': str(timestamp),
        'page_size': 10
    }
    # Headers
    headers = {
        'x-tts-access-token': access_token,
        'content-type': 'application/json'
    }

    request_option = {
        'qs': qs,
        'uri': uri_path,
        'headers': headers,
        'body':{
            "status": "PUBLISHED",
            "seller_skus": [
                "Color-Red-001"
            ],
            "create_time_ge": 1694576429,
            "create_time_le": 1694576429,
            "update_time_ge": 1694576429,
            "update_time_le": 1694576429
        }
    }

    # Tính chữ ký
    sign = generate_sign(request_option, APP_SECRET_KEY)
    full_url = f"{base_url}{uri_path}"
    qs['sign'] = sign
    try:
        response = requests.post(full_url, params=qs, headers=headers, json=request_option['body'])
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


async def shop_orders_handler() -> APIResponse:
    access_token = None
    try:
        tmp = await prisma.tiktokshoptokens.find_unique(
            where={"customer_id": 1}
        )
        access_token = tmp.access_token
    except Exception as e:
        print(f"Error fetching access token: {e}")
        return APIResponse(code=500, message="Internal server error")
    if access_token is None:
        return APIResponse(code=400, message="No access token found")
    # Query parameters
    base_url = 'https://open-api.tiktokglobalshop.com'
    uri_path = '/order/202309/orders/search'
    timestamp = int(time.time())
    qs = {
        'app_key': APP_KEY,
        'timestamp': str(timestamp),
        'page_size': 10,
        'shop_cipher': 'ROW_hAKK2gAAAACj9WbsHCX7U3N2xriOLY5y'
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
        'body': {
            "shipping_type": "TIKTOK",
        }
    }

    # Tính chữ ký
    sign = generate_sign(request_option, APP_SECRET_KEY)
    full_url = f"{base_url}{uri_path}"
    qs['sign'] = sign
    try:
        response = requests.post(full_url, params=qs, headers=headers, json=request_option['body'])
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



def register_auth_routes(app):
    @router.get("/callback", tags=["auth"])
    async def callback(app_key: str = None, code: str = None):
        return await auth_callback_handler(app_key, code)
    @router.get("/refresh-token", tags=["auth"])
    async def refresh_token():
        return await refresh_token_handler()

    @router.get("/test", tags=["auth"])
    async def test_endpoint():
        return await shop_orders_handler()
    app.include_router(router, prefix="/auth")