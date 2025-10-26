"""
Gatekeeper node for the agent
"""
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import END

from services.api.agent.config import Configuration
from services.api.agent.schemas import AgentState, GatekeeperResponse
from services.api.agent.utils import get_current_date, update_state, get_mcp_tools_formatted
from services.api.agent.prompts.gatekeeper import prompt
from services.api.core.config import settings
from services.api.utils.logger import logger

def gatekeeper(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Gatekeeper node that can:
    1. Answer simple queries directly
    2. Route to the research planner
    3. Request clarification via human-in-the-loop
    """
    
    # Initialize the model and LLM instance
    configuration = Configuration.from_runnable_config(config)
    llm = ChatOpenAI(
        base_url=settings.LLM_BASE_URL,
        api_key="not-needed",  # llama.cpp doesn't require API key
        model=configuration.gatekeeper_agent_model,
        temperature=0.7
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
        structured_llm = llm.with_structured_output(GatekeeperResponse) 
        result = structured_llm.invoke(formatted_prompt)
        state = update_state(state, result, "gatekeeper")
    except Exception as e:
        logger.error(f"Error in gatekeeper node: {type(e).__name__}: {str(e)}", exc_info=True)
        result = GatekeeperResponse(
            action="clarification_needed",
            response="I'm having trouble processing your request right now. Could you please rephrase your question?",
        )
    return state

def after_gatekeeper(state: AgentState) -> str:
    """
    Route based on the action taken in the gatekeeper node.
    """
    # Check if the last message is from AI (direct answer or off-topic handled)
    if state.messages and state.messages[-1].type == "ai":
        return END  # End the conversation flow
    # Check if we need to go to human-in-the-loop for clarification
    if not state.messages[-1].additional_kwargs.get("relevant", True):
        return "human_in_loop"
    
    # If relevant=True, proceed to planner for research
    return "planner"
