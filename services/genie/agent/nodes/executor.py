import os
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from services.genie.agent.config import Configuration
from services.genie.agent.schemas import AgentState, ToolExecutorResponse
from services.genie.agent.prompts.executor import prompt
from services.genie.agent.utils import get_current_date, get_tools, count_messages

from services.genie.agent.nodes.tools import multiply

def executor(state: AgentState, config: RunnableConfig) -> AgentState:
    """LangGraph node which assesses the relevance of the user's question to the topic"""
    
    # Initialize the relevance model and LLM instance
    executor_model = Configuration.from_runnable_config(config).executor_model
    llm = ChatGoogleGenerativeAI(
        model=executor_model,
        temperature=0,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    
    # Initialize the structured LLM instance
    structured_llm = llm.with_structured_output(ToolExecutorResponse)
    llm = create_react_agent(llm, [multiply])
    
    # Execute the subtasks
    for plan in state.plan[-1].subtasks:
        # Format the prompt
        formatted_prompt = prompt.format(
            current_date=get_current_date(),
            task=plan, 
            tools=str(get_tools(params=True))
        )

        # Run inference
        result = structured_llm.invoke(formatted_prompt)
        
        # Update the state with the result
        state.tool_calls.append(result)

    # Update the state with the result
    state.messages[-1].additional_kwargs["executor"] = state.tool_calls[-1].executor
    state.message_counts = count_messages(state.messages)
    return state