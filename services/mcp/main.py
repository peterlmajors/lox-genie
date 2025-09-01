import asyncio
from fastmcp import FastMCP, Client
from starlette.requests import Request
from starlette.responses import PlainTextResponse

mcp = FastMCP("Lox MCP Server")

# ------------- TOOLS -------------
@mcp.tool
def process_data(input: str) -> str:
    """Process data on the server"""
    return f"Processed: {input}"

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

# Create ASGI application
app = mcp.http_app()

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8001)
