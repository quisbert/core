import uuid

from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.db.entity import BaseEntity


class AuditLog(BaseEntity):
    __tablename__ = "audit_logs"

    __table_args__ = (
        Index("ix_audit_logs_table", "table_name"),
        Index("ix_audit_logs_record", "entity_id"),
        Index("ix_audit_logs_action", "action"),
        {"schema": settings.core_schema},
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    table_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    entity_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    endpoint: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    http_method: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        INET,
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    old_values: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    new_values: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="audit_logs",
    )

    def __repr__(self) -> str:
        return (
            f"<AuditLog(table='{self.table_name}', "
            f"action='{self.action}')>"
        )