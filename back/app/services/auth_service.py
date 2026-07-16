import uuid
from datetime import datetime, timezone

from sqlalchemy import or_, select, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user import User
from app.models.user_role import UserRole
from app.models.user_session import UserSession


def find_user_by_login(
    db: Session,
    login: str,
) -> User | None:
    statement = select(User).where(
        or_(
            User.username == login,
            User.email == login,
        )
    )

    return db.scalar(statement)


def find_active_user(
    db: Session,
    user_id: uuid.UUID,
) -> User | None:
    statement = select(User).where(
        User.id == user_id,
        User.is_active.is_(True),
        User.is_locked.is_(False),
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
    user = find_user_by_login(
        db=db,
        login=login,
    )

    if user is None:
        return None

    if (
        not user.is_active
        or user.deleted_at is not None
        or user.is_locked
    ):
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        user.failed_login_attempts += 1

        if (
            user.failed_login_attempts
            >= settings.max_login_attempts
        ):
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


def generate_tokens(
    db: Session,
    user: User,
    ip_address: str | None,
    user_agent: str | None,
    device_name: str | None = None,
) -> dict[str, str]:
    now = datetime.now(timezone.utc)

    access_data = create_access_token(user.id)
    refresh_data = create_refresh_token(user.id)

    db.execute(
        update(UserSession)
        .where(
            UserSession.user_id == user.id,
            UserSession.is_active.is_(True),
            UserSession.deleted_at.is_(None),
        )
        .values(
            is_active=False,
            updated_at=now,
            updated_by=user.id,
        )
    )

    user_session = UserSession(
        user_id=user.id,
        access_jti=access_data["jti"],
        refresh_jti=refresh_data["jti"],
        ip_address=ip_address,
        user_agent=user_agent,
        device_name=device_name,
        last_activity_at=now,
        expires_at=refresh_data["expires_at"],
        is_active=True,
        created_by=user.id,
    )

    db.add(user_session)
    db.commit()
    db.refresh(user_session)

    return {
        "access_token": access_data["token"],
        "refresh_token": refresh_data["token"],
        "token_type": "bearer",
    }


def find_active_session_by_access_jti(
    db: Session,
    user_id: uuid.UUID,
    access_jti: str,
) -> UserSession | None:
    statement = select(UserSession).where(
        UserSession.user_id == user_id,
        UserSession.access_jti == access_jti,
        UserSession.is_active.is_(True),
        UserSession.deleted_at.is_(None),
        UserSession.expires_at > datetime.now(timezone.utc),
    )

    return db.scalar(statement)


def find_active_session_by_refresh_jti(
    db: Session,
    user_id: uuid.UUID,
    refresh_jti: str,
) -> UserSession | None:
    statement = select(UserSession).where(
        UserSession.user_id == user_id,
        UserSession.refresh_jti == refresh_jti,
        UserSession.is_active.is_(True),
        UserSession.deleted_at.is_(None),
        UserSession.expires_at > datetime.now(timezone.utc),
    )

    return db.scalar(statement)


def refresh_session_tokens(
    db: Session,
    session: UserSession,
    user: User,
) -> dict[str, str]:
    now = datetime.now(timezone.utc)

    access_data = create_access_token(user.id)
    refresh_data = create_refresh_token(user.id)

    session.access_jti = access_data["jti"]
    session.refresh_jti = refresh_data["jti"]
    session.last_activity_at = now
    session.expires_at = refresh_data["expires_at"]
    session.updated_at = now
    session.updated_by = user.id

    db.commit()
    db.refresh(session)

    return {
        "access_token": access_data["token"],
        "refresh_token": refresh_data["token"],
        "token_type": "bearer",
    }


def update_session_activity(
    db: Session,
    session: UserSession,
) -> None:
    session.last_activity_at = datetime.now(timezone.utc)

    db.commit()


def close_session(
    db: Session,
    session: UserSession,
    user_id: uuid.UUID,
) -> None:
    now = datetime.now(timezone.utc)

    session.is_active = False
    session.updated_at = now
    session.updated_by = user_id

    db.commit()


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
            Role.is_active.is_(True),
            Role.deleted_at.is_(None),
        )
        .order_by(Role.code)
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
        .join(
            Role,
            Role.id == UserRole.role_id,
        )
        .where(
            UserRole.user_id == user_id,
            Role.is_active.is_(True),
            Role.deleted_at.is_(None),
            Permission.is_active.is_(True),
            Permission.deleted_at.is_(None),
        )
        .distinct()
        .order_by(Permission.code)
    ).all()

    return list(roles), list(permissions)