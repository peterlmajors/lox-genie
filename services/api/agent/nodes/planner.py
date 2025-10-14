import os
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

from services.api.agent.config import Configuration
from services.api.agent.schemas import AgentState, PlanResponse
from services.api.agent.utils import get_current_date, count_messages
from services.api.agent.prompts.planner import prompt

def planner(state: AgentState, config: RunnableConfig) -> AgentState:
    """LangGraph node which plans the trajectory of the agent."""

    # Initialize the planning model and LLM instance
    configuration = Configuration.from_runnable_config(config)
    llm = ChatOpenAI(
        base_url=os.getenv("LLM_BASE_URL"),
        api_key="not-needed",  # llama.cpp doesn't require API key
        model=configuration.planning_agent_model,
        temperature=0.3,
    )

    # Format the prompt
    formatted_prompt = prompt.format(current_date=get_current_date(),tools="",
                                     messages=state.messages[:-1],question=state.messages[-1].content)

    # Run inference
    structured_llm = llm.with_structured_output(PlanResponse)
    result = structured_llm.invoke(formatted_prompt)

    # Update the state with the result
    state.plan.append(result)
    state.message_counts = count_messages(state.messages)
    return state