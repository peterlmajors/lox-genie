"""
Planner node for the agent
"""
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

from services.api.agent.config import Configuration
from services.api.agent.schemas import AgentState, PlanResponse
from services.api.agent.utils import get_current_date, update_state, get_mcp_tools_formatted
from services.api.agent.prompts.planner import prompt
from services.api.core.config import settings
from services.api.utils.logger import logger

def planner(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Planner node that can:
    1. Plan the trajectory of the agent
    2. Update the state with the result
    """
    
    # Initialize the planning model and LLM instance
    configuration = Configuration.from_runnable_config(config)
    llm = ChatOpenAI(
        base_url=settings.LLM_BASE_URL,
        api_key="not-needed",  # llama.cpp doesn't require API key
        model=configuration.planning_agent_model,
        temperature=0.5,
    )

    # Format the prompt
    formatted_prompt = prompt.format(
        current_date=get_current_date(),
        tools=get_mcp_tools_formatted(),
        messages=state.messages[:-1],
        question=state.messages[-1].content,
    )

    # Invoke the LLM and parse the JSON response
    result = None
    try:
        # Create structured LLM, invoke the endpoint, and update state
        structured_llm = llm.with_structured_output(PlanResponse) 
        result = structured_llm.invoke(formatted_prompt)
        state = update_state(state, result, "planner")
    except Exception as e:
        logger.error(f"Error in planner node: {type(e).__name__}: {str(e)}", exc_info=True)
        result = PlanResponse(
            subtasks=[],
        )
    return state