from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_type import DocumentType


def run(db: Session) -> None:

    data = [
        {
            "code": "CI",
            "name": "Identity Card",
        },
        {
            "code": "PASSPORT",
            "name": "Passport",
        },
        {
            "code": "OTHER",
            "name": "Other",
        },
    ]

    for item in data:

        exists = db.scalar(
            select(DocumentType).where(
                DocumentType.code == item["code"]
            )
        )

        if exists:
            continue

        db.add(DocumentType(**item))

    db.commit()