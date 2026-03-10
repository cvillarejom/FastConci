from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.services.rule_service import RuleService


router = APIRouter(prefix="/rule-profiles", tags=["Rule Profiles"])


# Schemas
class RuleProfileCreate(BaseModel):
    name: str = Field(..., max_length=255)

    match_index_a: int = Field(..., ge=0)
    match_index_a_name: str = Field(..., max_length=255)

    match_index_b: int = Field(..., ge=0)
    match_index_b_name: str = Field(..., max_length=255)

    amount_tolerance: float = Field(..., ge=0)
    date_tolerance_days: int = Field(..., ge=0)
    aggregate_days: int = Field(..., ge=0)

    config_json: Dict[str, Any] = Field(default_factory=dict)


class RuleProfileUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)

    match_index_a: Optional[int] = Field(default=None, ge=0)
    match_index_a_name: Optional[str] = Field(default=None, max_length=255)

    match_index_b: Optional[int] = Field(default=None, ge=0)
    match_index_b_name: Optional[str] = Field(default=None, max_length=255)

    amount_tolerance: Optional[float] = Field(default=None, ge=0)
    date_tolerance_days: Optional[int] = Field(default=None, ge=0)
    aggregate_days: Optional[int] = Field(default=None, ge=0)

    config_json: Optional[Dict[str, Any]] = None
    active: Optional[bool] = None


class RuleProfileOut(BaseModel):
    id: int
    name: str

    match_index_a: int
    match_index_a_name: str
    match_index_b: int
    match_index_b_name: str

    amount_tolerance: float
    date_tolerance_days: int
    aggregate_days: int

    config_json: Dict[str, Any]
    user_id: int
    active: bool

    class Config:
        from_attributes = True


# Placeholders for auth
def _phase1_user_id() -> int:
    return 1


def _phase1_updated_by() -> int:
    return 1



@router.post(
    "",
    response_model=RuleProfileOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a rule profile",
)
def create_rule_profile(payload: RuleProfileCreate, db: Session = Depends(get_db)) -> RuleProfileOut:
    service = RuleService(db)
    user_id = _phase1_user_id()
    updated_by = _phase1_updated_by()

    try:
        rule = service.create_rule(
            user_id=user_id,
            name=payload.name,
            match_index_a=payload.match_index_a,
            match_index_a_name=payload.match_index_a_name,
            match_index_b=payload.match_index_b,
            match_index_b_name=payload.match_index_b_name,
            amount_tolerance=payload.amount_tolerance,
            date_tolerance_days=payload.date_tolerance_days,
            aggregate_days=payload.aggregate_days,
            config_json=payload.config_json,
            updated_by=updated_by,
            enforce_unique_name=True,
        )
        return rule
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get(
    "/{rule_id}",
    response_model=RuleProfileOut,
    summary="Get a rule profile by id",
)
def get_rule_profile(rule_id: int, db: Session = Depends(get_db)) -> RuleProfileOut:
    service = RuleService(db)

    rule = service.get_rule(rule_id, include_inactive=True)
    if rule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule profile not found")

    return rule


@router.put(
    "/{rule_id}",
    response_model=RuleProfileOut,
    summary="Update a rule profile",
)
def update_rule_profile(rule_id: int, payload: RuleProfileUpdate, db: Session = Depends(get_db)) -> RuleProfileOut:
    service = RuleService(db)
    user_id = _phase1_user_id()
    updated_by = _phase1_updated_by()

    values = payload.model_dump(exclude_unset=True)

    try:
        updated = service.update_rule(
            rule_id,
            user_id=user_id,
            values=values,
            updated_by=updated_by,
            enforce_unique_name=True,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule profile not found")

    return updated


@router.delete(
    "/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft delete a rule profile",
)
def delete_rule_profile(rule_id: int, db: Session = Depends(get_db)) -> None:
    service = RuleService(db)
    user_id = _phase1_user_id()
    updated_by = _phase1_updated_by()

    ok = service.deactivate_rule(rule_id, user_id=user_id, updated_by=updated_by)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule profile not found")
    return None