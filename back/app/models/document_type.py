from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.entity import BaseEntity


class DocumentType(BaseEntity):
    __tablename__ = "document_types"

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    people = relationship(
        "Person",
        back_populates="document_type",
    )

    def __repr__(self) -> str:
        return f"<DocumentType(code='{self.code}', name='{self.name}')>"