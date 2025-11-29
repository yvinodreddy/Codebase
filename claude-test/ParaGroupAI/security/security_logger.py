#!/usr/bin/env python3
"""
S5: Security Event Logging
Dedicated logger for security events across all guardrail layers.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from config import UltrathinkConfig as Config

# Create logs directory if needed (production-ready: use script directory)
SCRIPT_DIR = Path(__file__).parent.parent.resolve()
log_dir = SCRIPT_DIR / "logs"
log_dir.mkdir(exist_ok=True)

# Create security logger
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

# File handler for security events
if Config.LOG_SECURITY_EVENTS_TO_FILE:
    file_handler = logging.FileHandler(Config.LOG_SECURITY_FILE_PATH)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    security_logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(logging.Formatter(
    '🔒 SECURITY: %(message)s'
))
security_logger.addHandler(console_handler)


def log_security_event(event_type: str, details: str, severity: str = "INFO"):
    """
    Log a security event.

    Args:
        event_type: Type of event (e.g., "PROMPT_INJECTION_BLOCKED")
        details: Event details
        severity: INFO, WARNING, ERROR, CRITICAL
    """
    message = f"{event_type} | {details}"

    if severity == "CRITICAL":
        security_logger.critical(message)
    elif severity == "ERROR":
        security_logger.error(message)
    elif severity == "WARNING":
        security_logger.warning(message)
    else:
        security_logger.info(message)


if __name__ == "__main__":
    log_security_event("TEST", "Security logger initialized", "INFO")
    print("✅ Security logger test complete")
