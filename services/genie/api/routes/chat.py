
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from services.genie.core.config import settings
from services.genie.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/genie", response_model=ChatResponse)
async def lox_genie(request: ChatRequest) -> ChatResponse:
    """
    Chat with Gemini AI model.

    Args:
        request: Chat request containing messages and parameters

    Returns:
        ChatResponse: AI response with content and metadata
    """
    try:
        return 'Hello, how are you?'
    except Exception as exc:
        logger.error(f"Error in chat_with_gemini: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(exc)}")


@router.post("/genie/stream")
async def lox_genie_stream(request: ChatRequest) -> StreamingResponse:
    """
    Stream chat response from Gemini AI model.

    Args:
        request: Chat request containing messages and parameters

    Returns:
        StreamingResponse: Streamed AI response
    """
    try:
        return ChatResponse(response="Hello, how are you?", model=settings.GEMINI_MODEL)
    except Exception as exc:
        logger.error(f"Error in chat_with_gemini_stream: {exc}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to start streaming response: {str(exc)}"
        )