import os
from services.genie.agent.graph import graph
from langchain_core.messages import HumanMessage
from services.genie.agent.schemas import AgentState
from services.genie.agent.utils import count_messages

def main(state: AgentState = AgentState()) -> dict:
    while True:
        user_input = input("\nEnter your question (or 'exit' to quit): ")
        if user_input.strip().lower() == "exit":
            break

        # Append the user's question to the state
        state.messages.append(HumanMessage(content=user_input))
        state.message_counts = count_messages(state.messages)

        # Print the user's question
        print(f"\nUser: {state.messages[-1].content}")
        print(f"\n{30*'='}")
        # Invoke the graph
        state_dict = graph.invoke(state)
        state = AgentState.model_validate(state_dict)

        # Print the genie's response
        print(f"\nGenie: {state.messages[-1].content}")
        print(f"\n{30*'='}")
    return state
state = main()