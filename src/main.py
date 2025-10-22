from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from routes import auth_route
from db.client import connect_db, disconnect_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()

load_dotenv()
PORT = os.getenv("PORT", 8000)
app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

auth_route.register_auth_routes(app)
# shop_route.register_shop_routes(app)

if __name__ == "__main__":
    print(f"Starting server on port {PORT}...")
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)