"""
Configuration settings for Redis service
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Redis service configuration settings"""
    
    # Redis connection settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None
    redis_db: int = 0
    
    # Redis key settings
    redis_key_prefix: str = "thread"
    redis_ttl_seconds: int = 86400 * 30  # 30 days default TTL
    
    # Service settings
    service_name: str = "lox-genie-redis"
    log_level: str = "INFO"
    
    # Cleanup settings
    cleanup_interval_hours: int = 24
    max_ttl_days: int = 30
    
    class Config:
        env_file = ".env"
        env_prefix = "REDIS_"


def get_settings() -> Settings:
    """Get Redis service settings"""
    return Settings()
