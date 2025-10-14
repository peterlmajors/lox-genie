from fastapi import APIRouter
from services.api.core.config import settings
from services.api.schemas.health import HealthResponse
# from services.api.redis.client import get_redis_client, RedisClient
import socket
import time

# redis_client: RedisClient = Depends(get_redis_client)

router = APIRouter()

_start_time = time.time()

@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Comprehensive health check endpoint for service monitoring."""
    now = time.time()
    
    # Get Redis health status
    # redis_health = await redis_client.health_check()
    
    response = HealthResponse(
        status="ok",
        service=settings.NAME,
        version=settings.VERSION,
        environment=settings.ENV,
        hostname=socket.gethostname(),
        uptime=now - _start_time,
        timestamp=now
    )
    return response