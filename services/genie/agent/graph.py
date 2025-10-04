from langgraph.graph import StateGraph
from langgraph.graph import START, END
from services.genie.agent.schemas import AgentState
from services.genie.agent.nodes.gatekeeper import gatekeeper, after_gatekeeper
from services.genie.agent.nodes.human_in_loop import human_in_loop
from services.genie.agent.nodes.executor import executor
from services.genie.agent.nodes.planner import planner
from services.genie.agent.config import Configuration

# Build Lox Genie Agent Graph
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
