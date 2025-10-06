
import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from typing import Optional

from services.api.agent.graph import graph
from services.api.agent.schemas import AgentState
from services.api.agent.utils import count_messages
from services.api.schemas.chat import ChatResponse, ChatMessage
from services.api.redis.client import get_redis_client, RedisClient
from services.api.redis.models.agent_state import AgentStateRedis

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/genie", response_model=ChatResponse)
async def lox_genie(
    message: str, 
    thread_id: Optional[str] = None,
    redis_client: RedisClient = Depends(get_redis_client)
) -> ChatResponse:
    """
    Chat with the Lox Genie.
    Args:
        message: User message to chat with Lox Genie
        thread_id: Optional thread ID for conversation continuity
        redis_client: Redis client for state management
    Returns:
        ChatResponse: AI response with content and metadata
    """
    try:
        # Get or create agent state
        if thread_id:
            redis_state = await redis_client.get_agent_state(thread_id)
            if redis_state:
                state = redis_state.to_agent_state()
            else:
                # Create new state if thread_id doesn't exist
                state = AgentState(thread_id=thread_id, messages=[], stream=False)
        else:
            # Create new conversation
            state = AgentState(messages=[], stream=False)
        
        # Add user message
        state.messages.append(HumanMessage(content=message))
        state.message_counts = count_messages(state.messages)

        # Invoke the graph with the state
        state_dict = graph.invoke(state)
        state = AgentState.model_validate(state_dict)

        # Save state to Redis
        redis_state = AgentStateRedis.from_agent_state(state)
        await redis_client.set_agent_state(redis_state)

        # Return the response
        return ChatResponse(response=state.messages[-1].content)
    except Exception as exc:
        logger.error(f"Error in lox_genie: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(exc)}")


@router.post("/genie/stream")
async def lox_genie_stream(message: str) -> StreamingResponse:
    """
    Stream chat response from Lox Genie.

    Args:
        message: User message to chat with Lox Genie

    Returns:
        StreamingResponse: Streamed AI response
    """
    try:
        request = AgentState(messages=[ChatMessage(role="user", content=message)], stream=True)
        request.messages.append(HumanMessage(content=message))
        request.message_counts = count_messages(request.messages)
        return StreamingResponse(graph.stream(request))
    except Exception as exc:
        logger.error(f"Error in lox_genie_stream: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to start streaming response: {str(exc)}")