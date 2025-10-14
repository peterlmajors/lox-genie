from pydantic import BaseModel
from typing import List, Optional

class ThreadResponse(BaseModel):
    thread_id: str
    messages: List[dict]
    message_counts: dict
    reduced_context: dict
    relevant: bool
    plan: List[dict]
    tool_calls: List[dict]
    created_at: str
    last_updated: str
    ttl_seconds: Optional[int] = None


class ThreadListResponse(BaseModel):
    thread_ids: List[str]
    count: int