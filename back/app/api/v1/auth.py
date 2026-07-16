import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import CurrentUser, oauth2_scheme
from app.core.security import TokenError, decode_token
from app.db.database import get_db
from app.schemas.auth import (
    CurrentUserResponse,
    RefreshTokenRequest,
    TokenResponse,
)
from app.schemas.register import (
    RegisterRequest,
    RegisterResponse,
)
from app.services.auth_service import (
    authenticate_user,
    close_session,
    find_active_session_by_access_jti,
    find_active_session_by_refresh_jti,
    find_active_user,
    generate_tokens,
    get_user_roles_permissions,
    refresh_session_tokens,
)
from app.services.register_service import (
    RegisterError,
    register_user,
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
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    ip_address = (
        request.client.host
        if request.client
        else None
    )

    user_agent = request.headers.get(
        "user-agent"
    )

    device_name = request.headers.get(
        "x-device-name"
    )

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
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    tokens = generate_tokens(
        db=db,
        user=user,
        ip_address=ip_address,
        user_agent=user_agent,
        device_name=device_name,
    )

    return TokenResponse(**tokens)


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_token(
    payload: RefreshTokenRequest,
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid, expired or inactive refresh token.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        token_payload = decode_token(
            payload.refresh_token,
            expected_type="refresh",
        )

        user_id = uuid.UUID(
            token_payload["sub"]
        )

        refresh_jti = token_payload["jti"]

    except (
        TokenError,
        ValueError,
        KeyError,
    ):
        raise credentials_exception

    user = find_active_user(
        db=db,
        user_id=user_id,
    )

    if user is None or user.is_locked:
        raise credentials_exception

    user_session = (
        find_active_session_by_refresh_jti(
            db=db,
            user_id=user_id,
            refresh_jti=refresh_jti,
        )
    )

    if user_session is None:
        raise credentials_exception

    tokens = refresh_session_tokens(
        db=db,
        session=user_session,
        user=user,
    )

    return TokenResponse(**tokens)


@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
def get_me(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> CurrentUserResponse:
    roles, permissions = (
        get_user_roles_permissions(
            db=db,
            user_id=current_user.id,
        )
    )

    return CurrentUserResponse(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        roles=roles,
        permissions=permissions,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
def logout(
    current_user: CurrentUser,
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
    db: Annotated[Session, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or inactive session.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        token_payload = decode_token(
            token,
            expected_type="access",
        )

        user_id = uuid.UUID(
            token_payload["sub"]
        )

        access_jti = token_payload["jti"]

    except (
        TokenError,
        ValueError,
        KeyError,
    ):
        raise credentials_exception

    if user_id != current_user.id:
        raise credentials_exception

    user_session = (
        find_active_session_by_access_jti(
            db=db,
            user_id=user_id,
            access_jti=access_jti,
        )
    )

    if user_session is None:
        raise credentials_exception

    close_session(
        db=db,
        session=user_session,
        user_id=current_user.id,
    )

    return {
        "message": "Logout successful.",
    }


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
) -> RegisterResponse:
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