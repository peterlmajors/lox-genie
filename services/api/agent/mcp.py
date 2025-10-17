"""
MCP client for the gatekeeper agent
"""

import os
from fastmcp.client import Client

# MCP configuration
config = {
    "lox-mcp": {
        "url": f"http://localhost:8001/mcp",
        "transport": "http",
    }
}

# Define MCP client
client = Client(config)

# Get gatekeeper resources
gatekeeper_resources = [resource for resource in client.resources()]

# Get executor tools
executor_tools = [tool for tool in client.tools() if tool.name.startswith("executor")]