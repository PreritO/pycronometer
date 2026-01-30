# pycronometer

A Python client library for accessing [Cronometer](https://cronometer.com) personal nutrition data exports.

> **Note**: This is an unofficial client for personal data backup. It is not affiliated with Cronometer. Use responsibly.

## Installation

```bash
pip install pycronometer
```

Or install from source:

```bash
pip install git+https://github.com/yourusername/pycronometer.git
```

## Quick Start

```python
from pycronometer import CronometerClient
from datetime import date

# Initialize and login
client = CronometerClient()
client.login("your-email@example.com", "your-password")

# Get food servings for a date range
servings = client.get_servings(
    start=date(2024, 1, 1),
    end=date(2024, 1, 31)
)

for serving in servings:
    print(f"{serving.logged_at}: {serving.food_name} - {serving.calories} kcal")
```

## Features

- **Authentication**: Handle Cronometer login with CSRF and GWT protocol
- **Data Exports**: Retrieve servings, biometrics, notes, exercises, and daily nutrition
- **Typed Models**: All data returned as Python dataclasses with proper types
- **Configurable**: Override GWT magic values when Cronometer updates

## API Reference

### CronometerClient

```python
from pycronometer import CronometerClient

# Basic initialization
client = CronometerClient()

# With GWT value overrides (when defaults break)
client = CronometerClient(
    gwt_permutation="NEW_HASH",
    gwt_header="NEW_HEADER"
)
```

### Authentication

```python
client.login("email@example.com", "password")
```

Raises `CronometerAuthError` on invalid credentials.

### Export Methods

All export methods accept `start` and `end` as `date` objects.

```python
from datetime import date

start = date(2024, 1, 1)
end = date(2024, 1, 31)

# Food servings
servings = client.get_servings(start, end)

# Daily nutrition summaries
daily = client.get_daily_nutrition(start, end)

# Biometric measurements
biometrics = client.get_biometrics(start, end)

# Notes
notes = client.get_notes(start, end)

# Exercises
exercises = client.get_exercises(start, end)

# Raw CSV (for any export type)
raw_csv = client.get_servings_raw(start, end)
```

### Data Models

#### Serving
```python
@dataclass
class Serving:
    logged_at: datetime
    food_name: str
    serving_size: str
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    sugar_g: float
    sodium_mg: float
    # ... more nutrients
    raw_data: dict  # Original CSV row
```

#### BiometricEntry
```python
@dataclass
class BiometricEntry:
    logged_at: datetime
    metric: str      # "Weight", "Body Fat", etc.
    value: float
    unit: str
    raw_data: dict
```

#### Note
```python
@dataclass
class Note:
    logged_at: datetime
    content: str
    raw_data: dict
```

### Error Handling

```python
from pycronometer import CronometerClient
from pycronometer.exceptions import (
    CronometerAuthError,
    GWTVersionError,
    ExportError
)

try:
    client.login(email, password)
except CronometerAuthError as e:
    print(f"Login failed: {e}")

try:
    servings = client.get_servings(start, end)
except GWTVersionError as e:
    print(f"GWT values outdated: {e}")
except ExportError as e:
    print(f"Export failed: {e}")
```

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CRONOMETER_GWT_PERMUTATION` | Override GWT permutation hash |
| `CRONOMETER_GWT_HEADER` | Override GWT header hash |

### Updating GWT Values

When Cronometer updates their app, the GWT magic values may change. To find new values:

1. Open Cronometer in your browser
2. Open DevTools (F12) → Network tab
3. Perform any action (like viewing your diary)
4. Find a request to `cronometer/app`
5. Copy the `x-gwt-permutation` header value
6. In the request body, find the hash after the URL (pipe-delimited string)

Then either:
- Set environment variables
- Pass values to `CronometerClient()` constructor
- Submit a PR to update the defaults

## Development

```bash
# Clone the repo
git clone https://github.com/yourusername/pycronometer.git
cd pycronometer

# Install with dev dependencies
uv sync --dev

# Run tests
uv run pytest

# Run linter
uv run ruff check src tests

# Run type checker
uv run mypy src
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Disclaimer

This is an unofficial client intended only for personal data backup. It is not affiliated with or endorsed by Cronometer. Please respect Cronometer's terms of service and do not use this for scraping or commercial purposes.

## Credits

Inspired by [gocronometer](https://github.com/jrmycanady/gocronometer), the Go implementation.
