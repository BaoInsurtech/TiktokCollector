from fastapi import APIRouter

router = APIRouter()

def register_auth_routes(app):
    app.include_router(router, prefix="/auth")
    @router.get("/login", tags=["auth"])
    async def login():
        return {"message": "Login endpoint"}