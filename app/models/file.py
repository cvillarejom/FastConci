from app.models.base import BaseEntity

from sqlalchemy import String, BigInteger, Integer, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, Dict, Any

class File(BaseEntity):
    __tablename__ = "files"

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    storage_path: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    size_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    row_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    columns_json: Mapped[List[Dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    updated_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True
    )

    
    user = relationship("User", foreign_keys=[user_id])
    updated_by_user = relationship("User", foreign_keys=[updated_by])

    
    __table_args__ = (
        Index(
            "idx_files_user_created",
            "user_id",
            "date_created"
        ),
    )