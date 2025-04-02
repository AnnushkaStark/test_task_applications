from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from constants.application import (
    MAX_APPLICATION_NAME_LENGTH,
    MAX_APPLICATION_TEXT_LENGTH,
    MIN_APPLICATION_NAME_LENGTH,
    MIN_APPLICATION_TEXT_LENGTH,
    ApplicationStatus,
)
from schemas.pagination import PaginatedResponseBase


class ApplicationBase(BaseModel):
    name: str = Field(
        min_length=MIN_APPLICATION_NAME_LENGTH,
        max_length=MAX_APPLICATION_NAME_LENGTH,
    )
    description: str = Field(
        min_length=MIN_APPLICATION_TEXT_LENGTH,
        max_length=MAX_APPLICATION_TEXT_LENGTH,
    )


class AppllicationCreate(ApplicationBase):
    ...


class ApplicationCreateDB(AppllicationCreate):
    author_id: int
    status: ApplicationStatus = Field(default=ApplicationStatus.OPEN)


class ApplicationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ApplicationStatus] = None


class ApplicationResponse(ApplicationBase):
    id: int
    uid: UUID
    status: ApplicationStatus
    created_at: datetime


class ApplicationPaginatedResponse(PaginatedResponseBase):
    objects: List[ApplicationResponse]
