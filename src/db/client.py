from prisma import Prisma
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_DB = os.getenv("MONGO_DB", "tiktok_collector")
MONGO_URL = os.getenv("MONGO_URL")

prisma = Prisma()
_mongo_client = AsyncIOMotorClient(MONGO_URL)
mongo = _mongo_client[MONGO_DB]

async def connect_db():
    await prisma.connect()

async def disconnect_db():
    await prisma.disconnect()
