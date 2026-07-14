from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.schemas.role_permission import RolePermissionCreate


class RolePermissionError(Exception):
    pass


def get_role_permissions(
    db: Session,
    role_id,
):

    statement = (
        select(RolePermission, Permission)
        .join(
            Permission,
            RolePermission.permission_id == Permission.id,
        )
        .where(
            RolePermission.role_id == role_id,
        )
        .order_by(Permission.code)
    )

    return db.execute(statement).all()


def assign_permission(
    db: Session,
    data: RolePermissionCreate,
):

    role = db.get(
        Role,
        data.role_id,
    )

    if role is None:
        raise RolePermissionError(
            "Role not found."
        )

    permission = db.get(
        Permission,
        data.permission_id,
    )

    if permission is None:
        raise RolePermissionError(
            "Permission not found."
        )

    exists = db.scalar(
        select(RolePermission).where(
            RolePermission.role_id == data.role_id,
            RolePermission.permission_id == data.permission_id,
        )
    )

    if exists:
        raise RolePermissionError(
            "Permission already assigned."
        )

    relation = RolePermission(
        role_id=data.role_id,
        permission_id=data.permission_id,
    )

    db.add(relation)
    db.commit()

    return relation


def remove_permission(
    db: Session,
    role_id,
    permission_id,
):

    relation = db.scalar(
        select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        )
    )

    if relation is None:
        raise RolePermissionError(
            "Assignment not found."
        )

    db.delete(relation)
    db.commit()