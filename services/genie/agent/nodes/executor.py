import os
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from services.genie.agent.config import Configuration
from services.genie.agent.schemas import AgentState, ToolExecutorResponse
from services.genie.agent.prompts.executor import prompt
from services.genie.agent.utils import get_current_date, count_messages, get_tools  
from services.genie.agent.tools import *

def executor(state: AgentState, config: RunnableConfig) -> AgentState:
    """LangGraph node which assesses the relevance of the user's question to the topic"""

    # Initialize the relevance model and LLM instance
    executor_model = Configuration.from_runnable_config(config).executor_model
    llm = ChatGoogleGenerativeAI(
        model=executor_model,
        temperature=0,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY"),
        tool_call=True,
    )
    
    tools = get_tools()
    tool_functions = [tool.func for tool in tools]

    # Initialize structured output for the react agent with tools and output type
    llm_with_tools = llm.bind_tools(tool_functions)
    llm_with_structured_output = llm_with_tools.with_structured_output(ToolExecutorResponse)
    react_agent = create_react_agent(llm_with_structured_output, tool_functions)

    # Run inference on each subtask
    for subtask in state.plan[-1].subtasks:
        formatted_prompt = prompt.format(current_date=get_current_date(), tools=str(tools), task=subtask)
        result = react_agent.invoke(formatted_prompt)
        state.tool_calls.append(result)

    # Update the state with the result
    # state.message_counts = count_messages(state.messages)
    return state
