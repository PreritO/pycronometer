"""Tests for GWT protocol utilities."""

import os
from unittest import mock

from pycronometer.gwt import (
    DEFAULT_GWT_HEADER,
    DEFAULT_GWT_PERMUTATION,
    build_authenticate_body,
    build_generate_token_body,
    build_gwt_headers,
    get_gwt_config,
    parse_auth_token,
    parse_user_id,
)


class TestGetGwtConfig:
    """Tests for get_gwt_config."""

    def test_returns_defaults(self) -> None:
        """Test that defaults are returned when no overrides."""
        config = get_gwt_config()
        assert config.permutation == DEFAULT_GWT_PERMUTATION
        assert config.header == DEFAULT_GWT_HEADER

    def test_parameter_overrides(self) -> None:
        """Test that parameters override defaults."""
        config = get_gwt_config(permutation="CUSTOM_PERM", header="CUSTOM_HEAD")
        assert config.permutation == "CUSTOM_PERM"
        assert config.header == "CUSTOM_HEAD"

    def test_env_var_overrides(self) -> None:
        """Test that env vars override defaults."""
        with mock.patch.dict(
            os.environ,
            {
                "CRONOMETER_GWT_PERMUTATION": "ENV_PERM",
                "CRONOMETER_GWT_HEADER": "ENV_HEAD",
            },
        ):
            config = get_gwt_config()
            assert config.permutation == "ENV_PERM"
            assert config.header == "ENV_HEAD"

    def test_parameter_overrides_env_var(self) -> None:
        """Test that parameters take precedence over env vars."""
        with mock.patch.dict(
            os.environ,
            {"CRONOMETER_GWT_PERMUTATION": "ENV_PERM"},
        ):
            config = get_gwt_config(permutation="PARAM_PERM")
            assert config.permutation == "PARAM_PERM"


class TestBuildGwtHeaders:
    """Tests for build_gwt_headers."""

    def test_builds_correct_headers(self) -> None:
        """Test that headers are built correctly."""
        config = get_gwt_config()
        headers = build_gwt_headers(config)

        assert headers["content-type"] == "text/x-gwt-rpc; charset=UTF-8"
        assert headers["x-gwt-module-base"] == "https://cronometer.com/cronometer/"
        assert headers["x-gwt-permutation"] == config.permutation


class TestBuildAuthenticateBody:
    """Tests for build_authenticate_body."""

    def test_contains_expected_parts(self) -> None:
        """Test that authenticate body contains expected parts."""
        config = get_gwt_config()
        body = build_authenticate_body(config)

        assert "cronometer.com/cronometer" in body
        assert config.header in body
        assert "authenticate" in body


class TestBuildGenerateTokenBody:
    """Tests for build_generate_token_body."""

    def test_contains_nonce_and_user_id(self) -> None:
        """Test that token body contains nonce and user ID."""
        config = get_gwt_config()
        body = build_generate_token_body(config, "test_nonce", "12345")

        assert "test_nonce" in body
        assert "12345" in body
        assert "generateAuthorizationToken" in body


class TestParseUserId:
    """Tests for parse_user_id."""

    def test_parses_user_id(self) -> None:
        """Test parsing user ID from response."""
        response = "//OK[12345,2,1,...]"
        user_id = parse_user_id(response)
        assert user_id == "12345"

    def test_returns_none_for_invalid(self) -> None:
        """Test that None is returned for invalid response."""
        response = "some invalid response"
        user_id = parse_user_id(response)
        assert user_id is None


class TestParseAuthToken:
    """Tests for parse_auth_token."""

    def test_parses_token(self) -> None:
        """Test parsing auth token from response."""
        response = '//OK["abc123def456"]'
        token = parse_auth_token(response)
        assert token == "abc123def456"

    def test_returns_none_for_invalid(self) -> None:
        """Test that None is returned for invalid response."""
        response = "some invalid response"
        token = parse_auth_token(response)
        assert token is None
