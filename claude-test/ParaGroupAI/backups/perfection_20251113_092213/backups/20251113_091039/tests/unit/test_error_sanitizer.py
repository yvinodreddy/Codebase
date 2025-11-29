#!/usr/bin/env python3
"""
Unit Tests for security/error_sanitizer.py
Tests error message sanitization and user-friendly error creation.

Test Coverage Target: 90%+
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from security.error_sanitizer import (
    sanitize_error_message,
    create_user_friendly_error,
)


# ==========================================
# SANITIZE ERROR MESSAGE TESTS
# ==========================================

class TestSanitizeErrorMessage:
    """Test error message sanitization."""

    def test_development_mode_no_sanitization(self):
        """In development mode, error should not be sanitized."""
        error = "Error in /home/user/file.py line 42: sk-ant-1234567890"
        result = sanitize_error_message(error, production_mode=False)
        assert result == error

    def test_production_mode_removes_unix_paths(self):
        """Production mode should remove Unix file paths."""
        error = "Error in /home/user/secret.py line 42"
        result = sanitize_error_message(error, production_mode=True)
        assert "/home/user/secret.py" not in result
        assert "[FILE]" in result

    def test_production_mode_removes_windows_paths(self):
        """Production mode should remove Windows file paths."""
        error = "Error in C:\\Users\\user\\secret.py line 42"
        result = sanitize_error_message(error, production_mode=True)
        assert "C:\\Users\\user\\secret.py" not in result
        assert "[FILE]" in result

    def test_production_mode_removes_line_numbers(self):
        """Production mode should remove line numbers."""
        error = "Error at line 42 in function"
        result = sanitize_error_message(error, production_mode=True)
        assert "line 42" not in result
        assert "line [REDACTED]" in result

    def test_production_mode_removes_api_keys(self):
        """Production mode should remove API keys."""
        error = "Invalid API key: sk-1234567890abcdefghijklmnopqrst"
        result = sanitize_error_message(error, production_mode=True)
        assert "sk-1234567890abcdefghijklmnopqrst" not in result
        assert "[API_KEY]" in result

    def test_production_mode_removes_internal_variables(self):
        """Production mode should remove internal variable names."""
        error = "Error in db_internal_connection variable"
        result = sanitize_error_message(error, production_mode=True)
        assert "db_internal_connection" not in result
        assert "[INTERNAL]" in result

    def test_production_mode_multiple_sanitizations(self):
        """Production mode should handle multiple sensitive items."""
        error = "Error in /home/user/app.py line 42: sk-1234567890abcdefghijklmn in var_internal"
        result = sanitize_error_message(error, production_mode=True)
        assert "/home/user/app.py" not in result
        assert "line 42" not in result
        assert "sk-1234567890abcdefghijklmn" not in result
        assert "var_internal" not in result
        assert "[FILE]" in result
        assert "[REDACTED]" in result
        assert "[API_KEY]" in result
        assert "[INTERNAL]" in result

    def test_empty_error_message(self):
        """Empty error message should return empty string."""
        result = sanitize_error_message("", production_mode=True)
        assert result == ""

    def test_benign_error_message_unchanged(self):
        """Benign error messages without sensitive info should pass through."""
        error = "Connection timeout"
        result = sanitize_error_message(error, production_mode=True)
        assert result == error

    def test_default_production_mode(self):
        """Default production_mode should be False."""
        error = "Error in /home/user/file.py"
        result = sanitize_error_message(error)
        # Should not sanitize by default
        assert result == error


# ==========================================
# CREATE USER-FRIENDLY ERROR TESTS
# ==========================================

class TestCreateUserFriendlyError:
    """Test user-friendly error message creation."""

    def test_api_error_message(self):
        """API_ERROR should return friendly message."""
        result = create_user_friendly_error("API_ERROR")
        assert "AI service" in result
        assert "try again" in result.lower()

    def test_validation_error_message(self):
        """VALIDATION_ERROR should return friendly message."""
        result = create_user_friendly_error("VALIDATION_ERROR")
        assert "validation" in result.lower()
        assert "input" in result.lower()

    def test_timeout_error_message(self):
        """TIMEOUT should return friendly message."""
        result = create_user_friendly_error("TIMEOUT")
        assert "timeout" in result.lower()
        assert "too long" in result.lower()

    def test_rate_limit_error_message(self):
        """RATE_LIMIT should return friendly message."""
        result = create_user_friendly_error("RATE_LIMIT")
        assert "requests" in result.lower()
        assert "wait" in result.lower()

    def test_unknown_error_type(self):
        """Unknown error type should return generic message."""
        result = create_user_friendly_error("UNKNOWN_ERROR_TYPE")
        assert "error occurred" in result.lower()
        assert "support" in result.lower()

    def test_empty_error_type(self):
        """Empty error type should return generic message."""
        result = create_user_friendly_error("")
        assert "error occurred" in result.lower()
        assert "support" in result.lower()

    def test_technical_details_parameter_accepted(self):
        """Technical details parameter should be accepted (but not used in current impl)."""
        result = create_user_friendly_error("API_ERROR", technical_details="Connection refused")
        # Should return the same message regardless of technical details
        assert "AI service" in result

    def test_all_error_types_return_strings(self):
        """All error types should return non-empty strings."""
        error_types = ["API_ERROR", "VALIDATION_ERROR", "TIMEOUT", "RATE_LIMIT", "UNKNOWN"]
        for error_type in error_types:
            result = create_user_friendly_error(error_type)
            assert isinstance(result, str)
            assert len(result) > 0


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestErrorSanitizerIntegration:
    """Test integration scenarios."""

    def test_sanitize_then_create_friendly(self):
        """Test sanitizing error then creating friendly message."""
        raw_error = "API error in /home/user/api.py line 100: sk-1234567890abcdefghijklmn invalid"

        # Sanitize the technical error
        sanitized = sanitize_error_message(raw_error, production_mode=True)
        assert "[FILE]" in sanitized
        assert "[REDACTED]" in sanitized
        assert "[API_KEY]" in sanitized

        # Create friendly message
        friendly = create_user_friendly_error("API_ERROR")
        assert "AI service" in friendly
        assert "try again" in friendly.lower()

    def test_development_vs_production_mode(self):
        """Test difference between development and production mode."""
        error = "Error in /home/user/app.py line 42"

        dev_result = sanitize_error_message(error, production_mode=False)
        prod_result = sanitize_error_message(error, production_mode=True)

        # Development should show everything
        assert "/home/user/app.py" in dev_result
        assert "line 42" in dev_result

        # Production should sanitize
        assert "/home/user/app.py" not in prod_result
        assert "line 42" not in prod_result

    def test_multiple_api_keys_sanitized(self):
        """Test multiple API keys are all sanitized."""
        error = "Keys sk-1234567890abcdefghijklmn and sk-xyz9876543210fedcbaqwerty found"
        result = sanitize_error_message(error, production_mode=True)
        assert "sk-1234567890abcdefghijklmn" not in result
        assert "sk-xyz9876543210fedcbaqwerty" not in result
        assert result.count("[API_KEY]") == 2

    def test_mixed_path_types(self):
        """Test sanitization of both Unix and Windows paths in same error."""
        error = "Error in /home/user/app.py and C:\\Users\\user\\app.py"
        result = sanitize_error_message(error, production_mode=True)
        assert "/home/user/app.py" not in result
        assert "C:\\Users\\user\\app.py" not in result
        assert result.count("[FILE]") >= 1

    def test_preserves_non_sensitive_context(self):
        """Test that non-sensitive context is preserved."""
        error = "Connection failed: timeout after 30 seconds"
        result = sanitize_error_message(error, production_mode=True)
        assert "Connection failed" in result
        assert "timeout" in result
        assert "30 seconds" in result


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
