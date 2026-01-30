"""GWT protocol utilities for communicating with Cronometer.

Cronometer uses Google Web Toolkit (GWT) for its API. This module handles
the protocol details including headers, request body formatting, and
response parsing.
"""

import os
import re
from typing import NamedTuple

# Default GWT values - these may change when Cronometer updates their app
DEFAULT_GWT_CONTENT_TYPE = "text/x-gwt-rpc; charset=UTF-8"
DEFAULT_GWT_MODULE_BASE = "https://cronometer.com/cronometer/"
DEFAULT_GWT_PERMUTATION = "7B121DC5483BF272B1BC1916DA9FA963"
DEFAULT_GWT_HEADER = "2D6A926E3729946302DC68073CB0D550"

# Environment variable names for overrides
ENV_GWT_PERMUTATION = "CRONOMETER_GWT_PERMUTATION"
ENV_GWT_HEADER = "CRONOMETER_GWT_HEADER"


class GWTConfig(NamedTuple):
    """Configuration for GWT requests."""

    content_type: str
    module_base: str
    permutation: str
    header: str


def get_gwt_config(
    permutation: str | None = None,
    header: str | None = None,
) -> GWTConfig:
    """Get GWT configuration, checking env vars for overrides.

    Args:
        permutation: GWT permutation hash (overrides env var and default)
        header: GWT header hash (overrides env var and default)

    Returns:
        GWTConfig with resolved values
    """
    return GWTConfig(
        content_type=DEFAULT_GWT_CONTENT_TYPE,
        module_base=DEFAULT_GWT_MODULE_BASE,
        permutation=permutation or os.environ.get(ENV_GWT_PERMUTATION, DEFAULT_GWT_PERMUTATION),
        header=header or os.environ.get(ENV_GWT_HEADER, DEFAULT_GWT_HEADER),
    )


def build_gwt_headers(config: GWTConfig) -> dict[str, str]:
    """Build HTTP headers for a GWT request.

    Args:
        config: GWT configuration

    Returns:
        Dictionary of headers
    """
    return {
        "content-type": config.content_type,
        "x-gwt-module-base": config.module_base,
        "x-gwt-permutation": config.permutation,
    }


def build_authenticate_body(config: GWTConfig) -> str:
    """Build GWT request body for authentication.

    Args:
        config: GWT configuration

    Returns:
        GWT-RPC formatted request body
    """
    return (
        f"7|0|5|https://cronometer.com/cronometer/|{config.header}|"
        "com.cronometer.shared.rpc.CronometerService|authenticate|"
        "java.lang.Integer/3438268394|1|2|3|4|1|5|5|-300|"
    )


def build_generate_token_body(config: GWTConfig, nonce: str, user_id: str) -> str:
    """Build GWT request body for generating an auth token.

    Args:
        config: GWT configuration
        nonce: Session nonce from cookies
        user_id: User ID from authentication

    Returns:
        GWT-RPC formatted request body
    """
    return (
        f"7|0|8|https://cronometer.com/cronometer/|{config.header}|"
        "com.cronometer.shared.rpc.CronometerService|generateAuthorizationToken|"
        f"java.lang.String/2004016611|I|com.cronometer.shared.user.AuthScope/2065601159|{nonce}|"
        f"1|2|3|4|4|5|6|6|7|8|{user_id}|3600|7|2|"
    )


def build_logout_body(config: GWTConfig, nonce: str) -> str:
    """Build GWT request body for logout.

    Args:
        config: GWT configuration
        nonce: Session nonce from cookies

    Returns:
        GWT-RPC formatted request body
    """
    return (
        f"7|0|6|https://cronometer.com/cronometer/|{config.header}|"
        "com.cronometer.shared.rpc.CronometerService|logout|"
        f"java.lang.String/2004016611|{nonce}|1|2|3|4|1|5|6|"
    )


# Regex patterns for parsing GWT responses
USER_ID_PATTERN = re.compile(r"OK\[(\d+),")
TOKEN_PATTERN = re.compile(r'"(.*)"')


def parse_user_id(response_text: str) -> str | None:
    """Extract user ID from GWT authentication response.

    Args:
        response_text: Raw GWT response body

    Returns:
        User ID string or None if not found
    """
    match = USER_ID_PATTERN.search(response_text)
    return match.group(1) if match else None


def parse_auth_token(response_text: str) -> str | None:
    """Extract auth token from GWT generateAuthorizationToken response.

    Args:
        response_text: Raw GWT response body

    Returns:
        Auth token string or None if not found
    """
    match = TOKEN_PATTERN.search(response_text)
    return match.group(1) if match else None
