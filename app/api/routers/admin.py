from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.user_repository import UserRepository
from app.services.admin_service import AdminService
from app.schemas.user_dto import UserRegisterDTO, UserResponseDTO



#Main route
router = APIRouter(prefix="/admin", tags=["admin"])

#Dependency injection
def get_admin_service(db: Session = Depends(get_db)) -> AdminService:
    user_repository = UserRepository(db)
    return AdminService(user_repository)


#JWT dependency

@router.post("/register", response_model=UserResponseDTO, status_code=201)
def register(
    data: UserRegisterDTO,
    auth_service: AdminService = Depends(get_admin_service),
):
    user = auth_service.register_user(data)
    return UserResponseDTO.model_validate(user)


