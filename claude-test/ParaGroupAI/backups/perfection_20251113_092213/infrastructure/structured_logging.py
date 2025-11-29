#!/usr/bin/env python3
"""
Structured Logging with structlog
JSON-formatted logging for production systems
"""
import logging
import sys
from typing import Optional
try:
    import structlog
    from structlog.processors import JSONRenderer
except ImportError:
    print("⚠️  structlog not installed. Run: pip install structlog")
    structlog = None


def configure_structured_logging(
    log_level: str = "INFO",
    json_output: bool = True,
    log_file: Optional[str] = None
):
    """
    Configure structured logging for the application

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_output: Output in JSON format
        log_file: Optional file path for log output

    Example:
        configure_structured_logging(
            log_level="INFO",
            json_output=True,
            log_file="logs/app.log"
        )

        logger = structlog.get_logger()
        logger.info("user_action", user_id=123, action="login")
    """
    if structlog is None:
        raise ImportError("structlog not installed")

    # Set up processors
    processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if json_output:
        processors.append(JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )

    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        logging.getLogger().addHandler(file_handler)


def get_logger(name: Optional[str] = None):
    """
    Get a structured logger instance

    Args:
        name: Logger name (default: calling module)

    Returns:
        Structured logger instance

    Example:
        logger = get_logger(__name__)
        logger.info("operation_complete", duration=1.5, items_processed=100)
    """
    if structlog is None:
        raise ImportError("structlog not installed")

    return structlog.get_logger(name)
