"""
Redis configuration for API service
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
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

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


def get_redis_settings() -> RedisSettings:
    """Get Redis settings"""
    import os

    print(f"DEBUG: Environment variables:")
    print(f"  REDIS_HOST: {os.getenv('REDIS_HOST', 'NOT_SET')}")
    print(f"  REDIS_PORT: {os.getenv('REDIS_PORT', 'NOT_SET')}")
    print(f"  REDIS_DB: {os.getenv('REDIS_DB', 'NOT_SET')}")

    settings = RedisSettings()
    print(f"DEBUG: Loaded settings:")
    print(f"  redis_host: {settings.redis_host}")
    print(f"  redis_port: {settings.redis_port}")
    print(f"  redis_db: {settings.redis_db}")

    return settings
