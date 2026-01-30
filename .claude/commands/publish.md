# /publish - Build and Publish to PyPI

Build the package and publish to PyPI.

## Pre-flight Checks

Before publishing:
1. All tests pass
2. Linting passes
3. Type checks pass
4. Version bumped in pyproject.toml
5. CHANGELOG updated
6. Git tag created

## Commands

```bash
# Build the package
uv build

# Check the build
ls -la dist/

# Test upload to TestPyPI first
uv publish --publish-url https://test.pypi.org/legacy/

# Publish to PyPI
uv publish
```

## Version Bumping

Update version in `pyproject.toml`:
```toml
version = "0.1.0"  # Change this
```

## Git Tagging

```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## Usage

```
/publish           # Full publish workflow
/publish --test    # Publish to TestPyPI only
/publish --build   # Build only, don't publish
```
