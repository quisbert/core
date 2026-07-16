import uuid

from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.db.entity import BaseEntity


class OrganizationSetting(BaseEntity):
    __tablename__ = "organization_settings"

    __table_args__ = (
        Index(
            "ix_organization_settings_theme_id",
            "theme_id",
        ),
        {
            "schema": settings.core_schema,
        },
    )

    organization_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    organization_abbreviation: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    system_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    system_abbreviation: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    logo_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.files.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    favicon_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.files.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    login_background_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.files.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    timezone: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="America/La_Paz",
    )

    language: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="es",
    )

    login_message: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    theme_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.themes.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    theme = relationship(
        "Theme",
        back_populates="organization_setting",
    )

    logo = relationship(
        "File",
        foreign_keys=[logo_id],
    )

    favicon = relationship(
        "File",
        foreign_keys=[favicon_id],
    )

    login_background = relationship(
        "File",
        foreign_keys=[login_background_id],
    )

    def __repr__(self) -> str:
        return (
            f"<OrganizationSetting("
            f"organization='{self.organization_name}', "
            f"system='{self.system_name}')>"
        )