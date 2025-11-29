"""
OpenTelemetry Integration for Distributed Tracing
Exports traces to Jaeger for visualization and debugging
"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import os


class DistributedTracing:
    """Manages distributed tracing configuration."""

    def __init__(self, service_name: str = "ultrathink"):
        self.service_name = service_name
        self.tracer_provider = None
        self.tracer = None

    def initialize(self):
        """Initialize OpenTelemetry with Jaeger exporter."""
        # Create resource with service information
        resource = Resource.create({
            "service.name": self.service_name,
            "service.version": "2.0.0",
            "deployment.environment": os.getenv("ENVIRONMENT", "production"),
        })

        # Create tracer provider
        self.tracer_provider = TracerProvider(resource=resource)

        # Configure Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name=os.getenv("JAEGER_AGENT_HOST", "localhost"),
            agent_port=int(os.getenv("JAEGER_AGENT_PORT", "6831")),
        )

        # Add batch span processor
        span_processor = BatchSpanProcessor(jaeger_exporter)
        self.tracer_provider.add_span_processor(span_processor)

        # Set global tracer provider
        trace.set_tracer_provider(self.tracer_provider)

        # Get tracer instance
        self.tracer = trace.get_tracer(__name__)

        return self.tracer

    def instrument_fastapi(self, app):
        """Instrument FastAPI application for automatic tracing."""
        FastAPIInstrumentor.instrument_app(app)

    def instrument_requests(self):
        """Instrument requests library for HTTP client tracing."""
        RequestsInstrumentor().instrument()

    def create_span(self, name: str, attributes: dict = None):
        """Create a custom span for tracing."""
        if self.tracer is None:
            self.initialize()

        span = self.tracer.start_span(name)
        if attributes:
            for key, value in attributes.items():
                span.set_attribute(key, str(value))
        return span

    def shutdown(self):
        """Shutdown tracer provider and flush remaining spans."""
        if self.tracer_provider:
            self.tracer_provider.shutdown()


# Global tracing instance
tracing = DistributedTracing()


# Decorator for tracing functions
def trace_function(func):
    """Decorator to trace function execution."""
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        tracer = tracing.tracer or tracing.initialize()
        with tracer.start_as_current_span(func.__name__) as span:
            span.set_attribute("function.module", func.__module__)
            span.set_attribute("function.name", func.__name__)
            try:
                result = func(*args, **kwargs)
                span.set_attribute("function.success", True)
                return result
            except Exception as e:
                span.set_attribute("function.success", False)
                span.set_attribute("function.error", str(e))
                span.record_exception(e)
                raise

    return wrapper
