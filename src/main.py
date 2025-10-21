from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import uvicorn
from dotenv import load_dotenv

from routes import auth_route
from db.client import connect_db, disconnect_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()

load_dotenv()
app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    auth_route.register_auth_routes(app)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)