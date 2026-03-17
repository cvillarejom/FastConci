from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.userDTO import UserLoginDTO, UserRegisterDTO, UserResponseDTO
from app.repositories.userRepository import UserRepository
from app.models.user import User

class UserService:
    def __init__ (self, userRepository: UserRepository):
        self.userRepository = userRepository
    
    def registerUser(self, data: UserRegisterDTO) -> User:

        #Check existing
        existingEmail = self.userRepository.get_by_email(data.email)
        if(existingEmail):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        
        #hash password
        hassedPassword = hash_password(data.password)

        #Create the user
        user = self.userRepository.create(
            email = data.email, 
            username= data.username,
            hashedPassword= hassedPassword
        )
        
        return user

    def loginUser():
        pass

    def softDeleteUser():
        pass