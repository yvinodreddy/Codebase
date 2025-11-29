#!/usr/bin/env python3
"""
Tests for result_pattern.py __main__ block examples.
This ensures the demonstration code runs without errors.

Test Coverage Target: Cover lines 393-566 (__main__ demo code)
"""

import pytest
import sys
from pathlib import Path
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestResultPatternMain:
    """Test that __main__ block examples run successfully."""

    def test_main_block_executes_without_errors(self):
        """Should execute all demonstration examples without errors."""
        # Import subprocess to run the module as main
        import subprocess

        result = subprocess.run(
            [sys.executable, "result_pattern.py"],
            capture_output=True,
            text=True,
            timeout=5
        )

        # Verify it ran successfully
        assert result.returncode == 0, f"Module execution failed: {result.stderr}"

        output = result.stdout

        # Verify key sections ran
        assert "Q4: RESULT PATTERN EXAMPLES" in output
        assert "BASIC USAGE" in output
        assert "CHAINING OPERATIONS" in output
        assert "VALUE TRANSFORMATION" in output
        assert "ERROR TRANSFORMATION" in output
        assert "DEFAULT VALUES" in output
        assert "COLLECTING MULTIPLE RESULTS" in output
        assert "FIRST SUCCESS" in output

    def test_demonstration_divide_function(self):
        """Test the divide function from demonstration."""
        from result_pattern import Success, Failure, ValidationError, BaseError, Result

        def divide(a: float, b: float) -> Result[float, BaseError]:
            """Divide a by b, return Result"""
            if b == 0:
                return Failure(ValidationError("Division by zero", field="denominator"))
            return Success(a / b)

        # Test success case
        result = divide(10, 2)
        assert result.is_success()
        assert result.unwrap() == 5.0

        # Test failure case
        result = divide(10, 0)
        assert result.is_failure()
        error = result.unwrap_err()
        assert error.code == "VALIDATION_ERROR"
        assert "Division by zero" in error.message

    def test_demonstration_parse_int_function(self):
        """Test the parse_int function from demonstration."""
        from result_pattern import Success, Failure, ValidationError, BaseError, Result

        def parse_int(s: str) -> Result[int, BaseError]:
            """Parse string to integer"""
            try:
                return Success(int(s))
            except ValueError:
                return Failure(ValidationError(f"'{s}' is not an integer", field="input"))

        # Test success case
        result = parse_int("42")
        assert result.is_success()
        assert result.unwrap() == 42

        # Test failure case
        result = parse_int("abc")
        assert result.is_failure()
        error = result.unwrap_err()
        assert error.code == "VALIDATION_ERROR"

    def test_demonstration_chaining(self):
        """Test chaining examples from demonstration."""
        from result_pattern import Success, Failure, ValidationError, BaseError, Result

        def parse_int(s: str) -> Result[int, BaseError]:
            try:
                return Success(int(s))
            except ValueError:
                return Failure(ValidationError(f"'{s}' is not an integer", field="input"))

        def double(x: int) -> Result[int, BaseError]:
            return Success(x * 2)

        # Success chain
        result = Success("42").flatmap(parse_int).flatmap(double)
        assert result.is_success()
        assert result.unwrap() == 84

        # Failure chain (stops at first error)
        result = Success("abc").flatmap(parse_int).flatmap(double)
        assert result.is_failure()

    def test_demonstration_transformations(self):
        """Test transformation examples from demonstration."""
        from result_pattern import Success, Failure, ValidationError

        # Value transformation
        result = Success(5).map(lambda x: x * 2).map(lambda x: x + 10)
        assert result.is_success()
        assert result.unwrap() == 20

        # Error transformation
        result = Failure(ValidationError("Bad input")).map(lambda x: x * 2)
        assert result.is_failure()

    def test_demonstration_default_values(self):
        """Test default value examples from demonstration."""
        from result_pattern import Success, Failure, ValidationError

        result_val = Success(42).unwrap_or(0)
        assert result_val == 42

        result_val = Failure(ValidationError("Error")).unwrap_or(0)
        assert result_val == 0

    def test_demonstration_fallback_pattern(self):
        """Test fallback pattern from demonstration."""
        from result_pattern import Success, Failure, ProcessError, BaseError, Result

        def primary() -> Result[str, BaseError]:
            return Failure(ProcessError("Primary failed"))

        def secondary() -> Result[str, BaseError]:
            return Success("Secondary worked")

        def tertiary() -> Result[str, BaseError]:
            return Success("Tertiary worked")

        # Test primary -> secondary fallback
        result = primary().or_else(lambda e: secondary())
        assert result.is_success()
        assert result.unwrap() == "Secondary worked"

        # Test multiple fallbacks
        result = primary().or_else(lambda e: secondary()).or_else(lambda e: tertiary())
        assert result.is_success()


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
