import uuid
from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.person import Person
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserError(Exception):
    pass


def get_users(
    db: Session,
    search: str | None = None,
) -> list[User]:
    statement = select(User).where(
        User.deleted_at.is_(None)
    )

    if search:
        search_value = f"%{search.strip()}%"

        statement = statement.where(
            or_(
                User.username.ilike(search_value),
                User.email.ilike(search_value),
            )
        )

    statement = statement.order_by(User.username)

    return list(db.scalars(statement).all())


def get_user(
    db: Session,
    user_id: uuid.UUID,
) -> User | None:
    statement = select(User).where(
        User.id == user_id,
        User.deleted_at.is_(None),
    )

    return db.scalar(statement)


def create_user(
    db: Session,
    data: UserCreate,
) -> User:
    person = db.scalar(
        select(Person).where(
            Person.id == data.person_id,
            Person.deleted_at.is_(None),
        )
    )

    if person is None:
        raise UserError("Person not found.")

    person_has_user = db.scalar(
        select(User).where(
            User.person_id == data.person_id,
            User.deleted_at.is_(None),
        )
    )

    if person_has_user:
        raise UserError("Person already has a user account.")

    username_exists = db.scalar(
        select(User).where(
            User.username == data.username,
            User.deleted_at.is_(None),
        )
    )

    if username_exists:
        raise UserError("Username already exists.")

    email_exists = db.scalar(
        select(User).where(
            User.email == data.email,
            User.deleted_at.is_(None),
        )
    )

    if email_exists:
        raise UserError("Email already exists.")

    user = User(
        person_id=data.person_id,
        username=data.username.strip(),
        email=data.email,
        hashed_password=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(
    db: Session,
    user: User,
    data: UserUpdate,
    updated_by: uuid.UUID,
) -> User:
    values = data.model_dump(exclude_unset=True)

    if "username" in values:
        username_exists = db.scalar(
            select(User).where(
                User.id != user.id,
                User.username == values["username"],
                User.deleted_at.is_(None),
            )
        )

        if username_exists:
            raise UserError("Username already exists.")

        values["username"] = values["username"].strip()

    if "email" in values:
        email_exists = db.scalar(
            select(User).where(
                User.id != user.id,
                User.email == values["email"],
                User.deleted_at.is_(None),
            )
        )

        if email_exists:
            raise UserError("Email already exists.")

    for key, value in values.items():
        setattr(user, key, value)

    user.updated_by = updated_by

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User,
    deleted_by: uuid.UUID,
) -> None:
    user.is_active = False
    user.deleted_at = datetime.now(timezone.utc)
    user.deleted_by = deleted_by

    db.commit()


def unlock_user(
    db: Session,
    user: User,
    updated_by: uuid.UUID,
) -> User:
    user.is_locked = False
    user.failed_login_attempts = 0
    user.updated_by = updated_by

    db.commit()
    db.refresh(user)

    return user


def reset_user_password(
    db: Session,
    user: User,
    password: str,
    updated_by: uuid.UUID,
) -> User:
    user.hashed_password = hash_password(password)
    user.failed_login_attempts = 0
    user.is_locked = False
    user.updated_by = updated_by

    db.commit()
    db.refresh(user)

    return user