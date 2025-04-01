import uvicorn
from fastapi import FastAPI

from api.v1.router import api_router as application_service_router

app = FastAPI(
    title="ApplicationsService",
    openapi_url="/application_service/openapi.json",
    docs_url="/application_service/docs",
)


app.include_router(application_service_router, prefix="/application_service")
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        proxy_headers=True,
    )
