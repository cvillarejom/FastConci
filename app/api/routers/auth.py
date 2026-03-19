from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_dto import TokenDTO
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repository = UserRepository(db)
    return AuthService(user_repository)

@router.post("/login", response_model=TokenDTO)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    token = auth_service.login_user(
        email=form_data.username,
        password=form_data.password,
    )
    return TokenDTO(access_token=token)