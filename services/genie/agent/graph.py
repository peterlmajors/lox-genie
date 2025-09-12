from langgraph.graph import StateGraph
from langgraph.graph import START, END
from services.genie.agent.schemas import AgentState
from services.genie.agent.nodes.relevance import relevance, after_relevance
from services.genie.agent.nodes.human_in_loop import human_in_loop
from services.genie.agent.nodes.executor import executor
from services.genie.agent.nodes.planner import planner
from services.genie.agent.config import Configuration

# Build Lox Genie Agent Graph
builder = StateGraph(AgentState, config_schema=Configuration)

# Nodes
builder.add_node("relevance", relevance)
builder.add_node("human_in_loop", human_in_loop)
builder.add_node("planner", planner)
builder.add_node("executor", executor)

# Edges
builder.add_edge(START, "relevance")
builder.add_conditional_edges("relevance", after_relevance)
builder.add_edge("human_in_loop", "relevance")
builder.add_edge("planner", "executor")
builder.add_edge("executor", END)

graph = builder.compile(name="lox-genie-agent")
