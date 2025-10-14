"""
Simple CRUD operations for AgentState in Redis
"""
import json
import logging
from typing import Dict, Any, Optional, List
import redis.asyncio as redis

from services.api.redis.agent_state import AgentStateRedis
from services.api.redis.config import get_redis_settings

logger = logging.getLogger(__name__)

class AgentStateCRUD:
    """Simple CRUD operations for AgentState in Redis"""
    
    def __init__(self):
        self.settings = get_redis_settings()
    
    def _get_key(self, thread_id: str) -> str:
        """Get Redis key for thread_id"""
        return AgentStateRedis.get_redis_key(thread_id)
    
    async def set_agent_state(self, redis_client: redis.Redis, thread_id: str, state_dict: Dict[str, Any]) -> bool:
        """Store agent state as dictionary in Redis"""
        try:
            key = self._get_key(thread_id)
            
            # Add timestamp
            redis_time = await redis_client.time()
            state_dict['redis_updated_at'] = json.dumps({"timestamp": redis_time[0]})
            
            # Serialize to JSON
            data = json.dumps(state_dict, default=str)
            
            # Store with TTL
            await redis_client.setex(key, self.settings.redis_ttl_seconds, data)
            
            logger.info(f"Stored agent state for thread {thread_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store agent state for thread {thread_id}: {e}")
            return False
    
    async def get_agent_state(self, redis_client: redis.Redis, thread_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve agent state as dictionary from Redis"""
        try:
            key = self._get_key(thread_id)
            data = await redis_client.get(key)
            
            if not data:
                return None
            
            # Parse JSON back to dict
            state_dict = json.loads(data)
            logger.info(f"Retrieved agent state for thread {thread_id}")
            logger.info(f"Parsed state_dict type: {type(state_dict)}")
            if 'message_counts' in state_dict:
                logger.info(f"message_counts type after JSON parse: {type(state_dict['message_counts'])}")
            return state_dict
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON for thread {thread_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to get agent state for thread {thread_id}: {e}")
            return None
    
    async def delete_agent_state(self, redis_client: redis.Redis, thread_id: str) -> bool:
        """Delete specific agent state by thread_id"""
        try:
            key = self._get_key(thread_id)
            result = await redis_client.delete(key)
            
            if result:
                logger.info(f"Deleted agent state for thread {thread_id}")
                return True
            else:
                logger.warning(f"Agent state for thread {thread_id} not found")
                return False
                
        except Exception as e:
            logger.error(f"Failed to delete agent state for thread {thread_id}: {e}")
            return False
    
    async def delete_all_threads(self, redis_client: redis.Redis) -> int:
        """Delete all agent states (all threads)"""
        try:
            # Find all keys with thread: prefix
            pattern = "thread:*"
            keys = await redis_client.keys(pattern)
            
            if not keys:
                logger.info("No agent states found to delete")
                return 0
            
            # Delete all keys
            deleted_count = await redis_client.delete(*keys)
            
            logger.info(f"Deleted {deleted_count} agent states (all threads)")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to delete all threads: {e}")
            return 0
    
    async def list_thread_ids(self, redis_client: redis.Redis) -> List[str]:
        """List all thread IDs"""
        try:
            pattern = "thread:*"
            keys = await redis_client.keys(pattern)
            
            # Extract thread IDs from keys
            thread_ids = []
            for key in keys:
                thread_id = key.decode('utf-8').replace("thread:", "")
                thread_ids.append(thread_id)
            
            logger.info(f"Found {len(thread_ids)} threads")
            return thread_ids
            
        except Exception as e:
            logger.error(f"Failed to list thread IDs: {e}")
            return []
    
    async def thread_exists(self, redis_client: redis.Redis, thread_id: str) -> bool:
        """Check if thread exists"""
        try:
            key = self._get_key(thread_id)
            return await redis_client.exists(key) > 0
        except Exception as e:
            logger.error(f"Failed to check if thread {thread_id} exists: {e}")
            return False
    
    async def get_thread_count(self, redis_client: redis.Redis) -> int:
        """Get total number of threads"""
        try:
            pattern = "thread:*"
            keys = await redis_client.keys(pattern)
            return len(keys)
        except Exception as e:
            logger.error(f"Failed to count threads: {e}")
            return 0