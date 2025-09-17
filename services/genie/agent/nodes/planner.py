import os
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI

from services.genie.agent.schemas import AgentState, PlanResponse
from services.genie.agent.config import Configuration
from services.genie.agent.prompts.planner import prompt
from services.genie.agent.utils import get_current_date, get_tools, count_messages


def planner(state: AgentState, config: RunnableConfig) -> AgentState:
    """LangGraph node which plans the trajectory of the agent."""

    # Initialize the planning model and LLM instance
    planning_model = Configuration.from_runnable_config(config).planning_agent_model

    # Format the prompt
    formatted_prompt = prompt.format(
        current_date=get_current_date(),
        tools=str(get_tools()),
        messages=state.messages[:-1],
        question=state.messages[-1].content,
    )

    # Initialize the LLM instance
    llm = ChatGoogleGenerativeAI(
        model=planning_model,
        temperature=0.3,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    # Run inference
    structured_llm = llm.with_structured_output(PlanResponse)
    result = structured_llm.invoke(formatted_prompt)

    # Update the state with the result
    state.plan.append(result)
    state.message_counts = count_messages(state.messages)
    return state