import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.db.entity import BaseEntity


class NotificationUser(BaseEntity):
    __tablename__ = "notification_users"

    __table_args__ = (
        Index(
            "ix_notification_user",
            "notification_id",
            "user_id",
            unique=True,
        ),
        Index(
            "ix_notification_status",
            "status",
        ),
        {
            "schema": settings.core_schema,
        },
    )

    notification_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.notifications.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    reply: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    reply_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        default="PENDING",
        nullable=False,
    )

    notification = relationship(
        "Notification",
        back_populates="recipients",
    )

    user = relationship(
        "User",
        back_populates="notifications",
    )