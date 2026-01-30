"""Export functions for fetching data from Cronometer."""

from datetime import date

import requests

from pycronometer.exceptions import ExportError

EXPORT_URL = "https://cronometer.com/export"


def _fetch_export(
    session: requests.Session,
    token: str,
    generate_type: str,
    start: date,
    end: date,
) -> str:
    """Fetch export data from Cronometer API.

    Args:
        session: Authenticated requests session
        token: Auth token from GWT generateAuthorizationToken
        generate_type: Export type (servings, dailySummary, biometrics, notes, exercises)
        start: Start date for export
        end: End date for export

    Returns:
        Raw CSV text

    Raises:
        ExportError: If export request fails
    """
    response = session.get(
        EXPORT_URL,
        params={
            "nonce": token,
            "generate": generate_type,
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d"),
        },
        headers={
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
        },
    )

    if response.status_code != 200:
        raise ExportError(
            f"Export failed with status {response.status_code}: {response.text[:200]}"
        )

    return response.text


def export_servings(
    session: requests.Session,
    token: str,
    start: date,
    end: date,
) -> str:
    """Export food servings data.

    Args:
        session: Authenticated requests session
        token: Auth token
        start: Start date
        end: End date

    Returns:
        Raw CSV text
    """
    return _fetch_export(session, token, "servings", start, end)


def export_daily_nutrition(
    session: requests.Session,
    token: str,
    start: date,
    end: date,
) -> str:
    """Export daily nutrition summary data.

    Args:
        session: Authenticated requests session
        token: Auth token
        start: Start date
        end: End date

    Returns:
        Raw CSV text
    """
    return _fetch_export(session, token, "dailySummary", start, end)


def export_biometrics(
    session: requests.Session,
    token: str,
    start: date,
    end: date,
) -> str:
    """Export biometrics data.

    Args:
        session: Authenticated requests session
        token: Auth token
        start: Start date
        end: End date

    Returns:
        Raw CSV text
    """
    return _fetch_export(session, token, "biometrics", start, end)


def export_notes(
    session: requests.Session,
    token: str,
    start: date,
    end: date,
) -> str:
    """Export notes data.

    Args:
        session: Authenticated requests session
        token: Auth token
        start: Start date
        end: End date

    Returns:
        Raw CSV text
    """
    return _fetch_export(session, token, "notes", start, end)


def export_exercises(
    session: requests.Session,
    token: str,
    start: date,
    end: date,
) -> str:
    """Export exercises data.

    Args:
        session: Authenticated requests session
        token: Auth token
        start: Start date
        end: End date

    Returns:
        Raw CSV text
    """
    return _fetch_export(session, token, "exercises", start, end)
