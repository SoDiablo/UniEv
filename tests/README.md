# UniEv Test Suite

This directory contains the pytest test suite for the UniEv application.

## Setup

1. Install pytest and dependencies:
```bash
pip install pytest pytest-cov
```

2. Make sure you're in the `uniev` directory:
```bash
cd uniev
```

## Running Tests

### Run all tests:
```bash
pytest tests/
```

### Run specific test file:
```bash
pytest tests/test_auth.py
pytest tests/test_fraud.py
```

### Run with coverage report:
```bash
pytest tests/ --cov=. --cov-report=html
```

### Run with verbose output:
```bash
pytest tests/ -v
```

### Run specific test class:
```bash
pytest tests/test_auth.py::TestRegistration
```

### Run specific test function:
```bash
pytest tests/test_auth.py::TestRegistration::test_register_valid_data
```

## Test Files

- `conftest.py` - Shared fixtures and test configuration
- `test_auth.py` - Authentication tests (registration, login, lockout)
- `test_fraud.py` - FraudScore calculation tests
- `test_listings.py` - Listing CRUD tests (TODO)
- `test_match.py` - Match Engine tests (TODO)
- `test_reports.py` - Report management tests (TODO)
- `test_kvkk.py` - KVKK/privacy tests (TODO)
- `test_ratings.py` - Rating system tests (TODO)

## Test Coverage

Current test coverage:
- ✅ Authentication (registration, login, lockout, password reset)
- ✅ FraudScore (all 7 factors + edge cases)
- ⏳ Listings (TODO)
- ⏳ Match Engine (TODO)
- ⏳ Reports (TODO)
- ⏳ KVKK (TODO)
- ⏳ Ratings (TODO)

## Writing New Tests

1. Create a new test file in `tests/` directory
2. Import necessary fixtures from `conftest.py`
3. Use `client` fixture for API testing
4. Use `db_session` fixture for database testing
5. Use `sample_student`, `sample_landlord`, `sample_admin` for user fixtures
6. Use `auth_headers_*` fixtures for authenticated requests

Example:
```python
def test_my_feature(client, auth_headers_student):
    response = client.get("/api/my-endpoint", headers=auth_headers_student)
    assert response.status_code == 200
```

## Notes

- Tests use an in-memory SQLite database
- Each test gets a fresh database (function scope)
- Tests are independent and can run in any order
- Mock data is created using fixtures
