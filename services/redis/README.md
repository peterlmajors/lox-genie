# Minimal Redis Service for Lox Genie

This is a minimal Redis service wrapper that provides basic Redis connectivity and health checks.

## ⚠️ Note

**For full Redis functionality with agent state management, use the Redis client in `services/api/redis/` instead.**

This minimal service is intended for:

- Simple Redis connectivity testing
- Basic health monitoring
- Lightweight Redis wrapper applications

## Features

- **Basic Redis Connection**: Connect to Redis server with configuration
- **Health Monitoring**: Simple health check functionality
- **Minimal Footprint**: Lightweight wrapper without complex state management

## Configuration

Environment variables (with `REDIS_` prefix):

- `REDIS_HOST`: Redis server host (default: localhost)
- `REDIS_PORT`: Redis server port (default: 6379)
- `REDIS_PASSWORD`: Redis password (optional)
- `REDIS_DB`: Redis database number (default: 0)

## Usage

### Basic Health Check

```python
from services.redis import get_redis_server

# Get Redis server instance
redis_server = await get_redis_server()

# Check health
health = await redis_server.health_check()
print(health)
# Output: {
#   "status": "healthy",
#   "redis_version": "7.0.0",
#   "connected_clients": 1,
#   "used_memory_human": "1.2M",
#   "keyspace": 5
# }
```

### Direct Redis Operations

```python
# Access the underlying Redis client for direct operations
redis_client = redis_server.redis_client
await redis_client.set("key", "value")
value = await redis_client.get("key")
```

## For Full Agent State Management

If you need full agent state management with LangChain integration, use:

```python
from services.api.redis.client import get_redis_client
from services.api.redis.models.agent_state import AgentStateRedis

redis_client = await get_redis_client()
agent_state = await redis_client.get_agent_state("thread_123")
```

## Docker

The Redis service uses the official Redis image and can be run with:

```bash
# Start Redis server with docker-compose
docker-compose up redis

# Or run Redis directly
docker run -p 6379:6379 redis:7-alpine
```
