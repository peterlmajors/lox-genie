# Lox API

A FastAPI service with MCP (Model Context Protocol) server for fantasy football data and calculations.

## Project Structure

```
lox-api/
├── services/              # Application services
│   ├── genie/            # FastAPI service
│   │   ├── api/          # API routes
│   │   ├── core/         # Core functionality
│   │   ├── crud/         # Database operations
│   │   ├── db/           # Database configuration
│   │   ├── models/       # Data models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── utils/        # Service-specific utilities
│   │   └── main.py       # Entry point
│   └── mcp/              # MCP service
│       ├── main.py       # Entry point
│       ├── tools/        # MCP tools
│       ├── prompts/      # MCP prompts
│       ├── resources/    # MCP resources
│       └── test/         # Tests
├── shared/               # Shared code between services
│   ├── utils/            # Shared utilities
│   ├── constants/        # Shared constants
│   └── types/            # Shared type definitions
├── docker/               # Docker configuration
│   ├── Dockerfile.api    # API service Dockerfile
│   ├── Dockerfile.mcp    # MCP service Dockerfile
│   └── README.md         # Docker documentation
├── requirements/         # Python dependencies
│   ├── requirements-api.txt # API service requirements
│   ├── requirements-mcp.txt # MCP service requirements
│   └── README.md         # Requirements documentation
├── config/               # Configuration files
│   ├── config.py         # Main configuration
│   └── README.md         # Configuration documentation
├── scripts/              # Development scripts
│   ├── run-dev.sh        # Unix/Linux/Mac dev script
│   ├── run-dev.bat       # Windows dev script
│   └── README.md         # Scripts documentation
├── tests/                # Integration tests
├── docs/                 # Documentation
├── docker-compose.yml    # Docker Compose configuration
└── README.md             # This file
```

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

#### Using Scripts

```bash
# Unix/Linux/Mac
./scripts/run-dev.sh

# Windows
scripts\run-dev.bat
```

#### Manual Start

```bash
# Install dependencies
pip install -r requirements/requirements-api.txt
pip install -r requirements/requirements-mcp.txt

# Start FastAPI service
python -m services.genie.main

# Start MCP server (in another terminal)
python services/mcp/main.py
```

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
