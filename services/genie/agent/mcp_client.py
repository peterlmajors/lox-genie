import asyncio
from fastmcp import Client
import httpx

config = {
    "lox-mcp": {
        "url": "http://localhost:8001/mcp",
        "transport": "http",
    }
}

client = Client(config)

async def main():
    async with client:
        ping_result = await client.ping()
        print(f"Connected: {ping_result}")
        if not ping_result:
            raise Exception("Failed to connect to MCP server")

        tools = await client.list_tools()
        print(f"Tools: {tools}")
        resources = await client.list_resources()
        print(f"Resources: {resources}")

asyncio.run(main())