"""
Agent node endpoints for testing and debugging individual agent components.
"""
import logging
from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from services.api.agent.nodes.gatekeeper import gatekeeper
from services.api.agent.nodes.planner import planner
from services.api.agent.nodes.executor import executor
from services.api.agent.schemas import AgentState, MessageCounts, PlanResponse
from services.api.schemas.agents import GatekeeperRequest, PlannerRequest, ExecutorRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/agents")

@router.post("/gatekeeper")
async def test_gatekeeper(request: GatekeeperRequest) -> dict:
    """
    Test the gatekeeper node directly.
    """
    try:
        # Build the state
        state = AgentState(
            thread_id=request.thread_id,
            messages=[HumanMessage(content=request.message)],
            message_counts=MessageCounts()
        )
        
        # Create runnable config
        config = RunnableConfig(configurable={})
        
        # Call the gatekeeper node and extract the response
        updated_state = gatekeeper(state, config)        
        last_message = updated_state.messages[-1]

        return {
            "response": last_message.content, # type: ignore
            "action": last_message.additional_kwargs.get("action", None), # type: ignore
            "relevant": last_message.additional_kwargs.get("relevant", None) # type: ignore
        }
        
    except Exception as exc:
        logger.error(f"Error in gatekeeper endpoint: {type(exc).__name__}: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process gatekeeper: {str(exc)}")


@router.post("/planner")
async def test_planner(request: PlannerRequest) -> dict:
    """
    Test the planner node directly.
    """
    try:
        # Build the state
        state = AgentState(
            thread_id=request.thread_id,
            messages=[HumanMessage(content=request.message)],
            message_counts=MessageCounts(),
        )
        
        # Create runnable config
        config = RunnableConfig(configurable={})
        
        # Call the planner node
        updated_state = planner(state, config)
    
        return {
            "subtasks": updated_state.messages[-1].content # type: ignore
        }
    except Exception as exc:
        logger.error(f"Error in planner endpoint: {type(exc).__name__}: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process planner: {str(exc)}")

@router.post("/executor")
async def test_executor(request: ExecutorRequest) -> dict[str, list[str]]:
    """
    Test the executor node directly.
    """
    try:
        # Build the state
        state = AgentState(
            thread_id=request.thread_id,
            messages=[HumanMessage(content=request.message)],
            message_counts=MessageCounts()
        )
        return state
        
    except Exception as exc:
        logger.error(f"Error in executor endpoint: {type(exc).__name__}: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process executor: {str(exc)}")


@router.post("/summarize")
async def test_summarize() -> dict[str, str]:
    """
    Test the summarize node directly.
    """
    return {
        "context": "This endpoint is reserved for future use."
    }