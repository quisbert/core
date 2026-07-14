from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.entity import BaseEntity


class Permission(BaseEntity):
    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    roles = relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Permission(code='{self.code}')>"