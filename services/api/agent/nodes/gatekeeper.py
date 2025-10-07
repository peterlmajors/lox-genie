import os
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama
from langgraph.graph import END

from services.api.agent.config import Configuration
from services.api.agent.schemas import AgentState, GatekeeperResponse
from services.api.agent.utils import get_current_date, count_messages
from services.api.agent.prompts.gatekeeper import prompt


def gatekeeper(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Gatekeeper node that can:
    1. Answer simple queries directly
    2. Route to the research planner
    3. Request clarification via human-in-the-loop
    4. Handle off-topic conversations
    """
    
    # Initialize the model and LLM instance
    model = Configuration.from_runnable_config(config).gatekeeper_agent_model
    llm = ChatOllama(
        model=model,
        temperature=0.3,
    )
    
    # Format the prompt
    formatted_prompt = prompt.format(
        current_date=get_current_date(),
        tools="",
        knowledge_base="",  # TODO: Add knowledge base content
        messages=state.messages[:-1],
        question=state.messages[-1].content,
    )

    # Run inference
    structured_llm = llm.with_structured_output(GatekeeperResponse)
    try:
        result = structured_llm.invoke(formatted_prompt)       
    except Exception as e:
        print(f"Error in gatekeeper node: {e}")
        result = GatekeeperResponse(
            action="clarification_needed",
            response="I'm having trouble processing your request right now. Could you please rephrase your question?",
        )
    
    # Handle different actions
    if result.action in ["direct_answer", "research_required"]:
        state.messages[-1].additional_kwargs["relevant"] = True
        state.messages.append(AIMessage(content=result.response))
    elif result.action in ["clarification_needed", "off_topic"]:
        state.messages[-1].additional_kwargs["relevant"] = False
        state.messages.append(AIMessage(content=result.response))
        
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
