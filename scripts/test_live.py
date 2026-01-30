#!/usr/bin/env python3
"""
Live test script for pycronometer.

Usage:
    1. Copy .env.example to .env and fill in your Cronometer credentials
    2. Run: python scripts/test_live.py

This script will:
    - Login to Cronometer
    - Fetch the last 7 days of data
    - Print summaries of what was retrieved
"""

import os
import sys
from datetime import date, timedelta
from pathlib import Path

# Load .env file
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()

from pycronometer import CronometerClient
from pycronometer.exceptions import CronometerAuthError, GWTVersionError, ExportError


def main() -> int:
    email = os.environ.get("CRONOMETER_EMAIL")
    password = os.environ.get("CRONOMETER_PASSWORD")

    if not email or not password:
        print("Error: CRONOMETER_EMAIL and CRONOMETER_PASSWORD must be set")
        print("Create a .env file with your credentials (see .env.example)")
        return 1

    # Date range: last 7 days
    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    print(f"Testing pycronometer")
    print(f"Date range: {start_date} to {end_date}")
    print("-" * 50)

    client = CronometerClient()

    # Login
    print(f"\n1. Logging in as {email}...")
    try:
        client.login(email, password)
        print("   ✓ Login successful!")
    except CronometerAuthError as e:
        print(f"   ✗ Login failed: {e}")
        return 1
    except GWTVersionError as e:
        print(f"   ✗ GWT authentication failed (values may be outdated): {e}")
        return 1

    # Test each export type
    print("\n2. Fetching servings...")
    try:
        servings = client.get_servings(start_date, end_date)
        print(f"   ✓ Retrieved {len(servings)} servings")
        if servings:
            print(f"   Sample: {servings[0].food_name} - {servings[0].calories} kcal")
    except ExportError as e:
        print(f"   ✗ Failed: {e}")

    print("\n3. Fetching daily nutrition...")
    try:
        daily = client.get_daily_nutrition(start_date, end_date)
        print(f"   ✓ Retrieved {len(daily)} daily summaries")
        if daily:
            print(f"   Sample: {daily[0].date} - {daily[0].calories} kcal")
    except ExportError as e:
        print(f"   ✗ Failed: {e}")

    print("\n4. Fetching biometrics...")
    try:
        biometrics = client.get_biometrics(start_date, end_date)
        print(f"   ✓ Retrieved {len(biometrics)} biometric entries")
        if biometrics:
            print(f"   Sample: {biometrics[0].metric} = {biometrics[0].value} {biometrics[0].unit}")
    except ExportError as e:
        print(f"   ✗ Failed: {e}")

    print("\n5. Fetching notes...")
    try:
        notes = client.get_notes(start_date, end_date)
        print(f"   ✓ Retrieved {len(notes)} notes")
        if notes:
            preview = notes[0].content[:50] + "..." if len(notes[0].content) > 50 else notes[0].content
            print(f"   Sample: {preview}")
    except ExportError as e:
        print(f"   ✗ Failed: {e}")

    print("\n6. Fetching exercises...")
    try:
        exercises = client.get_exercises(start_date, end_date)
        print(f"   ✓ Retrieved {len(exercises)} exercises")
        if exercises:
            print(f"   Sample: {exercises[0].name} - {exercises[0].duration_minutes} min")
    except ExportError as e:
        print(f"   ✗ Failed: {e}")

    print("\n" + "-" * 50)
    print("Test complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
