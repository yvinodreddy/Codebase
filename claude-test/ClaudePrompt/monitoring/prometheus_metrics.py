"""
Prometheus metrics for ULTRATHINK system
"""
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Request metrics
request_count = Counter(
    'ultrathink_requests_total',
    'Total number of requests',
    ['method', 'status']
)

request_duration = Histogram(
    'ultrathink_request_duration_seconds',
    'Request duration in seconds',
    ['method']
)

# Guardrail metrics
guardrail_checks = Counter(
    'ultrathink_guardrail_checks_total',
    'Total guardrail checks',
    ['layer', 'result']
)

# Context metrics
context_tokens = Gauge(
    'ultrathink_context_tokens',
    'Current context window usage'
)

# Quality metrics
confidence_score = Histogram(
    'ultrathink_confidence_score',
    'Confidence scores'
)

def start_metrics_server(port: int = 9090):
    """Start Prometheus metrics HTTP server"""
    start_http_server(port)
    print(f"Metrics server started on port {port}")

if __name__ == "__main__":
    start_metrics_server()
