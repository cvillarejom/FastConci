from fastapi import APIRouter
from app.api.routers import utils, datasets, admin, auth

# Router files
api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(datasets.router)
api_router.include_router(admin.router)
api_router.include_router(auth.router)


