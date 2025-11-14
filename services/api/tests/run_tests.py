#!/usr/bin/env python3
"""
Convenience script to run agent endpoint tests.
Cross-platform alternative to run_tests.sh
"""
import sys
import subprocess
from pathlib import Path


def run_command(cmd: list[str], cwd: Path) -> int:
    """Run a command and return the exit code."""
    print(f"Running: {' '.join(cmd)}")
    print("-----------------------------------")
    result = subprocess.run(cmd, cwd=cwd)
    print("-----------------------------------")
    return result.returncode


def main():
    """Main test runner function."""
    # Get directories
    script_dir = Path(__file__).parent
    api_dir = script_dir.parent
    
    print("Running agent endpoint tests...")
    print(f"API Directory: {api_dir}")
    print("-----------------------------------")
    
    # Default pytest command
    base_cmd = ["pytest", "tests/test_agents.py"]
    
    # Parse command line arguments
    if len(sys.argv) == 1:
        # Run all tests with verbose output
        print("Running all agent tests...")
        cmd = base_cmd + ["-v"]
    else:
        arg = sys.argv[1]
        
        if arg == "gatekeeper":
            print("Running gatekeeper tests...")
            cmd = base_cmd + ["::TestGatekeeperEndpoint", "-v"]
        elif arg == "planner":
            print("Running planner tests...")
            cmd = base_cmd + ["::TestPlannerEndpoint", "-v"]
        elif arg == "executor":
            print("Running executor tests...")
            cmd = base_cmd + ["::TestExecutorEndpoint", "-v"]
        elif arg == "summarize":
            print("Running summarize tests...")
            cmd = base_cmd + ["::TestSummarizeEndpoint", "-v"]
        elif arg == "integration":
            print("Running integration tests...")
            cmd = base_cmd + ["::TestEndpointIntegration", "-v"]
        elif arg == "coverage":
            print("Running tests with coverage report...")
            cmd = base_cmd + [
                "--cov=api.routes.agents",
                "--cov-report=html",
                "--cov-report=term"
            ]
        elif arg == "verbose":
            print("Running all tests with detailed output...")
            cmd = base_cmd + ["-vv", "-s"]
        else:
            print(f"Unknown option: {arg}")
            print("Usage: python run_tests.py [gatekeeper|planner|executor|summarize|integration|coverage|verbose]")
            return 1
    
    # Run the tests
    exit_code = run_command(cmd, api_dir)
    
    if exit_code == 0:
        print("Tests completed successfully!")
    else:
        print(f"Tests failed with exit code {exit_code}")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
