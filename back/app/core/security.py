import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings


password_hash = PasswordHash.recommended()


class TokenError(Exception):
    pass


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_token(
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    extra_claims: dict[str, Any] | None = None,
) -> dict[str, Any]:

    now = datetime.now(timezone.utc)

    jti = str(uuid.uuid4())

    expires_at = now + expires_delta

    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "jti": jti,
        "iat": now,
        "exp": expires_at,
    }

    if extra_claims:
        payload.update(extra_claims)

    token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    return {
        "token": token,
        "jti": jti,
        "expires_at": expires_at,
    }


def create_access_token(
    user_id: uuid.UUID,
) -> dict[str, Any]:

    return create_token(
        subject=str(user_id),
        token_type="access",
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes,
        ),
    )


def create_refresh_token(
    user_id: uuid.UUID,
) -> dict[str, Any]:

    return create_token(
        subject=str(user_id),
        token_type="refresh",
        expires_delta=timedelta(
            days=settings.refresh_token_expire_days,
        ),
    )


def decode_token(
    token: str,
    expected_type: str,
) -> dict[str, Any]:

    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={
                "require": [
                    "sub",
                    "type",
                    "jti",
                    "iat",
                    "exp",
                ],
            },
        )

    except InvalidTokenError as exc:
        raise TokenError(
            "Invalid or expired token."
        ) from exc

    if payload.get("type") != expected_type:
        raise TokenError(
            "Invalid token type."
        )

    return payload