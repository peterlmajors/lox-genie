
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from services.api.core.config import settings
from services.api.redis.client import get_redis_client, RedisClient
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
    redis_status: dict

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
async def health_check(redis_client: RedisClient = Depends(get_redis_client)) -> JSONResponse:
    """Comprehensive health check endpoint for service monitoring."""
    now = time.time()
    
    # Get Redis health status
    redis_health = await redis_client.health_check()
    
    response = HealthResponse(
        status="ok",
        service=settings.NAME,
        version=settings.VERSION,
        environment=settings.ENV,
        hostname=socket.gethostname(),
        uptime=now - _start_time,
        timestamp=now,
        redis_status=redis_health,
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=response.model_dump())