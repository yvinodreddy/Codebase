#!/usr/bin/env python3
"""
Health and Metrics REST Endpoints
Provides /health and /metrics endpoints for monitoring
"""
from fastapi import FastAPI, Response
from typing import Dict, Any
import time
import psutil
from datetime import datetime
from infrastructure.prometheus_metrics import get_metrics_collector


def add_health_endpoints(app: FastAPI):
    """
    Add health and metrics endpoints to FastAPI app

    Example:
        from fastapi import FastAPI
        app = FastAPI()
        add_health_endpoints(app)
    """

    @app.get("/health")
    async def health_check() -> Dict[str, Any]:
        """
        Health check endpoint

        Returns:
            Health status and system metrics

        Example response:
            {
                "status": "healthy",
                "timestamp": "2025-11-12T18:00:00Z",
                "uptime_seconds": 3600,
                "system": {
                    "cpu_percent": 45.2,
                    "memory_percent": 62.1,
                    "disk_percent": 55.0
                },
                "checks": {
                    "database": "ok",
                    "cache": "ok",
                    "api": "ok"
                }
            }
        """
        # System metrics
        system_metrics = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent,
        }

        # Service checks
        checks = {
            "system": "ok",
            "cache": "ok",  # TODO: Add actual cache check
            "api": "ok",  # TODO: Add actual API check
        }

        # Determine overall status
        status = "healthy"
        if system_metrics["cpu_percent"] > 90:
            status = "degraded"
            checks["system"] = "high_cpu"
        if system_metrics["memory_percent"] > 90:
            status = "degraded"
            checks["system"] = "high_memory"

        return {
            "status": status,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "uptime_seconds": time.time() - psutil.boot_time(),
            "system": system_metrics,
            "checks": checks,
        }

    @app.get("/health/ready")
    async def readiness_check() -> Dict[str, str]:
        """
        Kubernetes readiness probe endpoint

        Returns:
            Ready status

        Example response:
            {"status": "ready"}
        """
        # TODO: Add actual readiness checks (DB connection, etc.)
        return {"status": "ready"}

    @app.get("/health/live")
    async def liveness_check() -> Dict[str, str]:
        """
        Kubernetes liveness probe endpoint

        Returns:
            Live status

        Example response:
            {"status": "live"}
        """
        return {"status": "live"}

    @app.get("/metrics")
    async def metrics_endpoint():
        """
        Prometheus metrics endpoint

        Returns:
            Metrics in Prometheus format

        Example:
            # HELP ultrathink_requests_total Total number of requests
            # TYPE ultrathink_requests_total counter
            ultrathink_requests_total{status="success"} 1234
        """
        try:
            metrics_collector = get_metrics_collector()
            metrics_data = metrics_collector.export_metrics()
            return Response(content=metrics_data, media_type="text/plain")
        except ImportError:
            return Response(
                content="# Prometheus metrics not available (prometheus_client not installed)\n",
                media_type="text/plain"
            )

    @app.get("/metrics/json")
    async def metrics_json_endpoint() -> Dict[str, Any]:
        """
        Metrics in JSON format (for dashboards)

        Returns:
            Metrics as JSON

        Example response:
            {
                "requests_total": 1234,
                "api_calls_total": 567,
                "cache_hit_rate": 85.5,
                "active_requests": 3
            }
        """
        # TODO: Implement JSON metrics export
        return {
            "requests_total": 0,
            "api_calls_total": 0,
            "cache_hit_rate": 0.0,
            "active_requests": 0,
        }
