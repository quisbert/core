import uuid
from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
)


class RoleError(Exception):
    pass


def get_roles(
    db: Session,
    search: str | None = None,
) -> list[Role]:

    statement = select(Role).where(
        Role.deleted_at.is_(None)
    )

    if search:

        search = f"%{search.strip()}%"

        statement = statement.where(
            or_(
                Role.code.ilike(search),
                Role.name.ilike(search),
                Role.description.ilike(search),
            )
        )

    statement = statement.order_by(
        Role.name,
    )

    return list(
        db.scalars(statement).all()
    )


def get_role(
    db: Session,
    role_id: uuid.UUID,
) -> Role | None:

    statement = select(Role).where(
        Role.id == role_id,
        Role.deleted_at.is_(None),
    )

    return db.scalar(statement)


def create_role(
    db: Session,
    data: RoleCreate,
) -> Role:

    exists = db.scalar(
        select(Role).where(
            or_(
                Role.code == data.code,
                Role.name == data.name,
            ),
            Role.deleted_at.is_(None),
        )
    )

    if exists:
        raise RoleError(
            "Role already exists."
        )

    role = Role(
        **data.model_dump()
    )

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


def update_role(
    db: Session,
    role: Role,
    data: RoleUpdate,
) -> Role:

    values = data.model_dump(
        exclude_unset=True,
    )

    if (
        "code" in values
        or "name" in values
    ):

        code = values.get(
            "code",
            role.code,
        )

        name = values.get(
            "name",
            role.name,
        )

        exists = db.scalar(
            select(Role).where(
                Role.id != role.id,
                or_(
                    Role.code == code,
                    Role.name == name,
                ),
                Role.deleted_at.is_(None),
            )
        )

        if exists:
            raise RoleError(
                "Role already exists."
            )

    for key, value in values.items():
        setattr(role, key, value)

    db.commit()
    db.refresh(role)

    return role


def delete_role(
    db: Session,
    role: Role,
    deleted_by: uuid.UUID,
) -> None:

    role.deleted_at = datetime.now(
        timezone.utc
    )

    role.deleted_by = deleted_by
    role.is_active = False

    db.commit()