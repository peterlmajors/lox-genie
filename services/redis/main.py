"""
Minimal Redis service for Lox Genie - Simple Redis wrapper
This is a lightweight Redis service that can be used for testing or as a simple wrapper.
For full functionality, use the Redis client in services/api/redis/
"""

import asyncio
import logging
from typing import Dict, Any

import redis.asyncio as redis

from .core.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedisServer:
    """Minimal Redis server wrapper"""

    def __init__(self):
        self.settings = get_settings()
        self.redis_client: redis.Redis = None

    async def connect(self) -> None:
        """Connect to Redis server"""
        try:
            self.redis_client = redis.Redis(
                host=self.settings.redis_host,
                port=self.settings.redis_port,
                password=self.settings.redis_password,
                db=self.settings.redis_db,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30,
            )

            # Test connection
            await self.redis_client.ping()
            logger.info(
                f"Connected to Redis at {self.settings.redis_host}:{self.settings.redis_port}"
            )

        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def disconnect(self) -> None:
        """Disconnect from Redis server"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Disconnected from Redis")

    async def health_check(self) -> Dict[str, Any]:
        """Check Redis server health"""
        try:
            if not self.redis_client:
                return {"status": "disconnected", "error": "No Redis connection"}

            # Test basic operations
            await self.redis_client.ping()

            # Get Redis info
            info = await self.redis_client.info()

            return {
                "status": "healthy",
                "redis_version": info.get("redis_version"),
                "connected_clients": info.get("connected_clients"),
                "used_memory_human": info.get("used_memory_human"),
                "keyspace": info.get("db0", {}).get("keys", 0),
            }

        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}


# Global Redis server instance
redis_server = RedisServer()


async def get_redis_server() -> RedisServer:
    """Get Redis server instance"""
    if not redis_server.redis_client:
        await redis_server.connect()
    return redis_server


async def startup_event():
    """Startup event handler"""
    await redis_server.connect()
    logger.info("Redis server started")


async def shutdown_event():
    """Shutdown event handler"""
    await redis_server.disconnect()
    logger.info("Redis server stopped")


if __name__ == "__main__":

    async def main():
        """Main function for testing"""
        server = RedisServer()
        await server.connect()

        # Test health check
        health = await server.health_check()
        print(f"Health check: {health}")

        await server.disconnect()

    asyncio.run(main())
