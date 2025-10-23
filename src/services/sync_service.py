import logging
from db.client import prisma
from datetime import datetime
from db.mongo_client import insert_document
from services.tiktok_service import TIKTOK_API_ENDPOINTS, call_tiktok_api

logger = logging.getLogger(__name__)

async def sync_for_customer(prisma, customer_id=None):
    """
    Lấy token từ Prisma -> gọi nhiều API -> lưu vào MongoDB
    Returns summary dict
    """
    logger.info(f"🔄 Bắt đầu sync cho customer_id={customer_id}")
    
    try:
        tokens = await prisma.tiktokshoptokens.find_many(
            where={"customer_id": customer_id}
        )
        shop_cipher = await prisma.tiktokshops.find_unique(
            where={"customer_id": customer_id}
        )

        logger.info(f"✅ Tìm thấy {len(tokens)} token(s)")
    except Exception as e:
        logger.error(f"❌ Lỗi lấy tokens: {e}", exc_info=True)
        raise
    
    if not tokens:
        logger.warning("⚠️ Không có token nào, dừng sync")
        return {"customers": 0, "calls": 0, "saved": 0, "errors": []}
    
    summary = {"customers": 0, "calls": 0, "saved": 0, "errors": []}

    for tok in tokens:
        summary["customers"] += 1
        
        # ✅ Lấy từ dict thay vì object
        access_token = tok['access_token']
        tok_customer_id = tok['customer_id']
        
        logger.info(f"📝 Đang xử lý customer: {tok_customer_id}")
        
        # gọi mỗi endpoint
        for path, name in TIKTOK_API_ENDPOINTS:
            try:
                logger.debug(f"🌐 Gọi API: {name} ({path})")
                
                res = await call_tiktok_api(access_token, path, params=None, body=None, shop_cipher=shop_cipher)
                
                logger.info(f"✅ API {name}: status={res.get('status_code')}, time={res.get('elapsed'):.2f}s")
                
                doc = {
                    "customer_id": tok_customer_id,
                    "api_name": name,
                    "api_path": path,
                    "fetched_at": datetime.utcnow().isoformat(),
                    "response_meta": {
                        "status_code": res.get("status_code"),
                        "url": res.get("url"),
                        "elapsed": res.get("elapsed")
                    },
                    "payload": res.get("data")
                }
                
                inserted_id = await insert_document("tiktok_api_responses", doc)
                logger.debug(f"💾 Đã lưu vào MongoDB: {inserted_id}")
                
                summary["calls"] += 1
                summary["saved"] += 1
                
            except Exception as e:
                logger.error(f"❌ API {name} lỗi cho customer {tok_customer_id}: {e}")
                summary["errors"].append({
                    "customer_id": tok_customer_id, 
                    "api": name, 
                    "error": str(e)
                })
        
        logger.info(f"✅ Hoàn thành customer: {tok_customer_id}")
    
    logger.info(f"🎉 Sync xong: customers={summary['customers']}, calls={summary['calls']}, saved={summary['saved']}, errors={len(summary['errors'])}")
    
    return summary