from services.genie.agent.schemas import MessageCounts
from services.genie.schemas.chat import ChatMessage
from typing import List

from datetime import datetime

def get_current_date():
    return datetime.now().strftime("%B %d, %Y")

def get_tools():
    return [
        {
            "name": "Reddit Search",
            "description": "Search Reddit for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The query to search Reddit for"},
                },
                "required": ["query"],
            }
        }
    ]

def count_messages(messages: List[ChatMessage]) -> MessageCounts:
    return MessageCounts(
        message_count=len(messages),
        human_messages=sum(1 for message in messages if message.__class__.__name__ == "HumanMessage"),
        ai_messages=sum(1 for message in messages if message.__class__.__name__ == "AIMessage"),
    )