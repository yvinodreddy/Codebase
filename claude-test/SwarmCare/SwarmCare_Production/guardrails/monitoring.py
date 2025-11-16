"""
Monitoring and Logging System for Guardrails
Tracks performance, failures, and statistics
"""

import os
import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Setup logger
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "guardrails.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@dataclass
class GuardrailEvent:
    """Guardrail validation event"""
    timestamp: str
    event_type: str  # validation_success, validation_failure, warning, error
    layer: str
    passed: bool
    message: str
    severity: Optional[int] = None
    details: Optional[Dict] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None


class GuardrailMonitor:
    """
    Monitor guardrail performance and events.
    Provides metrics, logging, and statistics tracking.
    """

    def __init__(self, metrics_file: str = "guardrail_metrics.json"):
        self.metrics_file = LOG_DIR / metrics_file
        self.enable_metrics = os.getenv("ENABLE_METRICS_LOGGING", "true").lower() == "true"

        # Initialize or load metrics
        self.metrics = self._load_metrics()

    def _load_metrics(self) -> Dict[str, Any]:
        """Load metrics from file or create new."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading metrics: {e}")

        return {
            "total_validations": 0,
            "successful_validations": 0,
            "failed_validations": 0,
            "warnings": 0,
            "errors": 0,
            "layer_stats": {
                "layer_1_prompt_shields": {"passed": 0, "failed": 0},
                "layer_2_input_content": {"passed": 0, "failed": 0},
                "layer_3_phi_detection": {"passed": 0, "failed": 0},
                "layer_4_terminology": {"passed": 0, "failed": 0},
                "layer_5_output_content": {"passed": 0, "failed": 0},
                "layer_6_groundedness": {"passed": 0, "failed": 0},
                "layer_7_compliance": {"passed": 0, "failed": 0}
            },
            "last_updated": datetime.now().isoformat()
        }

    def _save_metrics(self):
        """Save metrics to file."""
        if not self.enable_metrics:
            return

        try:
            self.metrics["last_updated"] = datetime.now().isoformat()
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")

    def log_validation(
        self,
        layer: str,
        passed: bool,
        message: str,
        severity: Optional[int] = None,
        details: Optional[Dict] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        """
        Log a validation event.

        Args:
            layer: Guardrail layer name
            passed: Whether validation passed
            message: Validation message
            severity: Severity level (0-10)
            details: Additional details
            user_id: User identifier
            session_id: Session identifier
        """
        event = GuardrailEvent(
            timestamp=datetime.now().isoformat(),
            event_type="validation_success" if passed else "validation_failure",
            layer=layer,
            passed=passed,
            message=message,
            severity=severity,
            details=details,
            user_id=user_id,
            session_id=session_id
        )

        # Log to logger
        log_level = logging.INFO if passed else logging.WARNING
        logger.log(
            log_level,
            f"[{layer}] {message}",
            extra={"event": asdict(event)}
        )

        # Update metrics
        self.metrics["total_validations"] += 1
        if passed:
            self.metrics["successful_validations"] += 1
            if layer in self.metrics["layer_stats"]:
                self.metrics["layer_stats"][layer]["passed"] += 1
        else:
            self.metrics["failed_validations"] += 1
            if layer in self.metrics["layer_stats"]:
                self.metrics["layer_stats"][layer]["failed"] += 1

        self._save_metrics()

    def log_warning(
        self,
        layer: str,
        message: str,
        details: Optional[Dict] = None
    ):
        """Log a warning event."""
        event = GuardrailEvent(
            timestamp=datetime.now().isoformat(),
            event_type="warning",
            layer=layer,
            passed=True,
            message=message,
            details=details
        )

        logger.warning(
            f"[{layer}] WARNING: {message}",
            extra={"event": asdict(event)}
        )

        self.metrics["warnings"] += 1
        self._save_metrics()

    def log_error(
        self,
        layer: str,
        error: str,
        details: Optional[Dict] = None
    ):
        """Log an error event."""
        event = GuardrailEvent(
            timestamp=datetime.now().isoformat(),
            event_type="error",
            layer=layer,
            passed=False,
            message=error,
            details=details
        )

        logger.error(
            f"[{layer}] ERROR: {error}",
            extra={"event": asdict(event)}
        )

        self.metrics["errors"] += 1
        self._save_metrics()

    def get_statistics(self) -> Dict[str, Any]:
        """Get current statistics."""
        total = self.metrics["total_validations"]
        success_rate = (
            (self.metrics["successful_validations"] / total * 100)
            if total > 0 else 0
        )

        return {
            "total_validations": total,
            "successful_validations": self.metrics["successful_validations"],
            "failed_validations": self.metrics["failed_validations"],
            "success_rate": round(success_rate, 2),
            "warnings": self.metrics["warnings"],
            "errors": self.metrics["errors"],
            "layer_statistics": self.metrics["layer_stats"],
            "last_updated": self.metrics["last_updated"]
        }

    def get_layer_performance(self, layer: str) -> Dict[str, Any]:
        """Get performance metrics for specific layer."""
        if layer not in self.metrics["layer_stats"]:
            return {"error": f"Unknown layer: {layer}"}

        stats = self.metrics["layer_stats"][layer]
        total = stats["passed"] + stats["failed"]
        pass_rate = (stats["passed"] / total * 100) if total > 0 else 0

        return {
            "layer": layer,
            "total_validations": total,
            "passed": stats["passed"],
            "failed": stats["failed"],
            "pass_rate": round(pass_rate, 2)
        }

    def reset_metrics(self):
        """Reset all metrics."""
        self.metrics = self._load_metrics()
        self.metrics["total_validations"] = 0
        self.metrics["successful_validations"] = 0
        self.metrics["failed_validations"] = 0
        self.metrics["warnings"] = 0
        self.metrics["errors"] = 0

        for layer in self.metrics["layer_stats"]:
            self.metrics["layer_stats"][layer] = {"passed": 0, "failed": 0}

        self._save_metrics()
        logger.info("Metrics reset")

    def generate_report(self, output_file: Optional[str] = None) -> str:
        """
        Generate a comprehensive metrics report.

        Args:
            output_file: Optional file to save report to

        Returns:
            Report as string
        """
        stats = self.get_statistics()

        report_lines = [
            "=" * 80,
            "GUARDRAIL SYSTEM PERFORMANCE REPORT",
            "=" * 80,
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "OVERALL STATISTICS",
            "-" * 80,
            f"Total Validations: {stats['total_validations']}",
            f"Successful: {stats['successful_validations']} ({stats['success_rate']}%)",
            f"Failed: {stats['failed_validations']}",
            f"Warnings: {stats['warnings']}",
            f"Errors: {stats['errors']}",
            "",
            "LAYER PERFORMANCE",
            "-" * 80,
        ]

        for layer, layer_stats in stats["layer_statistics"].items():
            total = layer_stats["passed"] + layer_stats["failed"]
            pass_rate = (layer_stats["passed"] / total * 100) if total > 0 else 0

            report_lines.extend([
                f"\n{layer}:",
                f"  Total: {total}",
                f"  Passed: {layer_stats['passed']}",
                f"  Failed: {layer_stats['failed']}",
                f"  Pass Rate: {pass_rate:.2f}%"
            ])

        report_lines.extend([
            "",
            "=" * 80,
            f"Last Updated: {stats['last_updated']}",
            "=" * 80
        ])

        report = "\n".join(report_lines)

        if output_file:
            report_path = LOG_DIR / output_file
            with open(report_path, 'w') as f:
                f.write(report)
            logger.info(f"Report saved to {report_path}")

        return report


# Global monitor instance
_monitor = None


def get_monitor() -> GuardrailMonitor:
    """Get or create global monitor instance."""
    global _monitor
    if _monitor is None:
        _monitor = GuardrailMonitor()
    return _monitor
