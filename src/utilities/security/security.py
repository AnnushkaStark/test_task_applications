from datetime import timedelta
from typing import TypedDict

from api.dependencies.auth import access_security, refresh_security
from config.configs import jwt_settings
from schemas.token import TokenAccessRefresh


class TokenSubject(TypedDict):
    username: str
    password: str


async def create_tokens(subject: TokenSubject) -> TokenAccessRefresh:
    access_token = access_security.create_access_token(
        subject=subject,
        expires_delta=timedelta(minutes=jwt_settings.JWT_ACCESS_TOKEN_EXPIRES),
    )
    refresh_token = refresh_security.create_refresh_token(
        subject=subject,
        expires_delta=timedelta(
            minutes=jwt_settings.JWT_REFRESH_TOKEN_EXPIRES
        ),
    )
    return TokenAccessRefresh(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


ACCESS_TOKEN_COOKIE_KEY = jwt_settings.ACCESS_TOKEN_COOKIE_KEY
REFRESH_TOKEN_COOKIE_KEY = jwt_settings.REFRESH_TOKEN_COOKIE_KEY
