# Redis Integration for API Service

This directory contains the Redis integration for the API service, allowing endpoints to interact with Redis for agent state management without needing to communicate across Docker containers.

## Structure

```
redis/
├── __init__.py
├── client.py              # Main Redis client wrapper
├── core/
│   ├── __init__.py
│   └── config.py          # Redis configuration settings
├── models/
│   ├── __init__.py
│   └── agent_state.py     # Pydantic models for agent state
├── crud/
│   ├── __init__.py
│   └── agent_state.py     # CRUD operations for agent state
├── example_usage.py       # Example usage patterns
└── README.md             # This file
```

## Features

- **Direct Redis Connection**: API service connects directly to Redis without container communication
- **Agent State Management**: Full CRUD operations for agent states with thread-based storage
- **FastAPI Integration**: Seamless integration with FastAPI dependency injection
- **Health Monitoring**: Redis health checks integrated into API health endpoints
- **Message Management**: Support for LangChain message types with Redis serialization
- **TTL Support**: Configurable time-to-live for agent states
- **Cleanup Operations**: Automatic cleanup of expired agent states

## Configuration

Redis configuration is managed through environment variables with the `REDIS_` prefix:

```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_password
REDIS_DB=0
REDIS_KEY_PREFIX=thread
REDIS_TTL_SECONDS=2592000  # 30 days
```

## Usage

### Basic Usage in FastAPI Routes

```python
from fastapi import APIRouter, Depends
from services.api.redis.client import get_redis_client, RedisClient
from services.api.redis.models.agent_state import AgentStateRedis

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(
    message: str,
    thread_id: str,
    redis_client: RedisClient = Depends(get_redis_client)
):
    # Get existing agent state
    agent_state = await redis_client.get_agent_state(thread_id)
    
    if not agent_state:
        # Create new state
        agent_state = AgentStateRedis(thread_id=thread_id)
    
    # Add message
    agent_state.add_message("human", message)
    
    # Process with AI (your logic here)
    # ...
    
    # Save updated state
    await redis_client.set_agent_state(agent_state)
    
    return {"response": "AI response here"}
```

### Available Endpoints

The Redis integration provides the following API endpoints:

#### Agent State Management
- `GET /redis/agent-state/{thread_id}` - Get agent state
- `POST /redis/agent-state` - Create new agent state
- `PUT /redis/agent-state/{thread_id}` - Update agent state
- `DELETE /redis/agent-state/{thread_id}` - Delete agent state

#### Message Operations
- `POST /redis/agent-state/{thread_id}/messages` - Add message to state

#### Context Management
- `PUT /redis/agent-state/{thread_id}/context` - Update context
- `PUT /redis/agent-state/{thread_id}/relevance` - Set relevance flag

#### Utility Operations
- `GET /redis/agent-states` - List all thread IDs
- `GET /redis/agent-states/recent` - Get recent states
- `GET /redis/agent-state/{thread_id}/exists` - Check existence
- `GET /redis/agent-state/{thread_id}/ttl` - Get TTL
- `POST /redis/agent-state/{thread_id}/extend-ttl` - Extend TTL
- `POST /redis/cleanup-expired` - Cleanup expired states

### Redis Client Methods

```python
# Basic CRUD operations
await redis_client.get_agent_state(thread_id)
await redis_client.set_agent_state(agent_state)
await redis_client.delete_agent_state(thread_id)
await redis_client.exists_agent_state(thread_id)

# Utility operations
await redis_client.list_thread_ids(pattern="*")
await redis_client.count_agent_states()
await redis_client.get_recent_agent_states(limit=10)
await redis_client.cleanup_expired_agent_states(max_age_days=30)

# TTL operations
await redis_client.get_agent_state_ttl(thread_id)
await redis_client.extend_agent_state_ttl(thread_id, ttl_seconds)

# Health check
await redis_client.health_check()
```

## Integration with Chat Routes

The chat routes have been updated to use Redis for state management:

```python
@router.post("/genie")
async def lox_genie(
    message: str, 
    thread_id: Optional[str] = None,
    redis_client: RedisClient = Depends(get_redis_client)
):
    # Get or create agent state from Redis
    if thread_id:
        redis_state = await redis_client.get_agent_state(thread_id)
        if redis_state:
            state = redis_state.to_agent_state()
        else:
            state = AgentState(thread_id=thread_id, messages=[], stream=False)
    else:
        state = AgentState(messages=[], stream=False)
    
    # Add user message and process
    state.messages.append(HumanMessage(content=message))
    # ... AI processing ...
    
    # Save updated state to Redis
    redis_state = AgentStateRedis.from_agent_state(state)
    await redis_client.set_agent_state(redis_state)
    
    return ChatResponse(response=state.messages[-1].content)
```

## Health Monitoring

Redis health is automatically included in the API health check endpoint:

```bash
GET /health
```

Returns:
```json
{
  "status": "ok",
  "service": "lox-genie-api",
  "version": "0.1.0",
  "environment": "development",
  "hostname": "localhost",
  "uptime": 123.45,
  "timestamp": 1640995200.0,
  "redis_status": {
    "status": "healthy",
    "redis_version": "7.0.0",
    "connected_clients": 5,
    "used_memory_human": "1.2M",
    "keyspace": 42
  }
}
```

## Error Handling

The Redis client includes comprehensive error handling:

- Connection failures are logged and reconnection is attempted
- Invalid data is handled gracefully with appropriate error messages
- TTL operations handle missing keys appropriately
- All operations return meaningful error responses

## Thread Safety

The Redis client is designed to be thread-safe and can be used concurrently across multiple FastAPI requests. Connection pooling is configured for optimal performance.

## Example

See `example_usage.py` for a complete example of how to use the Redis client for agent state management.
