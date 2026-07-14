import uuid

from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.db.entity import BaseEntity


class File(BaseEntity):
    __tablename__ = "files"

    __table_args__ = (
        Index("ix_files_entity", "entity_table", "entity_id"),
        {"schema": settings.core_schema},
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    original_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    extension: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    entity_table: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    entity_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False,
    )

    file_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    uploaded_by_user = relationship(
        "User",
        back_populates="uploaded_files",
        foreign_keys=[uploaded_by],
    )

    def __repr__(self) -> str:
        return (
            f"<File(original_name='{self.original_name}', "
            f"entity='{self.entity_table}')>"
        )