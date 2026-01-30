"""
pycronometer - Python client for Cronometer personal nutrition data exports.

Example usage:
    from pycronometer import CronometerClient
    from datetime import date

    client = CronometerClient()
    client.login("email@example.com", "password")
    servings = client.get_servings(date(2024, 1, 1), date(2024, 1, 31))
"""

from pycronometer.client import CronometerClient
from pycronometer.exceptions import (
    CronometerAuthError,
    CronometerError,
    ExportError,
    GWTVersionError,
)
from pycronometer.models import (
    BiometricEntry,
    DailyNutrition,
    Exercise,
    Note,
    Serving,
)

__version__ = "0.1.0"

__all__ = [
    # Client
    "CronometerClient",
    # Exceptions
    "CronometerError",
    "CronometerAuthError",
    "ExportError",
    "GWTVersionError",
    # Models
    "BiometricEntry",
    "DailyNutrition",
    "Exercise",
    "Note",
    "Serving",
]
