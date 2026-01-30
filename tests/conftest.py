"""Pytest configuration and fixtures."""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def servings_csv() -> str:
    """Load sample servings CSV."""
    return (FIXTURES_DIR / "servings.csv").read_text()


@pytest.fixture
def biometrics_csv() -> str:
    """Load sample biometrics CSV."""
    return (FIXTURES_DIR / "biometrics.csv").read_text()


@pytest.fixture
def notes_csv() -> str:
    """Load sample notes CSV."""
    return (FIXTURES_DIR / "notes.csv").read_text()


@pytest.fixture
def daily_nutrition_csv() -> str:
    """Load sample daily nutrition CSV."""
    return (FIXTURES_DIR / "daily_nutrition.csv").read_text()


@pytest.fixture
def exercises_csv() -> str:
    """Load sample exercises CSV."""
    return (FIXTURES_DIR / "exercises.csv").read_text()
