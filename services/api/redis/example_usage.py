"""
Example usage of Redis client for agent state management in API service
"""

import asyncio
from services.api.redis.client import get_redis_client
from services.api.redis.models.agent_state import AgentStateRedis


async def example_usage():
    """Example of how to use the Redis client for agent state management"""
    
    # Get Redis client (this would typically be injected via FastAPI dependency)
    redis_client = await get_redis_client()
    
    # Create a new agent state
    agent_state = AgentStateRedis(
        thread_id="example-thread-123",
        ttl_seconds=3600  # 1 hour TTL
    )
    
    # Add some messages
    agent_state.add_message("human", "Hello, how are you?")
    agent_state.add_message("ai", "I'm doing well, thank you! How can I help you today?")
    
    # Update context
    agent_state.update_context("User is asking about general well-being and seeking assistance")
    
    # Set relevance
    agent_state.set_relevance(True)
    
    # Save to Redis
    success = await redis_client.set_agent_state(agent_state)
    print(f"Agent state saved: {success}")
    
    # Retrieve from Redis
    retrieved_state = await redis_client.get_agent_state("example-thread-123")
    if retrieved_state:
        print(f"Retrieved agent state with {len(retrieved_state.messages)} messages")
        print(f"Last message: {retrieved_state.messages[-1].content}")
        print(f"Context: {retrieved_state.reduced_context.context}")
        print(f"Relevant: {retrieved_state.relevant}")
    
    # Add another message to existing state
    if retrieved_state:
        retrieved_state.add_message("human", "Can you help me with fantasy football?")
        await redis_client.set_agent_state(retrieved_state)
        print("Added another message to existing state")
    
    # Check if state exists
    exists = await redis_client.exists_agent_state("example-thread-123")
    print(f"Agent state exists: {exists}")
    
    # Get TTL
    ttl = await redis_client.get_agent_state_ttl("example-thread-123")
    print(f"TTL: {ttl} seconds")
    
    # List all thread IDs
    thread_ids = await redis_client.list_thread_ids()
    print(f"All thread IDs: {thread_ids}")
    
    # Get recent states
    recent_states = await redis_client.get_recent_agent_states(limit=5)
    print(f"Recent states count: {len(recent_states)}")
    
    # Clean up - delete the example state
    deleted = await redis_client.delete_agent_state("example-thread-123")
    print(f"Agent state deleted: {deleted}")


if __name__ == "__main__":
    asyncio.run(example_usage())
