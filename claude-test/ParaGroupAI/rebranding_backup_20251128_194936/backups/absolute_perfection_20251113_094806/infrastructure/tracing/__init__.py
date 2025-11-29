"""Distributed tracing infrastructure."""
from .opentelemetry_config import tracing, trace_function, DistributedTracing

__all__ = ['tracing', 'trace_function', 'DistributedTracing']
