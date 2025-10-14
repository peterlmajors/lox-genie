
import logging
from fastapi import APIRouter, HTTPException, Depends
from langchain_core.messages import HumanMessage

from services.api.agent.graph import graph
from services.api.agent.schemas import AgentState
from services.api.agent.utils import count_messages
from services.api.redis.client import get_redis_client, RedisClient
from services.api.redis.agent_state import AgentStateRedis

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/genie")
async def lox_genie(message: str, thread_id: str | None = None, redis_client: RedisClient = Depends(get_redis_client)) -> dict:
    """
    Chat with the Lox Genie.

    Args:
        message: User message to chat with Lox Genie
        thread_id: Optional thread ID for conversation continuity
    Returns:
        dict: AI response wit   h content and metadata
    """
    try:
        if thread_id:
            state_dict = await redis_client.get_agent_state(thread_id)
            if state_dict:
                logger.info(f"Retrieved state_dict type: {type(state_dict)}")
                logger.info(f"State dict keys: {list(state_dict.keys())}")
                if 'message_counts' in state_dict:
                    logger.info(f"message_counts type: {type(state_dict['message_counts'])}")
                state = AgentStateRedis.to_agent_state(state_dict)
            else:
                state = AgentState(thread_id=thread_id, messages=[HumanMessage(content=message)])
        else:
            # Create new conversation
            state = AgentState(messages=[HumanMessage(content=message)])
            state.message_counts = count_messages(state.messages)

        # Invoke the graph with the state
        state = graph.invoke(state)
        
        # Save state to Redis as dictionary
        state_dict = AgentStateRedis.from_agent_state(state)
        
        # Handle both dict and AgentState
        thread_id = state.get("thread_id") if isinstance(state, dict) else state.thread_id
        last_message = state.get("messages", [])[-1] if isinstance(state, dict) else state.messages[-1]
        last_message_content = last_message.get("content") if isinstance(last_message, dict) else last_message.content
        
        await redis_client.set_agent_state(thread_id, state_dict)

        # Return the response
        return {"response": last_message_content, "thread_id": thread_id}
    except Exception as exc:
        logger.error(f"Error in lox_genie: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(exc)}")