# Agent Endpoints Tests

Comprehensive test suite for the Lox Genie agent endpoints.

## Structure

- `test_agents.py` - Main test suite for all agent endpoints
- `agents_test_data.json` - Test data with sample inputs and expected outputs
- `conftest.py` - Pytest configuration and shared fixtures
- `__init__.py` - Package initialization

## Running Tests

### Run all tests
```bash
cd services/api
pytest tests/test_agents.py -v
```

### Run specific test class
```bash
pytest tests/test_agents.py::TestGatekeeperEndpoint -v
```

### Run specific test
```bash
pytest tests/test_agents.py::TestGatekeeperEndpoint::test_gatekeeper_responses -v
```

### Run with coverage
```bash
pytest tests/test_agents.py --cov=api.routes.agents --cov-report=html
```

### Run with detailed output
```bash
pytest tests/test_agents.py -vv -s
```

## Test Coverage

### Gatekeeper Endpoint Tests
- ✓ Fantasy football question processing
- ✓ Greeting handling
- ✓ Off-topic question detection
- ✓ Complex query processing
- ✓ Auto-generated thread IDs
- ✓ Empty message handling
- ✓ Invalid payload validation

### Planner Endpoint Tests
- ✓ Player comparison planning
- ✓ Waiver wire advice planning
- ✓ Trade analysis planning
- ✓ Lineup optimization planning
- ✓ Auto-generated thread IDs
- ✓ Complex multi-part queries
- ✓ Invalid payload validation

### Executor Endpoint Tests
- ✓ Simple task execution
- ✓ Multi-step execution
- ✓ State return validation
- ✓ Minimal input handling
- ✓ Empty subtasks handling
- ✓ Invalid payload validation

### Summarize Endpoint Tests
- ✓ Placeholder functionality
- ✓ Empty body handling

### Integration Tests
- ✓ Gatekeeper to planner flow
- ✓ Error handling consistency

## Test Data

Test data is stored in `agents_test_data.json` with the following structure:

```json
{
  "endpoint_name": [
    {
      "name": "test_case_name",
      "input": { /* request payload */ },
      "expected": { /* expected response structure */ }
    }
  ]
}
```

## Adding New Tests

1. Add test data to `agents_test_data.json`
2. Create or update test methods in `test_agents.py`
3. Use parametrize decorator for data-driven tests
4. Follow existing naming conventions

## Dependencies

- pytest
- fastapi
- httpx (via TestClient)

Install test dependencies:
```bash
pip install pytest pytest-cov pytest-asyncio
```

