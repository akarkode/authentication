# Tests

This directory contains the test suite for the Authentication Service.

## Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures and configuration
├── factories.py             # Test data factories
├── test_security.py         # Token generation and validation tests
├── test_models.py           # Database model tests
├── test_schemas.py          # Pydantic schema validation tests
├── test_api_user.py         # User endpoint integration tests
└── test_api_google.py       # Google OAuth integration tests
```

## Running Tests

### Install Test Dependencies

```bash
poetry install --with dev
```

### Run All Tests

```bash
poetry run pytest
```

### Run Tests with Coverage

```bash
poetry run pytest --cov=app --cov-report=html
```

### Run Specific Test Categories

```bash
# Run only unit tests
poetry run pytest -m unit

# Run only integration tests
poetry run pytest -m integration

# Run specific test file
poetry run pytest tests/test_security.py

# Run specific test class
poetry run pytest tests/test_security.py::TestTokenService

# Run specific test method
poetry run pytest tests/test_security.py::TestTokenService::test_generate_access_token
```

### Run Tests in Verbose Mode

```bash
poetry run pytest -v
```

### Run Tests and Stop on First Failure

```bash
poetry run pytest -x
```

## Test Markers

Tests are organized with markers:

- `@pytest.mark.unit` - Fast unit tests that don't require external dependencies
- `@pytest.mark.integration` - Integration tests that test multiple components together
- `@pytest.mark.slow` - Slow running tests

## Test Fixtures

### Database Fixtures

- `test_db_engine` - Creates an in-memory SQLite database for testing
- `db_session` - Provides a database session that rolls back after each test
- `client` - HTTP client with overridden database session

### Auth Fixtures

- `valid_jwt_payload` - Returns a valid JWT payload for testing
- `test_settings` - Returns test configuration settings

## Writing New Tests

### Unit Test Example

```python
import pytest

@pytest.mark.unit
def test_something():
    assert True
```

### Async Test Example

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

### Integration Test Example

```python
import pytest
from httpx import AsyncClient

@pytest.mark.integration
@pytest.mark.asyncio
async def test_endpoint(client: AsyncClient):
    response = await client.get("/v1/user/me")
    assert response.status_code == 200
```

## Coverage Reports

After running tests with coverage, you can view the HTML report:

```bash
# Generate coverage report
poetry run pytest --cov=app --cov-report=html

# Open the report (adjust path for your OS)
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines. The test configuration uses:

- In-memory SQLite database (no external DB required)
- Environment variables set via pytest-env
- Automatic async test handling via pytest-asyncio

## Best Practices

1. **Keep tests isolated** - Each test should be independent
2. **Use factories** - Use the factories in `factories.py` for test data
3. **Mock external services** - Google OAuth is mocked in tests
4. **Test edge cases** - Include tests for error conditions
5. **Descriptive names** - Test names should describe what they test
6. **Follow AAA pattern** - Arrange, Act, Assert
