from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from .routes import auth_route
from src.routes.sync_route import router as sync_route
from src.db.client import connect_db, disconnect_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()

load_dotenv()
PORT = os.getenv("PORT", 3000)
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "TikTok MultiConnect demo - use POST /sync/trigger to run"}

auth_route.register_auth_routes(app)
app.include_router(sync_route)

if __name__ == "__main__":
    print(f"Starting server on port {PORT}...")
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)