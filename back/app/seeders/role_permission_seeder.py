from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission


def run(db: Session):

    admin = db.scalar(
        select(Role).where(Role.code == "ADMIN")
    )

    user = db.scalar(
        select(Role).where(Role.code == "USER")
    )

    permissions = db.scalars(
        select(Permission)
    ).all()

    # ADMIN -> todos los permisos
    for permission in permissions:

        exists = db.scalar(
            select(RolePermission).where(
                RolePermission.role_id == admin.id,
                RolePermission.permission_id == permission.id,
            )
        )

        if not exists:
            db.add(
                RolePermission(
                    role_id=admin.id,
                    permission_id=permission.id,
                )
            )

    # USER -> permisos básicos
    user_permissions = [
        "profile.read",
        "profile.update",
        "profile.change_password",
        "notifications.read",
        "notifications.create",
        "notifications.update",
        "notifications.delete",
        "notifications.reply",
    ]

    for code in user_permissions:

        permission = db.scalar(
            select(Permission).where(
                Permission.code == code
            )
        )

        exists = db.scalar(
            select(RolePermission).where(
                RolePermission.role_id == user.id,
                RolePermission.permission_id == permission.id,
            )
        )

        if permission and not exists:
            db.add(
                RolePermission(
                    role_id=user.id,
                    permission_id=permission.id,
                )
            )

    db.commit()