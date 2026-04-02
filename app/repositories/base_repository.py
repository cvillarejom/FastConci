from typing import TypeVar, Generic, Type, Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.base import BaseEntity

T = TypeVar("T", bound=BaseEntity)

#Base repository methods should be overrided if specifity calls for it
#Otherwise use the base repo or use it internally to interact with db
class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    #GET Methods
    def get_by_id(self, entity_id: int, *, include_inactive: bool = False) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == entity_id)

        #Include entities flagged with active = false
        if not include_inactive:
            stmt = stmt.where(self.model.active.is_(True))

        return self.db.execute(stmt).scalar_one_or_none()

    def list(self,*,include_inactive: bool = False, limit: int = 50, offset: int = 0,) -> List[T]:

        stmt = select(self.model)

        if not include_inactive:
            stmt = stmt.where(self.model.active.is_(True))

        stmt = stmt.limit(limit).offset(offset)

        return list(self.db.execute(stmt).scalars().all())
    

    #CREATE METHODS
    def create(self, entity: T) -> T:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    #DELETE METHODS
    def soft_delete(self, entity_id: int, *, updated_by: int | None = None) -> bool:

        entity = self.get(entity_id, include_inactive=True)

        if not entity:
            return False

        entity.active = False
        entity.updated_by = updated_by

        self.db.commit()
        return True
    
    #Query methods
    def check_if_active(self, entity_id: int) -> bool:
        stmt = select(self.model.active).where(self.model.id == entity_id)
        result = self.db.execute(stmt).scalar_one_or_none()

        if result is None:
            return False  
        
        return bool(result)
    
    def exists(self, entity_id: int) -> bool:
        stmt = select(self.model.id).where(self.model.id == entity_id)
        return self.db.execute(stmt).scalar_one_or_none() is not None