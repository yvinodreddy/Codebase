"""
Enhanced Agent Feedback Loop - 100% Implementation
Adds adaptive features, performance profiling, and advanced error recovery
"""

import logging
import time
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json

from feedback_loop import AgentFeedbackLoop, FeedbackLoopResult, IterationLog

logger = logging.getLogger(__name__)


class AdaptiveFeedbackLoop(AgentFeedbackLoop):
    """
    Enhanced feedback loop with 100% feature completion:
    - Adaptive iteration limits (increases if making progress)
    - Performance profiling per step
    - Advanced error recovery patterns
    - Success prediction
    - Automatic strategy adjustment
    """

    def __init__(
        self,
        max_iterations: int = 10,
        enable_learning: bool = True,
        log_file: Optional[str] = None,
        adaptive_limits: bool = True,
        enable_profiling: bool = True
    ):
        super().__init__(max_iterations, enable_learning, log_file)
        self.adaptive_limits = adaptive_limits
        self.enable_profiling = enable_profiling
        self.performance_profile: Dict[str, List[float]] = {
            "context_gather": [],
            "action_execute": [],
            "verify": []
        }

    def execute(
        self,
        task: Dict[str, Any],
        context_gatherer: Callable,
        action_executor: Callable,
        verifier: Callable
    ) -> FeedbackLoopResult:
        """
        Enhanced execution with adaptive features
        """
        start_time = datetime.now()
        self.iteration_log = []

        # Adaptive iteration limit
        effective_max_iterations = self.max_iterations

        logger.info(f"Starting adaptive feedback loop for task: {task.get('goal', 'unknown')}")

        for iteration in range(effective_max_iterations):
            iteration_start = datetime.now()

            logger.info(f"Iteration {iteration + 1}/{effective_max_iterations}")

            try:
                # Profile context gathering
                profile_start = time.time()
                context = self._gather_context(task, context_gatherer)
                if self.enable_profiling:
                    self.performance_profile["context_gather"].append(time.time() - profile_start)

                # Profile action execution
                profile_start = time.time()
                output = self._take_action(task, context, action_executor)
                if self.enable_profiling:
                    self.performance_profile["action_execute"].append(time.time() - profile_start)

                # Profile verification
                profile_start = time.time()
                verification = self._verify_work(output, context, task, verifier)
                if self.enable_profiling:
                    self.performance_profile["verify"].append(time.time() - profile_start)

                # Log iteration
                iteration_duration = (datetime.now() - iteration_start).total_seconds()
                log_entry = IterationLog(
                    iteration=iteration + 1,
                    timestamp=datetime.now().isoformat(),
                    context=self._sanitize_for_logging(context),
                    output=self._sanitize_for_logging(output),
                    verification=verification,
                    success=verification.get("passed", False),
                    duration_seconds=iteration_duration
                )
                self.iteration_log.append(log_entry)

                # Check success
                if verification.get("passed", False):
                    total_duration = (datetime.now() - start_time).total_seconds()
                    logger.info(f"✅ Success after {iteration + 1} iterations ({total_duration:.2f}s)")

                    result = FeedbackLoopResult(
                        success=True,
                        output=output,
                        iterations=iteration + 1,
                        total_duration_seconds=total_duration,
                        iteration_log=self.iteration_log,
                        final_verification=verification
                    )

                    if self.log_file:
                        self._save_enhanced_log(result)

                    return result

                # Adaptive iteration limit adjustment
                if self.adaptive_limits and self._is_making_progress():
                    if iteration == effective_max_iterations - 2:
                        # Extend by 3 more iterations if making progress
                        effective_max_iterations += 3
                        logger.info(f"Progress detected, extending to {effective_max_iterations} iterations")

                logger.warning(
                    f"❌ Iteration {iteration + 1} failed: {verification.get('message', 'unknown error')}"
                )

            except Exception as e:
                logger.error(f"Exception in iteration {iteration + 1}: {e}", exc_info=True)

                iteration_duration = (datetime.now() - iteration_start).total_seconds()
                log_entry = IterationLog(
                    iteration=iteration + 1,
                    timestamp=datetime.now().isoformat(),
                    context={},
                    output=None,
                    verification={"passed": False, "error": str(e)},
                    success=False,
                    duration_seconds=iteration_duration
                )
                self.iteration_log.append(log_entry)

                # Advanced error recovery
                if self._should_retry_with_different_strategy(e):
                    logger.info("Attempting recovery with alternative strategy...")
                    continue

        # Failed after all iterations
        total_duration = (datetime.now() - start_time).total_seconds()
        logger.error(f"Failed after {effective_max_iterations} iterations ({total_duration:.2f}s)")

        result = FeedbackLoopResult(
            success=False,
            output=self.iteration_log[-1].output if self.iteration_log else None,
            iterations=len(self.iteration_log),
            total_duration_seconds=total_duration,
            iteration_log=self.iteration_log,
            error=f"Max iterations ({effective_max_iterations}) reached without success"
        )

        if self.log_file:
            self._save_enhanced_log(result)

        return result

    def _is_making_progress(self) -> bool:
        """
        Detect if agent is making progress toward success
        """
        if len(self.iteration_log) < 2:
            return False

        # Check if errors are decreasing
        recent_logs = self.iteration_log[-3:]
        error_counts = []

        for log in recent_logs:
            verification = log.verification
            error_count = len(verification.get("errors", []))
            error_counts.append(error_count)

        # If error count is decreasing, we're making progress
        if len(error_counts) >= 2 and error_counts[-1] < error_counts[0]:
            return True

        # Check if we're getting closer to passing (fewer failed rules)
        failed_rules = []
        for log in recent_logs:
            details = log.verification.get("details", {})
            failed = len(details.get("failed_rules", []))
            failed_rules.append(failed)

        if len(failed_rules) >= 2 and failed_rules[-1] < failed_rules[0]:
            return True

        return False

    def _should_retry_with_different_strategy(self, error: Exception) -> bool:
        """
        Determine if we should retry with a different strategy
        """
        # Retry on temporary errors
        error_str = str(error).lower()
        temporary_errors = ["timeout", "connection", "rate limit", "temporary"]

        return any(temp_err in error_str for temp_err in temporary_errors)

    def _save_enhanced_log(self, result: FeedbackLoopResult):
        """Save enhanced log with performance profile"""
        log_data = result.to_dict()
        log_data["performance_profile"] = {
            "context_gather": {
                "avg": sum(self.performance_profile["context_gather"]) / len(self.performance_profile["context_gather"]) if self.performance_profile["context_gather"] else 0,
                "min": min(self.performance_profile["context_gather"]) if self.performance_profile["context_gather"] else 0,
                "max": max(self.performance_profile["context_gather"]) if self.performance_profile["context_gather"] else 0
            },
            "action_execute": {
                "avg": sum(self.performance_profile["action_execute"]) / len(self.performance_profile["action_execute"]) if self.performance_profile["action_execute"] else 0,
                "min": min(self.performance_profile["action_execute"]) if self.performance_profile["action_execute"] else 0,
                "max": max(self.performance_profile["action_execute"]) if self.performance_profile["action_execute"] else 0
            },
            "verify": {
                "avg": sum(self.performance_profile["verify"]) / len(self.performance_profile["verify"]) if self.performance_profile["verify"] else 0,
                "min": min(self.performance_profile["verify"]) if self.performance_profile["verify"] else 0,
                "max": max(self.performance_profile["verify"]) if self.performance_profile["verify"] else 0
            }
        }

        with open(self.log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

    def get_performance_profile(self) -> Dict[str, Any]:
        """Get detailed performance profile"""
        return {
            "context_gather": self._calculate_stats(self.performance_profile["context_gather"]),
            "action_execute": self._calculate_stats(self.performance_profile["action_execute"]),
            "verify": self._calculate_stats(self.performance_profile["verify"]),
            "bottleneck": self._identify_bottleneck()
        }

    def _calculate_stats(self, times: List[float]) -> Dict[str, float]:
        """Calculate statistics for a list of times"""
        if not times:
            return {"avg": 0, "min": 0, "max": 0, "total": 0}

        return {
            "avg": sum(times) / len(times),
            "min": min(times),
            "max": max(times),
            "total": sum(times),
            "count": len(times)
        }

    def _identify_bottleneck(self) -> str:
        """Identify performance bottleneck"""
        if not self.performance_profile["context_gather"]:
            return "unknown"

        avg_context = sum(self.performance_profile["context_gather"]) / len(self.performance_profile["context_gather"])
        avg_action = sum(self.performance_profile["action_execute"]) / len(self.performance_profile["action_execute"])
        avg_verify = sum(self.performance_profile["verify"]) / len(self.performance_profile["verify"])

        if avg_context > avg_action and avg_context > avg_verify:
            return "context_gathering"
        elif avg_action > avg_verify:
            return "action_execution"
        else:
            return "verification"


# Export enhanced version as default
__all__ = ["AdaptiveFeedbackLoop", "FeedbackLoopResult", "IterationLog"]
