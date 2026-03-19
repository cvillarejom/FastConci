from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user_dto import UserRegisterDTO, UserResponseDTO
from app.repositories.user_repository import UserRepository
from app.models.user import User

class AdminService:
    def __init__ (self, userRepository: UserRepository):
        self.userRepository = userRepository
    
    def register_user(self, data: UserRegisterDTO) -> User:

        #Check existing
        existingEmail = self.userRepository.get_by_email(data.email)
        if(existingEmail):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        print("PASSWORD:", data.password)
        print("TYPE:", type(data.password))
        print("LEN:", len(data.password))
        
        #hash password
        hassedPassword = hash_password(data.password)

        #Create the user
        user = self.userRepository.create(
            email = data.email, 
            name= data.name,
            password_hash= hassedPassword
        )
        
        return user

    #TODO: add a soft-delete function
    def softDeleteUser():
        pass