from fastapi import APIRouter
from controllers.auth_controller import *

router = APIRouter()

def register_auth_routes(app):
    @router.get("/callback", tags=["auth"])
    async def callback(app_key: str = None, code: str = None):
        return await auth_callback_handler(app_key, code)

    app.include_router(router, prefix="/auth")