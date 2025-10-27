from fastapi import APIRouter
from controllers.auth_controller import *

router = APIRouter()

def register_auth_routes(app):
    @router.get("/callback", tags=["auth"])
    async def callback(app_key: str = None, code: str = None):
        return await auth_callback_handler(app_key, code)
    @router.get("/shop-data", tags=["auth"])
    async def shop_data():
        return await shop_data_handler()
    @router.get("/refresh-token", tags=["auth"])
    async def refresh_token():
        return await refresh_token_handler()
    app.include_router(router, prefix="/auth")