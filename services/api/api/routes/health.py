
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from services.api.core.config import settings
import socket
import time

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
    hostname: str
    uptime: float
    timestamp: float

_start_time = time.time()

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check endpoint",
    description="Returns service health, version, environment, hostname, uptime, and timestamp.",
    tags=["Health"],
    response_description="Health status and service metadata.",
    status_code=status.HTTP_200_OK,
)
async def health_check() -> JSONResponse:
    """Comprehensive health check endpoint for service monitoring."""
    now = time.time()
    response = HealthResponse(
        status="ok",
        service=settings.NAME,
        version=settings.VERSION,
        environment=settings.ENV,
        hostname=socket.gethostname(),
        uptime=now - _start_time,
        timestamp=now,
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=response.model_dump())