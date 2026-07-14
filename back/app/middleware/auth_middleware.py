from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.security import TokenError, decode_token


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user_id = None
        request.state.token_payload = None

        authorization = request.headers.get("Authorization")

        if authorization:
            scheme, _, token = authorization.partition(" ")

            if scheme.lower() == "bearer" and token:
                try:
                    payload = decode_token(
                        token,
                        expected_type="access",
                    )
                    request.state.user_id = payload["sub"]
                    request.state.token_payload = payload
                except TokenError:
                    pass

        return await call_next(request)