from services.genie.agent.schemas import MessageCounts
from services.genie.schemas.chat import ChatMessage
from datetime import datetime
from typing import List
import importlib
import inspect


def get_current_date():
    """Get the current date."""
    return datetime.now().strftime("%B %d, %Y")


def get_tools():
    """Get the tools from the tools module."""
    tools_module = importlib.import_module("services.genie.agent.tools")
    tools = [
        obj for name, obj in inspect.getmembers(tools_module)
        if callable(obj) and hasattr(obj, "description")
    ]
  
    for tool in tools:
        desc_lines = tool.description.split("\n")
        for i in range(len(desc_lines)):
            if desc_lines[i].endswith(":"):
                desc_lines[i] = desc_lines[i] + " " + desc_lines[i+1].strip()
        desc_lines = [desc for desc in desc_lines if ":" in desc]
        
        tool.description = "\n".join(desc_lines)
    return tools

def count_messages(messages: List[ChatMessage]) -> MessageCounts:
    """Count the messages in the list."""
    return MessageCounts(
        message_count=len(messages),
        human_messages=sum(
            1 for message in messages if message.__class__.__name__ == "HumanMessage"
        ),
        ai_messages=sum(
            1 for message in messages if message.__class__.__name__ == "AIMessage"
        ),
    )
