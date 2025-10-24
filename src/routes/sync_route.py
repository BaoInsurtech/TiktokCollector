from fastapi import APIRouter
from controllers.sync_controller import *

router = APIRouter()

def register_sync_routes(app):
    @router.post("/trigger", tags=["sync"])
    async def trigger_sync():
        return await sync_trigger_handler()
    app.include_router(router, prefix="/sync")

    @router.get("/response", tags=["sync"])
    async def get_sync_response():
        return await sync_response_handler()
    app.include_router(router, prefix="/sync")