"""Main client class for Cronometer API."""

from datetime import date

import requests

from pycronometer.auth import (
    authenticate_gwt,
    extract_csrf_token,
    generate_export_token,
    get_session_nonce,
    perform_login,
)
from pycronometer.exceptions import CronometerAuthError
from pycronometer.exports import (
    export_biometrics,
    export_daily_nutrition,
    export_exercises,
    export_notes,
    export_servings,
)
from pycronometer.gwt import GWTConfig, get_gwt_config
from pycronometer.models import (
    BiometricEntry,
    DailyNutrition,
    Exercise,
    Note,
    Serving,
)
from pycronometer.parsers import (
    parse_biometrics,
    parse_daily_nutrition,
    parse_exercises,
    parse_notes,
    parse_servings,
)


class CronometerClient:
    """Client for accessing Cronometer personal data exports.

    Example:
        client = CronometerClient()
        client.login("email@example.com", "password")
        servings = client.get_servings(date(2024, 1, 1), date(2024, 1, 31))
    """

    def __init__(
        self,
        gwt_permutation: str | None = None,
        gwt_header: str | None = None,
    ) -> None:
        """Initialize client.

        Args:
            gwt_permutation: Override GWT permutation hash (optional)
            gwt_header: Override GWT header hash (optional)
        """
        self._session = requests.Session()
        self._gwt_config: GWTConfig = get_gwt_config(gwt_permutation, gwt_header)
        self._user_id: str | None = None
        self._nonce: str | None = None

    def login(self, email: str, password: str) -> None:
        """Authenticate with Cronometer.

        Args:
            email: Cronometer account email
            password: Cronometer account password

        Raises:
            CronometerAuthError: If login fails
            GWTVersionError: If GWT authentication fails
        """
        # Step 1: Get CSRF token
        csrf_token = extract_csrf_token(self._session)

        # Step 2: Login with credentials
        perform_login(self._session, email, password, csrf_token)

        # Step 3: Authenticate with GWT
        self._user_id = authenticate_gwt(self._session, self._gwt_config)

        # Store nonce for later use
        self._nonce = get_session_nonce(self._session)

    def _ensure_authenticated(self) -> None:
        """Ensure client is authenticated."""
        if not self._user_id or not self._nonce:
            raise CronometerAuthError("Not authenticated. Call login() first.")

    def _get_export_token(self) -> str:
        """Generate a fresh export token."""
        self._ensure_authenticated()
        assert self._nonce is not None
        assert self._user_id is not None
        return generate_export_token(
            self._session,
            self._gwt_config,
            self._nonce,
            self._user_id,
        )

    # --- Parsed export methods ---

    def get_servings(self, start: date, end: date) -> list[Serving]:
        """Get food servings for date range.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)

        Returns:
            List of Serving objects
        """
        csv_text = self.get_servings_raw(start, end)
        return parse_servings(csv_text)

    def get_daily_nutrition(self, start: date, end: date) -> list[DailyNutrition]:
        """Get daily nutrition summaries for date range.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)

        Returns:
            List of DailyNutrition objects
        """
        csv_text = self.get_daily_nutrition_raw(start, end)
        return parse_daily_nutrition(csv_text)

    def get_biometrics(self, start: date, end: date) -> list[BiometricEntry]:
        """Get biometric entries for date range.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)

        Returns:
            List of BiometricEntry objects
        """
        csv_text = self.get_biometrics_raw(start, end)
        return parse_biometrics(csv_text)

    def get_notes(self, start: date, end: date) -> list[Note]:
        """Get notes for date range.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)

        Returns:
            List of Note objects
        """
        csv_text = self.get_notes_raw(start, end)
        return parse_notes(csv_text)

    def get_exercises(self, start: date, end: date) -> list[Exercise]:
        """Get exercises for date range.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)

        Returns:
            List of Exercise objects
        """
        csv_text = self.get_exercises_raw(start, end)
        return parse_exercises(csv_text)

    # --- Raw export methods ---

    def get_servings_raw(self, start: date, end: date) -> str:
        """Get raw CSV for food servings.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)

        Returns:
            Raw CSV text
        """
        token = self._get_export_token()
        return export_servings(self._session, token, start, end)

    def get_daily_nutrition_raw(self, start: date, end: date) -> str:
        """Get raw CSV for daily nutrition summaries.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)

        Returns:
            Raw CSV text
        """
        token = self._get_export_token()
        return export_daily_nutrition(self._session, token, start, end)

    def get_biometrics_raw(self, start: date, end: date) -> str:
        """Get raw CSV for biometrics.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)

        Returns:
            Raw CSV text
        """
        token = self._get_export_token()
        return export_biometrics(self._session, token, start, end)

    def get_notes_raw(self, start: date, end: date) -> str:
        """Get raw CSV for notes.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)

        Returns:
            Raw CSV text
        """
        token = self._get_export_token()
        return export_notes(self._session, token, start, end)

    def get_exercises_raw(self, start: date, end: date) -> str:
        """Get raw CSV for exercises.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)

        Returns:
            Raw CSV text
        """
        token = self._get_export_token()
        return export_exercises(self._session, token, start, end)
