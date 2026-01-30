"""Tests for CSV parsers."""

from datetime import date, datetime

from pycronometer.parsers import (
    parse_biometrics,
    parse_daily_nutrition,
    parse_exercises,
    parse_notes,
    parse_servings,
)


class TestParseServings:
    """Tests for parse_servings."""

    def test_parses_servings_correctly(self, servings_csv: str) -> None:
        """Test that servings are parsed with correct values."""
        servings = parse_servings(servings_csv)

        assert len(servings) == 6

        # Check first serving (Oatmeal)
        oatmeal = servings[0]
        assert oatmeal.food_name == "Oatmeal"
        assert oatmeal.logged_at == datetime(2024, 1, 15, 8, 30)
        assert oatmeal.serving_size == "1 cup"
        assert oatmeal.calories == 150.0
        assert oatmeal.protein_g == 5.0
        assert oatmeal.carbs_g == 27.0
        assert oatmeal.fat_g == 3.0
        assert oatmeal.fiber_g == 4.0
        assert oatmeal.group == "Grains"

    def test_preserves_raw_data(self, servings_csv: str) -> None:
        """Test that raw CSV data is preserved."""
        servings = parse_servings(servings_csv)
        assert "Energy (kcal)" in servings[0].raw_data


class TestParseBiometrics:
    """Tests for parse_biometrics."""

    def test_parses_biometrics_correctly(self, biometrics_csv: str) -> None:
        """Test that biometrics are parsed with correct values."""
        entries = parse_biometrics(biometrics_csv)

        assert len(entries) == 5

        weight = entries[0]
        assert weight.metric == "Weight"
        assert weight.value == 175.5
        assert weight.unit == "lb"
        assert weight.logged_at == datetime(2024, 1, 15, 7, 0)


class TestParseNotes:
    """Tests for parse_notes."""

    def test_parses_notes_correctly(self, notes_csv: str) -> None:
        """Test that notes are parsed with correct values."""
        notes = parse_notes(notes_csv)

        assert len(notes) == 4

        first_note = notes[0]
        assert "BM: Type 4" in first_note.content
        assert first_note.logged_at == datetime(2024, 1, 15, 8, 0)


class TestParseDailyNutrition:
    """Tests for parse_daily_nutrition."""

    def test_parses_daily_nutrition_correctly(self, daily_nutrition_csv: str) -> None:
        """Test that daily nutrition is parsed with correct values."""
        summaries = parse_daily_nutrition(daily_nutrition_csv)

        assert len(summaries) == 3

        day1 = summaries[0]
        assert day1.date == date(2024, 1, 15)
        assert day1.calories == 2145.0
        assert day1.protein_g == 84.0


class TestParseExercises:
    """Tests for parse_exercises."""

    def test_parses_exercises_correctly(self, exercises_csv: str) -> None:
        """Test that exercises are parsed with correct values."""
        exercises = parse_exercises(exercises_csv)

        assert len(exercises) == 4

        running = exercises[0]
        assert running.name == "Running"
        assert running.duration_minutes == 30.0
        assert running.calories_burned == 350.0
