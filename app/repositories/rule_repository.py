from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.rules import Rule
from app.repositories.base_repository import BaseRepository


class RuleRepository(BaseRepository[Rule]):
    def __init__(self, session: Session):
        super().__init__(session, Rule)