import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUser
from app.core.security import TokenError, decode_token
from app.db.database import get_db

from app.schemas.auth import (
    CurrentUserResponse,
    RefreshTokenRequest,
    TokenResponse,
)

from app.services.auth_service import (
    authenticate_user,
    find_active_user,
    generate_tokens,
)

from app.schemas.register import (
    RegisterRequest,
    RegisterResponse,
)

from app.services.register_service import (
    register_user,
    RegisterError,
)

from app.services.auth_service import (
    authenticate_user,
    find_active_user,
    generate_tokens,
    get_user_roles_permissions,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    user = authenticate_user(
        db=db,
        login=form_data.username.strip(),
        password=form_data.password,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or blocked user.",
        )

    return TokenResponse(**generate_tokens(user))


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_token(
    payload: RefreshTokenRequest,
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:

    try:
        token_payload = decode_token(
            payload.refresh_token,
            expected_type="refresh",
        )
        user_id = uuid.UUID(token_payload["sub"])

    except (TokenError, ValueError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
        )

    user = find_active_user(db, user_id)

    if user is None or user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive or blocked.",
        )

    return TokenResponse(**generate_tokens(user))


@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
def get_me(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):

    roles, permissions = get_user_roles_permissions(
        db=db,
        user_id=current_user.id,
    )

    return CurrentUserResponse(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        roles=roles,
        permissions=permissions,
    )

@router.post("/logout")
def logout():

    return {
        "message": "Logout successful."
    }


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):

    try:
        return register_user(
            db=db,
            data=payload,
        )

    except RegisterError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )