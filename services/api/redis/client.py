
import asyncio
import logging
from typing import Optional, Dict, Any, List
import redis.asyncio as redis

from services.api.redis.config import get_redis_settings
from services.api.redis.agent_state import AgentStateRedis
from services.api.redis.agent_state_crud import AgentStateCRUD

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client wrapper for API service"""

    def __init__(self):
        self.settings = get_redis_settings()
        self.redis_client: Optional[redis.Redis] = None
        self.crud = AgentStateCRUD()
        self._connection_lock = asyncio.Lock()

    async def connect(self) -> None:
        """Connect to Redis server"""
        async with self._connection_lock:
            if self.redis_client and await self._is_connected():
                return

            try:
                logger.info(
                    f"Connecting to Redis at {self.settings.redis_host}:{self.settings.redis_port}"
                )

                self.redis_client = redis.Redis(
                    host=self.settings.redis_host,
                    port=self.settings.redis_port,
                    password=self.settings.redis_password,
                    db=self.settings.redis_db,
                    decode_responses=True,
                    socket_connect_timeout=self.settings.redis_socket_connect_timeout,
                    socket_timeout=self.settings.redis_socket_timeout,
                    health_check_interval=self.settings.redis_health_check_interval,
                    max_connections=self.settings.redis_max_connections,
                )

                # Test connection
                await self.redis_client.ping()
                logger.info(
                    f"Connected to Redis at {self.settings.redis_host}:{self.settings.redis_port}"
                )

            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                self.redis_client = None
                raise

    async def disconnect(self) -> None:
        """Disconnect from Redis server"""
        async with self._connection_lock:
            if self.redis_client:
                await self.redis_client.aclose()
                self.redis_client = None
                logger.info("Disconnected from Redis")

    async def _is_connected(self) -> bool:
        """Check if Redis client is connected"""
        try:
            if self.redis_client:
                await self.redis_client.ping()
                return True
        except Exception:
            pass
        return False

    async def ensure_connected(self) -> None:
        """Ensure Redis connection is established"""
        if not self.redis_client or not await self._is_connected():
            await self.connect()

    async def health_check(self) -> Dict[str, Any]:
        """Check Redis server health"""
        try:
            await self.ensure_connected()

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

    # Agent State Operations
    async def get_agent_state(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Get agent state as dictionary by thread_id"""
        try:
            await self.ensure_connected()
            return await self.crud.get_agent_state(self.redis_client, thread_id)
        except Exception as e:
            logger.error(f"Failed to get agent state for thread {thread_id}: {e}")
            return None

    async def set_agent_state(self, thread_id: str, state_dict: Dict[str, Any]) -> bool:
        """Set agent state as dictionary with thread_id as key"""
        try:
            await self.ensure_connected()
            return await self.crud.set_agent_state(self.redis_client, thread_id, state_dict)
        except Exception as e:
            logger.error(f"Failed to set agent state for thread {thread_id}: {e}")
            return False

    async def delete_agent_state(self, thread_id: str) -> bool:
        """Delete agent state by thread_id"""
        try:
            await self.ensure_connected()
            return await self.crud.delete_agent_state(self.redis_client, thread_id)
        except Exception as e:
            logger.error(f"Failed to delete agent state for thread {thread_id}: {e}")
            return False

    async def delete_all_threads(self) -> int:
        """Delete all agent states (all threads)"""
        try:
            await self.ensure_connected()
            return await self.crud.delete_all_threads(self.redis_client)
        except Exception as e:
            logger.error(f"Failed to delete all threads: {e}")
            return 0

    async def list_thread_ids(self) -> List[str]:
        """List all thread IDs"""
        try:
            await self.ensure_connected()
            return await self.crud.list_thread_ids(self.redis_client)
        except Exception as e:
            logger.error(f"Failed to list thread IDs: {e}")
            return []

    async def thread_exists(self, thread_id: str) -> bool:
        """Check if thread exists"""
        try:
            await self.ensure_connected()
            return await self.crud.thread_exists(self.redis_client, thread_id)
        except Exception as e:
            logger.error(f"Failed to check if thread {thread_id} exists: {e}")
            return False

    async def get_thread_count(self) -> int:
        """Get total number of threads"""
        try:
            await self.ensure_connected()
            return await self.crud.get_thread_count(self.redis_client)
        except Exception as e:
            logger.error(f"Failed to count threads: {e}")
            return 0


# Global Redis client instance
redis_client = RedisClient()


async def get_redis_client() -> RedisClient:
    """Get Redis client instance - FastAPI dependency"""
    if not redis_client.redis_client or not await redis_client._is_connected():
        await redis_client.connect()
    return redis_client


async def startup_redis():
    """Startup Redis connection"""
    await redis_client.connect()
    logger.info("Redis client started")


async def shutdown_redis():
    """Shutdown Redis connection"""
    await redis_client.disconnect()
    logger.info("Redis client stopped")
