#!/usr/bin/env python3
"""
Circuit Breaker Pattern Implementation
Prevents cascading failures by failing fast when error threshold is exceeded
"""
import time
import logging
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Any, Optional
from functools import wraps

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing fast
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker"""
    failure_threshold: int = 5  # Failures before opening
    success_threshold: int = 2  # Successes to close from half-open
    timeout: int = 60  # Seconds to wait before trying again
    expected_exception: type = Exception


class CircuitBreaker:
    """
    Circuit breaker implementation for resilient service calls

    States:
    - CLOSED: Normal operation, calls go through
    - OPEN: Too many failures, reject calls immediately
    - HALF_OPEN: Testing if service recovered

    Example:
        breaker = CircuitBreaker(failure_threshold=3, timeout=30)

        @breaker
        def risky_api_call():
            return api.get_data()
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout: int = 60,
        expected_exception: type = Exception,
        name: str = "default"
    ):
        self.config = CircuitBreakerConfig(
            failure_threshold=failure_threshold,
            success_threshold=success_threshold,
            timeout=timeout,
            expected_exception=expected_exception
        )
        self.name = name
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None

        logger.info(
            f"Circuit breaker '{name}' initialized: "
            f"failure_threshold={failure_threshold}, timeout={timeout}s"
        )

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Call function through circuit breaker

        Args:
            func: Function to call
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            CircuitBreakerOpenError: If circuit is open
            Original exception: If function fails and circuit allows it
        """
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info(f"Circuit breaker '{self.name}' entering HALF_OPEN state")
            else:
                raise CircuitBreakerOpenError(
                    f"Circuit breaker '{self.name}' is OPEN. "
                    f"Retry after {self._time_until_retry():.1f}s"
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.config.expected_exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
                logger.info(f"Circuit breaker '{self.name}' CLOSED (recovered)")

    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.success_count = 0

        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(
                f"Circuit breaker '{self.name}' OPENED "
                f"(failures: {self.failure_count}/{self.config.failure_threshold})"
            )

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.config.timeout

    def _time_until_retry(self) -> float:
        """Calculate seconds until retry is allowed"""
        if self.last_failure_time is None:
            return 0.0
        elapsed = time.time() - self.last_failure_time
        return max(0.0, self.config.timeout - elapsed)

    def __call__(self, func: Callable) -> Callable:
        """Decorator usage"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        return wrapper

    def reset(self):
        """Manually reset circuit breaker to CLOSED state"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        logger.info(f"Circuit breaker '{self.name}' manually reset to CLOSED")

    @property
    def is_open(self) -> bool:
        """Check if circuit is open"""
        return self.state == CircuitState.OPEN

    @property
    def is_closed(self) -> bool:
        """Check if circuit is closed"""
        return self.state == CircuitState.CLOSED


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass


# Global circuit breakers for common services
api_breaker = CircuitBreaker(
    failure_threshold=5,
    timeout=60,
    name="claude_api"
)

database_breaker = CircuitBreaker(
    failure_threshold=3,
    timeout=30,
    name="database"
)

external_service_breaker = CircuitBreaker(
    failure_threshold=10,
    timeout=120,
    name="external_service"
)
