"""
Redis routes for agent state management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from services.api.redis.client import get_redis_client, RedisClient
from services.api.redis.models.agent_state import AgentStateRedis, MessageRedis

router = APIRouter()


# Request/Response Models
class AgentStateResponse(BaseModel):
    thread_id: str
    messages: List[dict]
    message_counts: dict
    reduced_context: dict
    relevant: bool
    plan: List[dict]
    tool_calls: List[dict]
    created_at: str
    last_updated: str
    ttl_seconds: Optional[int] = None


class CreateAgentStateRequest(BaseModel):
    thread_id: Optional[str] = None
    ttl_seconds: Optional[int] = None


class AddMessageRequest(BaseModel):
    message_type: str  # "human" or "ai"
    content: str
    metadata: Optional[Dict[str, Any]] = None


class UpdateContextRequest(BaseModel):
    context: str


class SetRelevanceRequest(BaseModel):
    relevant: bool


class ListResponse(BaseModel):
    thread_ids: List[str]
    count: int


class RecentStatesResponse(BaseModel):
    agent_states: List[AgentStateResponse]
    count: int


# Agent State CRUD Routes
@router.get(
    "/agent-state/{thread_id}",
    response_model=AgentStateResponse,
    summary="Get agent state",
    description="Retrieve agent state by thread ID",
    tags=["Agent State"]
)
async def get_agent_state(
    thread_id: str,
    redis_client: RedisClient = Depends(get_redis_client)
) -> AgentStateResponse:
    """Get agent state by thread ID"""
    agent_state = await redis_client.get_agent_state(thread_id)
    
    if not agent_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent state not found for thread {thread_id}"
        )
    
    return AgentStateResponse(**agent_state.model_dump(mode='json'))


@router.post(
    "/agent-state",
    response_model=AgentStateResponse,
    summary="Create agent state",
    description="Create a new agent state",
    tags=["Agent State"]
)
async def create_agent_state(
    request: CreateAgentStateRequest,
    redis_client: RedisClient = Depends(get_redis_client)
) -> AgentStateResponse:
    """Create a new agent state"""
    agent_state = AgentStateRedis(
        thread_id=request.thread_id,
        ttl_seconds=request.ttl_seconds
    )
    
    success = await redis_client.set_agent_state(agent_state)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create agent state"
        )
    
    return AgentStateResponse(**agent_state.model_dump(mode='json'))


@router.put(
    "/agent-state/{thread_id}",
    response_model=AgentStateResponse,
    summary="Update agent state",
    description="Update an existing agent state",
    tags=["Agent State"]
)
async def update_agent_state(
    thread_id: str,
    agent_state_data: dict,
    redis_client: RedisClient = Depends(get_redis_client)
) -> AgentStateResponse:
    """Update an existing agent state"""
    # Get existing state
    existing_state = await redis_client.get_agent_state(thread_id)
    if not existing_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent state not found for thread {thread_id}"
        )
    
    # Update fields
    for key, value in agent_state_data.items():
        if hasattr(existing_state, key):
            setattr(existing_state, key, value)
    
    # Save updated state
    success = await redis_client.set_agent_state(existing_state)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update agent state"
        )
    
    return AgentStateResponse(**existing_state.model_dump(mode='json'))


@router.delete(
    "/agent-state/{thread_id}",
    summary="Delete agent state",
    description="Delete agent state by thread ID",
    tags=["Agent State"]
)
async def delete_agent_state(
    thread_id: str,
    redis_client: RedisClient = Depends(get_redis_client)
) -> JSONResponse:
    """Delete agent state by thread ID"""
    success = await redis_client.delete_agent_state(thread_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent state not found for thread {thread_id}"
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Agent state deleted for thread {thread_id}"}
    )


# Message Operations
@router.post(
    "/agent-state/{thread_id}/messages",
    response_model=AgentStateResponse,
    summary="Add message to agent state",
    description="Add a new message to the agent state",
    tags=["Agent State Messages"]
)
async def add_message(
    thread_id: str,
    request: AddMessageRequest,
    redis_client: RedisClient = Depends(get_redis_client)
) -> AgentStateResponse:
    """Add a message to the agent state"""
    agent_state = await redis_client.get_agent_state(thread_id)
    
    if not agent_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent state not found for thread {thread_id}"
        )
    
    agent_state.add_message(
        message_type=request.message_type,
        content=request.content,
        metadata=request.metadata
    )
    
    success = await redis_client.set_agent_state(agent_state)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update agent state"
        )
    
    return AgentStateResponse(**agent_state.model_dump(mode='json'))


# Context Operations
@router.put(
    "/agent-state/{thread_id}/context",
    response_model=AgentStateResponse,
    summary="Update context",
    description="Update the reduced context for an agent state",
    tags=["Agent State Context"]
)
async def update_context(
    thread_id: str,
    request: UpdateContextRequest,
    redis_client: RedisClient = Depends(get_redis_client)
) -> AgentStateResponse:
    """Update the reduced context for an agent state"""
    agent_state = await redis_client.get_agent_state(thread_id)
    
    if not agent_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent state not found for thread {thread_id}"
        )
    
    agent_state.update_context(request.context)
    
    success = await redis_client.set_agent_state(agent_state)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update agent state"
        )
    
    return AgentStateResponse(**agent_state.model_dump(mode='json'))


# Relevance Operations
@router.put(
    "/agent-state/{thread_id}/relevance",
    response_model=AgentStateResponse,
    summary="Set relevance",
    description="Set the relevance flag for an agent state",
    tags=["Agent State Relevance"]
)
async def set_relevance(
    thread_id: str,
    request: SetRelevanceRequest,
    redis_client: RedisClient = Depends(get_redis_client)
) -> AgentStateResponse:
    """Set the relevance flag for an agent state"""
    agent_state = await redis_client.get_agent_state(thread_id)
    
    if not agent_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent state not found for thread {thread_id}"
        )
    
    agent_state.set_relevance(request.relevant)
    
    success = await redis_client.set_agent_state(agent_state)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update agent state"
        )
    
    return AgentStateResponse(**agent_state.model_dump(mode='json'))


# Utility Routes
@router.get(
    "/agent-states",
    response_model=ListResponse,
    summary="List agent states",
    description="List all agent state thread IDs",
    tags=["Agent State Utilities"]
)
async def list_agent_states(
    pattern: str = "*",
    redis_client: RedisClient = Depends(get_redis_client)
) -> ListResponse:
    """List all agent state thread IDs"""
    thread_ids = await redis_client.list_thread_ids(pattern)
    count = await redis_client.count_agent_states()
    
    return ListResponse(thread_ids=thread_ids, count=count)


@router.get(
    "/agent-states/recent",
    response_model=RecentStatesResponse,
    summary="Get recent agent states",
    description="Get recent agent states ordered by last updated",
    tags=["Agent State Utilities"]
)
async def get_recent_agent_states(
    limit: int = 10,
    redis_client: RedisClient = Depends(get_redis_client)
) -> RecentStatesResponse:
    """Get recent agent states"""
    agent_states = await redis_client.get_recent_agent_states(limit)
    
    response_states = [
        AgentStateResponse(**state.model_dump(mode='json'))
        for state in agent_states
    ]
    
    return RecentStatesResponse(
        agent_states=response_states,
        count=len(response_states)
    )


@router.get(
    "/agent-state/{thread_id}/exists",
    summary="Check agent state existence",
    description="Check if an agent state exists",
    tags=["Agent State Utilities"]
)
async def check_agent_state_exists(
    thread_id: str,
    redis_client: RedisClient = Depends(get_redis_client)
) -> JSONResponse:
    """Check if an agent state exists"""
    exists = await redis_client.exists_agent_state(thread_id)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"exists": exists, "thread_id": thread_id}
    )


@router.get(
    "/agent-state/{thread_id}/ttl",
    summary="Get agent state TTL",
    description="Get the time-to-live for an agent state",
    tags=["Agent State Utilities"]
)
async def get_agent_state_ttl(
    thread_id: str,
    redis_client: RedisClient = Depends(get_redis_client)
) -> JSONResponse:
    """Get the TTL for an agent state"""
    ttl = await redis_client.get_agent_state_ttl(thread_id)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"ttl": ttl, "thread_id": thread_id}
    )


@router.post(
    "/agent-state/{thread_id}/extend-ttl",
    summary="Extend agent state TTL",
    description="Extend the time-to-live for an agent state",
    tags=["Agent State Utilities"]
)
async def extend_agent_state_ttl(
    thread_id: str,
    ttl_seconds: int,
    redis_client: RedisClient = Depends(get_redis_client)
) -> JSONResponse:
    """Extend the TTL for an agent state"""
    success = await redis_client.extend_agent_state_ttl(thread_id, ttl_seconds)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent state not found for thread {thread_id}"
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"TTL extended for thread {thread_id}"}
    )


@router.post(
    "/cleanup-expired",
    summary="Cleanup expired agent states",
    description="Clean up expired agent states",
    tags=["Agent State Utilities"]
)
async def cleanup_expired_agent_states(
    max_age_days: int = 30,
    redis_client: RedisClient = Depends(get_redis_client)
) -> JSONResponse:
    """Clean up expired agent states"""
    deleted_count = await redis_client.cleanup_expired_agent_states(max_age_days)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"deleted_count": deleted_count, "max_age_days": max_age_days}
    )
