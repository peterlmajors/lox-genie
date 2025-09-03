import logging
from google import genai
from services.genie.core.config import settings
from fastapi import HTTPException

logger = logging.getLogger(__name__)

# Initialize Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(settings.GEMINI_MODEL)
else:
    model = None
    logger.warning("GEMINI_API_KEY not configured. Chat functionality will be limited.")

# Validate Gemini Config
def validate_gemini_config() -> None:
    """Validate that Gemini is properly configured."""
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Gemini API not configured. Please set GEMINI_API_KEY environment variable.",
        )