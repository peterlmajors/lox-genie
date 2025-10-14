from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.api.core.config import settings

router = APIRouter()

# Root endpoint
@router.get("/", tags=["Root"], summary="Root endpoint")
async def root() -> JSONResponse:
    """
    Root endpoint providing service metadata and available endpoints.
    """
    return JSONResponse(
        content={
            "message": f"Welcome to {settings.NAME}",
            "version": settings.VERSION,
            "environment": settings.ENV,
            "docs_url": "/docs",
            "openapi_url": "/openapi.json",
            "health_check": "/genie/health"
        }
    )