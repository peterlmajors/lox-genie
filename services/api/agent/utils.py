"""
Utility functions for the agent
"""
from datetime import datetime
from typing import List, Literal, Union
from functools import lru_cache
from fastmcp.client import Client
from langchain_core.messages import HumanMessage, AIMessage

from services.api.agent.schemas import MessageCounts, AgentState, GatekeeperResponse, PlanResponse, ToolExecutorResponse
from services.api.core.config import settings
from services.api.utils.logger import logger

def get_current_date() -> str:
    """Get the current date and time in UTC."""
    return datetime.utcnow().strftime("%B %d, %Y %H:%M UTC")

def count_messages(messages: List[Union[HumanMessage, AIMessage]]) -> MessageCounts:
    """Count of messages from the state."""
        
    return MessageCounts(
        total=len(messages),
        user=sum(1 for message in messages if isinstance(message, HumanMessage)),
        lox=sum(1 for message in messages if isinstance(message, AIMessage)),
    )

def update_state(state: AgentState, result: Union[GatekeeperResponse, PlanResponse, ToolExecutorResponse], agent: Literal["gatekeeper", "planner", "executor"]) -> AgentState:

    # Update the state based on the agent
    if agent == "gatekeeper":
        # Add message
        state.messages.append(AIMessage(content=result.response))
        # Updating action kwarg
        state.messages[-1].additional_kwargs["action"] = result.action
        # Updating relevance kwarg
        if result and result.action in ["direct_answer", "research_required"]:
            state.messages[-1].additional_kwargs["relevant"] = True
        elif result and result.action in ["clarification_needed"]:
            state.messages[-1].additional_kwargs["relevant"] = False

    elif agent == "planner":
        # Adding plan as message (to be displayed to user)
        state.messages.append(AIMessage(content=result.subtasks))

    state.message_counts = count_messages(state.messages)
    return state

@lru_cache(maxsize=1)
def get_mcp_tools() -> List:
    """
    Get tools from the MCP server with caching.
    
    This function is cached so the MCP connection is only made once.
    Subsequent calls return the cached result.
    
    Returns:
        List of tools from the MCP server
    """
    try:
        logger.info(f"Connecting to MCP server at {settings.MCP_BASE_URL}")
        config = {
            "lox-mcp": {
                "url": settings.MCP_BASE_URL,
                "transport": "http",
            }
        }
        client = Client(config)
        tools = [tool for tool in client.tools()]
        logger.info(f"Successfully loaded {len(tools)} tools from MCP")
        return tools
    except Exception as e:
        logger.error(f"Failed to load tools from MCP: {e}", exc_info=True)
        return []


def get_mcp_tools_formatted() -> str:
    """
    Get MCP tools formatted as a string for prompt injection.
    
    Returns:
        Formatted string describing available tools
    """
    tools = get_mcp_tools()
    if not tools:
        return "No tools available."
    
    tool_descriptions = []
    for tool in tools:
        name = getattr(tool, 'name', 'Unknown')
        description = getattr(tool, 'description', 'No description')
        tool_descriptions.append(f"- {name}: {description}")
    
    return "\n".join(tool_descriptions)