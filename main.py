import os
from services.genie.agent.schemas import AgentState
from services.genie.agent.graph import graph
from langchain_core.messages import HumanMessage

def main(state: AgentState = AgentState()) -> dict:
    while True:
        user_input = input("\nEnter your question (or 'exit' to quit): ")
        if user_input.strip().lower() == "exit":
            break
        # Append the user's question to the state
        state.messages.append(HumanMessage(content=user_input))

        # Print the user's question
        last_message = state.messages[-1]
        print(f"\nUser: {getattr(last_message, 'content', last_message)}")
        
        # Invoke the graph
        state_dict = graph.invoke(state)
        state = AgentState.model_validate(state_dict)

        # Print the genie's response
        last_message = state.messages[-1]
        print(f"\nGenie: {getattr(last_message, 'content', last_message)}")
    return state

state = main()