"""
Gatekeeper node for the agent
"""
import os
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import END

from services.api.agent.config import Configuration
from services.api.agent.schemas import AgentState, GatekeeperResponse
from services.api.agent.utils import get_current_date, count_messages
from services.api.agent.prompts.gatekeeper import prompt
from services.api.utils.logger import logger
from services.api.core.config import settings

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
        temperature=0.3,
    )
    
    # Format the prompt
    formatted_prompt = prompt.format(
        current_date=get_current_date(),
        tools="",
        messages=state.messages[:-1],
        question=state.messages[-1].content,
    )

    # Run inference
    structured_llm = llm.with_structured_output(GatekeeperResponse)
    try:
        result = structured_llm.invoke(formatted_prompt)
        logger.info(f"Gatekeeper result: {result}")
    except Exception as e:
        print(f"Error in gatekeeper node: {e}")
        result = GatekeeperResponse(
            action="clarification_needed",
            response="I'm having trouble processing your request right now. Could you please rephrase your question?",
        )

    # Update the state with the result
    state.messages.append(AIMessage(content=result.response))
    
    # Direct answers and research required are relevant
    if result.action in ["direct_answer", "research_required"]:
        state.messages[-1].additional_kwargs["relevant"] = True
    elif result.action in ["clarification_needed"]:
        state.messages[-1].additional_kwargs["relevant"] = False

    # Update the action type in the AI response and message count
    state.messages[-1].additional_kwargs["action"] = result.action
    state.message_counts = count_messages(state.messages)
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
