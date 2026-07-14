import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.db.entity import BaseEntity


class User(BaseEntity):
    __tablename__ = "users"

    person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.people.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_login_ip: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    last_login_user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    failed_login_attempts: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )

    is_locked: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    person = relationship(
        "Person",
        back_populates="user",
    )

    notifications = relationship(
        "NotificationUser",
        back_populates="user",
    )

    roles = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    uploaded_files = relationship(
        "File",
        back_populates="uploaded_by_user",
        foreign_keys="File.uploaded_by",
    )

    audit_logs = relationship(
        "AuditLog",
        back_populates="user",
    )

    def __repr__(self) -> str:
        return f"<User(username='{self.username}')>"