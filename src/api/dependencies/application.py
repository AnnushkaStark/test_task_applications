from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.dependencies.auth import verify_user
from api.dependencies.database import get_async_db
from crud.application import application_crud
from models import Application, User


async def user_application(
    application_uid: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(verify_user),
) -> Optional[Application]:
    found_application = await application_crud.get_by_uid(
        db=db, uid=application_uid
    )
    if not found_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        )
    if found_application.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission!",
        )
    return found_application
