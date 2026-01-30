"""Custom exceptions for pycronometer."""


class CronometerError(Exception):
    """Base exception for all pycronometer errors."""

    pass


class CronometerAuthError(CronometerError):
    """Raised when authentication fails."""

    pass


class GWTVersionError(CronometerError):
    """Raised when GWT magic values are outdated or responses are malformed.

    This typically means Cronometer has updated their app and the GWT
    permutation/header values need to be updated.
    """

    pass


class ExportError(CronometerError):
    """Raised when data export fails."""

    pass
