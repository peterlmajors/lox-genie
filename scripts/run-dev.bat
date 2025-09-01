@echo off
echo Starting Lox API services in development mode...

echo Starting FastAPI service on port 8000...
start "FastAPI Service" cmd /k "python -m services.genie.main"

echo Starting MCP service on port 8001...
start "MCP Service" cmd /k "python services/mcp/main.py"

echo.
echo Services started!
echo FastAPI: http://localhost:8000
echo MCP Server: http://localhost:8001
echo.
echo Close the command windows to stop the services
pause
