"""
Agent Feedback Loop Implementation
Implements Anthropic's core agent pattern: gather context → take action → verify work → repeat

This is the fundamental building block for reliable, self-correcting agents.
"""

import logging
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class IterationLog:
    """Log entry for a single iteration"""
    iteration: int
    timestamp: str
    context: Dict[str, Any]
    output: Any
    verification: Dict[str, Any]
    success: bool
    duration_seconds: float


@dataclass
class FeedbackLoopResult:
    """Result from feedback loop execution"""
    success: bool
    output: Any
    iterations: int
    total_duration_seconds: float
    iteration_log: List[IterationLog] = field(default_factory=list)
    error: Optional[str] = None
    final_verification: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "success": self.success,
            "output": str(self.output),
            "iterations": self.iterations,
            "total_duration_seconds": self.total_duration_seconds,
            "iteration_log": [
                {
                    "iteration": log.iteration,
                    "timestamp": log.timestamp,
                    "success": log.success,
                    "duration_seconds": log.duration_seconds
                }
                for log in self.iteration_log
            ],
            "error": self.error,
            "final_verification": self.final_verification
        }

    def save_to_file(self, filepath: str):
        """Save result to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


class AgentFeedbackLoop:
    """
    Implements Anthropic's agent feedback loop pattern.

    The core pattern for building reliable agents:
    1. GATHER CONTEXT - Collect relevant information
    2. TAKE ACTION - Perform the task
    3. VERIFY WORK - Check if output is correct
    4. REPEAT - If verification fails, try again with learned information

    This pattern enables:
    - Self-correction (agents fix their own mistakes)
    - Iterative improvement (each attempt gets better)
    - Resilience (agents don't give up on first failure)
    - Transparency (full log of what was tried)

    Example:
        >>> loop = AgentFeedbackLoop(max_iterations=5)
        >>> result = loop.execute(
        ...     task={"goal": "implement feature X"},
        ...     context_gatherer=gather_context_func,
        ...     action_executor=execute_action_func,
        ...     verifier=verify_output_func
        ... )
        >>> if result.success:
        ...     print(f"Success after {result.iterations} iterations!")
    """

    def __init__(
        self,
        max_iterations: int = 10,
        enable_learning: bool = True,
        log_file: Optional[str] = None
    ):
        """
        Initialize feedback loop.

        Args:
            max_iterations: Maximum number of iterations before giving up
            enable_learning: If True, passes iteration log to context gatherer
            log_file: Optional file to save execution log
        """
        self.max_iterations = max_iterations
        self.enable_learning = enable_learning
        self.log_file = log_file
        self.iteration_log: List[IterationLog] = []

        logger.info(f"AgentFeedbackLoop initialized (max_iterations={max_iterations})")

    def execute(
        self,
        task: Dict[str, Any],
        context_gatherer: Callable,
        action_executor: Callable,
        verifier: Callable
    ) -> FeedbackLoopResult:
        """
        Execute task with feedback loop.

        Args:
            task: Task description/configuration
            context_gatherer: Function(task, iteration_log) -> context
            action_executor: Function(task, context) -> output
            verifier: Function(output, context, task) -> verification_result

        Returns:
            FeedbackLoopResult with success status, output, and logs

        Example:
            >>> def gather_context(task, log):
            ...     # Analyze previous failures if any
            ...     if log:
            ...         previous_errors = [l.verification.get("error") for l in log]
            ...         return {"previous_errors": previous_errors, "task": task}
            ...     return {"task": task}
            ...
            >>> def take_action(task, context):
            ...     # Implement the task
            ...     return implementation_result
            ...
            >>> def verify(output, context, task):
            ...     # Check if output is correct
            ...     return {"passed": True, "message": "All checks passed"}
            ...
            >>> result = loop.execute(task, gather_context, take_action, verify)
        """
        start_time = datetime.now()
        self.iteration_log = []

        logger.info(f"Starting feedback loop for task: {task.get('goal', 'unknown')}")

        for iteration in range(self.max_iterations):
            iteration_start = datetime.now()

            logger.info(f"Iteration {iteration + 1}/{self.max_iterations}")

            try:
                # STEP 1: GATHER CONTEXT
                logger.debug("Step 1: Gathering context...")
                context = self._gather_context(task, context_gatherer)

                # STEP 2: TAKE ACTION
                logger.debug("Step 2: Taking action...")
                output = self._take_action(task, context, action_executor)

                # STEP 3: VERIFY WORK
                logger.debug("Step 3: Verifying work...")
                verification = self._verify_work(output, context, task, verifier)

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

                # STEP 4: CHECK SUCCESS
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
                        result.save_to_file(self.log_file)

                    return result

                # Verification failed, prepare for next iteration
                logger.warning(
                    f"❌ Iteration {iteration + 1} failed: {verification.get('message', 'unknown error')}"
                )

                # If last iteration, break
                if iteration == self.max_iterations - 1:
                    logger.error("Max iterations reached without success")
                    break

            except Exception as e:
                logger.error(f"Exception in iteration {iteration + 1}: {e}", exc_info=True)

                # Log error iteration
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

                # If last iteration or critical error, give up
                if iteration == self.max_iterations - 1 or "critical" in str(e).lower():
                    break

        # Failed after all iterations
        total_duration = (datetime.now() - start_time).total_seconds()
        logger.error(f"Failed after {self.max_iterations} iterations ({total_duration:.2f}s)")

        result = FeedbackLoopResult(
            success=False,
            output=self.iteration_log[-1].output if self.iteration_log else None,
            iterations=len(self.iteration_log),
            total_duration_seconds=total_duration,
            iteration_log=self.iteration_log,
            error=f"Max iterations ({self.max_iterations}) reached without success"
        )

        if self.log_file:
            result.save_to_file(self.log_file)

        return result

    def _gather_context(self, task: Dict[str, Any], context_gatherer: Callable) -> Dict[str, Any]:
        """
        Execute context gathering step.

        If enable_learning=True, passes iteration_log to gatherer so it can
        learn from previous failures.
        """
        if self.enable_learning:
            return context_gatherer(task, self.iteration_log)
        else:
            return context_gatherer(task, [])

    def _take_action(self, task: Dict[str, Any], context: Dict[str, Any], action_executor: Callable) -> Any:
        """Execute action step."""
        return action_executor(task, context)

    def _verify_work(
        self,
        output: Any,
        context: Dict[str, Any],
        task: Dict[str, Any],
        verifier: Callable
    ) -> Dict[str, Any]:
        """
        Execute verification step.

        Verifier should return:
        {
            "passed": bool,
            "message": str,
            "details": dict (optional),
            "recommendations": list (optional)
        }
        """
        verification = verifier(output, context, task)

        # Ensure required fields
        if "passed" not in verification:
            verification["passed"] = False
        if "message" not in verification:
            verification["message"] = "Unknown verification result"

        return verification

    def _sanitize_for_logging(self, obj: Any) -> Any:
        """Sanitize object for logging (avoid huge objects in logs)"""
        if obj is None:
            return None

        if isinstance(obj, (str, int, float, bool)):
            return obj

        if isinstance(obj, dict):
            # Limit dict size in logs
            if len(str(obj)) > 1000:
                return {"_truncated": True, "_preview": str(obj)[:500] + "..."}
            return {k: self._sanitize_for_logging(v) for k, v in obj.items()}

        if isinstance(obj, list):
            # Limit list size in logs
            if len(obj) > 20:
                return [self._sanitize_for_logging(obj[i]) for i in range(10)] + ["...(truncated)"]
            return [self._sanitize_for_logging(item) for item in obj]

        # For other types, convert to string and truncate if needed
        obj_str = str(obj)
        if len(obj_str) > 500:
            return obj_str[:500] + "...(truncated)"
        return obj_str

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics from last execution"""
        if not self.iteration_log:
            return {"error": "No execution log available"}

        success_count = sum(1 for log in self.iteration_log if log.success)
        failure_count = len(self.iteration_log) - success_count
        avg_duration = sum(log.duration_seconds for log in self.iteration_log) / len(self.iteration_log)

        return {
            "total_iterations": len(self.iteration_log),
            "successful_iterations": success_count,
            "failed_iterations": failure_count,
            "success_rate": success_count / len(self.iteration_log) if self.iteration_log else 0,
            "average_iteration_duration": avg_duration,
            "total_duration": sum(log.duration_seconds for log in self.iteration_log)
        }


if __name__ == "__main__":
    # Example usage
    def example_context_gatherer(task, iteration_log):
        """Example context gatherer that learns from failures"""
        context = {"task": task}

        if iteration_log:
            # Learn from previous failures
            previous_errors = [log.verification.get("error") for log in iteration_log if not log.success]
            context["previous_errors"] = previous_errors
            context["attempt_number"] = len(iteration_log) + 1

        return context

    def example_action_executor(task, context):
        """Example action executor"""
        attempt = context.get("attempt_number", 1)

        # Simulate: fail first 2 times, succeed on 3rd
        if attempt < 3:
            return {"result": "incomplete", "attempt": attempt}
        return {"result": "success", "attempt": attempt}

    def example_verifier(output, context, task):
        """Example verifier"""
        if output.get("result") == "success":
            return {
                "passed": True,
                "message": "Output is correct",
                "details": {"checks_passed": ["format", "content", "quality"]}
            }
        return {
            "passed": False,
            "message": f"Output incomplete at attempt {output.get('attempt')}",
            "error": "result != success"
        }

    # Run example
    loop = AgentFeedbackLoop(max_iterations=5, log_file="/tmp/feedback_loop_example.json")

    task = {"goal": "complete the task", "requirements": ["A", "B", "C"]}

    result = loop.execute(
        task=task,
        context_gatherer=example_context_gatherer,
        action_executor=example_action_executor,
        verifier=example_verifier
    )

    print("\n" + "=" * 60)
    print("FEEDBACK LOOP EXAMPLE RESULT")
    print("=" * 60)
    print(f"Success: {result.success}")
    print(f"Iterations: {result.iterations}")
    print(f"Duration: {result.total_duration_seconds:.2f}s")
    print(f"Output: {result.output}")
    print(f"\nStatistics:")
    print(json.dumps(loop.get_statistics(), indent=2))
