#!/usr/bin/env python3
"""
Unit Tests for result_pattern.py
Tests the Result<T, E> pattern for explicit error handling.

Test Coverage Target: 90%+ (comprehensive coverage of all Result methods)
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from result_pattern import (
    Result,
    Success,
    Failure,
    BaseError,
    ValidationError,
    GuardrailError,
    VerificationError,
    ProcessError,
    ConfigError,
    TimeoutError,
    ErrorSeverity,
    try_result,
    collect_results,
    first_success,
)


# ==========================================
# ERROR TYPE TESTS
# ==========================================

class TestErrorTypes:
    """Test error type classes."""

    def test_base_error_creation(self):
        """BaseError should be created with message and code."""
        error = BaseError(
            message="Test error",
            code="TEST_ERROR",
            severity=ErrorSeverity.ERROR
        )
        assert error.message == "Test error"
        assert error.code == "TEST_ERROR"
        assert error.severity == ErrorSeverity.ERROR
        assert error.context == {}

    def test_base_error_with_context(self):
        """BaseError should support context dictionary."""
        error = BaseError(
            message="Test error",
            code="TEST_ERROR",
            context={"key": "value"}
        )
        assert error.context["key"] == "value"

    def test_base_error_str(self):
        """BaseError __str__ should format as [CODE] message."""
        error = BaseError(message="Test error", code="TEST_ERROR")
        assert str(error) == "[TEST_ERROR] Test error"

    def test_validation_error_creation(self):
        """ValidationError should have correct code and severity."""
        error = ValidationError("Invalid input", field="username")
        assert error.code == "VALIDATION_ERROR"
        assert error.severity == ErrorSeverity.WARNING
        assert error.context["field"] == "username"

    def test_validation_error_without_field(self):
        """ValidationError should work without field parameter."""
        error = ValidationError("Invalid input")
        assert error.code == "VALIDATION_ERROR"
        assert error.context == {}

    def test_guardrail_error_creation(self):
        """GuardrailError should have correct code and severity."""
        error = GuardrailError("Harmful content", layer="Layer 3")
        assert error.code == "GUARDRAIL_ERROR"
        assert error.severity == ErrorSeverity.ERROR
        assert error.context["layer"] == "Layer 3"

    def test_verification_error_creation(self):
        """VerificationError should have correct code and severity."""
        error = VerificationError("Output invalid", method="structural")
        assert error.code == "VERIFICATION_ERROR"
        assert error.severity == ErrorSeverity.ERROR
        assert error.context["method"] == "structural"

    def test_process_error_creation(self):
        """ProcessError should have correct code and severity."""
        error = ProcessError("Processing failed", step="tokenization")
        assert error.code == "PROCESS_ERROR"
        assert error.severity == ErrorSeverity.ERROR
        assert error.context["step"] == "tokenization"

    def test_config_error_creation(self):
        """ConfigError should have CRITICAL severity."""
        error = ConfigError("Invalid config", key="API_KEY")
        assert error.code == "CONFIG_ERROR"
        assert error.severity == ErrorSeverity.CRITICAL
        assert error.context["key"] == "API_KEY"

    def test_timeout_error_creation(self):
        """TimeoutError should store timeout duration."""
        error = TimeoutError("Request timeout", timeout_seconds=5.0)
        assert error.code == "TIMEOUT_ERROR"
        assert error.severity == ErrorSeverity.ERROR
        assert error.context["timeout_seconds"] == 5.0


# ==========================================
# RESULT CONSTRUCTORS
# ==========================================

class TestResultConstructors:
    """Test Success() and Failure() constructors."""

    def test_success_creation(self):
        """Success() should create successful result."""
        result = Success(42)
        assert result.is_success()
        assert not result.is_failure()

    def test_success_with_none_value(self):
        """Success(None) should be valid (None can be a value)."""
        result = Success(None)
        assert result.is_success()
        assert result.unwrap() is None

    def test_failure_creation(self):
        """Failure() should create failed result."""
        error = ValidationError("Bad input")
        result = Failure(error)
        assert result.is_failure()
        assert not result.is_success()

    def test_success_type_generic(self):
        """Success should work with any type."""
        result_int = Success(42)
        result_str = Success("hello")
        result_list = Success([1, 2, 3])
        result_dict = Success({"key": "value"})

        assert result_int.unwrap() == 42
        assert result_str.unwrap() == "hello"
        assert result_list.unwrap() == [1, 2, 3]
        assert result_dict.unwrap() == {"key": "value"}


# ==========================================
# RESULT METHODS - BASIC
# ==========================================

class TestResultBasicMethods:
    """Test basic Result methods (is_success, is_failure, unwrap, etc.)."""

    def test_is_success_on_success(self):
        """is_success() should return True for Success."""
        result = Success(42)
        assert result.is_success() is True

    def test_is_success_on_failure(self):
        """is_success() should return False for Failure."""
        result = Failure(ValidationError("Error"))
        assert result.is_success() is False

    def test_is_failure_on_success(self):
        """is_failure() should return False for Success."""
        result = Success(42)
        assert result.is_failure() is False

    def test_is_failure_on_failure(self):
        """is_failure() should return True for Failure."""
        result = Failure(ValidationError("Error"))
        assert result.is_failure() is True

    def test_unwrap_on_success(self):
        """unwrap() should return value for Success."""
        result = Success(42)
        assert result.unwrap() == 42

    def test_unwrap_on_failure_raises(self):
        """unwrap() should raise ValueError for Failure."""
        result = Failure(ValidationError("Error"))
        with pytest.raises(ValueError, match="Called unwrap\\(\\) on Failure"):
            result.unwrap()

    def test_unwrap_err_on_failure(self):
        """unwrap_err() should return error for Failure."""
        error = ValidationError("Test error")
        result = Failure(error)
        assert result.unwrap_err() == error

    def test_unwrap_err_on_success_raises(self):
        """unwrap_err() should raise ValueError for Success."""
        result = Success(42)
        with pytest.raises(ValueError, match="Called unwrap_err\\(\\) on Success"):
            result.unwrap_err()

    def test_unwrap_or_on_success(self):
        """unwrap_or() should return value for Success."""
        result = Success(42)
        assert result.unwrap_or(0) == 42

    def test_unwrap_or_on_failure(self):
        """unwrap_or() should return default for Failure."""
        result = Failure(ValidationError("Error"))
        assert result.unwrap_or(0) == 0

    def test_unwrap_or_else_on_success(self):
        """unwrap_or_else() should return value for Success."""
        result = Success(42)
        assert result.unwrap_or_else(lambda e: 0) == 42

    def test_unwrap_or_else_on_failure(self):
        """unwrap_or_else() should compute from error for Failure."""
        result = Failure(ValidationError("Error"))
        assert result.unwrap_or_else(lambda e: len(e.message)) == 5  # len("Error")


# ==========================================
# RESULT METHODS - TRANSFORMATIONS
# ==========================================

class TestResultTransformations:
    """Test Result transformation methods (map, map_err, flatmap, etc.)."""

    def test_map_on_success(self):
        """map() should transform success value."""
        result = Success(5).map(lambda x: x * 2)
        assert result.is_success()
        assert result.unwrap() == 10

    def test_map_on_failure(self):
        """map() should leave failure unchanged."""
        error = ValidationError("Error")
        result = Failure(error).map(lambda x: x * 2)
        assert result.is_failure()
        assert result.unwrap_err() == error

    def test_map_chaining(self):
        """map() should support chaining."""
        result = Success(5).map(lambda x: x * 2).map(lambda x: x + 10)
        assert result.unwrap() == 20

    def test_map_err_on_success(self):
        """map_err() should leave success unchanged."""
        result = Success(42).map_err(lambda e: ProcessError("New error"))
        assert result.is_success()
        assert result.unwrap() == 42

    def test_map_err_on_failure(self):
        """map_err() should transform error."""
        result = Failure(ValidationError("Bad")).map_err(
            lambda e: ProcessError(f"Wrapped: {e.message}")
        )
        assert result.is_failure()
        error = result.unwrap_err()
        assert isinstance(error, ProcessError)
        assert "Wrapped: Bad" in error.message

    def test_flatmap_on_success_to_success(self):
        """flatmap() should chain successful operations."""
        def double(x: int) -> Result[int, BaseError]:
            return Success(x * 2)

        result = Success(5).flatmap(double)
        assert result.is_success()
        assert result.unwrap() == 10

    def test_flatmap_on_success_to_failure(self):
        """flatmap() should propagate failure from chained operation."""
        def validate(x: int) -> Result[int, BaseError]:
            if x < 0:
                return Failure(ValidationError("Negative"))
            return Success(x)

        result = Success(-5).flatmap(validate)
        assert result.is_failure()
        assert result.unwrap_err().code == "VALIDATION_ERROR"

    def test_flatmap_on_failure(self):
        """flatmap() should leave failure unchanged."""
        error = ValidationError("Error")
        result = Failure(error).flatmap(lambda x: Success(x * 2))
        assert result.is_failure()
        assert result.unwrap_err() == error

    def test_flatmap_chaining(self):
        """flatmap() should support complex chaining."""
        def parse_int(s: str) -> Result[int, BaseError]:
            try:
                return Success(int(s))
            except ValueError:
                return Failure(ValidationError("Not an integer"))

        def divide_by_10(x: int) -> Result[float, BaseError]:
            if x == 0:
                return Failure(ValidationError("Zero"))
            return Success(10.0 / x)

        result = Success("5").flatmap(parse_int).flatmap(divide_by_10)
        assert result.is_success()
        assert result.unwrap() == 2.0

    def test_and_then_alias(self):
        """and_then() should work as flatmap() alias."""
        def double(x: int) -> Result[int, BaseError]:
            return Success(x * 2)

        result = Success(5).and_then(double)
        assert result.unwrap() == 10

    def test_or_else_on_success(self):
        """or_else() should leave success unchanged."""
        result = Success(42).or_else(lambda e: Success(0))
        assert result.is_success()
        assert result.unwrap() == 42

    def test_or_else_on_failure(self):
        """or_else() should provide fallback for failure."""
        def fallback(e: BaseError) -> Result[int, BaseError]:
            return Success(0)

        result = Failure(ValidationError("Error")).or_else(fallback)
        assert result.is_success()
        assert result.unwrap() == 0


# ==========================================
# RESULT EQUALITY AND REPR
# ==========================================

class TestResultEquality:
    """Test Result equality and representation."""

    def test_success_equality(self):
        """Two Success with same value should be equal."""
        result1 = Success(42)
        result2 = Success(42)
        assert result1 == result2

    def test_success_inequality(self):
        """Two Success with different values should not be equal."""
        result1 = Success(42)
        result2 = Success(100)
        assert result1 != result2

    def test_failure_equality(self):
        """Two Failure with same error should be equal."""
        error = ValidationError("Error")
        result1 = Failure(error)
        result2 = Failure(error)
        assert result1 == result2

    def test_success_failure_inequality(self):
        """Success and Failure should not be equal."""
        result1 = Success(42)
        result2 = Failure(ValidationError("Error"))
        assert result1 != result2

    def test_result_not_equal_to_non_result(self):
        """Result should not be equal to non-Result types."""
        result = Success(42)
        assert result != 42
        assert result != "42"
        assert result != None

    def test_success_repr(self):
        """Success __repr__ should show value."""
        result = Success(42)
        assert repr(result) == "Success(42)"

    def test_failure_repr(self):
        """Failure __repr__ should show error."""
        error = ValidationError("Test")
        result = Failure(error)
        assert "Failure" in repr(result)
        assert "ValidationError" in repr(result)


# ==========================================
# HELPER FUNCTIONS
# ==========================================

class TestHelperFunctions:
    """Test helper functions (try_result, collect_results, first_success)."""

    def test_try_result_success(self):
        """try_result() should return Success for successful function."""
        def safe_operation():
            return 42

        result = try_result(safe_operation)
        assert result.is_success()
        assert result.unwrap() == 42

    def test_try_result_exception(self):
        """try_result() should catch exceptions and return Failure."""
        def risky_operation():
            raise ValueError("Something went wrong")

        result = try_result(risky_operation)
        assert result.is_failure()
        error = result.unwrap_err()
        assert isinstance(error, ProcessError)
        assert "Something went wrong" in error.message

    def test_collect_results_all_success(self):
        """collect_results() should return Success with all values if all succeed."""
        results = [Success(1), Success(2), Success(3)]
        collected = collect_results(results)
        assert collected.is_success()
        assert collected.unwrap() == [1, 2, 3]

    def test_collect_results_some_failures(self):
        """collect_results() should return Failure with all errors if any fail."""
        error1 = ValidationError("E1")
        error2 = ValidationError("E2")
        results = [Success(1), Failure(error1), Failure(error2)]
        collected = collect_results(results)
        assert collected.is_failure()
        errors = collected.unwrap_err()
        assert len(errors) == 2
        assert error1 in errors
        assert error2 in errors

    def test_collect_results_empty_list(self):
        """collect_results() should handle empty list."""
        results = []
        collected = collect_results(results)
        assert collected.is_success()
        assert collected.unwrap() == []

    def test_first_success_finds_first(self):
        """first_success() should return first successful result."""
        error1 = ValidationError("E1")
        results = [Failure(error1), Success(42), Success(100)]
        result = first_success(results)
        assert result.is_success()
        assert result.unwrap() == 42

    def test_first_success_all_failures(self):
        """first_success() should return all errors if all fail."""
        error1 = ValidationError("E1")
        error2 = ValidationError("E2")
        results = [Failure(error1), Failure(error2)]
        result = first_success(results)
        assert result.is_failure()
        errors = result.unwrap_err()
        assert len(errors) == 2

    def test_first_success_empty_list(self):
        """first_success() should return Failure for empty list."""
        results = []
        result = first_success(results)
        assert result.is_failure()
        errors = result.unwrap_err()
        assert errors == []


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestResultPatternIntegration:
    """Test real-world usage patterns."""

    def test_validation_pipeline(self):
        """Test validation pipeline with multiple stages."""
        def validate_input(text: str) -> Result[str, BaseError]:
            if not text.strip():
                return Failure(ValidationError("Input is empty"))
            return Success(text.strip())

        def check_length(text: str) -> Result[str, BaseError]:
            if len(text) > 100:
                return Failure(ValidationError("Input too long"))
            return Success(text)

        def process(text: str) -> Result[str, BaseError]:
            return Success(f"Processed: {text}")

        # Valid input
        result = (
            Success("hello")
            .flatmap(validate_input)
            .flatmap(check_length)
            .flatmap(process)
        )
        assert result.is_success()
        assert "Processed: hello" in result.unwrap()

        # Empty input (fails at first stage)
        result = (
            Success("   ")
            .flatmap(validate_input)
            .flatmap(check_length)
            .flatmap(process)
        )
        assert result.is_failure()
        assert result.unwrap_err().code == "VALIDATION_ERROR"

    def test_fallback_pattern(self):
        """Test fallback pattern with or_else()."""
        def primary() -> Result[str, BaseError]:
            return Failure(ProcessError("Primary failed"))

        def secondary() -> Result[str, BaseError]:
            return Success("Secondary worked")

        result = primary().or_else(lambda e: secondary())
        assert result.is_success()
        assert result.unwrap() == "Secondary worked"

    def test_error_transformation_chain(self):
        """Test transforming errors through pipeline."""
        result = (
            Failure(ValidationError("Bad input"))
            .map_err(lambda e: ProcessError(f"Step 1: {e.message}"))
            .map_err(lambda e: ProcessError(f"Step 2: {e.message}"))
        )
        assert result.is_failure()
        error = result.unwrap_err()
        assert "Step 2: Step 1: Bad input" in error.message

    def test_mixed_map_and_flatmap(self):
        """Test combining map() and flatmap() operations."""
        def parse_int(s: str) -> Result[int, BaseError]:
            try:
                return Success(int(s))
            except ValueError:
                return Failure(ValidationError("Not an integer"))

        result = (
            Success("42")
            .flatmap(parse_int)  # Parse to int
            .map(lambda x: x * 2)  # Double it
            .map(lambda x: x + 10)  # Add 10
        )
        assert result.is_success()
        assert result.unwrap() == 94  # (42 * 2) + 10


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
