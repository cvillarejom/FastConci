from __future__ import annotations

from typing import Any, Dict, Optional

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Integer,
    Numeric,
    String
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

#Common fields/audit import from base
from app.domain.base import Base


class Rule(Base):
    __tablename__ = "rules"

    #Columns
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True, 
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    match_index_a: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )
    match_index_a_name: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )

    match_index_b: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )
    match_index_b_name: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )

    amount_tolerance: Mapped[float] = mapped_column(
        Numeric(18, 4), 
        nullable=False
    )
    
    date_tolerance_days: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )
    
    aggregate_days: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )

    config_json: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, 
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id", 
            onupdate="NO ACTION", 
            ondelete="NO ACTION"
        ),
        nullable=False,
    )

    updated_by: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id", 
            onupdate="NO ACTION", 
            ondelete="NO ACTION"
        ),
        nullable=True,
    )


    # Foreing keys
    owner = relationship(
        "User",
        foreign_keys=[user_id],
        lazy="joined",
    )

    updated_by_user = relationship(
        "User",
        foreign_keys=[updated_by],
        lazy="joined",
    )

