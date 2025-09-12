# Scripts

This folder contains development and utility scripts for the Lox API project.

## Files

- `run-dev.sh` - Unix/Linux/Mac development script to run both services locally
- `run-dev.bat` - Windows development script to run both services locally

## Usage

### Unix/Linux/Mac

```bash
chmod +x scripts/run-dev.sh
./scripts/run-dev.sh
```

### Windows

```cmd
scripts\run-dev.bat
```

## What the scripts do

Both scripts start the FastAPI service on port 8000 and the MCP server on port 8001 in separate processes, allowing you to develop and test both services simultaneously.
