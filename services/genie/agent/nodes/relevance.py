
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama
  
from services.genie.agent.config import Configuration
from services.genie.agent.schemas import AgentState, RelevanceResponse  
from services.genie.agent.utils import get_current_date, get_tools, count_messages
from services.genie.agent.prompts.relevance import prompt

def relevance(state: AgentState, config: RunnableConfig) -> AgentState:
    """LangGraph node which assesses the relevance of the user's question to the topic"""
    
    # Initialize the relevance model and LLM instance
    relevance_model = Configuration.from_runnable_config(config).relevance_agent_model
    llm = ChatOllama(
        model=relevance_model,
        temperature=0
    )
    
    # Format the prompt
    formatted_prompt = prompt.format(
        current_date=get_current_date(),
        tools=str(get_tools()),
        messages=state.messages[:-1],
        question=state.messages[-1].content,
    )

    # Run inference
    structured_llm = llm.with_structured_output(RelevanceResponse)
    result = structured_llm.invoke(formatted_prompt)
    print('result', result)
    
    # Update the state with the result
    state.messages[-1].additional_kwargs["relevant"] = result.relevant
    if not result.relevant:
        state.messages.append(AIMessage(content=result.reasoning))
        state.message_counts = count_messages(state.messages)
    return state
    
# Route to planner if relevant, human_in_loop if not relevant
def after_relevance(state: AgentState) -> str:
    """Route to planner if relevant, human_in_loop if not relevant"""
    last_human_message = next((m for m in reversed(state.messages) if m.type == "human"), None)
    return "planner" if last_human_message.additional_kwargs["relevant"] else "human_in_loop"