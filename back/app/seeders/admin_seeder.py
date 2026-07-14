from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.document_type import DocumentType
from app.models.gender import Gender
from app.models.person import Person
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole


def run(db: Session) -> None:

    exists = db.scalar(
        select(User).where(
            User.username == "admin"
        )
    )

    if exists:
        return

    gender = db.scalar(
        select(Gender).where(
            Gender.code == "M"
        )
    )

    document = db.scalar(
        select(DocumentType).where(
            DocumentType.code == "CI"
        )
    )

    role = db.scalar(
        select(Role).where(
            Role.code == "ADMIN"
        )
    )

    person = Person(
        first_name="System",
        last_name="Administrator",
        document_type_id=document.id,
        document_number="0",
        gender_id=gender.id,
        email="admin@core.local",
    )

    db.add(person)
    db.flush()

    user = User(
        person_id=person.id,
        username="admin",
        email="admin@core.local",
        hashed_password=hash_password("Admin123*"),
    )

    db.add(user)
    db.flush()

    db.add(
        UserRole(
            user_id=user.id,
            role_id=role.id,
        )
    )

    db.commit()