"""
Comprehensive monitoring with detailed metrics and alerting
"""
from prometheus_client import Counter, Histogram, Gauge, Summary, Info
import time
from typing import Dict, Any

# Comprehensive metrics
class MonitoringMetrics:
    """Centralized monitoring metrics"""

    def __init__(self):
        # Request metrics
        self.requests_total = Counter(
            'ultrathink_requests_total',
            'Total requests processed',
            ['method', 'endpoint', 'status', 'version']
        )

        self.request_duration = Histogram(
            'ultrathink_request_duration_seconds',
            'Request duration distribution',
            ['method', 'endpoint'],
            buckets=[0.001, 0.01, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
        )

        # Guardrail metrics
        self.guardrail_checks = Counter(
            'ultrathink_guardrail_checks_total',
            'Total guardrail checks',
            ['layer', 'result', 'category']
        )

        self.guardrail_duration = Histogram(
            'ultrathink_guardrail_duration_seconds',
            'Guardrail check duration',
            ['layer']
        )

        # Agent metrics
        self.agent_iterations = Histogram(
            'ultrathink_agent_iterations',
            'Agent feedback loop iterations',
            buckets=[1, 2, 5, 10, 15, 20]
        )

        self.agent_success_rate = Gauge(
            'ultrathink_agent_success_rate',
            'Agent success rate (rolling average)'
        )

        # Context metrics
        self.context_tokens = Gauge(
            'ultrathink_context_tokens',
            'Current context window tokens used'
        )

        self.context_compactions = Counter(
            'ultrathink_context_compactions_total',
            'Context window compactions'
        )

        # Quality metrics
        self.confidence_score = Histogram(
            'ultrathink_confidence_score',
            'Response confidence scores',
            buckets=[0, 50, 75, 90, 95, 97, 99, 99.5, 100]
        )

        self.verification_checks = Counter(
            'ultrathink_verification_checks_total',
            'Verification checks performed',
            ['method', 'result']
        )

        # System metrics
        self.errors_total = Counter(
            'ultrathink_errors_total',
            'Total errors encountered',
            ['type', 'component', 'severity']
        )

        self.circuit_breaker_state = Gauge(
            'ultrathink_circuit_breaker_state',
            'Circuit breaker state (0=closed, 1=open, 2=half_open)',
            ['service']
        )

        # Cache metrics
        self.cache_hits = Counter(
            'ultrathink_cache_hits_total',
            'Cache hits'
        )

        self.cache_misses = Counter(
            'ultrathink_cache_misses_total',
            'Cache misses'
        )

        self.cache_size = Gauge(
            'ultrathink_cache_size',
            'Current cache size'
        )

        # API metrics
        self.api_response_size = Histogram(
            'ultrathink_api_response_size_bytes',
            'API response sizes',
            buckets=[100, 1000, 10000, 100000, 1000000]
        )

        # System info
        self.build_info = Info(
            'ultrathink_build_info',
            'Build information'
        )

        self.build_info.info({
            'version': '2.0.0',
            'build_date': time.strftime('%Y-%m-%d'),
            'python_version': '3.12'
        })

# Global metrics instance
metrics = MonitoringMetrics()
