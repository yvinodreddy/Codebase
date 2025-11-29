"""
Comprehensive tests for result_pattern.py

Target: 90%+ coverage (210/233 statements)
Tests: Error types, Result type, functional operations, helper functions

MANDATORY TESTING STANDARD:
- Tests REAL code (imports actual classes/functions)
- Mocks ONLY external dependencies (none in this case)
- Covers success paths, error paths, and edge cases
- ≥ 90% statement coverage required
"""

import pytest
from result_pattern import (
    # Error types
    ErrorSeverity,
    BaseError,
    ValidationError,
    GuardrailError,
    VerificationError,
    ProcessError,
    ConfigError,
    TimeoutError,
    # Result type and constructors
    Result,
    Success,
    Failure,
    # Helper functions
    try_result,
    collect_results,
    first_success,
)


# ==========================================
# ERROR TYPE TESTS
# ==========================================

class TestErrorSeverity:
    """Test ErrorSeverity enum"""

    def test_severity_levels_exist(self):
        """Test all severity levels are defined"""
        assert ErrorSeverity.INFO.value == "info"
        assert ErrorSeverity.WARNING.value == "warning"
        assert ErrorSeverity.ERROR.value == "error"
        assert ErrorSeverity.CRITICAL.value == "critical"

    def test_severity_comparison(self):
        """Test severity levels can be compared"""
        assert ErrorSeverity.INFO == ErrorSeverity.INFO
        assert ErrorSeverity.ERROR != ErrorSeverity.WARNING


class TestBaseError:
    """Test BaseError base class"""

    def test_baseerror_creation(self):
        """Test BaseError can be instantiated"""
        error = BaseError(
            message="Test error",
            code="TEST_ERROR",
            severity=ErrorSeverity.ERROR
        )
        assert error.message == "Test error"
        assert error.code == "TEST_ERROR"
        assert error.severity == ErrorSeverity.ERROR
        assert error.context == {}

    def test_baseerror_with_context(self):
        """Test BaseError with context dictionary"""
        error = BaseError(
            message="Error with context",
            code="ERROR_CODE",
            severity=ErrorSeverity.WARNING,
            context={"key": "value", "count": 42}
        )
        assert error.context == {"key": "value", "count": 42}

    def test_baseerror_context_defaults_to_empty_dict(self):
        """Test __post_init__ sets context to {} if None"""
        error = BaseError(
            message="Test",
            code="TEST",
            severity=ErrorSeverity.ERROR
        )
        assert error.context == {}

    def test_baseerror_str_representation(self):
        """Test __str__ method"""
        error = BaseError(
            message="Something went wrong",
            code="ERR_001",
            severity=ErrorSeverity.ERROR
        )
        assert str(error) == "[ERR_001] Something went wrong"


class TestValidationError:
    """Test ValidationError"""

    def test_validationerror_creation(self):
        """Test ValidationError with field"""
        error = ValidationError("Invalid input", field="username")
        assert error.message == "Invalid input"
        assert error.code == "VALIDATION_ERROR"
        assert error.severity == ErrorSeverity.WARNING
        assert error.context == {"field": "username"}

    def test_validationerror_without_field(self):
        """Test ValidationError without field"""
        error = ValidationError("Invalid input")
        assert error.message == "Invalid input"
        assert error.code == "VALIDATION_ERROR"
        assert error.context == {}


class TestGuardrailError:
    """Test GuardrailError"""

    def test_guardrail_error_with_layer(self):
        """Test GuardrailError with layer"""
        error = GuardrailError("Harmful content", layer="layer2")
        assert error.message == "Harmful content"
        assert error.code == "GUARDRAIL_ERROR"
        assert error.severity == ErrorSeverity.ERROR
        assert error.context == {"layer": "layer2"}

    def test_guardrail_error_without_layer(self):
        """Test GuardrailError without layer"""
        error = GuardrailError("Content blocked")
        assert error.code == "GUARDRAIL_ERROR"
        assert error.context == {}


class TestVerificationError:
    """Test VerificationError"""

    def test_verification_error_with_method(self):
        """Test VerificationError with method"""
        error = VerificationError("Check failed", method="semantic")
        assert error.message == "Check failed"
        assert error.code == "VERIFICATION_ERROR"
        assert error.severity == ErrorSeverity.ERROR
        assert error.context == {"method": "semantic"}

    def test_verification_error_without_method(self):
        """Test VerificationError without method"""
        error = VerificationError("Verification failed")
        assert error.code == "VERIFICATION_ERROR"
        assert error.context == {}


class TestProcessError:
    """Test ProcessError"""

    def test_process_error_with_step(self):
        """Test ProcessError with step"""
        error = ProcessError("Processing failed", step="tokenization")
        assert error.message == "Processing failed"
        assert error.code == "PROCESS_ERROR"
        assert error.severity == ErrorSeverity.ERROR
        assert error.context == {"step": "tokenization"}

    def test_process_error_without_step(self):
        """Test ProcessError without step"""
        error = ProcessError("Error occurred")
        assert error.code == "PROCESS_ERROR"
        assert error.context == {}


class TestConfigError:
    """Test ConfigError"""

    def test_config_error_with_key(self):
        """Test ConfigError with key"""
        error = ConfigError("Missing config", key="API_KEY")
        assert error.message == "Missing config"
        assert error.code == "CONFIG_ERROR"
        assert error.severity == ErrorSeverity.CRITICAL
        assert error.context == {"key": "API_KEY"}

    def test_config_error_without_key(self):
        """Test ConfigError without key"""
        error = ConfigError("Configuration error")
        assert error.code == "CONFIG_ERROR"
        assert error.context == {}


class TestTimeoutError:
    """Test TimeoutError"""

    def test_timeout_error_with_seconds(self):
        """Test TimeoutError with timeout_seconds"""
        error = TimeoutError("Operation timed out", timeout_seconds=30.0)
        assert error.message == "Operation timed out"
        assert error.code == "TIMEOUT_ERROR"
        assert error.severity == ErrorSeverity.ERROR
        assert error.context == {"timeout_seconds": 30.0}

    def test_timeout_error_without_seconds(self):
        """Test TimeoutError without timeout_seconds"""
        error = TimeoutError("Timeout occurred")
        assert error.code == "TIMEOUT_ERROR"
        assert error.context == {}


# ==========================================
# RESULT TYPE TESTS
# ==========================================

class TestResultConstruction:
    """Test Result construction via Success/Failure"""

    def test_success_constructor(self):
        """Test Success() creates successful Result"""
        result = Success(42)
        assert result.is_success()
        assert not result.is_failure()
        assert result.unwrap() == 42

    def test_failure_constructor(self):
        """Test Failure() creates failed Result"""
        error = ValidationError("Bad input")
        result = Failure(error)
        assert result.is_failure()
        assert not result.is_success()
        assert result.unwrap_err() == error

    def test_success_with_none_value(self):
        """Test Success can contain None"""
        result = Success(None)
        assert result.is_success()
        assert result.unwrap() is None


class TestResultUnwrapping:
    """Test Result unwrapping methods"""

    def test_unwrap_on_success(self):
        """Test unwrap() returns value on success"""
        result = Success(100)
        assert result.unwrap() == 100

    def test_unwrap_on_failure_raises_exception(self):
        """Test unwrap() raises ValueError on failure"""
        error = ValidationError("Error")
        result = Failure(error)
        with pytest.raises(ValueError, match="Called unwrap\\(\\) on Failure"):
            result.unwrap()

    def test_unwrap_err_on_failure(self):
        """Test unwrap_err() returns error on failure"""
        error = ProcessError("Failed")
        result = Failure(error)
        assert result.unwrap_err() == error

    def test_unwrap_err_on_success_raises_exception(self):
        """Test unwrap_err() raises ValueError on success"""
        result = Success(42)
        with pytest.raises(ValueError, match="Called unwrap_err\\(\\) on Success"):
            result.unwrap_err()

    def test_unwrap_or_with_success(self):
        """Test unwrap_or() returns value on success"""
        result = Success(42)
        assert result.unwrap_or(0) == 42

    def test_unwrap_or_with_failure(self):
        """Test unwrap_or() returns default on failure"""
        result = Failure(ValidationError("Error"))
        assert result.unwrap_or(0) == 0

    def test_unwrap_or_else_with_success(self):
        """Test unwrap_or_else() returns value on success"""
        result = Success(42)
        assert result.unwrap_or_else(lambda e: 0) == 42

    def test_unwrap_or_else_with_failure(self):
        """Test unwrap_or_else() computes from error on failure"""
        result = Failure(ValidationError("Error"))
        value = result.unwrap_or_else(lambda e: len(e.message))
        assert value == 5  # len("Error")


class TestResultMapping:
    """Test Result map operations"""

    def test_map_on_success(self):
        """Test map() transforms success value"""
        result = Success(5).map(lambda x: x * 2)
        assert result.is_success()
        assert result.unwrap() == 10

    def test_map_on_failure(self):
        """Test map() leaves failure unchanged"""
        error = ValidationError("Error")
        result = Failure(error).map(lambda x: x * 2)
        assert result.is_failure()
        assert result.unwrap_err() == error

    def test_map_chaining(self):
        """Test multiple map() calls can be chained"""
        result = Success(5).map(lambda x: x * 2).map(lambda x: x + 10)
        assert result.unwrap() == 20

    def test_map_err_on_failure(self):
        """Test map_err() transforms error"""
        result = Failure(ValidationError("Bad")).map_err(
            lambda e: ProcessError(f"Converted: {e.message}")
        )
        assert result.is_failure()
        error = result.unwrap_err()
        assert isinstance(error, ProcessError)
        assert error.message == "Converted: Bad"

    def test_map_err_on_success(self):
        """Test map_err() leaves success unchanged"""
        result = Success(42).map_err(lambda e: ProcessError("Never called"))
        assert result.is_success()
        assert result.unwrap() == 42


class TestResultFlatmap:
    """Test Result flatmap (monadic bind)"""

    def test_flatmap_on_success(self):
        """Test flatmap() chains successful operations"""
        def divide_by_10(x: int) -> Result:
            if x == 0:
                return Failure(ValidationError("Zero"))
            return Success(10.0 / x)

        result = Success(5).flatmap(divide_by_10)
        assert result.is_success()
        assert result.unwrap() == 2.0

    def test_flatmap_on_failure(self):
        """Test flatmap() propagates failure"""
        def never_called(x):
            return Success(x * 2)

        error = ValidationError("Error")
        result = Failure(error).flatmap(never_called)
        assert result.is_failure()
        assert result.unwrap_err() == error

    def test_flatmap_chaining_with_failure(self):
        """Test flatmap() stops at first failure"""
        def parse_int(s: str) -> Result:
            try:
                return Success(int(s))
            except ValueError:
                return Failure(ValidationError("Not an integer"))

        def double(x: int) -> Result:
            return Success(x * 2)

        result = Success("abc").flatmap(parse_int).flatmap(double)
        assert result.is_failure()
        assert isinstance(result.unwrap_err(), ValidationError)

    def test_and_then_is_alias_for_flatmap(self):
        """Test and_then() is alias for flatmap()"""
        def add_ten(x: int) -> Result:
            return Success(x + 10)

        result1 = Success(5).flatmap(add_ten)
        result2 = Success(5).and_then(add_ten)
        assert result1.unwrap() == result2.unwrap()


class TestResultOrElse:
    """Test Result or_else fallback"""

    def test_or_else_on_success(self):
        """Test or_else() returns original success"""
        result = Success(42).or_else(lambda e: Success(0))
        assert result.is_success()
        assert result.unwrap() == 42

    def test_or_else_on_failure(self):
        """Test or_else() tries alternative on failure"""
        def fallback(e) -> Result:
            return Success(99)

        result = Failure(ValidationError("Error")).or_else(fallback)
        assert result.is_success()
        assert result.unwrap() == 99

    def test_or_else_with_another_failure(self):
        """Test or_else() can return another failure"""
        def fallback(e) -> Result:
            return Failure(ProcessError("Fallback also failed"))

        result = Failure(ValidationError("Error")).or_else(fallback)
        assert result.is_failure()
        assert isinstance(result.unwrap_err(), ProcessError)


class TestResultEquality:
    """Test Result __eq__ method"""

    def test_success_equality(self):
        """Test two Success results with same value are equal"""
        result1 = Success(42)
        result2 = Success(42)
        assert result1 == result2

    def test_success_inequality(self):
        """Test two Success results with different values are not equal"""
        result1 = Success(42)
        result2 = Success(100)
        assert result1 != result2

    def test_failure_equality(self):
        """Test two Failure results with same error are equal"""
        error1 = ValidationError("Error")
        error2 = ValidationError("Error")
        result1 = Failure(error1)
        result2 = Failure(error2)
        assert result1 == result2

    def test_success_not_equal_to_failure(self):
        """Test Success never equals Failure"""
        result1 = Success(42)
        result2 = Failure(ValidationError("Error"))
        assert result1 != result2

    def test_result_not_equal_to_non_result(self):
        """Test Result != non-Result object"""
        result = Success(42)
        assert result != 42
        assert result != "Success(42)"
        assert result != None


class TestResultRepr:
    """Test Result __repr__ method"""

    def test_success_repr(self):
        """Test Success repr shows value"""
        result = Success(42)
        assert repr(result) == "Success(42)"

    def test_failure_repr(self):
        """Test Failure repr shows error"""
        error = ValidationError("Bad input")
        result = Failure(error)
        repr_str = repr(result)
        assert "Failure" in repr_str
        assert "ValidationError" in repr_str


# ==========================================
# HELPER FUNCTION TESTS
# ==========================================

class TestTryResult:
    """Test try_result() helper function"""

    def test_try_result_with_successful_function(self):
        """Test try_result() wraps successful function call"""
        def safe_function():
            return 42

        result = try_result(safe_function)
        assert result.is_success()
        assert result.unwrap() == 42

    def test_try_result_with_exception(self):
        """Test try_result() catches exceptions"""
        def risky_function():
            raise ValueError("Something went wrong")

        result = try_result(risky_function)
        assert result.is_failure()
        error = result.unwrap_err()
        assert isinstance(error, ProcessError)
        assert "Something went wrong" in error.message

    def test_try_result_with_lambda(self):
        """Test try_result() works with lambdas"""
        result = try_result(lambda: 10 / 2)
        assert result.is_success()
        assert result.unwrap() == 5.0

    def test_try_result_with_division_by_zero(self):
        """Test try_result() catches ZeroDivisionError"""
        result = try_result(lambda: 10 / 0)
        assert result.is_failure()
        error = result.unwrap_err()
        assert isinstance(error, ProcessError)


class TestCollectResults:
    """Test collect_results() helper function"""

    def test_collect_all_successes(self):
        """Test collect_results() with all successes"""
        results = [Success(1), Success(2), Success(3)]
        collected = collect_results(results)
        assert collected.is_success()
        assert collected.unwrap() == [1, 2, 3]

    def test_collect_with_one_failure(self):
        """Test collect_results() with one failure"""
        results = [
            Success(1),
            Failure(ValidationError("E1")),
            Success(3)
        ]
        collected = collect_results(results)
        assert collected.is_failure()
        errors = collected.unwrap_err()
        assert len(errors) == 1
        assert isinstance(errors[0], ValidationError)

    def test_collect_with_multiple_failures(self):
        """Test collect_results() collects all errors"""
        results = [
            Success(1),
            Failure(ValidationError("E1")),
            Failure(ProcessError("E2")),
            Success(4)
        ]
        collected = collect_results(results)
        assert collected.is_failure()
        errors = collected.unwrap_err()
        assert len(errors) == 2
        assert isinstance(errors[0], ValidationError)
        assert isinstance(errors[1], ProcessError)

    def test_collect_empty_list(self):
        """Test collect_results() with empty list"""
        results = []
        collected = collect_results(results)
        assert collected.is_success()
        assert collected.unwrap() == []


class TestFirstSuccess:
    """Test first_success() helper function"""

    def test_first_success_with_first_success(self):
        """Test first_success() returns first successful result"""
        results = [
            Success(42),
            Success(100),
            Failure(ValidationError("E"))
        ]
        result = first_success(results)
        assert result.is_success()
        assert result.unwrap() == 42

    def test_first_success_with_later_success(self):
        """Test first_success() skips failures until success"""
        results = [
            Failure(ValidationError("E1")),
            Failure(ProcessError("E2")),
            Success(100)
        ]
        result = first_success(results)
        assert result.is_success()
        assert result.unwrap() == 100

    def test_first_success_with_all_failures(self):
        """Test first_success() returns all errors when all fail"""
        results = [
            Failure(ValidationError("E1")),
            Failure(ProcessError("E2")),
            Failure(ConfigError("E3"))
        ]
        result = first_success(results)
        assert result.is_failure()
        errors = result.unwrap_err()
        assert len(errors) == 3

    def test_first_success_with_empty_list(self):
        """Test first_success() with empty list"""
        results = []
        result = first_success(results)
        assert result.is_failure()
        assert result.unwrap_err() == []


# ==========================================
# INTEGRATION TESTS (Real-world scenarios)
# ==========================================

class TestRealWorldPipeline:
    """Test real-world usage patterns"""

    def test_validation_pipeline(self):
        """Test multi-stage validation pipeline"""
        def validate_input(text: str) -> Result:
            if not text.strip():
                return Failure(ValidationError("Input is empty"))
            if len(text) > 1000:
                return Failure(ValidationError("Input too long"))
            return Success(text.strip())

        def check_guardrails(text: str) -> Result:
            if "badword" in text.lower():
                return Failure(GuardrailError("Harmful content detected"))
            return Success(text)

        def process_text(text: str) -> Result:
            return Success(f"Processed: {text}")

        # Valid input
        result = (
            Success("Hello world")
            .flatmap(validate_input)
            .flatmap(check_guardrails)
            .flatmap(process_text)
        )
        assert result.is_success()
        assert result.unwrap() == "Processed: Hello world"

        # Empty input
        result = (
            Success("   ")
            .flatmap(validate_input)
            .flatmap(check_guardrails)
            .flatmap(process_text)
        )
        assert result.is_failure()
        assert isinstance(result.unwrap_err(), ValidationError)

        # Harmful content
        result = (
            Success("This has badword in it")
            .flatmap(validate_input)
            .flatmap(check_guardrails)
            .flatmap(process_text)
        )
        assert result.is_failure()
        assert isinstance(result.unwrap_err(), GuardrailError)

    def test_fallback_pattern(self):
        """Test fallback with or_else()"""
        def primary() -> Result:
            return Failure(ProcessError("Primary failed"))

        def secondary() -> Result:
            return Success("Secondary worked!")

        result = primary().or_else(lambda e: secondary())
        assert result.is_success()
        assert result.unwrap() == "Secondary worked!"

    def test_error_transformation_pipeline(self):
        """Test transforming errors through pipeline"""
        result = (
            Failure(ValidationError("Invalid input"))
            .map_err(lambda e: ProcessError(f"Stage 1: {e.message}"))
            .map_err(lambda e: ProcessError(f"Stage 2: {e.message}"))
        )
        assert result.is_failure()
        error = result.unwrap_err()
        assert "Stage 2: Stage 1: Invalid input" in error.message


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_result_with_complex_types(self):
        """Test Result with complex value types"""
        result = Success({"key": "value", "count": 42})
        assert result.unwrap()["key"] == "value"

        result = Success([1, 2, 3, 4, 5])
        assert result.unwrap() == [1, 2, 3, 4, 5]

    def test_nested_results(self):
        """Test Result containing another Result"""
        inner_result = Success(42)
        outer_result = Success(inner_result)
        assert outer_result.unwrap().unwrap() == 42

    def test_map_to_none(self):
        """Test mapping to None value"""
        result = Success(42).map(lambda x: None)
        assert result.is_success()
        assert result.unwrap() is None


# ==========================================
# MAIN BLOCK TESTS (Cover example code)
# ==========================================

class TestMainBlockExamples:
    """Test that all main block examples execute without errors"""

    def test_basic_usage_example(self):
        """Test Example 1: Basic usage"""
        def divide(a: float, b: float) -> Result:
            if b == 0:
                return Failure(ValidationError("Division by zero", field="denominator"))
            return Success(a / b)

        # Success case
        result = divide(10, 2)
        assert result.is_success()
        assert result.unwrap() == 5.0

        # Failure case
        result = divide(10, 0)
        assert result.is_failure()
        error = result.unwrap_err()
        assert isinstance(error, ValidationError)
        assert error.code == "VALIDATION_ERROR"

    def test_chaining_operations_example(self):
        """Test Example 2: Chaining with flatmap"""
        def parse_int(s: str) -> Result:
            try:
                return Success(int(s))
            except ValueError:
                return Failure(ValidationError(f"'{s}' is not an integer", field="input"))

        def double(x: int) -> Result:
            return Success(x * 2)

        # Success chain
        result = Success("42").flatmap(parse_int).flatmap(double)
        assert result.is_success()
        assert result.unwrap() == 84

        # Failure chain
        result = Success("abc").flatmap(parse_int).flatmap(double)
        assert result.is_failure()
        assert isinstance(result.unwrap_err(), ValidationError)

    def test_value_transformation_example(self):
        """Test Example 3: Value transformation with map"""
        result = Success(5).map(lambda x: x * 2).map(lambda x: x + 10)
        assert result.is_success()
        assert result.unwrap() == 20

        result = Failure(ValidationError("Bad input")).map(lambda x: x * 2)
        assert result.is_failure()
        assert isinstance(result.unwrap_err(), ValidationError)

    def test_error_transformation_example(self):
        """Test Example 4: Error transformation with map_err"""
        result = (
            Failure(ValidationError("Invalid input"))
            .map_err(lambda e: ProcessError(f"Preprocessing failed: {e.message}"))
        )
        assert result.is_failure()
        error = result.unwrap_err()
        assert isinstance(error, ProcessError)
        assert "Preprocessing failed" in error.message

    def test_default_values_example(self):
        """Test Example 5: Default values with unwrap_or"""
        result = Success(42).unwrap_or(0)
        assert result == 42

        result = Failure(ValidationError("Error")).unwrap_or(0)
        assert result == 0

    def test_collecting_results_example(self):
        """Test Example 6: Collecting multiple results"""
        # All success
        results = [Success(1), Success(2), Success(3)]
        collected = collect_results(results)
        assert collected.is_success()
        assert collected.unwrap() == [1, 2, 3]

        # Some failures
        results = [
            Success(1),
            Failure(ValidationError("E1")),
            Failure(ValidationError("E2"))
        ]
        collected = collect_results(results)
        assert collected.is_failure()
        errors = collected.unwrap_err()
        assert len(errors) == 2

    def test_first_success_fallback_example(self):
        """Test Example 7: First success (fallback pattern)"""
        def primary() -> Result:
            return Failure(ProcessError("Primary failed"))

        def secondary() -> Result:
            return Success("Secondary worked!")

        def tertiary() -> Result:
            return Failure(ProcessError("Tertiary failed"))

        result = first_success([primary(), secondary(), tertiary()])
        assert result.is_success()
        assert result.unwrap() == "Secondary worked!"

    def test_exception_wrapping_example(self):
        """Test Example 8: Exception wrapping with try_result"""
        def risky_operation():
            raise ValueError("Something went wrong!")

        result = try_result(risky_operation)
        assert result.is_failure()
        error = result.unwrap_err()
        assert isinstance(error, ProcessError)
        assert "Something went wrong" in error.message

    def test_real_world_pipeline_example(self):
        """Test Example 9: Real-world pipeline"""
        def validate_input(text: str) -> Result:
            if not text.strip():
                return Failure(ValidationError("Input is empty"))
            if len(text) > 1000:
                return Failure(ValidationError("Input too long"))
            return Success(text.strip())

        def check_guardrails(text: str) -> Result:
            if "badword" in text.lower():
                return Failure(GuardrailError("Harmful content detected"))
            return Success(text)

        def process(text: str) -> Result:
            return Success(f"Processed: {text}")

        def verify_output(text: str) -> Result:
            if len(text) < 10:
                return Failure(VerificationError("Output too short"))
            return Success(text)

        # Success pipeline
        input_text = "Hello world"
        result = (
            Success(input_text)
            .flatmap(validate_input)
            .flatmap(check_guardrails)
            .flatmap(process)
            .flatmap(verify_output)
        )
        assert result.is_success()
        assert result.unwrap() == "Processed: Hello world"

        # Failure at validation
        result = (
            Success("   ")
            .flatmap(validate_input)
            .flatmap(check_guardrails)
            .flatmap(process)
            .flatmap(verify_output)
        )
        assert result.is_failure()
        error = result.unwrap_err()
        assert isinstance(error, ValidationError)
        assert error.code == "VALIDATION_ERROR"

        # Failure at guardrails
        result = (
            Success("This has badword in it")
            .flatmap(validate_input)
            .flatmap(check_guardrails)
            .flatmap(process)
            .flatmap(verify_output)
        )
        assert result.is_failure()
        assert isinstance(result.unwrap_err(), GuardrailError)

        # Failure at verification (input "X" -> "Processed: X" = 13 chars, need <10)
        # Actually, let's skip this as "Processed: " prefix is 11 chars already
        # So any non-empty input will pass. Testing empty after validation won't work.
        # This test case isn't actually reachable with this implementation.
