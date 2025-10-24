from src.db.client import prisma, mongo
from src.model.common_model import APIResponse

async def sync_trigger_handler() -> APIResponse:
    # Lấy dữ liệu token và shop cipher từ Prisma (mysql)
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

    except Exception as e:
        print("Error fetching data from Prisma:", str(e))
        return APIResponse(success=False, 
                           message="Failed to fetch data from Prisma",
                           code=500)
    finally:
        await prisma.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(sync_trigger_handler())