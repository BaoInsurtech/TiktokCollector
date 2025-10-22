from fastapi import APIRouter
from controllers.shop_controller import *

router = APIRouter()

def register_shop_routes(app):
    @router.get("/info", tags=["shop"])
    async def shop_info():
        return await shop_info_handler()
    
    @router.get("/", tags=["shop"])
    async def shop_root():
        return {"message": "Shop route is working"}

    app.include_router(router, prefix="/shop")