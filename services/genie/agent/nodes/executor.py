
import uuid
from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama

from services.genie.agent.config import Configuration
from services.genie.agent.schemas import AgentState, ToolExecutorResponse
from services.genie.agent.utils import get_current_date, count_messages, get_tools  
from services.genie.agent.prompts.executor import prompt

def executor(state: AgentState, config: RunnableConfig) -> AgentState:
    """LangGraph node which assesses the relevance of the user's question to the topic"""

    # Initialize the executor model and LLM instance
    executor_model = Configuration.from_runnable_config(config).executor_model
    llm = ChatOllama(
        model=executor_model,
        reasoning=True,
        temperature=0
    )
    structured_llm = llm.with_structured_output(ToolExecutorResponse)

    # Initialize the tools and bind
    tools = get_tools()
    llm.bind_tools([tool.func for tool in tools])

    # Run inference on each subtask and add to the state
    for subtask in state.plan[-1].subtasks:
        formatted_prompt = prompt.format(current_date=get_current_date(), tools=str(tools), task=subtask)
        result = structured_llm.invoke(formatted_prompt)
        
        result.plan_id = state.plan[-1].plan_id
        result.tool_id = str(uuid.uuid4())
        state.tool_calls.append(result)

    # Update the state with the result
    state.message_counts = count_messages(state.messages)
    return state