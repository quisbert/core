from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role


def run(db: Session) -> None:

    data = [
        {
            "code": "ADMIN",
            "name": "Administrator",
            "description": "System Administrator",
        },
        {
            "code": "USER",
            "name": "User",
            "description": "Standard User",
        },
    ]

    for item in data:

        exists = db.scalar(
            select(Role).where(
                Role.code == item["code"]
            )
        )

        if exists:
            continue

        db.add(Role(**item))

    db.commit()