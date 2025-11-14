"""
Pytest configuration and shared fixtures for agent tests.
"""
import logging
import sys
from pathlib import Path

import pytest

# Add the services/api directory to the path for imports
api_path = Path(__file__).parent.parent
if str(api_path) not in sys.path:
    sys.path.insert(0, str(api_path))

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration."""
    return {
        "test_mode": True,
        "skip_external_calls": False,  # Set to True to skip actual API calls
    }


@pytest.fixture(scope="function")
def sample_thread_id():
    """Generate a unique thread ID for each test."""
    import uuid
    return f"test-thread-{uuid.uuid4()}"


@pytest.fixture(scope="function")
def sample_messages():
    """Provide sample message data for testing."""
    return [
        {
            "type": "human",
            "content": "Who is the best running back this week?",
            "additional_kwargs": {}
        },
        {
            "type": "ai",
            "content": "Based on matchups and recent performance...",
            "additional_kwargs": {}
        }
    ]

