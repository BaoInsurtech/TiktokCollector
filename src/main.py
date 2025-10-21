from fastapi import FastAPI
import uvicorn

from routes import auth_route

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    auth_route.register_auth_routes(app)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)