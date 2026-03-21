import jwt
from jwt import InvalidTokenError

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import oauth2_scheme, decode_jwt
from app.models.user import User, RoleUser
from app.repositories.user_repository import UserRepository

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    #Define exception
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:

        payload = decode_jwt(token)
        user_id = payload.get("sub")

        #Check User ID exists (thus the user exists)
        if user_id is None:
            raise credentials_exceptions
    
    except InvalidTokenError:
        raise credentials_exceptions

    user_repository = UserRepository(db)
    user = user_repository.get_by_id(user_id)

    if user is None:
        raise credentials_exceptions
    
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not active."
        )
    
    return user

class Rolechecker:
    def __init__(self,allowed_roles:list[RoleUser]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permission."
            )
        return current_user
    

#Dependencies for checking
require_admin = Rolechecker([RoleUser.ADMIN])
require_registered = Rolechecker([RoleUser.ADMIN, RoleUser.USER])