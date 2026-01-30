# Test Runner Agent

Run tests and help fix failures.

## Capabilities
- Run pytest with various options
- Analyze test failures
- Suggest fixes for failing tests
- Check code coverage

## Tools Available
- Bash (for running pytest, ruff, mypy)
- Read (for reading test files and source code)
- Grep (for searching code)
- Glob (for finding files)

## When to Use
- After implementing new features
- When tests are failing
- To check coverage before commits

## Commands

```bash
# Run all tests
uv run pytest -v

# Run with coverage
uv run pytest --cov=pycronometer --cov-report=term-missing

# Run specific test
uv run pytest tests/test_client.py -v

# Run tests matching pattern
uv run pytest -k "test_login" -v

# Verbose output for debugging
uv run pytest -vvs
```
