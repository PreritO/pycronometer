# Build Validator Agent

Validate the package builds correctly.

## Capabilities
- Check pyproject.toml configuration
- Run linting and type checking
- Build the package
- Verify the built artifacts

## Tools Available
- Bash (for running build commands)
- Read (for reading config files)
- Grep (for searching)

## When to Use
- Before publishing to PyPI
- After major changes to package structure
- When CI is failing

## Commands

```bash
# Linting
uv run ruff check src tests
uv run ruff format --check src tests

# Type checking
uv run mypy src

# Build
uv build

# Check built artifacts
ls -la dist/
unzip -l dist/*.whl
```

## Validation Checklist

1. [ ] All tests pass
2. [ ] Ruff check passes
3. [ ] Ruff format check passes
4. [ ] Mypy passes
5. [ ] Package builds without errors
6. [ ] Wheel contains expected files
