from __future__ import annotations

from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.domain.rules import Rule
from app.repositories.rule_repository import RuleRepository
from app.services.base_service import BaseService


class RuleService(BaseService[Rule]):
    def __init__(self, db: Session):
        super().__init__(db, RuleRepository(db))

    def create_rule(
        self,
        *,
        user_id: int,
        name: str,
        match_index_a: int,
        match_index_a_name: str,
        match_index_b: int,
        match_index_b_name: str,
        amount_tolerance: Any,
        date_tolerance_days: int,
        aggregate_days: int,
        config_json: Dict[str, Any],
        updated_by: int | None = None,
        enforce_unique_name: bool = True,
    ) -> Rule:
        if enforce_unique_name and self.repo.exists_name_for_user(user_id, name):
            raise ValueError(f"Reconciliation ruleset with '{name}' already exists for this user.")

        rule = Rule(
            name=name,
            match_index_a=match_index_a,
            match_index_a_name=match_index_a_name,
            match_index_b=match_index_b,
            match_index_b_name=match_index_b_name,
            amount_tolerance=amount_tolerance,
            date_tolerance_days=date_tolerance_days,
            aggregate_days=aggregate_days,
            config_json=config_json,
            user_id=user_id,
            updated_by=updated_by,
            active=True,
        )

        self.repo.create(rule)
        self.commit()
        self.db.refresh(rule)
        return rule
    
    def get_rule(self, rule_id: int, *, include_inactive: bool = False) -> Optional[Rule]:
        return self.repo.get(rule_id, include_inactive=include_inactive)