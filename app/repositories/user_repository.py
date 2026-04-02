from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, *, email: str, name: str, password_hash: str) -> User:
        user = User(
            email=email,
            name=name,
            password_hash=password_hash,
            active=True,
        )

        return super().create(user)
    
    
