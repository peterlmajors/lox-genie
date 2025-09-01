#!/bin/bash

# Development script to run both services locally

echo "Starting Lox API services in development mode..."

# Start FastAPI service in background
echo "Starting FastAPI service on port 8000..."
python -m services.genie.main &
API_PID=$!

# Start MCP service in background
echo "Starting MCP service on port 8001..."
python services/mcp/main.py &
MCP_PID=$!

echo "Services started!"
echo "FastAPI: http://localhost:8000"
echo "MCP Server: http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt signal
trap "echo 'Stopping services...'; kill $API_PID $MCP_PID; exit" INT

# Wait for background processes
wait
