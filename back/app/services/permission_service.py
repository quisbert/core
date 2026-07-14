import uuid
from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.schemas.permission import (
    PermissionCreate,
    PermissionUpdate,
)


class PermissionError(Exception):
    pass


def get_permissions(
    db: Session,
    search: str | None = None,
) -> list[Permission]:

    statement = select(Permission).where(
        Permission.deleted_at.is_(None)
    )

    if search:

        search = f"%{search.strip()}%"

        statement = statement.where(
            or_(
                Permission.code.ilike(search),
                Permission.name.ilike(search),
                Permission.description.ilike(search),
            )
        )

    statement = statement.order_by(
        Permission.code,
    )

    return list(db.scalars(statement).all())


def get_permission(
    db: Session,
    permission_id: uuid.UUID,
) -> Permission | None:

    statement = select(Permission).where(
        Permission.id == permission_id,
        Permission.deleted_at.is_(None),
    )

    return db.scalar(statement)


def create_permission(
    db: Session,
    data: PermissionCreate,
) -> Permission:

    exists = db.scalar(
        select(Permission).where(
            or_(
                Permission.code == data.code,
                Permission.name == data.name,
            ),
            Permission.deleted_at.is_(None),
        )
    )

    if exists:
        raise PermissionError(
            "Permission already exists."
        )

    permission = Permission(
        **data.model_dump()
    )

    db.add(permission)

    db.commit()
    db.refresh(permission)

    return permission


def update_permission(
    db: Session,
    permission: Permission,
    data: PermissionUpdate,
) -> Permission:

    values = data.model_dump(
        exclude_unset=True,
    )

    if (
        "code" in values
        or "name" in values
    ):

        code = values.get(
            "code",
            permission.code,
        )

        name = values.get(
            "name",
            permission.name,
        )

        exists = db.scalar(
            select(Permission).where(
                Permission.id != permission.id,
                or_(
                    Permission.code == code,
                    Permission.name == name,
                ),
                Permission.deleted_at.is_(None),
            )
        )

        if exists:
            raise PermissionError(
                "Permission already exists."
            )

    for key, value in values.items():
        setattr(permission, key, value)

    db.commit()
    db.refresh(permission)

    return permission


def delete_permission(
    db: Session,
    permission: Permission,
    deleted_by: uuid.UUID,
) -> None:

    permission.deleted_at = datetime.now(
        timezone.utc,
    )

    permission.deleted_by = deleted_by
    permission.is_active = False

    db.commit()