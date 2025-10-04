#!/bin/bash

# Development script to run both services locally
echo "Starting Lox API services in development mode..."

# Start FastAPI service in background
echo "Starting FastAPI service on port 8000..."
python -m services/api/main.py &
API_PID=$!

# Start MCP service in background
echo "Starting MCP service on port 8001..."
python -m services/mcp/main.py &
MCP_PID=$!

# Start UI service in background
echo "Starting UI service on port 80..."
docker build -f docker/Dockerfile.ui -t lox-ui . && docker run --rm -p 80:80 lox-ui &
UI_PID=$!

echo "Services started!"
echo "FastAPI: http://localhost:8000"
echo "MCP Server: http://localhost:8001"
echo "UI: http://localhost:80"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt signal
trap "echo 'Stopping services...'; kill $API_PID $MCP_PID $UI_PID; exit" INT

# Wait for background processes
wait
