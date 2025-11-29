#!/usr/bin/env python3
"""
Unit Tests for security/security_logger.py
Tests security event logging functionality.

Test Coverage Target: 90%+
"""

import pytest
import sys
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# ==========================================
# LOG SECURITY EVENT TESTS
# ==========================================

class TestLogSecurityEvent:
    """Test log_security_event function."""

    @patch('security.security_logger.security_logger')
    def test_info_severity(self, mock_logger):
        """INFO severity should call logger.info()."""
        from security.security_logger import log_security_event

        log_security_event("TEST_EVENT", "Test details", "INFO")
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "TEST_EVENT" in call_args
        assert "Test details" in call_args

    @patch('security.security_logger.security_logger')
    def test_warning_severity(self, mock_logger):
        """WARNING severity should call logger.warning()."""
        from security.security_logger import log_security_event

        log_security_event("TEST_EVENT", "Test details", "WARNING")
        mock_logger.warning.assert_called_once()
        call_args = mock_logger.warning.call_args[0][0]
        assert "TEST_EVENT" in call_args
        assert "Test details" in call_args

    @patch('security.security_logger.security_logger')
    def test_error_severity(self, mock_logger):
        """ERROR severity should call logger.error()."""
        from security.security_logger import log_security_event

        log_security_event("TEST_EVENT", "Test details", "ERROR")
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args[0][0]
        assert "TEST_EVENT" in call_args
        assert "Test details" in call_args

    @patch('security.security_logger.security_logger')
    def test_critical_severity(self, mock_logger):
        """CRITICAL severity should call logger.critical()."""
        from security.security_logger import log_security_event

        log_security_event("TEST_EVENT", "Test details", "CRITICAL")
        mock_logger.critical.assert_called_once()
        call_args = mock_logger.critical.call_args[0][0]
        assert "TEST_EVENT" in call_args
        assert "Test details" in call_args

    @patch('security.security_logger.security_logger')
    def test_default_severity_is_info(self, mock_logger):
        """Default severity should be INFO."""
        from security.security_logger import log_security_event

        log_security_event("TEST_EVENT", "Test details")
        mock_logger.info.assert_called_once()

    @patch('security.security_logger.security_logger')
    def test_unknown_severity_defaults_to_info(self, mock_logger):
        """Unknown severity should default to INFO."""
        from security.security_logger import log_security_event

        log_security_event("TEST_EVENT", "Test details", "UNKNOWN")
        mock_logger.info.assert_called_once()

    @patch('security.security_logger.security_logger')
    def test_message_format(self, mock_logger):
        """Message should be formatted as 'event_type | details'."""
        from security.security_logger import log_security_event

        log_security_event("INJECTION_BLOCKED", "Malicious prompt detected", "WARNING")
        mock_logger.warning.assert_called_once()
        call_args = mock_logger.warning.call_args[0][0]
        assert "INJECTION_BLOCKED | Malicious prompt detected" == call_args


# ==========================================
# LOGGER CONFIGURATION TESTS
# ==========================================

class TestSecurityLoggerConfiguration:
    """Test security logger module configuration."""

    def test_logger_exists(self):
        """Security logger should be created."""
        from security import security_logger
        assert security_logger.security_logger is not None

    def test_logger_has_correct_name(self):
        """Security logger should have name 'security'."""
        from security import security_logger
        assert security_logger.security_logger.name == 'security'

    def test_logger_level_is_info(self):
        """Security logger level should be INFO."""
        from security import security_logger
        assert security_logger.security_logger.level == logging.INFO

    def test_logger_has_handlers(self):
        """Security logger should have at least one handler."""
        from security import security_logger
        assert len(security_logger.security_logger.handlers) > 0

    def test_console_handler_exists(self):
        """Console handler should exist."""
        from security import security_logger
        console_handlers = [
            h for h in security_logger.security_logger.handlers
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        ]
        assert len(console_handlers) > 0

    def test_console_handler_level_is_warning(self):
        """Console handler should be set to WARNING level."""
        from security import security_logger
        console_handlers = [
            h for h in security_logger.security_logger.handlers
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        ]
        if console_handlers:
            assert console_handlers[0].level == logging.WARNING


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestSecurityLoggerIntegration:
    """Test real-world security logging scenarios."""

    @patch('security.security_logger.security_logger')
    def test_prompt_injection_logging(self, mock_logger):
        """Test logging prompt injection attempt."""
        from security.security_logger import log_security_event

        log_security_event(
            "PROMPT_INJECTION_BLOCKED",
            "Detected SQL injection pattern in user prompt",
            "WARNING"
        )
        mock_logger.warning.assert_called_once()
        call_args = mock_logger.warning.call_args[0][0]
        assert "PROMPT_INJECTION_BLOCKED" in call_args
        assert "SQL injection" in call_args

    @patch('security.security_logger.security_logger')
    def test_rate_limit_logging(self, mock_logger):
        """Test logging rate limit violation."""
        from security.security_logger import log_security_event

        log_security_event(
            "RATE_LIMIT_EXCEEDED",
            "User exceeded 500 requests in 360 seconds",
            "WARNING"
        )
        mock_logger.warning.assert_called_once()
        call_args = mock_logger.warning.call_args[0][0]
        assert "RATE_LIMIT_EXCEEDED" in call_args
        assert "500 requests" in call_args

    @patch('security.security_logger.security_logger')
    def test_security_bypass_attempt_logging(self, mock_logger):
        """Test logging security bypass attempt."""
        from security.security_logger import log_security_event

        log_security_event(
            "BYPASS_ATTEMPT",
            "Attempt to circumvent guardrail layer 3",
            "CRITICAL"
        )
        mock_logger.critical.assert_called_once()
        call_args = mock_logger.critical.call_args[0][0]
        assert "BYPASS_ATTEMPT" in call_args
        assert "guardrail layer 3" in call_args

    @patch('security.security_logger.security_logger')
    def test_multiple_events_logging(self, mock_logger):
        """Test logging multiple security events."""
        from security.security_logger import log_security_event

        log_security_event("EVENT1", "Details 1", "INFO")
        log_security_event("EVENT2", "Details 2", "WARNING")
        log_security_event("EVENT3", "Details 3", "ERROR")

        assert mock_logger.info.call_count == 1
        assert mock_logger.warning.call_count == 1
        assert mock_logger.error.call_count == 1

    @patch('security.security_logger.security_logger')
    def test_empty_details(self, mock_logger):
        """Test logging with empty details."""
        from security.security_logger import log_security_event

        log_security_event("TEST_EVENT", "", "INFO")
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "TEST_EVENT |" in call_args

    @patch('security.security_logger.security_logger')
    def test_special_characters_in_details(self, mock_logger):
        """Test logging with special characters in details."""
        from security.security_logger import log_security_event

        log_security_event(
            "TEST_EVENT",
            "Details with | pipe and \n newline and 'quotes'",
            "INFO"
        )
        mock_logger.info.assert_called_once()
        # Should not crash, and should include the special characters
        call_args = mock_logger.info.call_args[0][0]
        assert "TEST_EVENT" in call_args


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
