# Requirements

This folder contains Python dependency requirements for the Lox API project.

## Files

- `requirements-api.txt` - Main requirements for the FastAPI service and general dependencies
- `requirements-mcp.txt` - Additional requirements specific to the MCP (Model Context Protocol) server

## Usage

### Install all dependencies

```bash
pip install -r requirements/requirements-api.txt
pip install -r requirements/requirements-mcp.txt
```

### Install only API dependencies

```bash
pip install -r requirements/requirements-api.txt
```

### Install only MCP dependencies

```bash
pip install -r requirements/requirements-mcp.txt
```

## Note

The Dockerfiles automatically install both requirement files when building the containers.
