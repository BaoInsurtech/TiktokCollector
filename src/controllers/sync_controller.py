from db.client import prisma
from db.mongo_client import insert_document, find_documents, get_db
from model.common_model import APIResponse

import api.order_api as orders
import api.product_api as products
import api.authorized_api as authorized
import api.seller_api as seller
import api.analytics_api as analytics
import api.finance_api as finance

import time

async def sync_trigger_handler() -> APIResponse:
    # Lấy dữ liệu token và shop cipher từ Prisma (mysql)
    if not prisma.is_connected():
        await prisma.connect()

    try:
        tmp = await prisma.tokens.find_unique(
            where={"customer_id": 1}
        )
        access_token = tmp.access_token

        shop = await prisma.shop_data.find_first(
            where={"customer_id": 1}
        )
        shop_cipher = shop.cipher

        print("Tokens from Prisma:", access_token)
        print("Shop Cipher from Prisma:", shop_cipher)

        pageSize = 100
        

        # Gọi API lấy danh sách đơn hàng
        # res = await orders.get_order_list(access_token, shop_cipher, pageSize=pageSize)
        # doc = {
        #     "customer_id": 1,
        #     "api_name": "orders_list",
        #     "date_fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        #     "code": res.get("code", 500),
        #     "message": res.get("message", ""),
        #     "data": res.get("data", {}),
        # }
        # await insert_document("tiktok_api_responses", doc)

        # I lấy danh sách quyền của người bán
        # res = await seller.get_seller_permisions(access_token, shop_cipher, pageSize=pageSize)
        # print("Seller permissions response:", res)
        # doc = {
        #     "customer_id": 1,
        #     "api_name": "orders_list",
        #     "date_fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        #     "code": res.get("code", 500),
        #     "message": res.get("message", ""),
        #     "data": res.get("data", {}),
        # }
        # await insert_document("tiktok_api_responses", doc)

        # Gọi API lấy danh sách danh mục được ủy quyền
        # res = await authorized.get_authorized_categories_set(access_token, shop_cipher, pageSize=pageSize)
        # doc = {
        #     "customer_id": 1,
        #     "api_name": "orders_list",
        #     "date_fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        #     "code": res.get("code", 500),
        #     "message": res.get("message", ""),
        #     "data": res.get("data", {}),
        # }
        # await insert_document("tiktok_api_responses", doc)

        # Gọi API lấy danh sách danh mục sản phẩm
        # res = await products.get_product(access_token, "1732607077493474317", shop_cipher)
        # print("Product categories response:", res)
        # await insert_document("tiktok_api_responses", res)

        # Gọi API lấy danh sách danh mục sản phẩm
        # res = await products.get_categories(access_token, shop_cipher, pageSize=pageSize)
        # await insert_document("tiktok_api_responses", res)
        # print(f"✅Inserted product categories response into MongoDB: {res}")

        # # API gọi tìm kiếm sản phẩm
        # res = await products.search_product(access_token, shop_cipher, pageSize=pageSize)
        # print("Seller permissions response:", res)
        # await insert_document("tiktok_api_responses", res)

        # API gọi lấy chi tiết giá của đơn hàng
        # res = await orders.get_price_detail(access_token,580453115811694573, shop_cipher)
        # print("Get price detail: ", res)
        # doc = {
        #     "customer_id": 1,
        #     "api_name": "orders_list",
        #     "date_fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        #     "code": res.get("code", 500),
        #     "message": res.get("message", ""),
        #     "data": res.get("data", {}),
        # }
        # await insert_document("tiktok_api_responses", doc)
        
        # Gọi API lấy hiệu suất cửa hàng
        res = await analytics.get_shop_performance(access_token, shop_cipher, start_date_ge="2025-08-01", end_date_lt="2025-10-25")
        print("Seller response:", res)
        await insert_document("tiktok_api_responses", res)

        # Gọi api lây giao dịch chưa thanh toán
        res = await finance.get_unsettled_transactions(access_token, shop_cipher)
        print("Seller response:", res)
        await insert_document("tiktok_api_responses", res)

        # Goi api lay bang ke 
        res = await finance.get_statements(access_token, shop_cipher)
        print("Seller response:", res)
        await insert_document("tiktok_api_responses", res)

         # Gọi API lấy hiệu suất sản phẩm cửa hàng
        res = await analytics.get_shop_product_performance_list(access_token, shop_cipher, start_date_ge="2025-08-01", end_date_lt="2025-10-25")
        print("Seller response:", res)
        await insert_document("tiktok_api_responses", res)

        
        code = res.get("code", 500)
        message = res.get("message", "")
        data = res.get("data", {})

        return APIResponse(code=code, message=message, data=data)

    finally:
        await prisma.disconnect()


async def sync_response_handler(limit: int | None = 4,
    api_name: str | None = None,
    customer_id: int | None = None,
):
    
    try:
        mongo_db = get_db()  # Motor database
        collection = mongo_db["tiktok_api_responses"]

        query: dict = {}
        if api_name:
            query["api_name"] = api_name
        if customer_id is not None:
            query["customer_id"] = customer_id

        # Sắp xếp theo _id giảm dần để lấy record mới nhất
        cursor = collection.find(query).sort("_id", -1).limit(limit)
        docs = await cursor.to_list(length=limit)  # ✅ Motor needs await

        for doc in docs:
            doc["_id"] = str(doc["_id"])
      
        return {"count": len(docs), "items": docs}

    except Exception as e:
        return {"count": 0, "items": [], "error": str(e)}