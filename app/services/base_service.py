from __future__ import annotations

from typing import Generic, Optional, TypeVar

from sqlalchemy.orm import Session

from app.domain.base import BaseEntity
from app.repositories.base_repository import BaseRepository

T = TypeVar("T", bound=BaseEntity)

#Common service functions go here
class BaseService(Generic[T]):
    def __init__(self, db: Session, repo: BaseRepository[T]):
        self.db = db
        self.repo = repo

    #Basic transaction
    def commit(self) -> None:
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def rollback(self) -> None:
        self.db.rollback()

    #basic crud 
    def get(self, entity_id: int, *, include_inactive: bool = False) -> Optional[T]:
        return self.repo.get(entity_id, include_inactive=include_inactive)

    def list(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        include_inactive: bool = False,
        newest_first: bool = True,
    ) -> list[T]:
        return self.repo.list(
            limit=limit,
            offset=offset,
            include_inactive=include_inactive,
            newest_first=newest_first,
        )

    def soft_delete(self, entity_id: int, *, updated_by: int | None = None) -> bool:
        ok = self.repo.soft_delete(entity_id, updated_by=updated_by)
        if ok:
            self.commit()
        return ok