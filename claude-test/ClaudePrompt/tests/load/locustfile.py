"""
Advanced Load Testing Suite for ULTRATHINK API
Framework: Locust
Target: Production-grade load patterns
"""

from locust import HttpUser, task, between, events
import json
import time
from datetime import datetime


class UltrathinkUser(HttpUser):
    """Simulates a user interacting with ULTRATHINK API."""

    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks

    def on_start(self):
        """Called when a user starts."""
        self.client.verify = False  # For testing with self-signed certs
        self.prompts = [
            "What is 2+2?",
            "Explain quantum computing in simple terms.",
            "Write a Python function to sort a list.",
            "What are the benefits of microservices architecture?",
            "How does machine learning work?",
        ]
        self.prompt_index = 0

    @task(10)
    def test_root_endpoint(self):
        """Test root endpoint (high frequency)."""
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(5)
    def test_health_endpoint(self):
        """Test health endpoint (medium frequency)."""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(3)
    def test_prompt_processing(self):
        """Test prompt processing (lower frequency, more expensive)."""
        prompt = self.prompts[self.prompt_index % len(self.prompts)]
        self.prompt_index += 1

        payload = {
            "prompt": prompt,
            "verbose": False,
            "max_iterations": 5,
            "confidence_threshold": 95.0
        }

        start_time = time.time()
        with self.client.post("/v1/prompt",
                             json=payload,
                             catch_response=True,
                             timeout=30) as response:
            duration = time.time() - start_time

            if response.status_code == 200:
                try:
                    data = response.json()
                    if "response" in data and "confidence" in data:
                        response.success()
                    else:
                        response.failure("Missing required fields in response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        with self.client.get("/metrics", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")


class SpikeTestUser(HttpUser):
    """Simulates spike traffic patterns."""

    wait_time = between(0.1, 0.5)  # Very short wait time for spike

    @task
    def spike_request(self):
        """Generate spike traffic."""
        self.client.get("/")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when test starts."""
    print(f"🚀 Load test starting at {datetime.now()}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when test stops."""
    print(f"✅ Load test completed at {datetime.now()}")
    stats = environment.stats
    print(f"Total requests: {stats.total.num_requests}")
    print(f"Total failures: {stats.total.num_failures}")
    print(f"Average response time: {stats.total.avg_response_time:.2f}ms")
    print(f"P95 response time: {stats.total.get_response_time_percentile(0.95):.2f}ms")
    print(f"P99 response time: {stats.total.get_response_time_percentile(0.99):.2f}ms")
    print(f"Requests per second: {stats.total.current_rps:.2f}")
