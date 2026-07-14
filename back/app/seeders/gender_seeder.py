from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.gender import Gender


def run(db: Session) -> None:

    data = [
        {
            "code": "M",
            "name": "Male",
            "description": "Male",
        },
        {
            "code": "F",
            "name": "Female",
            "description": "Female",
        },
    ]

    for item in data:

        exists = db.scalar(
            select(Gender).where(
                Gender.code == item["code"]
            )
        )

        if exists:
            continue

        db.add(Gender(**item))

    db.commit()