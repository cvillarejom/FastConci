from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user_dto import UserLoginDTO
from app.repositories.user_repository import UserRepository
from app.models.user import User

class AuthService:
    def __init__ (self, userRepository: UserRepository):
        self.userRepository = userRepository
    
    def login_user(self, email: str, password: str) -> str:
        user = self.userRepository.get_by_email(email)

        #Check hash first
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

        #check if user is active
        if not user.active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not active")

        return create_access_token(data={"sub": str(user.id), "email": user.email})
