
from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama

from services.genie.agent.config import Configuration
from services.genie.agent.schemas import AgentState, PlanResponse
from services.genie.agent.utils import get_current_date, count_messages, get_tools
from services.genie.agent.prompts.planner import prompt

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
    formatted_prompt = prompt.format(current_date=get_current_date(),tools=str(get_tools()),
                                     messages=state.messages[:-1],question=state.messages[-1].content)

    # Run inference
    structured_llm = llm.with_structured_output(PlanResponse)
    result = structured_llm.invoke(formatted_prompt)

    # Update the state with the result
    state.plan.append(result)
    state.message_counts = count_messages(state.messages)
    return state