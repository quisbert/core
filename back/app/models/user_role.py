import uuid

from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.db.base import BaseModel
from app.db.mixins import UUIDMixin


class UserRole( BaseModel,UUIDMixin,):
    __tablename__ = "user_roles"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "role_id",
            name="uq_user_roles",
        ),
        Index(
            "ix_user_roles_user",
            "user_id",
        ),
        Index(
            "ix_user_roles_role",
            "role_id",
        ),
        {"schema": settings.core_schema},
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.roles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="roles",
    )

    role = relationship(
        "Role",
        back_populates="users",
    )