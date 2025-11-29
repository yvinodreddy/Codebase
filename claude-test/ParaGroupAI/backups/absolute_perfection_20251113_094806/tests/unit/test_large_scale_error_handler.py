#!/usr/bin/env python3
"""
Unit Tests for large_scale_error_handler.py
Tests production-grade error handling for massive workloads.

Test Coverage Target: 80%+
Production-Ready Quality Standards
"""

import pytest
import sys
import time
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from large_scale_error_handler import (
    ErrorSeverity,
    ErrorCategory,
    ErrorContext,
    CircuitBreaker,
    LargeScaleErrorHandler,
    get_global_error_handler
)


# ==========================================
# ERROR SEVERITY TESTS
# ==========================================

class TestErrorSeverity:
    """Test ErrorSeverity enum."""

    def test_severity_levels_exist(self):
        """All severity levels should exist."""
        assert ErrorSeverity.LOW
        assert ErrorSeverity.MEDIUM
        assert ErrorSeverity.HIGH
        assert ErrorSeverity.FATAL


# ==========================================
# ERROR CATEGORY TESTS
# ==========================================

class TestErrorCategory:
    """Test ErrorCategory enum."""

    def test_category_types_exist(self):
        """All category types should exist."""
        assert ErrorCategory.MEMORY
        assert ErrorCategory.IO
        assert ErrorCategory.NETWORK
        assert ErrorCategory.VALIDATION
        assert ErrorCategory.PROCESSING
        assert ErrorCategory.CONFIGURATION


# ==========================================
# ERROR CONTEXT TESTS
# ==========================================

class TestErrorContext:
    """Test ErrorContext dataclass."""

    def test_error_context_creation(self):
        """Should create error context with required fields."""
        from datetime import datetime

        context = ErrorContext(
            error_id="ERR_001",
            timestamp=datetime.now(),
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.MEMORY,
            message="Out of memory",
            details={"usage": "95%"}
        )

        assert context.error_id == "ERR_001"
        assert context.severity == ErrorSeverity.HIGH
        assert context.category == ErrorCategory.MEMORY
        assert context.message == "Out of memory"
        assert context.details["usage"] == "95%"


# ==========================================
# CIRCUIT BREAKER INITIALIZATION TESTS
# ==========================================

class TestCircuitBreakerInit:
    """Test CircuitBreaker initialization."""

    def test_init_with_defaults(self):
        """Should initialize with default values."""
        cb = CircuitBreaker()

        assert cb.failure_threshold == 5
        assert cb.timeout_seconds == 60
        assert cb.failure_count == 0
        assert cb.state == "CLOSED"

    def test_init_with_custom_values(self):
        """Should initialize with custom values."""
        cb = CircuitBreaker(failure_threshold=3, timeout_seconds=30)

        assert cb.failure_threshold == 3
        assert cb.timeout_seconds == 30


# ==========================================
# CIRCUIT BREAKER STATE TESTS
# ==========================================

class TestCircuitBreakerState:
    """Test CircuitBreaker state management."""

    def test_starts_in_closed_state(self):
        """Should start in CLOSED state."""
        cb = CircuitBreaker()
        assert cb.get_state() == "CLOSED"
        assert cb.can_attempt() is True

    def test_records_success(self):
        """Should record success and reset failure count."""
        cb = CircuitBreaker()
        cb.failure_count = 3

        cb.record_success()

        assert cb.failure_count == 0
        assert cb.state == "CLOSED"

    def test_records_failure(self):
        """Should record failure and increment count."""
        cb = CircuitBreaker()

        cb.record_failure()

        assert cb.failure_count == 1
        assert cb.last_failure_time is not None

    def test_opens_after_threshold(self):
        """Should open circuit after hitting threshold."""
        cb = CircuitBreaker(failure_threshold=3)

        cb.record_failure()
        cb.record_failure()
        cb.record_failure()

        assert cb.state == "OPEN"
        assert cb.can_attempt() is False

    def test_transitions_to_half_open(self):
        """Should transition to HALF_OPEN after timeout."""
        cb = CircuitBreaker(failure_threshold=2, timeout_seconds=0.1)

        # Open the circuit
        cb.record_failure()
        cb.record_failure()
        assert cb.state == "OPEN"

        # Wait for timeout
        time.sleep(0.2)

        # Should allow attempt (transitions to HALF_OPEN)
        assert cb.can_attempt() is True


# ==========================================
# LARGE SCALE ERROR HANDLER INITIALIZATION
# ==========================================

class TestLargeScaleErrorHandlerInit:
    """Test LargeScaleErrorHandler initialization."""

    def test_init_without_log_file(self):
        """Should initialize without log file."""
        handler = LargeScaleErrorHandler()

        assert handler.errors == []
        assert handler.circuit_breakers == {}
        assert handler.log_file is None

    def test_init_with_log_file(self):
        """Should initialize with log file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as tf:
            handler = LargeScaleErrorHandler(log_file=tf.name)

            assert handler.log_file == Path(tf.name)


# ==========================================
# HANDLE ERROR TESTS
# ==========================================

class TestHandleError:
    """Test handle_error method."""

    def test_handles_error_without_recovery(self):
        """Should handle error without recovery strategy."""
        handler = LargeScaleErrorHandler()

        error = ValueError("Test error")
        success, result = handler.handle_error(
            error=error,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.MEDIUM,
            context={"test": "context"}
        )

        assert success is False
        assert result is None
        assert len(handler.errors) == 1

    def test_handles_error_with_recovery(self):
        """Should handle error with recovery strategy."""
        handler = LargeScaleErrorHandler()

        error = ValueError("Test error")

        def recovery_strategy(err, ctx):
            return "Recovered!"

        success, result = handler.handle_error(
            error=error,
            category=ErrorCategory.PROCESSING,
            severity=ErrorSeverity.MEDIUM,
            context={"test": "context"},
            recovery_strategy=recovery_strategy
        )

        assert success is True
        assert result == "Recovered!"
        assert handler.errors[0].recovery_attempted is True
        assert handler.errors[0].recovery_successful is True

    def test_handles_recovery_failure(self):
        """Should handle recovery strategy failure."""
        handler = LargeScaleErrorHandler()

        error = ValueError("Test error")

        def failing_recovery(err, ctx):
            raise Exception("Recovery failed")

        success, result = handler.handle_error(
            error=error,
            category=ErrorCategory.PROCESSING,
            severity=ErrorSeverity.HIGH,
            context={},
            recovery_strategy=failing_recovery
        )

        assert success is False
        assert result is None


# ==========================================
# RETRY WITH BACKOFF TESTS
# ==========================================

class TestRetryWithBackoff:
    """Test retry_with_backoff method."""

    def test_succeeds_on_first_try(self):
        """Should succeed on first try."""
        handler = LargeScaleErrorHandler()

        def successful_operation():
            return "Success"

        success, result, errors = handler.retry_with_backoff(
            operation=successful_operation,
            operation_name="test_op",
            max_retries=3,
            initial_delay=0.01
        )

        assert success is True
        assert result == "Success"
        assert len(errors) == 0

    def test_retries_until_success(self):
        """Should retry until operation succeeds."""
        handler = LargeScaleErrorHandler()

        attempt_count = {"count": 0}

        def flaky_operation():
            attempt_count["count"] += 1
            if attempt_count["count"] < 3:
                raise Exception(f"Attempt {attempt_count['count']} failed")
            return "Success"

        success, result, errors = handler.retry_with_backoff(
            operation=flaky_operation,
            operation_name="flaky_op",
            max_retries=5,
            initial_delay=0.01
        )

        assert success is True
        assert result == "Success"
        assert len(errors) == 2  # Failed twice before success

    def test_fails_after_max_retries(self):
        """Should fail after max retries exhausted."""
        handler = LargeScaleErrorHandler()

        def always_fails():
            raise Exception("Always fails")

        success, result, errors = handler.retry_with_backoff(
            operation=always_fails,
            operation_name="failing_op",
            max_retries=3,
            initial_delay=0.01
        )

        assert success is False
        assert result is None
        assert len(errors) == 3

    def test_respects_circuit_breaker(self):
        """Should respect circuit breaker state."""
        handler = LargeScaleErrorHandler()

        # Open the circuit breaker
        cb = CircuitBreaker(failure_threshold=1, timeout_seconds=60)
        cb.record_failure()
        handler.circuit_breakers["test_op"] = cb

        def some_operation():
            return "Success"

        success, result, errors = handler.retry_with_backoff(
            operation=some_operation,
            operation_name="test_op",
            max_retries=3
        )

        assert success is False
        assert "Circuit breaker OPEN" in errors[0]


# ==========================================
# MEMORY PRESSURE TESTS
# ==========================================

class TestHandleMemoryPressure:
    """Test handle_memory_pressure method."""

    def test_no_action_below_threshold(self):
        """Should take no action when below threshold."""
        handler = LargeScaleErrorHandler()

        result = handler.handle_memory_pressure(
            current_usage_mb=500.0,
            threshold_mb=1000.0
        )

        assert result["status"] == "OK"
        assert len(result["actions"]) == 0

    def test_takes_action_above_threshold(self):
        """Should take action when above threshold."""
        handler = LargeScaleErrorHandler()

        # Add some errors to test cleanup
        for i in range(150):
            handler.errors.append(ErrorContext(
                error_id=f"ERR_{i}",
                timestamp=None,
                severity=ErrorSeverity.LOW,
                category=ErrorCategory.PROCESSING,
                message="Test error",
                details={}
            ))

        result = handler.handle_memory_pressure(
            current_usage_mb=1200.0,
            threshold_mb=1000.0
        )

        assert result["status"] == "WARNING"
        assert len(result["actions"]) > 0
        assert len(handler.errors) == 100  # Should keep last 100


# ==========================================
# VALIDATE LARGE PROMPT TESTS
# ==========================================

class TestValidateLargePrompt:
    """Test validate_large_prompt method."""

    def test_accepts_normal_prompt(self):
        """Should accept normal-sized prompt."""
        handler = LargeScaleErrorHandler()

        prompt = "This is a normal prompt with a reasonable size."
        valid, error_msg = handler.validate_large_prompt(prompt)

        assert valid is True
        assert error_msg is None

    def test_accepts_prompt_with_many_tasks(self):
        """Should accept prompt with many tasks."""
        handler = LargeScaleErrorHandler()

        tasks = "\n".join([f"{i}. Task {i}" for i in range(1, 1001)])
        valid, error_msg = handler.validate_large_prompt(tasks, max_tasks=10000)

        assert valid is True

    def test_rejects_prompt_with_too_many_tasks(self):
        """Should reject prompt with too many tasks."""
        handler = LargeScaleErrorHandler()

        tasks = "\n".join([f"{i}. Task {i}" for i in range(1, 1001)])
        valid, error_msg = handler.validate_large_prompt(tasks, max_tasks=500)

        assert valid is False
        assert "tasks" in error_msg.lower()

    def test_rejects_empty_prompt(self):
        """Should reject empty prompt."""
        handler = LargeScaleErrorHandler()

        valid, error_msg = handler.validate_large_prompt("")

        assert valid is False
        assert "empty" in error_msg.lower()

    def test_rejects_excessively_large_prompt(self):
        """Should reject excessively large prompt."""
        handler = LargeScaleErrorHandler()

        huge_prompt = "x" * 2_000_000  # 2MB
        valid, error_msg = handler.validate_large_prompt(huge_prompt)

        assert valid is False
        assert "bytes" in error_msg.lower() or "MB" in error_msg


# ==========================================
# ERROR SUMMARY TESTS
# ==========================================

class TestGetErrorSummary:
    """Test get_error_summary method."""

    def test_empty_summary_with_no_errors(self):
        """Should return empty summary with no errors."""
        handler = LargeScaleErrorHandler()

        summary = handler.get_error_summary()

        assert summary["total_errors"] == 0
        assert summary["by_severity"] == {}
        assert summary["by_category"] == {}

    def test_summary_with_errors(self):
        """Should return correct summary with errors."""
        handler = LargeScaleErrorHandler()

        # Add some test errors
        from datetime import datetime

        handler.errors.append(ErrorContext(
            error_id="ERR_1",
            timestamp=datetime.now(),
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.MEMORY,
            message="Error 1",
            details={}
        ))

        handler.errors.append(ErrorContext(
            error_id="ERR_2",
            timestamp=datetime.now(),
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.NETWORK,
            message="Error 2",
            details={}
        ))

        summary = handler.get_error_summary()

        assert summary["total_errors"] == 2
        assert summary["by_severity"]["HIGH"] == 1
        assert summary["by_severity"]["MEDIUM"] == 1
        assert summary["by_category"]["MEMORY"] == 1
        assert summary["by_category"]["NETWORK"] == 1
        assert len(summary["recent_errors"]) == 2


# ==========================================
# EXPORT ERROR LOG TESTS
# ==========================================

class TestExportErrorLog:
    """Test export_error_log method."""

    def test_exports_error_log(self):
        """Should export error log to JSON file."""
        handler = LargeScaleErrorHandler()

        # Add a test error
        from datetime import datetime

        handler.errors.append(ErrorContext(
            error_id="ERR_1",
            timestamp=datetime.now(),
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.IO,
            message="Test error",
            details={"file": "test.txt"}
        ))

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            success = handler.export_error_log(tf.name)

            assert success is True
            assert Path(tf.name).exists()

            # Verify file contents
            import json
            with open(tf.name, 'r') as f:
                data = json.load(f)

            assert "summary" in data
            assert "errors" in data
            assert len(data["errors"]) == 1


# ==========================================
# GLOBAL ERROR HANDLER TESTS
# ==========================================

class TestGetGlobalErrorHandler:
    """Test get_global_error_handler function."""

    def test_creates_global_handler(self):
        """Should create global error handler."""
        handler = get_global_error_handler()

        assert handler is not None
        assert isinstance(handler, LargeScaleErrorHandler)

    def test_returns_same_instance(self):
        """Should return same global instance."""
        handler1 = get_global_error_handler()
        handler2 = get_global_error_handler()

        assert handler1 is handler2


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestLargeScaleErrorHandlerIntegration:
    """Test real-world error handling scenarios."""

    def test_complete_error_handling_workflow(self):
        """Test complete error handling workflow."""
        handler = LargeScaleErrorHandler()

        # Simulate error
        error = ValueError("Database connection failed")

        # Handle with recovery
        def recovery_strategy(err, ctx):
            # Simulate reconnection
            return {"status": "reconnected"}

        success, result = handler.handle_error(
            error=error,
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.HIGH,
            context={"database": "production", "attempt": 1},
            recovery_strategy=recovery_strategy
        )

        assert success is True
        assert result["status"] == "reconnected"

        # Check summary
        summary = handler.get_error_summary()
        assert summary["total_errors"] == 1
        assert summary["recovery_success_rate"] == 100.0

    def test_retry_with_exponential_backoff(self):
        """Test retry with exponential backoff."""
        handler = LargeScaleErrorHandler()

        attempts = {"count": 0}

        def unstable_operation():
            attempts["count"] += 1
            if attempts["count"] < 3:
                raise Exception("Temporary failure")
            return "Success"

        success, result, errors = handler.retry_with_backoff(
            operation=unstable_operation,
            operation_name="unstable_op",
            max_retries=5,
            initial_delay=0.01,
            exponential_base=2.0
        )

        assert success is True
        assert result == "Success"
        assert attempts["count"] == 3
        assert len(errors) == 2


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
