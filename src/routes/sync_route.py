from fastapi import APIRouter, HTTPException, Query
import logging

from db.client import prisma
from services.sync_service import sync_for_customer

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sync", tags=["sync"])

logger = logging.getLogger(__name__)
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(_h)
logger.setLevel(logging.INFO)
logger.propagate = False


@router.post("/trigger")
async def trigger_sync(
    customer_id: str | None = Query(None, description="optional customer_id to sync only that one")
):
    """
    Kích hoạt sync: lấy token từ Postgres (Prisma), gọi API TikTok, lưu vào MongoDB.
    """
    logger.info(f"🚀 Sync triggered for customer_id={customer_id}")
    
    try:
        # ✅ Prisma đã connected trong lifespan, không cần connect/disconnect
        summary = await sync_for_customer(prisma=prisma, customer_id=customer_id)
        
        logger.info(f"✅ Sync completed: {summary}")
        
        return {"status": "ok", "summary": summary}
        
    except Exception as e:
        logger.error(f"❌ Sync failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/responses")
async def get_responses(
    limit: int = 100,
    api_name: str | None = None,
    customer_id: int | None = None,
):
    """Lấy responses từ MongoDB, có thể lọc theo api_name và customer_id"""
    logger.info(
        f"📋 Fetching {limit} responses"
        + (f", api_name={api_name}" if api_name else "")
        + (f", customer_id={customer_id}" if customer_id is not None else "")
    )

    try:
        from ..db.mongo_client import get_db

        mongo_db = get_db()  # Motor database
        collection = mongo_db["tiktok_api_responses"]

        query: dict = {}
        if api_name:
            query["api_name"] = api_name
        if customer_id is not None:
            query["customer_id"] = customer_id

        cursor = collection.find(query).sort("fetched_at", -1).limit(limit)
        docs = await cursor.to_list(length=limit)  # ✅ Motor needs await

        for doc in docs:
            doc["_id"] = str(doc["_id"])

        logger.info(f"✅ Found {len(docs)} responses")
        return {"count": len(docs), "items": docs}

    except Exception as e:
        logger.error(f"❌ Failed to fetch responses: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))