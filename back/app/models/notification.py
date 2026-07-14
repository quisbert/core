import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.db.entity import BaseEntity


class Notification(BaseEntity):
    __tablename__ = "notifications"

    __table_args__ = (
        Index("ix_notifications_priority", "priority"),
        Index("ix_notifications_status", "status"),
        {
            "schema": settings.core_schema,
        },
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        default="NORMAL",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False,
    )

    entity_table: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    entity_id: Mapped[uuid.UUID | None] = mapped_column(
        nullable=True,
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    requires_response: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    recipients = relationship(
        "NotificationUser",
        back_populates="notification",
        cascade="all, delete-orphan",
    )