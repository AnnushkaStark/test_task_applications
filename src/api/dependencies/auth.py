from datetime import timedelta

from authlib.jose import JoseError
from fastapi import Depends, HTTPException, Security
from fastapi_jwt import (
    JwtAccessBearerCookie,
    JwtAuthorizationCredentials,
    JwtRefreshBearer,
)
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.configs import jwt_settings
from crud.user import user_crud
from databases.database import get_async_session
from models import User
from schemas.token import TokenPayload

access_security = JwtAccessBearerCookie(
    secret_key=jwt_settings.JWT_SECRET_KEY,
    auto_error=True,
    access_expires_delta=timedelta(
        minutes=jwt_settings.JWT_ACCESS_TOKEN_EXPIRES
    ),
)
refresh_security = JwtRefreshBearer(
    secret_key=jwt_settings.JWT_SECRET_KEY,
    refresh_expires_delta=timedelta(
        minutes=jwt_settings.JWT_REFRESH_TOKEN_EXPIRES
    ),
    auto_error=True,
)


async def get_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        token_user = TokenPayload(**credentials.subject)
    except (JoseError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return await user_crud.get_by_email(db=db, email=token_user.email)


async def verify_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_verify:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify  your account",
        )
    return user
