import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.db.entity import BaseEntity


class UserSession(BaseEntity):
    __tablename__ = "user_sessions"

    __table_args__ = (
        Index(
            "ix_user_sessions_access_jti",
            "access_jti",
            unique=True,
        ),
        Index(
            "ix_user_sessions_refresh_jti",
            "refresh_jti",
            unique=True,
        ),
        {
            "schema": settings.core_schema,
        },
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    access_jti: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
    )

    refresh_jti: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    device_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="sessions",
    )