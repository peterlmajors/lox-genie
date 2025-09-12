import os
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
  
from services.genie.agent.config import Configuration
from services.genie.agent.schemas import AgentState, ToolExecutorResponse
from services.genie.agent.prompts.tool_executor import prompt
from services.genie.agent.utils import get_current_date, get_tools, count_messages


def tool_executor(state: AgentState, config: RunnableConfig) -> AgentState:
    """LangGraph node which assesses the relevance of the user's question to the topic"""
    
    # Format the prompt
    formatted_prompt = prompt.format(
        current_date=get_current_date(),
        tools=str(get_tools()),
        messages=state.messages[:-1],
        question=state.messages[-1].content,
    )

    # Initialize the relevance model and LLM instance
    tool_executor_model = Configuration.from_runnable_config(config).tool_executor_model
    llm = ChatGoogleGenerativeAI(
        model=tool_executor_model,
        temperature=0,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    # Run inference
    structured_llm = llm.with_structured_output(ToolExecutorResponse)
    result = structured_llm.invoke(formatted_prompt)
    
    # Update the state with the result
    state.messages[-1].additional_kwargs["tool_executor"] = result.tool_executor
    state.messages.append(AIMessage(content=result.reasoning))
    state.message_counts = count_messages(state.messages)
    return state
    