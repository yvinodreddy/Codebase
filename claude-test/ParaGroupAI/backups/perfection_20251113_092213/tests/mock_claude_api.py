"""
T5: Mock Claude API for Cost-Free Testing
Simulates Anthropic Claude API responses without making real API calls

BENEFITS:
- Zero cost testing (no API charges)
- Fast tests (no network latency)
- Deterministic responses (reproducible tests)
- Test error scenarios (rate limits, timeouts, errors)
- Offline testing (no internet required)
"""

import time
import random
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MockMessage:
    """Mock Claude message format"""
    role: str  # "user" or "assistant"
    content: str


@dataclass
class MockUsage:
    """Mock token usage"""
    input_tokens: int
    output_tokens: int

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class MockResponse:
    """Mock Claude API response"""
    id: str
    model: str
    role: str
    content: List[Dict[str, Any]]
    stop_reason: str
    usage: MockUsage

    @property
    def text(self) -> str:
        """Extract text from content blocks"""
        for block in self.content:
            if block.get("type") == "text":
                return block.get("text", "")
        return ""


class MockClaudeClient:
    """
    T5: Mock Claude API client for testing.

    Simulates the Anthropic Claude API without making real requests.
    Use this for testing to avoid API costs and network dependencies.

    Example:
        >>> client = MockClaudeClient(behavior="success")
        >>> response = client.messages.create(
        ...     model="claude-sonnet-4-5-20250929",
        ...     max_tokens=1024,
        ...     messages=[{"role": "user", "content": "Hello"}]
        ... )
        >>> print(response.text)
        "Mock response to: Hello"
    """

    def __init__(
        self,
        behavior: str = "success",
        latency_ms: float = 100.0,
        error_rate: float = 0.0,
        custom_responses: Optional[Dict[str, str]] = None
    ):
        """
        Initialize mock client.

        Args:
            behavior: Response behavior mode
                - "success": Always return successful responses
                - "error": Always return errors
                - "rate_limit": Simulate rate limiting
                - "timeout": Simulate timeouts
                - "random": Random success/failure
            latency_ms: Simulated network latency in milliseconds
            error_rate: Probability of error (0.0-1.0) for "random" mode
            custom_responses: Custom responses for specific prompts
        """
        self.behavior = behavior
        self.latency_ms = latency_ms
        self.error_rate = error_rate
        self.custom_responses = custom_responses or {}

        # Statistics
        self.call_count = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.errors_raised = 0

        # Rate limiting simulation
        self.rate_limit_calls = []
        self.rate_limit_window = 60  # 1 minute
        self.rate_limit_max = 50  # 50 calls per minute

        # Initialize messages interface
        self.messages = self._MockMessages(self)

    class _MockMessages:
        """Mock messages interface"""
        def __init__(self, client):
            self.client = client

        def create(
            self,
            model: str,
            max_tokens: int,
            messages: List[Dict[str, str]],
            temperature: float = 1.0,
            **kwargs
        ) -> MockResponse:
            """Create mock message response"""
            return self.client._create_response(model, max_tokens, messages, temperature, **kwargs)

    def _create_response(
        self,
        model: str,
        max_tokens: int,
        messages: List[Dict[str, str]],
        temperature: float = 1.0,
        **kwargs
    ) -> MockResponse:
        """
        Create mock response based on behavior mode.
        """
        self.call_count += 1

        # Simulate latency
        time.sleep(self.latency_ms / 1000.0)

        # Extract last user message
        last_message = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_message = msg["content"]
                break

        # Check for custom response
        if last_message in self.custom_responses:
            response_text = self.custom_responses[last_message]
            return self._build_response(model, response_text, last_message)

        # Behavior modes
        if self.behavior == "error":
            self.errors_raised += 1
            raise MockAPIError("Simulated API error", status_code=500)

        elif self.behavior == "rate_limit":
            # Simulate rate limiting
            now = time.time()
            self.rate_limit_calls = [t for t in self.rate_limit_calls if now - t < self.rate_limit_window]

            if len(self.rate_limit_calls) >= self.rate_limit_max:
                self.errors_raised += 1
                raise MockRateLimitError("Rate limit exceeded", retry_after=60)

            self.rate_limit_calls.append(now)

        elif self.behavior == "timeout":
            self.errors_raised += 1
            raise MockTimeoutError("Request timeout")

        elif self.behavior == "random":
            if random.random() < self.error_rate:
                self.errors_raised += 1
                raise MockAPIError("Random error", status_code=500)

        # Generate mock response based on prompt
        response_text = self._generate_response(last_message)
        return self._build_response(model, response_text, last_message)

    def _generate_response(self, prompt: str) -> str:
        """Generate mock response based on prompt content"""
        prompt_lower = prompt.lower()

        # Code generation
        if any(word in prompt_lower for word in ["write", "implement", "create", "code", "function"]):
            return """Here's the implementation:

```python
def example_function(x):
    \"\"\"Example function implementation\"\"\"
    return x * 2
```

This implementation meets the requirements."""

        # Question answering
        if any(word in prompt_lower for word in ["what", "how", "why", "explain", "tell me"]):
            return """Based on my analysis, the answer is:

1. First point of explanation
2. Second point with details
3. Third point concluding the answer

This should fully address your question."""

        # Analysis
        if any(word in prompt_lower for word in ["analyze", "review", "evaluate", "assess"]):
            return """Analysis results:

**Strengths:**
- Good structure
- Clear implementation

**Areas for improvement:**
- Could add error handling
- Consider edge cases

**Overall assessment:** Solid implementation with minor improvements needed."""

        # Medical content
        if any(word in prompt_lower for word in ["patient", "medical", "diagnosis", "treatment"]):
            return """Medical assessment:

**Note:** This is a simulated response for testing purposes only.

- Condition: [Simulated medical information]
- Recommendation: [Simulated recommendation]
- Follow-up: [Simulated follow-up instructions]

**Disclaimer:** Consult healthcare professional for actual medical advice."""

        # Default response
        return f"""Mock response to: {prompt[:100]}

This is a simulated Claude API response. The actual API would provide a more detailed and contextual response based on the full conversation history and the specific task requirements."""

    def _build_response(self, model: str, response_text: str, input_text: str) -> MockResponse:
        """Build MockResponse object"""
        # Simulate token counting (rough estimate)
        input_tokens = len(input_text.split()) * 1.3
        output_tokens = len(response_text.split()) * 1.3

        self.total_input_tokens += int(input_tokens)
        self.total_output_tokens += int(output_tokens)

        usage = MockUsage(
            input_tokens=int(input_tokens),
            output_tokens=int(output_tokens)
        )

        return MockResponse(
            id=f"mock-msg-{self.call_count}",
            model=model,
            role="assistant",
            content=[{"type": "text", "text": response_text}],
            stop_reason="end_turn",
            usage=usage
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Get mock API statistics"""
        return {
            "total_calls": self.call_count,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "errors_raised": self.errors_raised,
            "cost_saved_estimate": self._estimate_cost_saved()
        }

    def _estimate_cost_saved(self) -> float:
        """Estimate cost saved by using mock API"""
        # Claude 3.5 Sonnet pricing (approximate)
        input_cost_per_1k = 0.003  # $3 per million tokens
        output_cost_per_1k = 0.015  # $15 per million tokens

        input_cost = (self.total_input_tokens / 1000) * input_cost_per_1k
        output_cost = (self.total_output_tokens / 1000) * output_cost_per_1k

        return round(input_cost + output_cost, 4)

    def reset_statistics(self):
        """Reset statistics counters"""
        self.call_count = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.errors_raised = 0


# ==========================================
# MOCK EXCEPTIONS
# ==========================================

class MockAPIError(Exception):
    """Mock API error"""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class MockRateLimitError(MockAPIError):
    """Mock rate limit error"""
    def __init__(self, message: str, retry_after: int = 60):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


class MockTimeoutError(Exception):
    """Mock timeout error"""
    pass


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def create_mock_client(scenario: str = "success") -> MockClaudeClient:
    """
    Create pre-configured mock client for common test scenarios.

    Scenarios:
        - "success": Always succeeds (default)
        - "fast": Fast responses (10ms latency)
        - "slow": Slow responses (2000ms latency)
        - "flaky": Random failures (20% error rate)
        - "rate_limit": Simulates rate limiting
        - "error": Always fails

    Example:
        >>> client = create_mock_client("success")
        >>> # Use in tests...
    """
    configs = {
        "success": {"behavior": "success", "latency_ms": 100.0},
        "fast": {"behavior": "success", "latency_ms": 10.0},
        "slow": {"behavior": "success", "latency_ms": 2000.0},
        "flaky": {"behavior": "random", "latency_ms": 100.0, "error_rate": 0.2},
        "rate_limit": {"behavior": "rate_limit", "latency_ms": 50.0},
        "error": {"behavior": "error", "latency_ms": 100.0}
    }

    config = configs.get(scenario, configs["success"])
    return MockClaudeClient(**config)


# ==========================================
# USAGE EXAMPLE
# ==========================================

if __name__ == "__main__":
    print("=" * 70)
    print("T5: MOCK CLAUDE API EXAMPLES")
    print("=" * 70)

    # Example 1: Basic success scenario
    print("\n1. BASIC SUCCESS SCENARIO:")
    print("-" * 70)
    client = create_mock_client("success")

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Write a Python function to calculate factorial"}]
    )

    print(f"Response: {response.text[:200]}...")
    print(f"Tokens: {response.usage.total_tokens}")

    # Example 2: Custom responses
    print("\n2. CUSTOM RESPONSES:")
    print("-" * 70)
    client = MockClaudeClient(
        custom_responses={
            "test prompt": "Custom test response",
            "another test": "Another custom response"
        }
    )

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "test prompt"}]
    )

    print(f"Response: {response.text}")

    # Example 3: Rate limiting simulation
    print("\n3. RATE LIMITING SIMULATION:")
    print("-" * 70)
    client = create_mock_client("rate_limit")

    try:
        # Make 60 calls (exceeds 50/min limit)
        for i in range(60):
            response = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=100,
                messages=[{"role": "user", "content": f"Request {i}"}]
            )
        print("All calls succeeded (unexpected)")
    except MockRateLimitError as e:
        print(f"✅ Rate limit triggered after {client.call_count} calls")
        print(f"   Error: {e.message}")
        print(f"   Retry after: {e.retry_after}s")

    # Example 4: Statistics
    print("\n4. MOCK API STATISTICS:")
    print("-" * 70)
    client = create_mock_client("success")

    # Make several calls
    for i in range(10):
        client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=500,
            messages=[{"role": "user", "content": f"Test query {i}"}]
        )

    stats = client.get_statistics()
    print(f"Total calls: {stats['total_calls']}")
    print(f"Total tokens: {stats['total_tokens']}")
    print(f"Cost saved: ${stats['cost_saved_estimate']:.4f}")

    # Example 5: Flaky behavior
    print("\n5. FLAKY BEHAVIOR (20% error rate):")
    print("-" * 70)
    client = create_mock_client("flaky")

    successes = 0
    failures = 0

    for i in range(20):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=100,
                messages=[{"role": "user", "content": f"Request {i}"}]
            )
            successes += 1
        except MockAPIError:
            failures += 1

    print(f"Successes: {successes}/20")
    print(f"Failures: {failures}/20")
    print(f"Error rate: {failures/20*100:.1f}%")

    print("\n" + "=" * 70)
    print("✅ T5 implementation complete!")
    print("=" * 70)
    print("\nBENEFITS:")
    print("- Zero API costs during testing")
    print("- Fast test execution (no network latency)")
    print("- Deterministic results (reproducible tests)")
    print("- Test error scenarios (rate limits, timeouts)")
    print("- Offline testing capability")
