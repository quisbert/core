import uuid
from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission


def find_user_by_login(db: Session, login: str) -> User | None:
    statement = select(User).where(
        or_(
            User.username == login,
            User.email == login,
        )
    )

    return db.scalar(statement)


def find_active_user(db: Session, user_id: uuid.UUID) -> User | None:
    statement = select(User).where(
        User.id == user_id,
        User.is_active.is_(True),
        User.deleted_at.is_(None),
    )

    return db.scalar(statement)


def authenticate_user(
    db: Session,
    login: str,
    password: str,
    ip_address: str | None,
    user_agent: str | None,
) -> User | None:
    user = find_user_by_login(db, login)

    if user is None:
        return None

    if (
        not user.is_active
        or user.deleted_at is not None
        or user.is_locked
    ):
        return None

    if not verify_password(password, user.hashed_password):
        user.failed_login_attempts += 1

        if user.failed_login_attempts >= settings.max_login_attempts:
            user.is_locked = True

        db.commit()
        return None

    user.failed_login_attempts = 0
    user.last_login_at = datetime.now(timezone.utc)
    user.last_login_ip = ip_address
    user.last_login_user_agent = user_agent

    db.commit()
    db.refresh(user)

    return user


def generate_tokens(user: User) -> dict[str, str]:
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }

def get_user_roles_permissions(
    db: Session,
    user_id: uuid.UUID,
) -> tuple[list[str], list[str]]:

    roles = db.scalars(
        select(Role.code)
        .join(
            UserRole,
            UserRole.role_id == Role.id,
        )
        .where(
            UserRole.user_id == user_id,
        )
    ).all()

    permissions = db.scalars(
        select(Permission.code)
        .join(
            RolePermission,
            RolePermission.permission_id == Permission.id,
        )
        .join(
            UserRole,
            UserRole.role_id == RolePermission.role_id,
        )
        .where(
            UserRole.user_id == user_id,
        )
        .distinct()
    ).all()

    return list(roles), list(permissions)