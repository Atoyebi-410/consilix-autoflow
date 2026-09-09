from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.automations import router as automation_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    automation_router,
    prefix="/api/v1",
)

@app.get("/")
def root():
    return {
        "message": "Consilix AutoFlow is running",
        "version": settings.app_version,
    }
