"""
MCP client for the gatekeeper agent
"""

import os
from fastmcp.client import Client

# MCP configuration
config = {
    "lox-mcp": {
        "url": f"{os.getenv('HOSTNAME', 'http://localhost')}{os.getenv('LLM_SERVICE_PORT', '8002')}",
        "transport": "http",
    }
}

# Define MCP client
client = Client(config)

# Get gatekeeper resources
gatekeeper_resources = [resource for resource in client.resources() if resource.name.startswith("gatekeeper")]

# Get executor tools
executor_tools = [tool for tool in client.tools() if tool.name.startswith("executor")]