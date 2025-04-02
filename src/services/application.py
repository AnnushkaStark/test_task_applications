from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from constants.application import ApplicationStatus
from crud.application import application_crud
from models import Application
from schemas.application import (
    ApplicationCreateDB,
    ApplicationUpdate,
    AppllicationCreate,
)
from utilities.validators.application import valid_schema


async def create(
    db: AsyncSession, create_schema: AppllicationCreate, user_id: int
) -> Application:
    create_data = ApplicationCreateDB(
        **create_schema.model_dump(),
        author_id=user_id,
        status=ApplicationStatus.OPEN
    )
    application = await application_crud.create(
        db=db, create_schema=create_data
    )
    return application


async def update(
    db: AsyncSession, update_data: ApplicationUpdate, db_obj: Application
) -> Optional[Application]:
    try:
        await valid_schema(schema=update_data)
    except Exception as e:
        raise Exception(str(e))
    return await application_crud.update(
        db=db, db_obj=db_obj, update_data=update_data
    )
