from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel

from services.api.redis.client import get_redis_client, RedisClient
from services.api.redis.agent_state import AgentStateRedis

router = APIRouter()


class ThreadResponse(BaseModel):
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


class ThreadListResponse(BaseModel):
    thread_ids: List[str]
    count: int


@router.get("/threads/{thread_id}", response_model=ThreadResponse)
async def get_thread_by_id(thread_id: str, redis_client: RedisClient = Depends(get_redis_client)) -> ThreadResponse:
    """
    Retrieve a thread by its thread_id from Redis.
    """
    agent_state = await redis_client.get_agent_state(thread_id)
    if not agent_state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")
    return ThreadResponse(
        thread_id=agent_state.thread_id,
        messages=[msg.model_dump() for msg in agent_state.messages],
        message_counts=agent_state.message_counts,
        reduced_context=agent_state.reduced_context.model_dump() if hasattr(agent_state.reduced_context, "model_dump") else agent_state.reduced_context,
        relevant=agent_state.relevant,
        plan=[plan.model_dump() if hasattr(plan, "model_dump") else plan for plan in getattr(agent_state, "plan", [])],
        tool_calls=[tool.model_dump() if hasattr(tool, "model_dump") else tool for tool in getattr(agent_state, "tool_calls", [])],
        created_at=agent_state.created_at,
        last_updated=agent_state.last_updated,
        ttl_seconds=getattr(agent_state, "ttl_seconds", None)
    )


@router.get("/threads", response_model=ThreadListResponse)
async def list_active_threads(redis_client: RedisClient = Depends(get_redis_client)) -> ThreadListResponse:
    """
    List all active thread IDs from Redis.
    """
    thread_ids = await redis_client.list_thread_ids()
    return ThreadListResponse(thread_ids=thread_ids, count=len(thread_ids))
