"""
Redis server for Lox Genie - Agent State Management
Handles storage and retrieval of AgentState objects using thread_id as key
"""

import asyncio
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

import redis.asyncio as redis
from pydantic import ValidationError

from .core.config import get_settings
from .models.agent_state import AgentStateRedis
from .crud.agent_state import AgentStateCRUD

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedisServer:
    """Redis server for managing agent state data"""
    
    def __init__(self):
        self.settings = get_settings()
        self.redis_client: Optional[redis.Redis] = None
        self.crud = AgentStateCRUD()
        
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
                health_check_interval=30
            )
            
            # Test connection
            await self.redis_client.ping()
            logger.info(f"Connected to Redis at {self.settings.redis_host}:{self.settings.redis_port}")
            
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
                "keyspace": info.get("db0", {}).get("keys", 0)
            }
            
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}
    
    async def get_agent_state(self, thread_id: str) -> Optional[AgentStateRedis]:
        """Get agent state by thread_id"""
        try:
            return await self.crud.get(self.redis_client, thread_id)
        except Exception as e:
            logger.error(f"Failed to get agent state for thread {thread_id}: {e}")
            return None
    
    async def set_agent_state(self, agent_state: AgentStateRedis) -> bool:
        """Set agent state with thread_id as key"""
        try:
            return await self.crud.set(self.redis_client, agent_state)
        except Exception as e:
            logger.error(f"Failed to set agent state for thread {agent_state.thread_id}: {e}")
            return False
    
    async def delete_agent_state(self, thread_id: str) -> bool:
        """Delete agent state by thread_id"""
        try:
            return await self.crud.delete(self.redis_client, thread_id)
        except Exception as e:
            logger.error(f"Failed to delete agent state for thread {thread_id}: {e}")
            return False
    
    async def list_thread_ids(self, pattern: str = "*") -> list[str]:
        """List all thread IDs matching pattern"""
        try:
            if not self.redis_client:
                return []
            
            keys = await self.redis_client.keys(pattern)
            return [key for key in keys if key.startswith("thread:")]
            
        except Exception as e:
            logger.error(f"Failed to list thread IDs: {e}")
            return []
    
    async def cleanup_expired_states(self, ttl_days: int = 30) -> int:
        """Clean up expired agent states"""
        try:
            if not self.redis_client:
                return 0
            
            cutoff_date = datetime.utcnow() - timedelta(days=ttl_days)
            deleted_count = 0
            
            # Get all thread keys
            thread_keys = await self.redis_client.keys("thread:*")
            
            for key in thread_keys:
                try:
                    # Get the agent state
                    agent_state = await self.crud.get(self.redis_client, key.replace("thread:", ""))
                    
                    if agent_state and agent_state.last_updated < cutoff_date:
                        await self.redis_client.delete(key)
                        deleted_count += 1
                        
                except Exception as e:
                    logger.warning(f"Failed to process key {key} during cleanup: {e}")
                    continue
            
            logger.info(f"Cleaned up {deleted_count} expired agent states")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired states: {e}")
            return 0


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
