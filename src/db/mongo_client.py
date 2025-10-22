from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from dotenv import load_dotenv

load_dotenv()

_client: MongoClient | None = None
_db = None

def connect_mongo():
    global _client, _db
    if _client:
        return _client, _db
    uri = os.getenv("MONGODB_URL", "mongodb://admin:tiktok_secret_2024@localhost:27017/tiktok_demo?authSource=admin")
    try:
        _client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        _client.admin.command("ping")
        db_name = uri.rsplit("/", 1)[-1].split("?")[0] or "tiktok_demo"
        _db = _client[db_name]
        print(f"✅ MongoDB connected: {uri}")
        return _client, _db
    except PyMongoError as e:
        print(f"❌ MongoDB connection failed: {e}")
        _client = None
        _db = None
        raise

def disconnect_mongo():
    global _client, _db
    if _client:
        _client.close()
        print("🔌 MongoDB disconnected")
    _client = None
    _db = None

def mongo_health() -> dict:
    try:
        if not _client:
            connect_mongo()
        _client.admin.command("ping")
        return {"status": "connected", "ok": True}
    except Exception as e:
        return {"status": "error", "ok": False, "error": str(e)}