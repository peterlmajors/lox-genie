"""
Request schema models for agent endpoints.
Response schemas are imported from services.api.agent.schemas.
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field
import uuid

class MessageRequest(BaseModel):
    """Request model for messages."""
    type: str = Field(..., description="Message type: 'human' or 'ai'")
    content: str = Field(..., description="Message content")
    additional_kwargs: Dict[str, Any] = Field(default_factory=dict, description="Additional message metadata")


class GatekeeperRequest(BaseModel):
    """Request model for gatekeeper endpoint."""
    message: str = Field(..., description="User message to process")
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Thread ID (auto-generated if not provided)")
    previous_messages: List[MessageRequest] = Field(default_factory=list, description="Previous conversation messages")


class PlannerRequest(BaseModel):
    """Request model for planner endpoint."""
    message: str = Field(..., description="User message to plan for")
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Thread ID (auto-generated if not provided)")
    previous_messages: List[MessageRequest] = Field(default_factory=list, description="Previous conversation messages")


class ExecutorRequest(BaseModel):
    """Request model for executor endpoint."""
    plan_id: str = Field(..., description="Plan ID to execute")
    subtasks: List[str] = Field(..., description="List of subtasks to execute")
    message: str = Field(..., description="User message context")
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Thread ID (auto-generated if not provided)")
    previous_messages: List[MessageRequest] = Field(default_factory=list, description="Previous conversation messages")

