# Lox API

The Lox API provides access to the Lox Genie, a fantasy football research agent developd with Langgraph, and the Lox MCP server.

## Project Structure

lox-api/
├── services/  
│ ├── genie/  
│ │ ├── api/  
│ │ │ ├── app.py # FastAPI app instance and router includes
│ │ │ └── routers/ # API route modules (e.g., user_routes.py)
│ │ ├── agent/ # Agent logic, nodes, prompts, config, schemas
│ │ │ ├── nodes/ # LangGraph nodes (e.g., relevance.py)
│ │ │ ├── prompts/ # Prompt templates
│ │ │ ├── config.py # Agent configuration
│ │ │ ├── schemas.py # Pydantic models for agent state
│ │ │ └── utils.py # Agent utilities
│ │ ├── core/ # Core FastAPI config and settings
│ │ ├── crud/ # Database CRUD operations
│ │ ├── db/ # Database connection/configuration
│ │ ├── models/ # SQLAlchemy models
│ │ ├── schemas/ # Pydantic schemas for API
│ │ ├── utils/ # Service-specific utilities
│ │ └── main.py # Genie service entry point
│ └── mcp/  
│ ├── main.py # MCP service entry point
│ ├── tools/ # MCP tools and utilities
│ ├── prompts/ # MCP prompt templates
│ ├── resources/ # MCP resources
│ └── test/ # MCP tests
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

## Services

- **FastAPI Service** (Port 8000): Main API for fantasy football data
- **MCP Server** (Port 8001): Model Context Protocol server

## Documentation

- [Docker Setup](docker/README-Docker.md)
- [Configuration](config/README.md)
- [Scripts](scripts/README.md)

## Health Checks

- FastAPI: http://localhost:8000/health
- MCP Server: http://localhost:8001/health
```