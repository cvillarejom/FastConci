from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class BaseEntity(Base):
    __abstract__ = True
    #Common columns shared through the entities (mostly for logs ajd soft delete, 
    # shouldn't be used in the rest of the program)

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
    )

    date_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    #TODO: Review sys as creator strategy
    updated_by: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
        default=1 #admin/root user id
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="true",
    )