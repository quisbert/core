import uuid
from datetime import date

from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.db.entity import BaseEntity


class Person(BaseEntity):
    __tablename__ = "people"

    __table_args__ = (
        Index(
            "ix_people_document",
            "document_type_id",
            "document_number",
            unique=True,
        ),
        {"schema": settings.core_schema},
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    middle_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    second_last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    birth_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    document_type_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.document_types.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    document_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    gender_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            f"{settings.core_schema}.genders.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        index=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    mobile: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    gender = relationship(
        "Gender",
        back_populates="people",
    )

    document_type = relationship(
        "DocumentType",
        back_populates="people",
    )

    user = relationship(
        "User",
        back_populates="person",
        uselist=False,
    )

    @property
    def full_name(self) -> str:
        return " ".join(
            filter(
                None,
                [
                    self.first_name,
                    self.middle_name,
                    self.last_name,
                    self.second_last_name,
                ],
            )
        )

    def __repr__(self) -> str:
        return (
            f"<Person(document='{self.document_number}', "
            f"name='{self.full_name}')>"
        )