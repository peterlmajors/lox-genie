"""
Executor node for the agent
"""
import os
import uuid
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig

from services.api.agent.config import Configuration
from services.api.agent.schemas import AgentState, ToolExecutorResponse
from services.api.agent.utils import get_current_date, update_state, get_mcp_tools_formatted
from services.api.agent.prompts.executor import prompt
from services.api.core.config import settings

def executor(state: AgentState, config: RunnableConfig) -> AgentState:

    # Initialize the executor model and LLM instance
    configuration = Configuration.from_runnable_config(config)
    llm = ChatOpenAI(
        base_url=settings.LLM_BASE_URL,
        api_key="not-needed",  # llama.cpp doesn't require API key
        model=configuration.executor_model,
        temperature=0.0
    )
    structured_llm = llm.with_structured_output(ToolExecutorResponse)

    # Run inference on each subtask and add to the state
    for subtask in state.plan[-1].subtasks:
        formatted_prompt = prompt.format(
            current_date=get_current_date(),
            tools=get_mcp_tools_formatted(),
            task=subtask
        )
        result = structured_llm.invoke(formatted_prompt)
        
        result.plan_id = state.plan[-1].plan_id
        result.tool_id = str(uuid.uuid4())
        state.tool_calls.append(result)

    # Update the state with the result
    state = update_state(state=state, result=result, agent="executor")
    return state