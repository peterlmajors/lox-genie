"""
Tests for agent endpoints.

This test suite validates the functionality of individual agent nodes:
- Gatekeeper: Validates and routes user messages
- Planner: Creates execution plans for user requests
- Executor: Executes planned tasks
- Summarize: Summarizes conversation context
"""
import json
import logging
from pathlib import Path
from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

from services.api.api.app import app

logger = logging.getLogger(__name__)

# Load test data
TEST_DATA_PATH = Path(__file__).parent / "agents_test_data.json"
with open(TEST_DATA_PATH) as f:
    TEST_DATA = json.load(f)

# Create test client
client = TestClient(app)


class TestGatekeeperEndpoint:
    """Tests for the /agents/gatekeeper endpoint."""

    @pytest.mark.parametrize("test_case", TEST_DATA["gatekeeper"])
    def test_gatekeeper_responses(self, test_case: Dict[str, Any]):
        """Test that gatekeeper processes various message types correctly."""
        response = client.post("/agents/gatekeeper", json=test_case["input"])
        
        assert response.status_code == 200, f"Failed for test case: {test_case['name']}"
        
        data = response.json()
        expected = test_case["expected"]
        
        # Validate response structure
        if expected["has_response"]:
            assert "response" in data, "Response should contain 'response' field"
            assert isinstance(data["response"], str), "Response should be a string"
            assert len(data["response"]) > 0, "Response should not be empty"
        
        if expected["has_action"]:
            assert "action" in data, "Response should contain 'action' field"
        
        if expected["has_relevant"]:
            assert "relevant" in data, "Response should contain 'relevant' field"

    def test_gatekeeper_without_thread_id(self):
        """Test gatekeeper with auto-generated thread_id."""
        response = client.post(
            "/agents/gatekeeper",
            json={"message": "Tell me about Lamar Jackson"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data

    def test_gatekeeper_empty_message(self):
        """Test gatekeeper with empty message."""
        response = client.post(
            "/agents/gatekeeper",
            json={"message": "", "thread_id": "test-empty"}
        )
        
        # Should either return 422 (validation error) or 200 with error handling
        assert response.status_code in [200, 422]

    def test_gatekeeper_invalid_payload(self):
        """Test gatekeeper with invalid payload."""
        response = client.post(
            "/agents/gatekeeper",
            json={"invalid_field": "value"}
        )
        
        assert response.status_code == 422  # Validation error


class TestPlannerEndpoint:
    """Tests for the /agents/planner endpoint."""

    @pytest.mark.parametrize("test_case", TEST_DATA["planner"])
    def test_planner_creates_subtasks(self, test_case: Dict[str, Any]):
        """Test that planner creates subtasks for various requests."""
        response = client.post("/agents/planner", json=test_case["input"])
        
        assert response.status_code == 200, f"Failed for test case: {test_case['name']}"
        
        data = response.json()
        expected = test_case["expected"]
        
        # Validate response structure
        if expected["has_subtasks"]:
            assert "subtasks" in data, "Response should contain 'subtasks' field"
            # Subtasks could be a string or list depending on implementation
            assert data["subtasks"] is not None, "Subtasks should not be None"

    def test_planner_without_thread_id(self):
        """Test planner with auto-generated thread_id."""
        response = client.post(
            "/agents/planner",
            json={"message": "Help me draft a quarterback"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "subtasks" in data

    def test_planner_complex_query(self):
        """Test planner with a complex multi-part query."""
        response = client.post(
            "/agents/planner",
            json={
                "message": "Analyze my team's weaknesses, suggest trades, and identify waiver wire targets",
                "thread_id": "test-complex-plan"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "subtasks" in data

    def test_planner_invalid_payload(self):
        """Test planner with missing required fields."""
        response = client.post(
            "/agents/planner",
            json={"thread_id": "test-invalid"}
        )
        
        assert response.status_code == 422  # Validation error


class TestExecutorEndpoint:
    """Tests for the /agents/executor endpoint."""

    @pytest.mark.parametrize("test_case", TEST_DATA["executor"])
    def test_executor_returns_state(self, test_case: Dict[str, Any]):
        """Test that executor processes tasks and returns state."""
        response = client.post("/agents/executor", json=test_case["input"])
        
        # Note: The current implementation just returns the state, so we expect 200
        # Once fully implemented, this will need updating
        assert response.status_code == 200, f"Failed for test case: {test_case['name']}"
        
        data = response.json()
        expected = test_case["expected"]
        
        # Validate response structure
        if expected["returns_state"]:
            # Check that response is a dict (AgentState)
            assert isinstance(data, dict), "Response should be a dictionary (state)"

    def test_executor_minimal_input(self):
        """Test executor with minimal required fields."""
        response = client.post(
            "/agents/executor",
            json={
                "message": "Test message",
                "plan_id": "test-plan",
                "subtasks": ["Task 1"]
            }
        )
        
        assert response.status_code == 200

    def test_executor_invalid_payload(self):
        """Test executor with missing required fields."""
        response = client.post(
            "/agents/executor",
            json={"message": "Test message"}
        )
        
        assert response.status_code == 422  # Validation error

    def test_executor_empty_subtasks(self):
        """Test executor with empty subtasks list."""
        response = client.post(
            "/agents/executor",
            json={
                "message": "Test message",
                "plan_id": "test-plan",
                "subtasks": [],
                "thread_id": "test-empty-tasks"
            }
        )
        
        # Should accept empty list but may handle it differently
        assert response.status_code in [200, 422]


class TestSummarizeEndpoint:
    """Tests for the /agents/summarize endpoint."""

    @pytest.mark.parametrize("test_case", TEST_DATA["summarize"])
    def test_summarize_placeholder(self, test_case: Dict[str, Any]):
        """Test the summarize placeholder endpoint."""
        response = client.post("/agents/summarize", json=test_case["input"])
        
        assert response.status_code == 200, f"Failed for test case: {test_case['name']}"
        
        data = response.json()
        expected = test_case["expected"]
        
        # Validate response structure
        if expected["has_context"]:
            assert "context" in data, "Response should contain 'context' field"
            
            if "context_contains" in expected:
                assert expected["context_contains"].lower() in data["context"].lower(), \
                    f"Context should contain '{expected['context_contains']}'"

    def test_summarize_with_empty_body(self):
        """Test summarize with no body."""
        response = client.post("/agents/summarize")
        
        # Should still work as it's a placeholder
        assert response.status_code in [200, 422]


class TestEndpointIntegration:
    """Integration tests for agent endpoints."""

    def test_gatekeeper_to_planner_flow(self):
        """Test a typical flow from gatekeeper to planner."""
        # First, check if message is relevant via gatekeeper
        gatekeeper_response = client.post(
            "/agents/gatekeeper",
            json={
                "message": "Help me decide between two players",
                "thread_id": "integration-test-001"
            }
        )
        
        assert gatekeeper_response.status_code == 200
        gatekeeper_data = gatekeeper_response.json()
        
        # If relevant, proceed to planner
        # Note: The actual flow logic isn't tested here, just the endpoint responses
        planner_response = client.post(
            "/agents/planner",
            json={
                "message": "Help me decide between two players",
                "thread_id": "integration-test-001"
            }
        )
        
        assert planner_response.status_code == 200
        planner_data = planner_response.json()
        assert "subtasks" in planner_data

    def test_error_handling_consistency(self):
        """Test that all endpoints handle errors consistently."""
        endpoints = [
            "/agents/gatekeeper",
            "/agents/planner",
            "/agents/executor",
        ]
        
        for endpoint in endpoints:
            # Send completely invalid JSON
            response = client.post(
                endpoint,
                json={"completely": "invalid", "payload": "structure"}
            )
            
            # All should return 422 for validation errors
            assert response.status_code == 422, \
                f"Endpoint {endpoint} should return 422 for invalid payload"


# Pytest fixtures for setup/teardown if needed
@pytest.fixture(scope="module")
def test_thread_cleanup():
    """Cleanup test threads after tests complete."""
    yield
    # Add cleanup logic here if needed
    logger.info("Test suite completed")


# Optional: Add markers for different test categories
pytestmark = pytest.mark.asyncio

