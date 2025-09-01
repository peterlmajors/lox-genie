from services.mcp.main import mcp

@mcp.tool(
    name="multiply",           # Custom tool name for the LLM
    description="Multiply two numbers", # Custom description
    tags={"lox-mcp"},      # Optional tags for organization/filtering
    meta={"version": "1.0", "author": "lox-mcp"}  # Custom metadata
)
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b
