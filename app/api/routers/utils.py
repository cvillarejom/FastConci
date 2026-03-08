from fastapi import APIRouter, Depends, HTTPException
from app.core.config import get_settings
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.api.dependencies import get_db

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
    
@router.get("/db")
def health_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "up"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=503,
            detail={"status": "error", "database": "down", "reason": str(e)},
        )