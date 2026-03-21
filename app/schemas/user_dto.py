from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.user import RoleUser

class UserRegisterDTO(BaseModel):
    email: EmailStr
    name: str = Field(min_length=10, max_length=60)
    password: str = Field(min_length=10, max_length=30)


class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, max_length=30)

class UserResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    active: bool
    role: RoleUser
    date_created: datetime


class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    