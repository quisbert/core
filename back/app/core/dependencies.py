import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import TokenError, decode_token
from app.db.database import get_db
from app.models.user import User
from app.services.auth_service import find_active_user

from sqlalchemy import select

from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.user_role import UserRole

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(
            token,
            expected_type="access",
        )
        current_user_id = uuid.UUID(payload["sub"])

    except (TokenError, ValueError, KeyError):
        raise credentials_exception

    user = find_active_user(
        db,
        current_user_id,
    )

    if user is None or user.is_locked:
        raise credentials_exception

    db.info["current_user_id"] = current_user_id

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

def require_permission(permission_code: str):

    def checker(
        current_user: CurrentUser,
        db: Annotated[Session, Depends(get_db)],
    ):

        permission = db.scalar(
            select(Permission).where(
                Permission.code == permission_code
            )
        )

        if permission is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission not found.",
            )

        exists = db.scalar(
            select(UserRole)
            .join(
                RolePermission,
                UserRole.role_id == RolePermission.role_id,
            )
            .where(
                UserRole.user_id == current_user.id,
                RolePermission.permission_id == permission.id,
            )
        )

        if exists is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied.",
            )

        return True

    return checker