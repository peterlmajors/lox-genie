@echo off
echo Starting Lox API services in development mode...

echo Starting FastAPI service on port 8000...
start "FastAPI Service" cmd /k "python -m services/api/main.py"

echo Starting MCP service on port 8001...
start "MCP Service" cmd /k "python -m services/mcp/main.py"

echo Starting UI service on port 80...
start "UI Service" cmd /k "docker build -f docker/Dockerfile.ui -t lox-ui . && docker run --rm -p 80:80 lox-ui"

echo.
echo Services started!
echo FastAPI: http://localhost:8000
echo MCP Server: http://localhost:8001
echo UI: http://localhost:80
echo.
echo Close the command windows to stop the services
pause