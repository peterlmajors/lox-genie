#!/bin/bash
# Convenience script to run agent endpoint tests

set -e

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_DIR="$(dirname "$SCRIPT_DIR")"

echo "Running agent endpoint tests..."
echo "API Directory: $API_DIR"
echo "-----------------------------------"

cd "$API_DIR"

# Default: run all tests with verbose output
if [ $# -eq 0 ]; then
    echo "Running all agent tests..."
    pytest tests/test_agents.py -v
else
    case "$1" in
        "gatekeeper")
            echo "Running gatekeeper tests..."
            pytest tests/test_agents.py::TestGatekeeperEndpoint -v
            ;;
        "planner")
            echo "Running planner tests..."
            pytest tests/test_agents.py::TestPlannerEndpoint -v
            ;;
        "executor")
            echo "Running executor tests..."
            pytest tests/test_agents.py::TestExecutorEndpoint -v
            ;;
        "summarize")
            echo "Running summarize tests..."
            pytest tests/test_agents.py::TestSummarizeEndpoint -v
            ;;
        "integration")
            echo "Running integration tests..."
            pytest tests/test_agents.py::TestEndpointIntegration -v
            ;;
        "coverage")
            echo "Running tests with coverage report..."
            pytest tests/test_agents.py --cov=api.routes.agents --cov-report=html --cov-report=term
            echo "Coverage report generated in htmlcov/index.html"
            ;;
        "verbose")
            echo "Running all tests with detailed output..."
            pytest tests/test_agents.py -vv -s
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [gatekeeper|planner|executor|summarize|integration|coverage|verbose]"
            exit 1
            ;;
    esac
fi

echo "-----------------------------------"
echo "Tests completed!"

