import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
load_dotenv()

MONGO_DB = os.getenv("MONGO_DB", "tiktok_collector")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

_mongo_client: AsyncIOMotorClient | None = None
_db = None 

def get_db():
    global _mongo_client, _db
    if _mongo_client is None:
        _mongo_client = AsyncIOMotorClient(MONGO_URL)
        _db = _mongo_client[MONGO_DB]
    return _db

async def close_db():
    global _mongo_client
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        _db = None

async def insert_document(collection_name: str, document: dict) -> str:
    db = get_db()
    result = await db[collection_name].insert_one(document)
    return str(result.inserted_id)

async def find_documents(collection_name: str, filter: dict = None, limit: int = 10) -> list[dict]:
    db = get_db()
    cursor = db[collection_name].find(filter or {}).limit(limit)
    return [doc async for doc in cursor]