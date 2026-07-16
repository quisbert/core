from sqlalchemy import Boolean
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.db.entity import BaseEntity


class Theme(BaseEntity):
    __tablename__ = "themes"

    __table_args__ = (
        Index(
            "ix_themes_type",
            "type",
        ),
        Index(
            "ix_themes_is_default",
            "is_default",
        ),
        {
            "schema": settings.core_schema,
        },
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
    )

    sidebar_background_color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    sidebar_foreground_color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    topbar_background_color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    topbar_foreground_color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    card_header_background_color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    card_header_foreground_color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    table_header_background_color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    table_header_foreground_color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    border_color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    organization_setting = relationship(
        "OrganizationSetting",
        back_populates="theme",
    )

    def __repr__(self) -> str:
        return (
            f"<Theme("
            f"name='{self.name}', "
            f"type='{self.type}')>"
        )