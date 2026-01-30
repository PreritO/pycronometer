"""Data models for Cronometer exports."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any


@dataclass
class Serving:
    """A single food serving entry from Cronometer."""

    logged_at: datetime
    food_name: str
    serving_size: str
    calories: float = 0.0
    protein_g: float = 0.0
    carbs_g: float = 0.0
    fat_g: float = 0.0
    fiber_g: float = 0.0
    sugar_g: float = 0.0
    sodium_mg: float = 0.0
    cholesterol_mg: float = 0.0
    saturated_fat_g: float = 0.0
    # Additional fields can be accessed via raw_data
    group: str | None = None
    raw_data: dict[str, Any] = field(default_factory=dict)


@dataclass
class BiometricEntry:
    """A biometric measurement entry from Cronometer."""

    logged_at: datetime
    metric: str  # e.g., "Weight", "Body Fat", "Blood Pressure"
    value: float
    unit: str
    raw_data: dict[str, Any] = field(default_factory=dict)


@dataclass
class Note:
    """A note entry from Cronometer."""

    logged_at: datetime
    content: str
    raw_data: dict[str, Any] = field(default_factory=dict)


@dataclass
class DailyNutrition:
    """Daily nutrition summary from Cronometer."""

    date: date
    calories: float = 0.0
    protein_g: float = 0.0
    carbs_g: float = 0.0
    fat_g: float = 0.0
    fiber_g: float = 0.0
    sugar_g: float = 0.0
    sodium_mg: float = 0.0
    # Additional nutrients can be accessed via raw_data
    raw_data: dict[str, Any] = field(default_factory=dict)


@dataclass
class Exercise:
    """An exercise entry from Cronometer."""

    logged_at: datetime
    name: str
    duration_minutes: float = 0.0
    calories_burned: float = 0.0
    raw_data: dict[str, Any] = field(default_factory=dict)
