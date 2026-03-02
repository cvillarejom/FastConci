from fastapi import APIRouter
from app.api.routers import utils, datasets

# Router files
api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(datasets.router)

