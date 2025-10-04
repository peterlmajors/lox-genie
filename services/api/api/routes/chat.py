
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage

from services.api.agent.graph import graph
from services.api.agent.schemas import AgentState
from services.api.agent.utils import count_messages
from services.api.schemas.chat import ChatResponse, ChatMessage

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/genie", response_model=ChatResponse)
async def lox_genie(message: str) -> ChatResponse:
    """
    Chat with the Lox Genie.
    Args:
        message: User message to chat with Lox Genie
    Returns:
        ChatResponse: AI response with content and metadata
    """
    try:

        
        # Create the request
        state = AgentState(messages=[ChatMessage(role="user", content=message)], stream=False)
        state.messages.append(HumanMessage(content=message))
        state.message_counts = count_messages(state.messages)

        # Invoke the graph with the state
        state_dict = graph.invoke(state)
        state = AgentState.model_validate(state_dict)

        # Return the response
        return ChatResponse(response=state.messages[-1].content)
    except Exception as exc:
        logger.error(f"Error in lox_genie: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(exc)}")


@router.post("/genie/stream")
async def lox_genie_stream(message: str) -> StreamingResponse:
    """
    Stream chat response from Lox Genie.

    Args:
        message: User message to chat with Lox Genie

    Returns:
        StreamingResponse: Streamed AI response
    """
    try:
        request = AgentState(messages=[ChatMessage(role="user", content=message)], stream=True)
        request.messages.append(HumanMessage(content=message))
        request.message_counts = count_messages(request.messages)
        return StreamingResponse(graph.stream(request))
    except Exception as exc:
        logger.error(f"Error in lox_genie_stream: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to start streaming response: {str(exc)}")