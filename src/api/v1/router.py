from fastapi import APIRouter

from api.v1.endpoints.application import router as application_router
from api.v1.endpoints.user import router as user_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(
    application_router, prefix="/application", tags=["Application"]
)
