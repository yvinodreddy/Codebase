#!/usr/bin/env python3
"""
Prometheus Metrics Collection
Export metrics for Prometheus monitoring
"""
from typing import Dict, Optional
try:
    from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest, REGISTRY
except ImportError:
    print("⚠️  prometheus_client not installed. Run: pip install prometheus-client")
    Counter = Histogram = Gauge = Info = None


class MetricsCollector:
    """
    Centralized metrics collection for Prometheus

    Example:
        metrics = MetricsCollector()
        metrics.track_request("success", duration=0.5)
        metrics.track_api_call("anthropic", tokens=1000)
    """

    def __init__(self):
        if Counter is None:
            raise ImportError("prometheus_client not installed")

        # Request metrics
        self.requests_total = Counter(
            "ultrathink_requests_total",
            "Total number of requests",
            ["status"]
        )

        self.request_duration = Histogram(
            "ultrathink_request_duration_seconds",
            "Request duration in seconds",
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
        )

        # API call metrics
        self.api_calls_total = Counter(
            "ultrathink_api_calls_total",
            "Total API calls",
            ["provider"]
        )

        self.api_tokens_used = Counter(
            "ultrathink_api_tokens_used_total",
            "Total API tokens used",
            ["provider"]
        )

        # System metrics
        self.active_requests = Gauge(
            "ultrathink_active_requests",
            "Number of active requests"
        )

        self.cache_hit_rate = Gauge(
            "ultrathink_cache_hit_rate",
            "Cache hit rate percentage"
        )

        # Agent metrics
        self.agents_allocated = Gauge(
            "ultrathink_agents_allocated",
            "Number of agents allocated"
        )

        # Guardrail metrics
        self.guardrail_checks = Counter(
            "ultrathink_guardrail_checks_total",
            "Total guardrail checks",
            ["layer", "result"]
        )

        # Info metric
        self.app_info = Info(
            "ultrathink_app",
            "Application information"
        )
        self.app_info.info({
            "version": "1.0.0",
            "name": "ULTRATHINK",
        })

    def track_request(self, status: str, duration: float):
        """Track a request"""
        self.requests_total.labels(status=status).inc()
        self.request_duration.observe(duration)

    def track_api_call(self, provider: str, tokens: int):
        """Track an API call"""
        self.api_calls_total.labels(provider=provider).inc()
        self.api_tokens_used.labels(provider=provider).inc(tokens)

    def set_active_requests(self, count: int):
        """Set number of active requests"""
        self.active_requests.set(count)

    def set_cache_hit_rate(self, rate: float):
        """Set cache hit rate (0-100)"""
        self.cache_hit_rate.set(rate)

    def set_agents_allocated(self, count: int):
        """Set number of agents allocated"""
        self.agents_allocated.set(count)

    def track_guardrail_check(self, layer: str, passed: bool):
        """Track a guardrail check"""
        result = "pass" if passed else "fail"
        self.guardrail_checks.labels(layer=layer, result=result).inc()

    def export_metrics(self) -> bytes:
        """Export metrics in Prometheus format"""
        return generate_latest(REGISTRY)


# Global metrics collector
_global_metrics = None


def get_metrics_collector() -> MetricsCollector:
    """Get global metrics collector instance"""
    global _global_metrics
    if _global_metrics is None:
        _global_metrics = MetricsCollector()
    return _global_metrics
