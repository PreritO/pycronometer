"""Authentication module for Cronometer.

Handles the multi-step authentication flow:
1. Fetch login page and extract CSRF token
2. POST login with credentials
3. Authenticate with GWT API
4. Generate auth tokens for exports
"""

import requests
from bs4 import BeautifulSoup, Tag

from pycronometer.exceptions import CronometerAuthError, GWTVersionError
from pycronometer.gwt import (
    GWTConfig,
    build_authenticate_body,
    build_generate_token_body,
    build_gwt_headers,
    parse_auth_token,
    parse_user_id,
)

# Cronometer URLs
LOGIN_PAGE_URL = "https://cronometer.com/login/"
LOGIN_API_URL = "https://cronometer.com/login"
GWT_API_URL = "https://cronometer.com/cronometer/app"
EXPORT_URL = "https://cronometer.com/export"


def extract_csrf_token(session: requests.Session) -> str:
    """Fetch login page and extract CSRF token.

    Args:
        session: Requests session to use

    Returns:
        CSRF token string

    Raises:
        CronometerAuthError: If CSRF token cannot be found
    """
    response = session.get(LOGIN_PAGE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    csrf_input = soup.find("input", {"name": "anticsrf"})

    if not isinstance(csrf_input, Tag):
        raise CronometerAuthError("Could not find CSRF token in login page")

    csrf_value = csrf_input.get("value")
    if not csrf_value or not isinstance(csrf_value, str):
        raise CronometerAuthError("CSRF token value is missing or invalid")

    return csrf_value


def perform_login(
    session: requests.Session,
    email: str,
    password: str,
    csrf_token: str,
) -> None:
    """Perform login POST request.

    Args:
        session: Requests session to use
        email: Cronometer email
        password: Cronometer password
        csrf_token: CSRF token from login page

    Raises:
        CronometerAuthError: If login fails
    """
    response = session.post(
        LOGIN_API_URL,
        data={
            "username": email,
            "password": password,
            "anticsrf": csrf_token,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()

    data = response.json()
    if not data.get("success"):
        error_msg = data.get("error", "Unknown login error")
        raise CronometerAuthError(f"Login failed: {error_msg}")


def authenticate_gwt(session: requests.Session, config: GWTConfig) -> str:
    """Authenticate with GWT API and get user ID.

    Args:
        session: Requests session (must have sesnonce cookie from login)
        config: GWT configuration

    Returns:
        User ID string

    Raises:
        GWTVersionError: If GWT response cannot be parsed
    """
    response = session.post(
        GWT_API_URL,
        data=build_authenticate_body(config),
        headers=build_gwt_headers(config),
    )
    response.raise_for_status()

    user_id = parse_user_id(response.text)
    if not user_id:
        raise GWTVersionError(
            "Could not parse user ID from GWT response. "
            "GWT values may be outdated. "
            f"Response: {response.text[:200]}"
        )

    return user_id


def generate_export_token(
    session: requests.Session,
    config: GWTConfig,
    nonce: str,
    user_id: str,
) -> str:
    """Generate auth token for export API.

    Args:
        session: Requests session
        config: GWT configuration
        nonce: Session nonce from cookies
        user_id: User ID from GWT authentication

    Returns:
        Auth token for export API

    Raises:
        GWTVersionError: If token cannot be parsed from response
    """
    response = session.post(
        GWT_API_URL,
        data=build_generate_token_body(config, nonce, user_id),
        headers=build_gwt_headers(config),
    )
    response.raise_for_status()

    token = parse_auth_token(response.text)
    if not token:
        raise GWTVersionError(
            "Could not parse auth token from GWT response. "
            "GWT values may be outdated. "
            f"Response: {response.text[:200]}"
        )

    return token


def get_session_nonce(session: requests.Session) -> str | None:
    """Get sesnonce cookie value from session.

    Args:
        session: Requests session

    Returns:
        Nonce value or None if not set
    """
    return session.cookies.get("sesnonce")
