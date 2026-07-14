from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.schemas.user_role import UserRoleCreate


class UserRoleError(Exception):
    pass


def get_user_roles(
    db: Session,
    user_id,
):

    statement = (
        select(UserRole, Role)
        .join(
            Role,
            UserRole.role_id == Role.id,
        )
        .where(
            UserRole.user_id == user_id,
        )
        .order_by(Role.name)
    )

    return db.execute(statement).all()


def assign_role(
    db: Session,
    data: UserRoleCreate,
):

    user = db.get(
        User,
        data.user_id,
    )

    if user is None:
        raise UserRoleError(
            "User not found."
        )

    role = db.get(
        Role,
        data.role_id,
    )

    if role is None:
        raise UserRoleError(
            "Role not found."
        )

    exists = db.scalar(
        select(UserRole).where(
            UserRole.user_id == data.user_id,
            UserRole.role_id == data.role_id,
        )
    )

    if exists:
        raise UserRoleError(
            "Role already assigned."
        )

    relation = UserRole(
        user_id=data.user_id,
        role_id=data.role_id,
    )

    db.add(relation)
    db.commit()

    return relation


def remove_role(
    db: Session,
    user_id,
    role_id,
):

    relation = db.scalar(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id,
        )
    )

    if relation is None:
        raise UserRoleError(
            "Assignment not found."
        )

    db.delete(relation)
    db.commit()