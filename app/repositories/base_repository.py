from __future__ import annotations

from typing import Generic, Iterable, Optional, TypeVar

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.domain.base import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def get(self, entity_id: int, *, include_inactive: bool = False) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == entity_id)
        if not include_inactive:
            stmt = stmt.where(self.model.active.is_(True))
        return self.session.execute(stmt).scalar_one_or_none()

    def list(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        include_inactive: bool = False,
        newest_first: bool = True,
    ) -> list[T]:
        stmt = select(self.model)
        if not include_inactive:
            stmt = stmt.where(self.model.active.is_(True))

        order_col = self.model.date_created.desc() if newest_first else self.model.date_created.asc()
        stmt = stmt.order_by(order_col).limit(limit).offset(offset)

        return list(self.session.execute(stmt).scalars().all())

    def create(self, entity: T) -> T:
        self.session.add(entity)
        self.session.flush()   
        self.session.refresh(entity)
        return entity

    #Basic update by ID
    def update_by_id(self, entity_id: int, *, values: dict, updated_by: int | None = None) -> Optional[T]:
        if updated_by is not None:
            values = {**values, "updated_by": updated_by}

        stmt = (
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        res = self.session.execute(stmt)
        if res.rowcount == 0:
            return None
        return self.get(entity_id, include_inactive=True)

    #Always use soft on endpoints
    def soft_delete(self, entity_id: int, *, updated_by: int | None = None) -> bool:
        values = {"active": False}
        if updated_by is not None:
            values["updated_by"] = updated_by
        stmt = (
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        res = self.session.execute(stmt)
        return res.rowcount > 0

    #Not to be used on endpoints (or non-admin endpoints)
    def hard_delete(self, entity_id: int) -> bool:
        obj = self.get(entity_id, include_inactive=True)
        if obj is None:
            return False
        self.session.delete(obj)
        return True