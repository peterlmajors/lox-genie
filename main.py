from services.genie.agent.schemas import AgentState
from services.genie.agent.graph import graph
from langchain_core.messages import HumanMessage

def main(state: AgentState = AgentState()) -> dict:
    while True:
        user_input = input("Enter your question (or 'exit' to quit): ")
        if user_input.strip().lower() == "exit":
            break
        
        state.messages.append(HumanMessage(content=user_input))
        last_message = state.messages[-1]
        print(f"User: {getattr(last_message, 'content', last_message)}")
        
        state = graph.invoke(state)
        last_message = state.messages[-1]
        print(f"Genie: {getattr(last_message, 'content', last_message)}")
    return state

state = main()