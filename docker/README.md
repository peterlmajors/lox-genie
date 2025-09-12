# Docker Configuration

This folder contains the Docker configuration files for the Lox API services.

## Files

- `Dockerfile.genie` - Dockerfile for the FastAPI service
- `Dockerfile.mcp` - Dockerfile for the MCP (Model Context Protocol) server

## Usage

These Dockerfiles are referenced by the `docker-compose.yml` file in the root directory.

### Building Individual Images

```bash
# Build API image
docker build -f docker/Dockerfile.genie -t lox-genie .

# Build MCP image
docker build -f docker/Dockerfile.mcp -t lox-mcp .
```

### Running with Docker Compose

```bash
# Build and start both services
docker-compose up --build

# Start in detached mode
docker-compose up -d --build
```

## Service Ports

- **API Service**: Port 8000
- **MCP Service**: Port 8001

## Network

Both services are connected via the `lox-network` Docker network defined in `docker-compose.yml`.
