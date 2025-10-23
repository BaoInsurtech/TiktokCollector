from prisma import Prisma
import logging
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

prisma = Prisma()

# MySQL connection config
MYSQL_CONFIG = {
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": int(os.getenv("DATABASE_PORT", 3306)),
    "user": os.getenv("DATABASE_USERNAME", "root"),
    "password": os.getenv("DATABASE_PASSWORD", ""),
    "database": os.getenv("DATABASE_NAME", "baohuyhq"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}

async def connect_db():
    """Kết nối Prisma Client"""
    if not prisma.is_connected():
        logger.info("🔌 Connecting to MySQL...")
        await prisma.connect()
        logger.info("✅ MySQL connected")
    else:
        logger.debug("⚠️ MySQL already connected")

async def disconnect_db():
    """Ngắt kết nối Prisma Client"""
    if prisma.is_connected():
        logger.info("🔌 Disconnecting MySQL...")
        await prisma.disconnect()
        logger.info("✅ MySQL disconnected")
    else:
        logger.debug("⚠️ MySQL already disconnected")

def get_access_token_by_id(customer_id: int | None = None):
    """
    Lấy access tokens từ database bằng pymysql (sync function)
    
    Args:
        customer_id: Nếu có, chỉ lấy token của customer đó. Nếu None, lấy dòng đầu tiên.
    
    Returns:
        List[Token]: Danh sách tokens (luôn trả về list để consistent)
    """
    logger.info(f"🔍 Fetching tokens for customer_id={customer_id}")
    
    connection = None
    try:
        # ✅ Kết nối MySQL trực tiếp
        connection = pymysql.connect(**MYSQL_CONFIG)
        
        with connection.cursor() as cursor:
            if customer_id:
                # Lấy token của 1 customer cụ thể
                sql = "SELECT * FROM TiktokShopTokens WHERE customer_id = %s LIMIT 1"
                cursor.execute(sql, (customer_id,))
            else:
                # Lấy dòng đầu tiên
                sql = "SELECT * FROM TiktokShopTokens LIMIT 1"
                cursor.execute(sql)
            
            result = cursor.fetchone()
            tokens = [result] if result else []
        
        logger.info(f"✅ Found {len(tokens)} token(s)")
        
        # ✅ Log access_token để kiểm tra
        if tokens:
            logger.info(f"📝 Access token: {tokens[0]['access_token'][:20]}...")
        
        return tokens
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch tokens: {e}", exc_info=True)
        raise
    finally:
        if connection:
            connection.close()

def get_shop_cipher_by_customer_id(customer_id: int):
    """
    Lấy shop_cipher từ database bằng pymysql (sync function)
    
    Args:
        customer_id: ID của customer.
    
    Returns:
        str | None: shop_cipher hoặc None nếu không tìm thấy.
    """
    logger.info(f"🔍 Fetching shop_cipher for customer_id={customer_id}")
    
    connection = None
    try:
        # ✅ Kết nối MySQL trực tiếp
        connection = pymysql.connect(**MYSQL_CONFIG)
        
        with connection.cursor() as cursor:
            sql = "SELECT * FROM TiktokShopData LIMIT 1"
            cursor.execute(sql, (customer_id,))
            result = cursor.fetchone()
            shop_cipher = result['shop_cipher'] if result else None
        
        if shop_cipher:
            logger.info(f"✅ Found shop_cipher for customer_id={customer_id}")
        else:
            logger.warning(f"⚠️ No shop_cipher found for customer_id={customer_id}")
        
        return shop_cipher
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch shop_cipher: {e}", exc_info=True)
        raise
    finally:
        if connection:
            connection.close()