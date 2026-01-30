# /lint - Run Linting and Type Checks

Run code quality checks.

## Instructions

1. Run ruff for linting
2. Run ruff for formatting
3. Run mypy for type checking
4. Report issues and offer to fix

## Commands

```bash
# Check linting
uv run ruff check src tests

# Fix auto-fixable issues
uv run ruff check --fix src tests

# Check formatting
uv run ruff format --check src tests

# Apply formatting
uv run ruff format src tests

# Type checking
uv run mypy src
```

## Usage

```
/lint           # Check all
/lint --fix     # Auto-fix issues
```
