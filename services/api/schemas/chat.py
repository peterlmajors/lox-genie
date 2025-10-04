from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid

class ChatMessage(BaseModel):
    """Individual chat message model."""
    message_id: str = Field(default=uuid.uuid4(), description="Unique ID for the message")
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[str] = Field(None, description="Timestamp of the message")

class ChatRequest(BaseModel):
    """Chat request model."""
    messages: List[ChatMessage] = Field(..., description="List of chat messages")
    stream: bool = Field(False, description="Whether to stream the response")

class ChatResponse(BaseModel):
    """Chat response model."""
    response: str = Field(..., description="AI response content")
    usage: Optional[Dict[str, Any]] = Field(None, description="Token usage information")