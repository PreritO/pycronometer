"""CSV parsers for Cronometer export data."""

import csv
from datetime import date, datetime
from io import StringIO
from typing import Any

from pycronometer.models import (
    BiometricEntry,
    DailyNutrition,
    Exercise,
    Note,
    Serving,
)


def _parse_float(value: str, default: float = 0.0) -> float:
    """Safely parse a float from string."""
    if not value or value.strip() == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _parse_datetime(date_str: str, time_str: str = "") -> datetime:
    """Parse date and optional time into datetime.

    Handles formats:
    - Date only: "2024-01-15"
    - Date + time: "2024-01-15" + "08:30"
    """
    if time_str:
        try:
            return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            pass
    return datetime.strptime(date_str, "%Y-%m-%d")


def _parse_date(date_str: str) -> date:
    """Parse date string into date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def parse_servings(csv_text: str) -> list[Serving]:
    """Parse servings export CSV into Serving objects.

    Args:
        csv_text: Raw CSV text from Cronometer servings export

    Returns:
        List of Serving objects
    """
    reader = csv.DictReader(StringIO(csv_text))
    servings = []

    for row in reader:
        raw_data: dict[str, Any] = dict(row)

        # Handle various date/time column names Cronometer might use
        date_str = row.get("Day") or row.get("Date") or row.get("date", "")
        time_str = row.get("Time") or row.get("time", "")

        serving = Serving(
            logged_at=_parse_datetime(date_str, time_str),
            food_name=row.get("Food Name") or row.get("Name") or "",
            serving_size=row.get("Amount") or row.get("Serving") or "",
            calories=_parse_float(row.get("Energy (kcal)") or row.get("Calories", "")),
            protein_g=_parse_float(row.get("Protein (g)") or row.get("Protein", "")),
            carbs_g=_parse_float(row.get("Carbs (g)") or row.get("Carbohydrates", "")),
            fat_g=_parse_float(row.get("Fat (g)") or row.get("Fat", "")),
            fiber_g=_parse_float(row.get("Fiber (g)") or row.get("Fiber", "")),
            sugar_g=_parse_float(row.get("Sugars (g)") or row.get("Sugar", "")),
            sodium_mg=_parse_float(row.get("Sodium (mg)") or row.get("Sodium", "")),
            cholesterol_mg=_parse_float(row.get("Cholesterol (mg)", "")),
            saturated_fat_g=_parse_float(row.get("Saturated (g)", "")),
            group=row.get("Food Group") or row.get("Group"),
            raw_data=raw_data,
        )
        servings.append(serving)

    return servings


def parse_biometrics(csv_text: str) -> list[BiometricEntry]:
    """Parse biometrics export CSV into BiometricEntry objects.

    Args:
        csv_text: Raw CSV text from Cronometer biometrics export

    Returns:
        List of BiometricEntry objects
    """
    reader = csv.DictReader(StringIO(csv_text))
    entries = []

    for row in reader:
        raw_data: dict[str, Any] = dict(row)

        date_str = row.get("Day") or row.get("Date") or row.get("date", "")
        time_str = row.get("Time") or row.get("time", "")

        entry = BiometricEntry(
            logged_at=_parse_datetime(date_str, time_str),
            metric=row.get("Metric") or row.get("Name") or row.get("Type") or "",
            value=_parse_float(row.get("Amount") or row.get("Value", "")),
            unit=row.get("Unit") or "",
            raw_data=raw_data,
        )
        entries.append(entry)

    return entries


def parse_notes(csv_text: str) -> list[Note]:
    """Parse notes export CSV into Note objects.

    Args:
        csv_text: Raw CSV text from Cronometer notes export

    Returns:
        List of Note objects
    """
    reader = csv.DictReader(StringIO(csv_text))
    notes = []

    for row in reader:
        raw_data: dict[str, Any] = dict(row)

        date_str = row.get("Day") or row.get("Date") or row.get("date", "")
        time_str = row.get("Time") or row.get("time", "")

        note = Note(
            logged_at=_parse_datetime(date_str, time_str),
            content=row.get("Note") or row.get("Content") or row.get("Text") or "",
            raw_data=raw_data,
        )
        notes.append(note)

    return notes


def parse_daily_nutrition(csv_text: str) -> list[DailyNutrition]:
    """Parse daily nutrition summary CSV into DailyNutrition objects.

    Args:
        csv_text: Raw CSV text from Cronometer daily summary export

    Returns:
        List of DailyNutrition objects
    """
    reader = csv.DictReader(StringIO(csv_text))
    summaries = []

    for row in reader:
        raw_data: dict[str, Any] = dict(row)

        date_str = row.get("Day") or row.get("Date") or row.get("date", "")

        summary = DailyNutrition(
            date=_parse_date(date_str),
            calories=_parse_float(row.get("Energy (kcal)") or row.get("Calories", "")),
            protein_g=_parse_float(row.get("Protein (g)") or row.get("Protein", "")),
            carbs_g=_parse_float(row.get("Carbs (g)") or row.get("Carbohydrates", "")),
            fat_g=_parse_float(row.get("Fat (g)") or row.get("Fat", "")),
            fiber_g=_parse_float(row.get("Fiber (g)") or row.get("Fiber", "")),
            sugar_g=_parse_float(row.get("Sugars (g)") or row.get("Sugar", "")),
            sodium_mg=_parse_float(row.get("Sodium (mg)") or row.get("Sodium", "")),
            raw_data=raw_data,
        )
        summaries.append(summary)

    return summaries


def parse_exercises(csv_text: str) -> list[Exercise]:
    """Parse exercises export CSV into Exercise objects.

    Args:
        csv_text: Raw CSV text from Cronometer exercises export

    Returns:
        List of Exercise objects
    """
    reader = csv.DictReader(StringIO(csv_text))
    exercises = []

    for row in reader:
        raw_data: dict[str, Any] = dict(row)

        date_str = row.get("Day") or row.get("Date") or row.get("date", "")
        time_str = row.get("Time") or row.get("time", "")

        exercise = Exercise(
            logged_at=_parse_datetime(date_str, time_str),
            name=row.get("Exercise") or row.get("Name") or "",
            duration_minutes=_parse_float(row.get("Minutes") or row.get("Duration", "")),
            calories_burned=_parse_float(row.get("Calories Burned") or row.get("Calories", "")),
            raw_data=raw_data,
        )
        exercises.append(exercise)

    return exercises
