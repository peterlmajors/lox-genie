"""
Lox Genie's Agent Graph
"""
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from services.api.agent.schemas import AgentState
from services.api.agent.nodes.gatekeeper import gatekeeper, after_gatekeeper
from services.api.agent.nodes.human_in_loop import human_in_loop
from services.api.agent.nodes.executor import executor
from services.api.agent.nodes.planner import planner
from services.api.agent.config import Configuration

# Build Lox Genie's Agent Graph
builder = StateGraph(AgentState, config_schema=Configuration)

# Nodes
builder.add_node("gatekeeper", gatekeeper)
builder.add_node("human_in_loop", human_in_loop)
builder.add_node("planner", planner)
builder.add_node("executor", executor)

# Edges
builder.add_edge(START, "gatekeeper")
builder.add_conditional_edges("gatekeeper", after_gatekeeper)
builder.add_edge("human_in_loop", "gatekeeper")
builder.add_edge("planner", "executor")
builder.add_edge("executor", END)

graph = builder.compile(name="lox-genie-agent")
