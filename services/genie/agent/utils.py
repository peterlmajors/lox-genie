
from datetime import datetime
from typing import List
import importlib
import inspect
import os

from services.genie.agent.schemas import MessageCounts
from services.genie.schemas.chat import ChatMessage

def get_current_date():
    """Get the current date."""
    return datetime.now().strftime("%B %d, %Y")

def get_tools():
    """Get the tools from the tools module."""
    tools = []
    tools_dir = os.path.join(os.path.dirname(__file__), "tools")
    tools_pkg = "services.genie.agent.tools"

    for filename in os.listdir(tools_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"{tools_pkg}.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module):
                    if callable(obj) and hasattr(obj, "description"):
                        tools.append(obj)
            except Exception:
                continue
  
    for tool in tools:
        desc_lines = tool.description.split("\n")
        for i in range(len(desc_lines)):
            if desc_lines[i].endswith(":"):
                desc_lines[i] = desc_lines[i] + " " + desc_lines[i+1].strip()
        desc_lines = [desc for desc in desc_lines if ":" in desc]
        tool.description = "\n".join(desc_lines)
        if hasattr(tool, "args_schema"):
         delattr(tool, "args_schema")
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
