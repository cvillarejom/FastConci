from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    func,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    name: mapped[str] = mapped_column(
        string(255),
        nullable=False
    )

    match_index_a: mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    match_index_a_name: mapped[str] = mapped_column(
        string(255),
        nullable=False
    )

    match_index_b: mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    match_index_b_name: mapped[str] = mapped_column(
        string(255),
        nullable=False
    )

    amount_tolerance: mapped[int] = mapped_column(
        Decimal,
        
    )







