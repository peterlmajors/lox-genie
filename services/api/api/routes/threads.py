from fastapi import APIRouter, Depends, HTTPException, status
from services.api.redis.client import get_redis_client, RedisClient
from services.api.utils.logger import logger

router = APIRouter(prefix="/threads")


@router.get("/{thread_id}")
async def get_thread_by_id(thread_id: str, redis_client: RedisClient = Depends(get_redis_client)) -> dict:
    """
    Retrieve a thread by its thread_id from Redis.
    """
    agent_state = await redis_client.get_agent_state(thread_id)
    if not agent_state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")
    logger.info(f"Thread {thread_id} found")
    return {
        "thread_id": agent_state.get("thread_id"),
        "messages": agent_state.get("messages", []),
        "message_counts": agent_state.get("message_counts", {}),
        "reduced_context": agent_state.get("reduced_context", {}),
        "relevant": agent_state.get("relevant", False),
        "plan": agent_state.get("plan", []),
        "tool_calls": agent_state.get("tool_calls", []),
        "created_at": agent_state.get("created_at"),
        "last_updated": agent_state.get("last_updated"),
        "ttl_seconds": agent_state.get("ttl_seconds")
    }


@router.get("/active")
async def list_active_threads(redis_client: RedisClient = Depends(get_redis_client)) -> dict:
    """
    List all active thread IDs from Redis.
    """
    thread_ids = await redis_client.list_thread_ids()
    logger.info(f"Listed {len(thread_ids)} threads")
    return {"thread_ids": thread_ids, "count": len(thread_ids)}


@router.delete("/{thread_id}")
async def delete_thread(thread_id: str, redis_client: RedisClient = Depends(get_redis_client)) -> dict:
    """
    Delete a thread by its thread_id from Redis.
    """
    await redis_client.delete_agent_state(thread_id)
    logger.info(f"Thread {thread_id} deleted")
    return {"success": True, "thread_id": thread_id}


@router.delete("/active")
async def delete_all_active_threads(redis_client: RedisClient = Depends(get_redis_client)) -> dict:
    """
    Delete all threads from Redis.
    """
    thread_ids = await redis_client.list_thread_ids()
    for thread_id in thread_ids:
        await redis_client.delete_agent_state(thread_id)
    logger.info(f"All {len(thread_ids)} threads deleted")
    return {"success": True, "deleted_count": len(thread_ids)}