# Running Tests Locally

## Prerequisites

Install dependencies:

```bash
pip install pytest
```

Or install from project:

```bash
pip install -e ".[dev]"
```

## Run Tests

### Run all tests:

```bash
python -m pytest tests/ -v
```

### Run specific test file:

```bash
python -m pytest tests/test_core.py -v
```

### Run specific test:

```bash
python -m pytest tests/test_core.py::ConstantsTestCase::test_openapi_version -v
```

### Run with coverage:

```bash
python -m pytest tests/ -v --cov=autoapi_swagger --cov-report=html
```

## Test Structure

- `tests/test_core.py` - Pure Python unit tests (no Django/DRF dependencies)

## Note

These tests are pure Python unit tests that don't require Django or DRF to be configured. They test:

- Constants and configuration values
- Response building functions (with mocks)
- Pure Python logic
