
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
    async def get_agent_state(self, thread_id: str) -> Optional[AgentStateRedis]:
        """Get agent state by thread_id"""
        try:
            await self.ensure_connected()
            return await self.crud.get(self.redis_client, thread_id)
        except Exception as e:
            logger.error(f"Failed to get agent state for thread {thread_id}: {e}")
            return None

    async def set_agent_state(self, agent_state: AgentStateRedis) -> bool:
        """Set agent state with thread_id as key"""
        try:
            await self.ensure_connected()
            return await self.crud.set(self.redis_client, agent_state)
        except Exception as e:
            logger.error(
                f"Failed to set agent state for thread {agent_state.thread_id}: {e}"
            )
            return False

    async def delete_agent_state(self, thread_id: str) -> bool:
        """Delete agent state by thread_id"""
        try:
            await self.ensure_connected()
            return await self.crud.delete(self.redis_client, thread_id)
        except Exception as e:
            logger.error(f"Failed to delete agent state for thread {thread_id}: {e}")
            return False

    async def exists_agent_state(self, thread_id: str) -> bool:
        """Check if agent state exists for thread_id"""
        try:
            await self.ensure_connected()
            return await self.crud.exists(self.redis_client, thread_id)
        except Exception as e:
            logger.error(f"Failed to check existence for thread {thread_id}: {e}")
            return False

    async def get_agent_state_ttl(self, thread_id: str) -> int:
        """Get TTL for agent state"""
        try:
            await self.ensure_connected()
            return await self.crud.get_ttl(self.redis_client, thread_id)
        except Exception as e:
            logger.error(f"Failed to get TTL for thread {thread_id}: {e}")
            return -1

    async def extend_agent_state_ttl(self, thread_id: str, ttl_seconds: int) -> bool:
        """Extend TTL for agent state"""
        try:
            await self.ensure_connected()
            return await self.crud.extend_ttl(self.redis_client, thread_id, ttl_seconds)
        except Exception as e:
            logger.error(f"Failed to extend TTL for thread {thread_id}: {e}")
            return False

    async def list_thread_ids(self, pattern: str = "*") -> List[str]:
        """List all thread IDs matching pattern"""
        try:
            await self.ensure_connected()
            return await self.crud.list_all(self.redis_client, pattern)
        except Exception as e:
            logger.error(f"Failed to list thread IDs: {e}")
            return []

    async def count_agent_states(self) -> int:
        """Count total number of agent states"""
        try:
            await self.ensure_connected()
            return await self.crud.count(self.redis_client)
        except Exception as e:
            logger.error(f"Failed to count agent states: {e}")
            return 0

    async def get_recent_agent_states(self, limit: int = 10) -> List[AgentStateRedis]:
        """Get recent agent states ordered by last_updated"""
        try:
            await self.ensure_connected()
            return await self.crud.get_recent(self.redis_client, limit)
        except Exception as e:
            logger.error(f"Failed to get recent agent states: {e}")
            return []

    async def cleanup_expired_agent_states(self, max_age_days: int = 30) -> int:
        """Clean up expired agent states"""
        try:
            await self.ensure_connected()
            return await self.crud.cleanup_expired(self.redis_client, max_age_days)
        except Exception as e:
            logger.error(f"Failed to cleanup expired agent states: {e}")
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
