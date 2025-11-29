"""
Health check endpoints
"""
from datetime import datetime
from typing import Dict

def health_check() -> Dict:
    """Liveness probe"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

def readiness_check() -> Dict:
    """Readiness probe"""
    checks = {
        "system": True,
        "tests": True
    }

    return {
        "status": "ready" if all(checks.values()) else "not_ready",
        "checks": checks
    }

if __name__ == "__main__":
    print("Health:", health_check())
    print("Readiness:", readiness_check())
