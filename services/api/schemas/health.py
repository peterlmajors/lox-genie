from pydantic import BaseModel
from typing import Dict, Optional

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
    hostname: str
    uptime: float
    timestamp: float
    redis_status: Optional[Dict[str, str]] = None