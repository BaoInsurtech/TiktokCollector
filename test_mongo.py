"""Test MongoDB connection directly"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")

print(f"Connecting to: {MONGO_URL}")
print(f"Database: {MONGO_DB}")

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    
    # Test connection
    client.admin.command('ping')
    print("✅ MongoDB connected successfully!")
    
    # Get database
    db = client[MONGO_DB]
    print(f"✅ Database '{MONGO_DB}' accessible")
    
    # List collections
    collections = db.list_collection_names()
    print(f"Collections: {collections}")
    
    client.close()
    
except Exception as e:
    print(f"❌ MongoDB connection error: {e}")
