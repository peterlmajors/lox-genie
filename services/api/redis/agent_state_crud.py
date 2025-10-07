"""
CRUD operations for AgentState in Redis - API service version
"""
import json
import logging
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import ValidationError
import redis.asyncio as redis

from services.api.redis.agent_state import AgentStateRedis
from services.api.redis.config import get_redis_settings

logger = logging.getLogger(__name__)

class AgentStateCRUD:
    """CRUD operations for AgentState in Redis"""
    
    def __init__(self):
        self.settings = get_redis_settings()
    
    def _get_key(self, thread_id: str) -> str:
        """Get Redis key for thread_id"""
        return f"{self.settings.redis_key_prefix}:{thread_id}"
    
    async def get(self, redis_client: redis.Redis, thread_id: str) -> Optional[AgentStateRedis]:
        """Get agent state by thread_id"""
        try:
            key = self._get_key(thread_id)
            data = await redis_client.get(key)
            
            if not data:
                return None
            
            # Parse JSON data
            state_dict = json.loads(data)
            
            # Convert datetime strings back to datetime objects
            if 'created_at' in state_dict and isinstance(state_dict['created_at'], str):
                state_dict['created_at'] = datetime.fromisoformat(state_dict['created_at'].replace('Z', '+00:00'))
            
            if 'last_updated' in state_dict and isinstance(state_dict['last_updated'], str):
                state_dict['last_updated'] = datetime.fromisoformat(state_dict['last_updated'].replace('Z', '+00:00'))
            
            # Convert message timestamps
            if 'messages' in state_dict:
                for message in state_dict['messages']:
                    if 'timestamp' in message and isinstance(message['timestamp'], str):
                        message['timestamp'] = datetime.fromisoformat(message['timestamp'].replace('Z', '+00:00'))
            
            return AgentStateRedis.from_dict(state_dict)
            
        except (json.JSONDecodeError, ValidationError, KeyError) as e:
            logger.error(f"Failed to parse agent state for thread {thread_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to get agent state for thread {thread_id}: {e}")
            return None
    
    async def set(self, redis_client: redis.Redis, agent_state: AgentStateRedis) -> bool:
        """Set agent state with thread_id as key"""
        try:
            key = self._get_key(agent_state.thread_id)
            
            # Update timestamp
            agent_state.update_timestamp()
            
            # Convert to JSON-serializable dict
            state_dict = agent_state.to_dict()
            
            # Serialize to JSON
            data = json.dumps(state_dict, default=str)
            
            # Set with TTL if specified
            if agent_state.ttl_seconds:
                await redis_client.setex(key, agent_state.ttl_seconds, data)
            else:
                await redis_client.setex(key, self.settings.redis_ttl_seconds, data)
            
            logger.info(f"Stored agent state for thread {agent_state.thread_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set agent state for thread {agent_state.thread_id}: {e}")
            return False
    
    async def delete(self, redis_client: redis.Redis, thread_id: str) -> bool:
        """Delete agent state by thread_id"""
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
    
    async def exists(self, redis_client: redis.Redis, thread_id: str) -> bool:
        """Check if agent state exists for thread_id"""
        try:
            key = self._get_key(thread_id)
            return await redis_client.exists(key) > 0
        except Exception as e:
            logger.error(f"Failed to check existence for thread {thread_id}: {e}")
            return False
    
    async def get_ttl(self, redis_client: redis.Redis, thread_id: str) -> int:
        """Get TTL for agent state"""
        try:
            key = self._get_key(thread_id)
            return await redis_client.ttl(key)
        except Exception as e:
            logger.error(f"Failed to get TTL for thread {thread_id}: {e}")
            return -1
    
    async def extend_ttl(self, redis_client: redis.Redis, thread_id: str, ttl_seconds: int) -> bool:
        """Extend TTL for agent state"""
        try:
            key = self._get_key(thread_id)
            result = await redis_client.expire(key, ttl_seconds)
            
            if result:
                logger.info(f"Extended TTL for thread {thread_id} to {ttl_seconds} seconds")
                return True
            else:
                logger.warning(f"Failed to extend TTL for thread {thread_id}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to extend TTL for thread {thread_id}: {e}")
            return False
    
    async def list_all(self, redis_client: redis.Redis, pattern: str = "*") -> List[str]:
        """List all thread IDs matching pattern"""
        try:
            search_pattern = f"{self.settings.redis_key_prefix}:{pattern}"
            keys = await redis_client.keys(search_pattern)
            
            # Extract thread IDs from keys
            thread_ids = []
            prefix_len = len(f"{self.settings.redis_key_prefix}:")
            
            for key in keys:
                if key.startswith(f"{self.settings.redis_key_prefix}:"):
                    thread_id = key[prefix_len:]
                    thread_ids.append(thread_id)
            
            return thread_ids
            
        except Exception as e:
            logger.error(f"Failed to list thread IDs: {e}")
            return []
    
    async def count(self, redis_client: redis.Redis) -> int:
        """Count total number of agent states"""
        try:
            pattern = f"{self.settings.redis_key_prefix}:*"
            keys = await redis_client.keys(pattern)
            return len(keys)
        except Exception as e:
            logger.error(f"Failed to count agent states: {e}")
            return 0
    
    async def get_recent(self, redis_client: redis.Redis, limit: int = 10) -> List[AgentStateRedis]:
        """Get recent agent states ordered by last_updated"""
        try:
            # Get all keys
            pattern = f"{self.settings.redis_key_prefix}:*"
            keys = await redis_client.keys(pattern)
            
            if not keys:
                return []
            
            # Get all agent states
            agent_states = []
            for key in keys:
                thread_id = key[len(f"{self.settings.redis_key_prefix}:"):]
                agent_state = await self.get(redis_client, thread_id)
                if agent_state:
                    agent_states.append(agent_state)
            
            # Sort by last_updated (most recent first)
            agent_states.sort(key=lambda x: x.last_updated, reverse=True)
            
            return agent_states[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get recent agent states: {e}")
            return []
    
    async def cleanup_expired(self, redis_client: redis.Redis, max_age_days: int = 30) -> int:
        """Clean up expired agent states"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=max_age_days)
            deleted_count = 0
            
            # Get all keys
            pattern = f"{self.settings.redis_key_prefix}:*"
            keys = await redis_client.keys(pattern)
            
            for key in keys:
                try:
                    thread_id = key[len(f"{self.settings.redis_key_prefix}:"):]
                    agent_state = await self.get(redis_client, thread_id)
                    
                    if agent_state and agent_state.last_updated < cutoff_date:
                        await self.delete(redis_client, thread_id)
                        deleted_count += 1
                        
                except Exception as e:
                    logger.warning(f"Failed to process key {key} during cleanup: {e}")
                    continue
            
            logger.info(f"Cleaned up {deleted_count} expired agent states")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired agent states: {e}")
            return 0