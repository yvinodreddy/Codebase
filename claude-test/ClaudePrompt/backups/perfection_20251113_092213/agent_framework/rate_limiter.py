#!/usr/bin/env python3
"""
S4: Rate Limiting for Claude API Calls
Token bucket rate limiter to prevent API overuse and cost overruns.

Configuration: 500 calls per 360 seconds (6 minutes) = ~83 calls/minute
"""

import time
import logging
from collections import deque
from typing import Optional
from config import UltrathinkConfig as Config

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Token bucket rate limiter for API calls.

    Prevents exceeding Anthropic API rate limits by throttling requests.
    Uses sliding window approach for smooth rate limiting.

    Configuration (from config.py):
    - Max calls: 500 per time window
    - Time window: 360 seconds (6 minutes)
    - Effective rate: ~83 calls/minute
    """

    def __init__(
        self,
        max_calls: int = None,
        time_window: int = None
    ):
        """
        Initialize rate limiter.

        Args:
            max_calls: Maximum calls per time window (default: from config)
            time_window: Time window in seconds (default: from config)
        """
        self.max_calls = max_calls or Config.RATE_LIMIT_CALLS
        self.time_window = time_window or Config.RATE_LIMIT_WINDOW
        self.calls = deque()  # Store timestamps of API calls

        logger.info(
            f"Rate limiter initialized: {self.max_calls} calls per {self.time_window}s "
            f"({self.max_calls / (self.time_window / 60):.1f} calls/min)"
        )

    def wait_if_needed(self, verbose: bool = False) -> float:
        """
        Check rate limit and wait if necessary.

        This method should be called BEFORE making an API call.
        It will block (sleep) if the rate limit would be exceeded.

        Args:
            verbose: If True, print waiting messages

        Returns:
            Seconds waited (0.0 if no wait needed)
        """
        now = time.time()

        # Remove calls outside the current time window (sliding window)
        while self.calls and self.calls[0] < now - self.time_window:
            self.calls.popleft()

        # Check if we're at the limit
        if len(self.calls) >= self.max_calls:
            # Calculate how long to wait
            oldest_call = self.calls[0]
            wait_until = oldest_call + self.time_window
            sleep_time = wait_until - now

            if sleep_time > 0:
                if verbose:
                    print(f"⏱️  Rate limit reached ({len(self.calls)}/{self.max_calls} calls)")
                    print(f"   Waiting {sleep_time:.1f}s before next API call...")

                logger.warning(
                    f"Rate limit reached: {len(self.calls)}/{self.max_calls} calls "
                    f"in last {self.time_window}s. Waiting {sleep_time:.1f}s"
                )

                time.sleep(sleep_time)

                # Remove the oldest call (now outside window)
                self.calls.popleft()

                return sleep_time

        # Record this call
        self.calls.append(now)

        if verbose:
            calls_remaining = self.max_calls - len(self.calls)
            print(f"✓ Rate limit OK: {len(self.calls)}/{self.max_calls} calls used, "
                  f"{calls_remaining} remaining")

        return 0.0

    def get_current_usage(self) -> dict:
        """
        Get current rate limiter statistics.

        Returns:
            Dict with usage stats:
            - current_calls: Number of calls in current window
            - max_calls: Maximum allowed calls
            - calls_remaining: Remaining call budget
            - usage_percent: Percentage of limit used
            - time_window_seconds: Time window size
            - current_rate_per_minute: Current call rate
            - max_rate_per_minute: Maximum call rate
        """
        now = time.time()

        # Clean up old calls
        while self.calls and self.calls[0] < now - self.time_window:
            self.calls.popleft()

        current_calls = len(self.calls)
        usage_percent = (current_calls / self.max_calls) * 100

        # Calculate current rate (calls per minute)
        if self.calls:
            time_span = now - self.calls[0] if len(self.calls) > 1 else self.time_window
            current_rate = (current_calls / time_span) * 60 if time_span > 0 else 0
        else:
            current_rate = 0

        return {
            'current_calls': current_calls,
            'max_calls': self.max_calls,
            'calls_remaining': self.max_calls - current_calls,
            'usage_percent': usage_percent,
            'time_window_seconds': self.time_window,
            'current_rate_per_minute': current_rate,
            'max_rate_per_minute': (self.max_calls / self.time_window) * 60,
        }

    def reset(self):
        """Reset the rate limiter (clear all call history)"""
        self.calls.clear()
        logger.info("Rate limiter reset")


# Convenience function for testing
def demonstrate_rate_limiter():
    """Demonstrate rate limiter behavior"""
    print("Rate Limiter Demonstration")
    print("="*70)

    # Create limiter with small limits for demo
    limiter = RateLimiter(max_calls=5, time_window=10)

    print(f"Config: {limiter.max_calls} calls per {limiter.time_window}s\n")

    # Simulate 10 API calls
    for i in range(10):
        print(f"Call {i+1}:")
        wait_time = limiter.wait_if_needed(verbose=True)

        # Show stats
        stats = limiter.get_current_usage()
        print(f"   Stats: {stats['current_calls']}/{stats['max_calls']} calls "
              f"({stats['usage_percent']:.1f}% used)")

        if wait_time:
            print(f"   ⏱️  Waited {wait_time:.1f}s")

        print()

        # Simulate some work
        time.sleep(0.5)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demonstrate_rate_limiter()
