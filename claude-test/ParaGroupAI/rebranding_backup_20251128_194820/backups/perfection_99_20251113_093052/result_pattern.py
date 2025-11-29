"""
Q4: Standardized Error Handling with Result Pattern
Replaces exceptions and error tuples with explicit Result<T, E> types

BEFORE (inconsistent error handling):
    def process():
        try:
            return do_work()  # or None? or raise? unclear
        except Exception as e:
            return None  # Lost error context!

    result = process()
    if result is None:  # Was it error or valid None?
        ...

AFTER (explicit Result pattern):
    def process() -> Result[Output, Error]:
        try:
            output = do_work()
            return Success(output)
        except Exception as e:
            return Failure(ProcessError(str(e)))

    result = process()
    if result.is_success():
        output = result.unwrap()
    else:
        error = result.unwrap_err()
        handle_error(error)

BENEFITS:
- No silent failures (Result is always checked)
- Explicit error types (no mystery exceptions)
- Functional programming style (map, flatmap, etc.)
- No try/except spaghetti
- Self-documenting (return type shows it can fail)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable, Union, Optional, Any
from enum import Enum


# ==========================================
# TYPE VARIABLES
# ==========================================

T = TypeVar('T')  # Success value type
E = TypeVar('E')  # Error type
U = TypeVar('U')  # Mapped value type


# ==========================================
# ERROR TYPES
# ==========================================

class ErrorSeverity(Enum):
    """Error severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class BaseError:
    """
    Base class for all errors in Result pattern.

    Attributes:
        message: Human-readable error message
        code: Machine-readable error code
        severity: Error severity level
        context: Additional context (metadata)
    """
    message: str
    code: str
    severity: ErrorSeverity = ErrorSeverity.ERROR
    context: dict[str, Any] = None

    def __post_init__(self):
        if self.context is None:
            self.context = {}

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


@dataclass
class ValidationError(BaseError):
    """Input validation failed"""
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            severity=ErrorSeverity.WARNING,
            context={"field": field} if field else {}
        )


@dataclass
class GuardrailError(BaseError):
    """Guardrail validation failed"""
    def __init__(self, message: str, layer: Optional[str] = None):
        super().__init__(
            message=message,
            code="GUARDRAIL_ERROR",
            severity=ErrorSeverity.ERROR,
            context={"layer": layer} if layer else {}
        )


@dataclass
class VerificationError(BaseError):
    """Output verification failed"""
    def __init__(self, message: str, method: Optional[str] = None):
        super().__init__(
            message=message,
            code="VERIFICATION_ERROR",
            severity=ErrorSeverity.ERROR,
            context={"method": method} if method else {}
        )


@dataclass
class ProcessError(BaseError):
    """General processing error"""
    def __init__(self, message: str, step: Optional[str] = None):
        super().__init__(
            message=message,
            code="PROCESS_ERROR",
            severity=ErrorSeverity.ERROR,
            context={"step": step} if step else {}
        )


@dataclass
class ConfigError(BaseError):
    """Configuration error"""
    def __init__(self, message: str, key: Optional[str] = None):
        super().__init__(
            message=message,
            code="CONFIG_ERROR",
            severity=ErrorSeverity.CRITICAL,
            context={"key": key} if key else {}
        )


@dataclass
class TimeoutError(BaseError):
    """Operation timeout"""
    def __init__(self, message: str, timeout_seconds: Optional[float] = None):
        super().__init__(
            message=message,
            code="TIMEOUT_ERROR",
            severity=ErrorSeverity.ERROR,
            context={"timeout_seconds": timeout_seconds} if timeout_seconds else {}
        )


# ==========================================
# RESULT TYPE
# ==========================================

class Result(Generic[T, E]):
    """
    Q4: Result<T, E> type for explicit error handling.

    A Result is either:
    - Success(value: T): Operation succeeded with value
    - Failure(error: E): Operation failed with error

    This replaces:
    - try/except blocks
    - None returns
    - Tuple returns (value, error)
    - Boolean flags

    Example:
        >>> def divide(a: int, b: int) -> Result[float, BaseError]:
        ...     if b == 0:
        ...         return Failure(ValidationError("Division by zero"))
        ...     return Success(a / b)

        >>> result = divide(10, 2)
        >>> if result.is_success():
        ...     print(f"Result: {result.unwrap()}")
        ... else:
        ...     print(f"Error: {result.unwrap_err()}")
    """

    def __init__(self, value: Optional[T] = None, error: Optional[E] = None):
        """Don't call directly - use Success() or Failure()"""
        self._value = value
        self._error = error
        self._is_success = error is None

    def is_success(self) -> bool:
        """Check if result is successful"""
        return self._is_success

    def is_failure(self) -> bool:
        """Check if result is a failure"""
        return not self._is_success

    def unwrap(self) -> T:
        """
        Get success value or raise exception.
        Use this when you're confident the result is successful.
        """
        if not self._is_success:
            raise ValueError(f"Called unwrap() on Failure: {self._error}")
        return self._value

    def unwrap_err(self) -> E:
        """
        Get error or raise exception.
        Use this when you're confident the result is a failure.
        """
        if self._is_success:
            raise ValueError("Called unwrap_err() on Success")
        return self._error

    def unwrap_or(self, default: T) -> T:
        """Get value if success, else return default"""
        return self._value if self._is_success else default

    def unwrap_or_else(self, fn: Callable[[E], T]) -> T:
        """Get value if success, else compute from error"""
        return self._value if self._is_success else fn(self._error)

    def map(self, fn: Callable[[T], U]) -> Result[U, E]:
        """
        Transform success value, leave error unchanged.

        Example:
            >>> Success(5).map(lambda x: x * 2)
            Success(10)
        """
        if self._is_success:
            return Success(fn(self._value))
        return Failure(self._error)

    def map_err(self, fn: Callable[[E], U]) -> Result[T, U]:
        """
        Transform error, leave success unchanged.

        Example:
            >>> Failure(ValidationError("Bad")).map_err(lambda e: ProcessError(str(e)))
            Failure(ProcessError(...))
        """
        if self._is_success:
            return Success(self._value)
        return Failure(fn(self._error))

    def flatmap(self, fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """
        Chain operations that return Results (monadic bind).

        Example:
            >>> def parse_int(s: str) -> Result[int, BaseError]:
            ...     try:
            ...         return Success(int(s))
            ...     except ValueError:
            ...         return Failure(ValidationError("Not an integer"))

            >>> def divide_by_10(x: int) -> Result[float, BaseError]:
            ...     if x == 0:
            ...         return Failure(ValidationError("Zero"))
            ...     return Success(10.0 / x)

            >>> Success("5").flatmap(parse_int).flatmap(divide_by_10)
            Success(2.0)
        """
        if self._is_success:
            return fn(self._value)
        return Failure(self._error)

    def and_then(self, fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """Alias for flatmap (more intuitive name)"""
        return self.flatmap(fn)

    def or_else(self, fn: Callable[[E], Result[T, U]]) -> Result[T, U]:
        """
        Try alternative on failure.

        Example:
            >>> primary().or_else(lambda e: fallback())
        """
        if self._is_success:
            return Success(self._value)
        return fn(self._error)

    def __repr__(self) -> str:
        if self._is_success:
            return f"Success({self._value!r})"
        return f"Failure({self._error!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Result):
            return False
        if self._is_success != other._is_success:
            return False
        if self._is_success:
            return self._value == other._value
        return self._error == other._error


# ==========================================
# CONSTRUCTORS
# ==========================================

def Success(value: T) -> Result[T, E]:
    """Create successful result"""
    return Result(value=value)


def Failure(error: E) -> Result[T, E]:
    """Create failed result"""
    return Result(error=error)


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def try_result(fn: Callable[[], T]) -> Result[T, BaseError]:
    """
    Wrap function call in Result, catching exceptions.

    Example:
        >>> result = try_result(lambda: risky_operation())
    """
    try:
        return Success(fn())
    except Exception as e:
        return Failure(ProcessError(str(e)))


def collect_results(results: list[Result[T, E]]) -> Result[list[T], list[E]]:
    """
    Collect multiple results into single result.
    Success if all succeed, Failure with all errors if any fail.

    Example:
        >>> results = [Success(1), Success(2), Success(3)]
        >>> collect_results(results)
        Success([1, 2, 3])

        >>> results = [Success(1), Failure(e1), Failure(e2)]
        >>> collect_results(results)
        Failure([e1, e2])
    """
    successes = []
    failures = []

    for result in results:
        if result.is_success():
            successes.append(result.unwrap())
        else:
            failures.append(result.unwrap_err())

    if failures:
        return Failure(failures)
    return Success(successes)


def first_success(results: list[Result[T, E]]) -> Result[T, list[E]]:
    """
    Return first successful result, or all errors if all fail.

    Example:
        >>> results = [Failure(e1), Success(42), Success(100)]
        >>> first_success(results)
        Success(42)
    """
    errors = []

    for result in results:
        if result.is_success():
            return Success(result.unwrap())
        errors.append(result.unwrap_err())

    return Failure(errors)


# ==========================================
# USAGE EXAMPLES
# ==========================================

if __name__ == "__main__":
    print("=" * 70)
    print("Q4: RESULT PATTERN EXAMPLES")
    print("=" * 70)

    # Example 1: Basic usage
    print("\n1. BASIC USAGE:")
    print("-" * 70)

    def divide(a: float, b: float) -> Result[float, BaseError]:
        """Divide a by b, return Result"""
        if b == 0:
            return Failure(ValidationError("Division by zero", field="denominator"))
        return Success(a / b)

    result = divide(10, 2)
    print(f"divide(10, 2) = {result}")
    if result.is_success():
        print(f"  Value: {result.unwrap()}")

    result = divide(10, 0)
    print(f"divide(10, 0) = {result}")
    if result.is_failure():
        error = result.unwrap_err()
        print(f"  Error: {error}")
        print(f"  Code: {error.code}")

    # Example 2: Chaining with flatmap
    print("\n2. CHAINING OPERATIONS:")
    print("-" * 70)

    def parse_int(s: str) -> Result[int, BaseError]:
        """Parse string to integer"""
        try:
            return Success(int(s))
        except ValueError:
            return Failure(ValidationError(f"'{s}' is not an integer", field="input"))

    def double(x: int) -> Result[int, BaseError]:
        """Double the number"""
        return Success(x * 2)

    # Success chain
    result = Success("42").flatmap(parse_int).flatmap(double)
    print(f"'42' -> parse -> double = {result}")

    # Failure chain (stops at first error)
    result = Success("abc").flatmap(parse_int).flatmap(double)
    print(f"'abc' -> parse -> double = {result}")

    # Example 3: Transformation with map
    print("\n3. VALUE TRANSFORMATION:")
    print("-" * 70)

    result = Success(5).map(lambda x: x * 2).map(lambda x: x + 10)
    print(f"Success(5).map(*2).map(+10) = {result}")

    result = Failure(ValidationError("Bad input")).map(lambda x: x * 2)
    print(f"Failure(...).map(*2) = {result}")

    # Example 4: Error transformation
    print("\n4. ERROR TRANSFORMATION:")
    print("-" * 70)

    result = (
        Failure(ValidationError("Invalid input"))
        .map_err(lambda e: ProcessError(f"Preprocessing failed: {e.message}"))
    )
    print(f"Transform ValidationError to ProcessError: {result}")

    # Example 5: Default values
    print("\n5. DEFAULT VALUES:")
    print("-" * 70)

    result = Success(42).unwrap_or(0)
    print(f"Success(42).unwrap_or(0) = {result}")

    result = Failure(ValidationError("Error")).unwrap_or(0)
    print(f"Failure(...).unwrap_or(0) = {result}")

    # Example 6: Collecting results
    print("\n6. COLLECTING MULTIPLE RESULTS:")
    print("-" * 70)

    results = [Success(1), Success(2), Success(3)]
    collected = collect_results(results)
    print(f"All success: {collected}")

    results = [Success(1), Failure(ValidationError("E1")), Failure(ValidationError("E2"))]
    collected = collect_results(results)
    print(f"Some failures: {collected}")

    # Example 7: First success (fallback pattern)
    print("\n7. FIRST SUCCESS (FALLBACK):")
    print("-" * 70)

    def primary() -> Result[str, BaseError]:
        return Failure(ProcessError("Primary failed"))

    def secondary() -> Result[str, BaseError]:
        return Success("Secondary worked!")

    def tertiary() -> Result[str, BaseError]:
        return Failure(ProcessError("Tertiary failed"))

    result = first_success([primary(), secondary(), tertiary()])
    print(f"First success: {result}")

    # Example 8: Exception wrapping
    print("\n8. EXCEPTION WRAPPING:")
    print("-" * 70)

    def risky_operation():
        raise ValueError("Something went wrong!")

    result = try_result(risky_operation)
    print(f"try_result(risky_operation) = {result}")

    # Example 9: Real-world example
    print("\n9. REAL-WORLD PIPELINE:")
    print("-" * 70)

    def validate_input(text: str) -> Result[str, BaseError]:
        """Validate input text"""
        if not text.strip():
            return Failure(ValidationError("Input is empty"))
        if len(text) > 1000:
            return Failure(ValidationError("Input too long"))
        return Success(text.strip())

    def check_guardrails(text: str) -> Result[str, BaseError]:
        """Check guardrails"""
        if "badword" in text.lower():
            return Failure(GuardrailError("Harmful content detected"))
        return Success(text)

    def process(text: str) -> Result[str, BaseError]:
        """Process text"""
        return Success(f"Processed: {text}")

    def verify_output(text: str) -> Result[str, BaseError]:
        """Verify output"""
        if len(text) < 10:
            return Failure(VerificationError("Output too short"))
        return Success(text)

    # Pipeline
    input_text = "Hello world"
    result = (
        Success(input_text)
        .flatmap(validate_input)
        .flatmap(check_guardrails)
        .flatmap(process)
        .flatmap(verify_output)
    )

    print(f"Input: '{input_text}'")
    print(f"Pipeline result: {result}")

    if result.is_success():
        print(f"Final output: {result.unwrap()}")
    else:
        error = result.unwrap_err()
        print(f"Pipeline failed at: {error.code}")
        print(f"Error message: {error.message}")

    print("\n" + "=" * 70)
    print("✅ Q4 implementation complete!")
    print("=" * 70)
    print("\nBENEFITS:")
    print("- No silent failures (explicit error handling)")
    print("- Type-safe (Result[T, E] in function signature)")
    print("- Composable (flatmap, map, or_else)")
    print("- No try/except spaghetti")
    print("- Self-documenting error types")
