from fastapi import APIRouter
from app.api.routers import utils, datasets, rules

# Main api routes
api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(datasets.router)
api_router.include_router(rules.router)

