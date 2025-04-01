from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from fastapi import APIRouter, Depends, HTTPException, Security, status

from api.dependencies.auth import refresh_security
from api.dependencies.database import get_async_db
from crud.user import user_crud
from models import User
from schemas.token import TokenAccessRefresh
from schemas.user import UserCreate, UserLogin
from services import user as user_service
from utilities.security.security import (
    ACCESS_TOKEN_COOKIE_KEY,
    REFRESH_TOKEN_COOKIE_KEY,
    access_security,
    create_tokens,
)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def user_create(
    create_data: UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        user_service.create(db=db, create_data=create_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

    

@router.post("/login/")