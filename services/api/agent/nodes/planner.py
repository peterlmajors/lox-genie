
from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama

from services.api.agent.config import Configuration
from services.api.agent.schemas import AgentState, PlanResponse
from services.api.agent.utils import get_current_date, count_messages
from services.api.agent.prompts.planner import prompt

def planner(state: AgentState, config: RunnableConfig) -> AgentState:
    """LangGraph node which plans the trajectory of the agent."""

    # Initialize the planning model and LLM instance
    planning_model = Configuration.from_runnable_config(config).planning_agent_model
    llm = ChatOllama(
        model=planning_model,
        reasoning=True,
        temperature=0.3
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