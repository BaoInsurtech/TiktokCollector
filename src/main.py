from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from routes import auth_route
from routes import sync_route
from db.client import connect_db, disconnect_db

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()

PORT = int(os.getenv("PORT", 3000))
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "TikTok MultiConnect demo - use POST /sync/trigger to run"}

auth_route.register_auth_routes(app)
sync_route.register_sync_routes(app)

if __name__ == "__main__":
    print(f"Starting server on port {PORT}...")
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)