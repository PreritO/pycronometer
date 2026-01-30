"""Tests for exception classes."""

from pycronometer.exceptions import (
    CronometerAuthError,
    CronometerError,
    ExportError,
    GWTVersionError,
)


class TestExceptions:
    """Tests for exception hierarchy."""

    def test_auth_error_inherits_from_base(self) -> None:
        """Test CronometerAuthError inherits from CronometerError."""
        error = CronometerAuthError("test")
        assert isinstance(error, CronometerError)
        assert isinstance(error, Exception)

    def test_gwt_version_error_inherits_from_base(self) -> None:
        """Test GWTVersionError inherits from CronometerError."""
        error = GWTVersionError("test")
        assert isinstance(error, CronometerError)

    def test_export_error_inherits_from_base(self) -> None:
        """Test ExportError inherits from CronometerError."""
        error = ExportError("test")
        assert isinstance(error, CronometerError)

    def test_exception_message(self) -> None:
        """Test that exception messages are preserved."""
        message = "Login failed: invalid password"
        error = CronometerAuthError(message)
        assert str(error) == message
