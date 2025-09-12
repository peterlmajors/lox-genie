from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from langgraph.types import interrupt

from services.genie.agent.schemas import AgentState
from services.genie.agent.utils import count_messages


def human_in_loop(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    This function asks the user to provide a relevant fantasy football question
    based on the relevance reasoning AIMessage from the most recent message in the state.

    Args:
        state: The current agent state containing messages
        config: The runnable configuration containing model settings

    Returns:
        AgentState: Updated agent state with user's clarification
    """
    # Ue the relevance reasoning as the interrupt message
    relevance_reasoning = state.messages[-1].content
    user_clarification = interrupt(relevance_reasoning)
    clarification_message = HumanMessage(content=user_clarification)

    # Update the state with the clarification message
    state.messages.append(clarification_message)
    state.message_counts = count_messages(state.messages)
    return state
