from fastapi import APIRouter
from app.core.config import get_settings

#Main route
router = APIRouter(prefix="/utils", tags=["utils"])

settings = get_settings()

#endpoints
@router.get("/health")
def health():
    return {"status":"ok"}

@router.get("/version")
def version():
    return {"name": settings.app_name, 
            "current_version": 0.1}