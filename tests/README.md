# Running Tests Locally

## Prerequisites

Install dependencies:

```bash
pip install Django djangorestframework pytest pytest-django
```

Or install from project:

```bash
pip install -e ".[dev]"
```

## Run Tests

### Run all tests:

```bash
pytest tests/ -v
```

### Run specific test file:

```bash
pytest tests/test_core.py -v
```

### Run specific test:

```bash
pytest tests/test_core.py::CoreTestCase::test_get_serializer_fields -v
```

### Run with coverage:

```bash
pytest tests/ -v --cov=autoapi_swagger --cov-report=html
```

## Test Structure

- `tests/settings.py` - Minimal Django settings for tests
- `tests/conftest.py` - Django setup for pytest
- `tests/urls.py` - URL configuration for tests
- `tests/test_core.py` - Core functionality tests
