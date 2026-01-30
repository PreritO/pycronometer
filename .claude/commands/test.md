# /test - Run Test Suite

Run the test suite and report results.

## Instructions

1. Run pytest with coverage
2. Report any failures clearly
3. Suggest fixes for failing tests

## Commands

```bash
# Run all tests with coverage
uv run pytest --cov=pycronometer --cov-report=term-missing -v

# Run specific test file
uv run pytest tests/test_client.py -v

# Run tests matching pattern
uv run pytest -k "test_login" -v

# Run with verbose output for debugging
uv run pytest -vvs
```

## Usage

```
/test              # Run all tests
/test client       # Run tests/test_client.py
/test -k login     # Run tests matching "login"
```
