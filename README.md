<div align="center">
  <img src="static/lox-logo512.png" alt="Lox Logo" width="128" height="128">
</div>

# Lox API

The Lox API provides access to the **Lox Genie**, a fantasy football consultant built with the Gemini family of LLMs and LangGraph, and the **Lox MCP Server**, a Model Context Protocol server offering specialized fantasy football data tools.

## 🏈 What is Lox Genie?

Lox Genie is a traditioanal deep research agent which uses LangGraph and a multi-node architecture that:

- **Assesses relevance** of user queries to fantasy football topics
- **Engages in human-in-the-loop** clarification when queries are unclear
- **Plans research strategies** by breaking down complex questions into actionable subtasks
- **Executes research** using specialized MCP tools for data gathering
- **Provides expert analysis** with concise, well-supported recommendations

The agent is designed to be maximally truth-seeking, providing resolute and non-ambiguous answers by blending its knowledge base with ground-up analysis.

## 🛠️ MCP Server Tools

The Lox MCP Server provides a comprehensive suite of fantasy football data tools:

### Sleeper Platform Integration

- **Draft Analysis**: Complete draft pick metadata, auction prices, and rookie/redraft classifications
- **League Management**: User rosters, team records, waiver budgets, and league standings
- **Player Data**: Comprehensive player information with metadata and statistics
- **Team Analysis**: Detailed roster breakdowns with starters, bench players, and taxi squads

### External Data Sources

- **Fantasy Calc Rankings**: Dynasty and redraft player rankings with customizable scoring settings
- **Utility Tools**: Mathematical operations and data processing capabilities

## 🏗️ Architecture

The platform is built with modern Python technologies and follows microservices architecture:

- **FastAPI Service** (Port 8000): RESTful API with streaming chat capabilities
- **MCP Server** (Port 8001): Model Context Protocol server for tool integration
- **LangGraph Agent**: Multi-node workflow orchestration for intelligent research
- **Docker Support**: Containerized deployment with docker-compose

## Project Structure

lox-api/
├── services/  
│ ├── genie/  
│ │ ├── api/  
│ │ │ ├── app.py
│ │ │ └── routers/
│ │ ├── agent/
│ │ │ ├── nodes/
│ │ │ ├── prompts/
│ │ │ ├── config.py
│ │ │ ├── schemas.py
│ │ │ └── utils.py
│ │ ├── core/
│ │ ├── crud/
│ │ ├── db/
│ │ ├── models/
│ │ ├── schemas/
│ │ ├── utils/
│ │ └── main.py
│ └── mcp/  
│ ├── main.py
│ ├── tools/
│ ├── prompts/
│ ├── resources/
│ └── test/
├── docker/  
│ ├── Dockerfile.api  
│ ├── Dockerfile.mcp  
│ └── README.md  
├── requirements/  
│ ├── requirements-api.txt  
│ ├── requirements-mcp.txt  
│ └── README.md  
├── config/  
│ ├── config.py  
│ └── README.md  
├── scripts/  
│ ├── run-dev.sh  
│ ├── run-dev.bat  
│ └── README.md  
├── tests/  
├── docs/  
├── docker-compose.yml  
└── README.md

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Docker (for containerized deployment)

## Quick Start

### Using Docker (Recommended)

```bash
# Start both services
docker-compose up --build

# Access services
# FastAPI: http://localhost:8000
# MCP Server: http://localhost:8001
```

### Local Development

#### Using uv (Windows)

```bash
# Install uv if you haven't already
pip install uv

# Install dependencies
uv sync

# Run the FastAPI service
uv run services/genie/main.py

# In another terminal, run the MCP server
uv run services/mcp/main.py
```

#### Using pip/venv

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements/requirements-api.txt
pip install -r requirements/requirements-mcp.txt

# Run services
python services/genie/main.py
python services/mcp/main.py
