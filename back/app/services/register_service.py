from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password

from app.models.person import Person
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole

from app.schemas.register import RegisterRequest


class RegisterError(Exception):
    pass


def register_user(
    db: Session,
    data: RegisterRequest,
) -> User:

    username_exists = db.scalar(
        select(User).where(
            User.username == data.user.username
        )
    )

    if username_exists:
        raise RegisterError("Username already exists.")

    email_exists = db.scalar(
        select(User).where(
            User.email == data.user.email
        )
    )

    if email_exists:
        raise RegisterError("Email already exists.")

    document_exists = db.scalar(
        select(Person).where(
            Person.document_type_id == data.person.document_type_id,
            Person.document_number == data.person.document_number,
        )
    )

    if document_exists:
        raise RegisterError("Document already exists.")

    role = db.scalar(
        select(Role).where(
            Role.code == "USER"
        )
    )

    if role is None:
        raise RegisterError("Default role not found.")

    person = Person(
        first_name=data.person.first_name,
        middle_name=data.person.middle_name,
        last_name=data.person.last_name,
        second_last_name=data.person.second_last_name,
        birth_date=data.person.birth_date,
        document_type_id=data.person.document_type_id,
        document_number=data.person.document_number,
        gender_id=data.person.gender_id,
        email=data.person.email,
        phone=data.person.phone,
        mobile=data.person.mobile,
        address=data.person.address,
    )

    db.add(person)
    db.flush()

    user = User(
        person_id=person.id,
        username=data.user.username,
        email=data.user.email,
        hashed_password=hash_password(data.user.password),
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
    db.refresh(user)

    return user