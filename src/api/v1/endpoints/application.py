from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import verify_user
from api.dependencies.database import get_async_db
from api.filters.application import ApplicationsFilter
from crud.application import application_crud
from crud.search import search_application_crud
from models import User
from schemas.application import (
    ApplicationPaginatedResponse,
    ApplicationResponse,
    ApplicationUpdate,
    AppllicationCreate,
)
from services import application as application_service

router = APIRouter()


@router.get("/search/", response_model=ApplicationPaginatedResponse)
async def search_application(
    skip: int = 0,
    limit: int = 0,
    query: str = Query(min_length=2),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(verify_user),
):
    return await search_application_crud.get_search_applications_result(
        db=db, query=query, skip=skip, limit=limit, user_id=current_user.id
    )


@router.get("/", response_model=ApplicationPaginatedResponse)
async def read_applications(
    skip: int = 0,
    limit: int = 0,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(verify_user),
    filter: ApplicationsFilter = FilterDepends(ApplicationsFilter),
):
    return await filter.filter(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )


@router.get("/{application_uid}/", response_model=ApplicationResponse)
async def read_application(
    application_uid: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(verify_user),
):
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


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_application(
    application: AppllicationCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(verify_user),
):
    return await application_service.create(
        db=db, create_schema=application, user_id=current_user.id
    )


@router.patch("/{application_uid}/", status_code=status.HTTP_200_OK)
async def update_application(
    application_uid: UUID,
    update_data: ApplicationUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(verify_user),
):
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
    try:
        return await application_service.update(
            db=db, db_obj=found_application, update_data=update_data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.delete("/{application_uid}/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_application(
    application_uid: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(verify_user),
):
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
    return await application_crud.remove(db=db, obj_id=found_application.id)
