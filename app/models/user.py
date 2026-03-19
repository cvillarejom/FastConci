from app.models.base import BaseEntity

from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from enum import Enum

class RoleUser(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseEntity):
    __tablename__="users"

    

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role:Mapped[RoleUser] = mapped_column(
        SqlEnum(RoleUser),
        nullable=False,
        default=RoleUser.USER
    )
