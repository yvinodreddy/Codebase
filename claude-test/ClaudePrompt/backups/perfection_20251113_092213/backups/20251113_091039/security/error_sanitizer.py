#!/usr/bin/env python3
"""
S9: Error Detail Sanitization
Sanitize error messages to prevent information disclosure in production.
"""

import re
from pathlib import Path


def sanitize_error_message(error_message: str, production_mode: bool = False) -> str:
    """
    Sanitize error message for safe display.

    Args:
        error_message: Raw error message
        production_mode: If True, heavily sanitize (hide internal details)

    Returns:
        Sanitized error message
    """
    if not production_mode:
        return error_message  # Development mode - show all details

    # Production mode - sanitize aggressively
    sanitized = error_message

    # Remove file paths
    sanitized = re.sub(r'/[^\s]+\.py', '[FILE]', sanitized)
    sanitized = re.sub(r'C:\\[^\s]+\.py', '[FILE]', sanitized)

    # Remove line numbers
    sanitized = re.sub(r'line \d+', 'line [REDACTED]', sanitized)

    # Remove API keys (if leaked)
    sanitized = re.sub(r'sk-[a-zA-Z0-9]{20,}', '[API_KEY]', sanitized)

    # Remove internal variable names
    sanitized = re.sub(r'\w+_internal\w*', '[INTERNAL]', sanitized)

    return sanitized


def create_user_friendly_error(error_type: str, technical_details: str = "") -> str:
    """
    Create user-friendly error message.

    Args:
        error_type: Type of error
        technical_details: Technical details (only shown in dev mode)

    Returns:
        User-friendly error message
    """
    messages = {
        "API_ERROR": "Unable to connect to AI service. Please try again later.",
        "VALIDATION_ERROR": "Input validation failed. Please check your input.",
        "TIMEOUT": "Request timeout. The operation took too long.",
        "RATE_LIMIT": "Too many requests. Please wait a moment and try again.",
    }

    return messages.get(error_type, "An error occurred. Please contact support.")


if __name__ == "__main__":
    test_error = "Error in /home/user/secret_file.py line 42: API key sk-ant-1234567890 invalid"
    print("Original:", test_error)
    print("Sanitized:", sanitize_error_message(test_error, production_mode=True))
