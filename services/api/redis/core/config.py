"""
Redis configuration for API service
"""

from pydantic_settings import BaseSettings
from typing import Optional


class RedisSettings(BaseSettings):
    """Redis configuration settings for API service"""
    
    # Redis connection settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None
    redis_db: int = 0
    
    # Redis key settings
    redis_key_prefix: str = "thread"
    redis_ttl_seconds: int = 86400 * 30  # 30 days default TTL
    
    # Connection pool settings
    redis_max_connections: int = 10
    redis_retry_on_timeout: bool = True
    redis_socket_connect_timeout: int = 5
    redis_socket_timeout: int = 5
    redis_health_check_interval: int = 30
    
    class Config:
        env_file = ".env"
        env_prefix = "REDIS_"


def get_redis_settings() -> RedisSettings:
    """Get Redis settings"""
    return RedisSettings()
