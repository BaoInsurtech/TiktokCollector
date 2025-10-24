from db.client import prisma
from db.mongo_client import insert_document, find_documents, get_db
from model.common_model import APIResponse
import api.order_api as orders
import api.product_api as products
import api.authorized_api as authorized
import api.seller_api as seller
import time

async def sync_trigger_handler() -> APIResponse:
    # Lấy dữ liệu token và shop cipher từ Prisma (mysql)
    if not prisma.is_connected():
        await prisma.connect()

    try:
        tmp = await prisma.tiktokshoptokens.find_unique(
            where={"customer_id": 1}
        )
        access_token = tmp.access_token

        shop = await prisma.tiktokshopdata.find_first(
            where={"customer_id": 1}
        )
        shop_cipher = shop.shop_cipher

        print("Tokens from Prisma:", access_token)
        print("Shop Cipher from Prisma:", shop_cipher)

        pageSize = 50
        

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
        # res = await products.get_product(access_token, "1729592969712207008")
        # print("Product categories response:", res)
        # doc = {
        #     "customer_id": 1,
        #     "api_name": "products_list",
        #     "date_fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        #     "code": res.get("code", 500),
        #     "message": res.get("message", ""),
        #     "data": res.get("data", {}),
        # }
        # await insert_document("tiktok_api_responses", doc)

        # Gọi API lấy danh sách danh mục sản phẩm
        # res = await products.get_categories(access_token, shop_cipher, pageSize=pageSize)
        # print("Product categories response:", res)
        # doc = {
        #     "customer_id": 1,
        #     "api_name": "products_list",
        #     "date_fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        #     "code": res.get("code", 500),
        #     "message": res.get("message", ""),
        #     "data": res.get("data", {}),
        # }
        # await insert_document("tiktok_api_responses", doc)
        # print(f"✅Inserted product categories response into MongoDB: {doc}")

        # API gọi tìm kiếm sản phẩm
        # res = await products.search_product(access_token, shop_cipher, pageSize=pageSize)
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

        # API gọi lấy chi tiết giá của đơn hàng
        res = await orders.get_price_detail(access_token,580453115811694573, shop_cipher)
        print("Get price detail: ", res)
        doc = {
            "customer_id": 1,
            "api_name": "orders_list",
            "date_fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "code": res.get("code", 500),
            "message": res.get("message", ""),
            "data": res.get("data", {}),
        }
        await insert_document("tiktok_api_responses", doc)
        

        
        code = res.get("code", 500)
        message = res.get("message", "")
        data = res.get("data", {})

        return APIResponse(code=code, message=message, data=data)

    except Exception as e:
        return APIResponse(code=code, message=message, data=data)

    finally:
        await prisma.disconnect()


async def sync_response_handler(limit: int | None = 10,
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

        cursor = collection.find(query).sort("date_fetched", -1).limit(limit)
        docs = await cursor.to_list(length=limit)  # ✅ Motor needs await

        for doc in docs:
            doc["_id"] = str(doc["_id"])

      
        return {"count": len(docs), "items": docs}

    except Exception as e:
        return {"count": 0, "items": [], "error": str(e)}