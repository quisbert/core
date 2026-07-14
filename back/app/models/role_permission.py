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

class RolePermission( BaseModel,UUIDMixin,):
    __tablename__ = "role_permissions"

    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "permission_id",
            name="uq_role_permissions",
        ),
        Index(
            "ix_role_permissions_role",
            "role_id",
        ),
        Index(
            "ix_role_permissions_permission",
            "permission_id",
        ),
        {"schema": settings.core_schema},
    )

    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.roles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    permission_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.permissions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    role = relationship(
        "Role",
        back_populates="permissions",
    )

    permission = relationship(
        "Permission",
        back_populates="roles",
    )