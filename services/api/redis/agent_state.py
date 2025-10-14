"""
Simplified AgentState Redis operations
"""
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from services.api.agent.schemas import AgentState

logger = logging.getLogger(__name__)

class AgentStateRedis:
    """Simple Redis operations for AgentState"""
    
    @staticmethod
    def from_agent_state(agent_state: AgentState | Dict[str, Any]) -> Dict[str, Any]:
        """Convert AgentState to dictionary for Redis storage"""
        try:
            # Handle both dict and AgentState inputs
            if isinstance(agent_state, dict):
                state_dict = agent_state.copy()
            else:
                # Convert to dict with proper serialization
                state_dict = agent_state.model_dump(mode='json', serialize_as_any=True)
            
            # Add metadata
            state_dict['redis_created_at'] = datetime.utcnow().isoformat()
            state_dict['redis_updated_at'] = datetime.utcnow().isoformat()
            
            return state_dict
        except Exception as e:
            logger.error(f"Failed to convert AgentState to dict: {e}")
            raise
    
    @staticmethod
    def to_agent_state(state_dict: Dict[str, Any]) -> AgentState:
        """Convert dictionary from Redis to AgentState"""
        try:
            # Remove Redis metadata before creating AgentState
            clean_dict = {k: v for k, v in state_dict.items() 
                         if not k.startswith('redis_')}

            return AgentState.model_validate(clean_dict)
        except Exception as e:
            logger.error(f"Failed to convert dict to AgentState: {e}")
            logger.error(f"State dict keys: {list(state_dict.keys())}")
            if 'message_counts' in state_dict:
                logger.error(f"message_counts type: {type(state_dict['message_counts'])}")
                logger.error(f"message_counts value: {state_dict['message_counts']}")
            if 'reduced_context' in state_dict:
                logger.error(f"reduced_context type: {type(state_dict['reduced_context'])}")
                logger.error(f"reduced_context value: {state_dict['reduced_context']}")
            raise
    
    @staticmethod
    def get_redis_key(thread_id: str) -> str:
        """Get Redis key for thread_id"""
        return f"thread:{thread_id}"