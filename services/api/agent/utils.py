
from typing import List
from datetime import datetime
from services.api.agent.schemas import MessageCounts

def get_current_date():
    """Get the current date and time in UTC."""
    return datetime.utcnow().strftime("%B %d, %Y %H:%M UTC")

def count_messages(messages: List) -> MessageCounts:
    """Count of messages from the state."""
    from langchain_core.messages import HumanMessage, AIMessage
    
    return MessageCounts(
        total=len(messages),
        user=sum(1 for message in messages if isinstance(message, HumanMessage)),
        lox=sum(1 for message in messages if isinstance(message, AIMessage)),
    )

# def get_tools():
#     """Get the tools from the tools module."""
#     tools = []
#     tools_dir = os.path.join(os.path.dirname(__file__), "tools")
#     tools_pkg = "services.api.agent.tools"

#     for filename in os.listdir(tools_dir):
#         if filename.endswith(".py") and not filename.startswith("__"):
#             module_name = f"{tools_pkg}.{filename[:-3]}"
#             try:
#                 module = importlib.import_module(module_name)
#                 for name, obj in inspect.getmembers(module):
#                     if callable(obj) and hasattr(obj, "description"):
#                         tools.append(obj)
#             except Exception:
#                 continue
  
#     for tool in tools:
#         desc_lines = tool.description.split("\n")
#         for i in range(len(desc_lines)):
#             if desc_lines[i].endswith(":"):
#                 desc_lines[i] = desc_lines[i] + " " + desc_lines[i+1].strip()
#         desc_lines = [desc for desc in desc_lines if ":" in desc]
#         tool.description = "\n".join(desc_lines)
#         if hasattr(tool, "args_schema"):
#          delattr(tool, "args_schema")
#     return tools

# def remove_blank_fields(message: Message) -> Message:
#     """Drop fields with values of null, {}, [], or '' except 'additional_kwargs'"""
#     return {k: v for k, v in message.model_dump().items() if k != "additional_kwargs" and v not in [None, {}, [], ""]}