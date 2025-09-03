import json
import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse

from services.genie.core.config import settings
from services.genie.models.chat import ChatRequest, ChatResponse
from services.genie.api.services.llm.gemini import validate_gemini_config
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/genie", response_model=ChatResponse)
async def lox_genie(request: ChatRequest, gemini_configured: None = Depends(validate_gemini_config)) -> ChatResponse:
    """
    Chat with Gemini AI model.

    Args:
        request: Chat request containing messages and parameters

    Returns:
        ChatResponse: AI response with content and metadata
    """
    try:
        return ChatResponse(response="Hello, how are you?", model=settings.GEMINI_MODEL)
    except Exception as exc:
        logger.error(f"Error in chat_with_gemini: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(exc)}")


@router.post("/genie/stream")
async def lox_genie_stream(request: ChatRequest, gemini_configured: None = Depends(validate_gemini_config)) -> StreamingResponse:
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