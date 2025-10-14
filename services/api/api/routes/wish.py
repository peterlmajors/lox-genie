"""
Generate a creative fantasy football question using LLM.
"""
import os
import logging
from fastapi import APIRouter, HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from services.api.agent.config import Configuration
from services.api.agent.utils import get_current_date
from services.api.agent.prompts.wish import prompt

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate-wish")
async def generate_wish() -> dict:
    """
    Generate a creative fantasy football question using LLM.
    
    Returns:
        dict: Generated question
    """
    try:
        # Initialize configuration
        config = Configuration.from_runnable_config()
        logger.info(f"Configuration: {config}")

        # Initialize LLM
        llm = ChatOpenAI(
            base_url=os.getenv("LLM_BASE_URL"),
            api_key="not-needed",
            model=config.gatekeeper_agent_model,
            temperature=0.9,
            max_tokens=150,
        )
        
        # Format the prompt
        messages = [SystemMessage(content=prompt.format(current_date=get_current_date()))]
        
        # Invoke the LLM asynchronously
        response = await llm.ainvoke(messages)
        generated_question = response.content.strip()
        
        # Remove quotes if the LLM wrapped the question in them
        if generated_question.startswith('"') and generated_question.endswith('"'):
            generated_question = generated_question[1:-1]
        if generated_question.startswith("'") and generated_question.endswith("'"):
            generated_question = generated_question[1:-1]
        
        logger.info(f"Generated wish: {generated_question}")
        
        return {"question": generated_question}
    
    except Exception as exc:
        logger.error(f"Error generating wish: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate wish: {str(exc)}")