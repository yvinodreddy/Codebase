"""
Subagent Orchestrator
Manages parallel subagent execution for performance and context isolation

Based on Anthropic's subagent pattern for parallelization and context management
"""

import logging
import time
import threading
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, Future
import json

try:
    from .context_manager import ContextManager
    from .feedback_loop import AgentFeedbackLoop
except ImportError:
    from context_manager import ContextManager
    from feedback_loop import AgentFeedbackLoop

logger = logging.getLogger(__name__)


@dataclass
class SubagentResult:
    """Result from subagent execution"""
    subagent_id: str
    task: Dict[str, Any]
    success: bool
    output: Any
    output_summary: Optional[str] = None
    key_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    iterations: int = 0
    duration_seconds: float = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "subagent_id": self.subagent_id,
            "task": self.task,
            "success": self.success,
            "output_summary": self.output_summary,
            "key_data": self.key_data,
            "error": self.error,
            "iterations": self.iterations,
            "duration_seconds": self.duration_seconds,
            "timestamp": self.timestamp
        }


class Subagent:
    """Individual subagent with isolated context"""

    def __init__(
        self,
        subagent_id: str,
        task: Dict[str, Any],
        context_window_size: int = 50000
    ):
        self.subagent_id = subagent_id
        self.task = task
        self.context = ContextManager(max_tokens=context_window_size)
        self.feedback_loop = AgentFeedbackLoop(max_iterations=5)
        self.status = "initialized"
        self.result: Optional[SubagentResult] = None

    def execute(
        self,
        context_gatherer: Callable,
        action_executor: Callable,
        verifier: Callable
    ) -> SubagentResult:
        """
        Execute subagent task.

        Returns SubagentResult with only relevant information (not full context)
        """
        start_time = time.time()
        self.status = "running"

        logger.info(f"Subagent {self.subagent_id} starting execution")

        try:
            # Execute with feedback loop
            loop_result = self.feedback_loop.execute(
                task=self.task,
                context_gatherer=context_gatherer,
                action_executor=action_executor,
                verifier=verifier
            )

            duration = time.time() - start_time

            # Extract only relevant information (not full context!)
            result = SubagentResult(
                subagent_id=self.subagent_id,
                task=self.task,
                success=loop_result.success,
                output=loop_result.output,
                output_summary=self._summarize_output(loop_result.output),
                key_data=self._extract_key_data(loop_result.output),
                error=loop_result.error,
                iterations=loop_result.iterations,
                duration_seconds=duration
            )

            self.status = "completed"
            self.result = result

            logger.info(
                f"Subagent {self.subagent_id} completed "
                f"(success={result.success}, iterations={result.iterations})"
            )

            return result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Subagent {self.subagent_id} failed: {e}", exc_info=True)

            result = SubagentResult(
                subagent_id=self.subagent_id,
                task=self.task,
                success=False,
                output=None,
                error=str(e),
                duration_seconds=duration
            )

            self.status = "failed"
            self.result = result

            return result

    def _summarize_output(self, output: Any) -> str:
        """Create brief summary of output (not full output!)"""
        if output is None:
            return "No output"

        if isinstance(output, dict):
            # Extract key fields
            keys = list(output.keys())[:5]
            return f"Dict with {len(output)} keys: {keys}"

        if isinstance(output, list):
            return f"List with {len(output)} items"

        if isinstance(output, str):
            # Return first 200 chars
            return output[:200] + ("..." if len(output) > 200 else "")

        return str(type(output).__name__)

    def _extract_key_data(self, output: Any) -> Optional[Dict[str, Any]]:
        """Extract only key data from output (not everything!)"""
        if output is None:
            return None

        if isinstance(output, dict):
            # Extract fields marked as "key" or "important"
            key_data = {}
            for k, v in output.items():
                if "key" in k.lower() or "important" in k.lower() or "summary" in k.lower():
                    key_data[k] = v
            return key_data if key_data else None

        return None


class SubagentOrchestrator:
    """
    Manages parallel subagent execution.

    Key benefits:
    1. Parallelization - Run multiple tasks simultaneously
    2. Context Isolation - Each subagent has own context window
    3. Efficiency - Return only relevant info, not full context

    Example:
        >>> orchestrator = SubagentOrchestrator(max_parallel=5)
        >>>
        >>> # Spawn multiple subagents
        >>> tasks = [
        >>>     {"goal": "search emails for 'project X'"},
        >>>     {"goal": "search calendar for meetings"},
        >>>     {"goal": "search docs for specifications"}
        >>> ]
        >>> subagent_ids = orchestrator.spawn_parallel(tasks)
        >>>
        >>> # Wait for results
        >>> results = orchestrator.wait_for_subagents(subagent_ids)
        >>>
        >>> # Merge results (only relevant info, not full context!)
        >>> merged = orchestrator.merge_subagent_results(results)
    """

    def __init__(
        self,
        max_parallel: int = 5,
        default_context_size: int = 50000
    ):
        """
        Initialize orchestrator.

        Args:
            max_parallel: Max number of subagents to run simultaneously
            default_context_size: Default context window size for subagents
        """
        self.max_parallel = max_parallel
        self.default_context_size = default_context_size
        self.active_subagents: Dict[str, Subagent] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_parallel)
        self.futures: Dict[str, Future] = {}

        logger.info(f"SubagentOrchestrator initialized (max_parallel={max_parallel})")

    def spawn_subagent(
        self,
        task: Dict[str, Any],
        context_window_size: Optional[int] = None
    ) -> str:
        """
        Spawn new subagent with isolated context.

        Args:
            task: Task description for subagent
            context_window_size: Context window size (default: use default_context_size)

        Returns:
            subagent_id: Identifier for this subagent
        """
        subagent_id = f"subagent_{len(self.active_subagents)}_{int(time.time()*1000)}"

        subagent = Subagent(
            subagent_id=subagent_id,
            task=task,
            context_window_size=context_window_size or self.default_context_size
        )

        self.active_subagents[subagent_id] = subagent

        logger.info(f"Spawned subagent {subagent_id} with task: {task.get('goal', 'unknown')}")

        return subagent_id

    def spawn_parallel(
        self,
        tasks: List[Dict[str, Any]],
        context_gatherer: Callable,
        action_executor: Callable,
        verifier: Callable
    ) -> List[str]:
        """
        Spawn multiple subagents in parallel.

        Args:
            tasks: List of task descriptions
            context_gatherer: Function for gathering context
            action_executor: Function for taking action
            verifier: Function for verifying output

        Returns:
            List of subagent IDs
        """
        # Limit to max_parallel
        batch_size = min(len(tasks), self.max_parallel)

        subagent_ids = []

        for i, task in enumerate(tasks[:batch_size]):
            subagent_id = self.spawn_subagent(task)
            subagent_ids.append(subagent_id)

            # Execute subagent in background
            future = self.executor.submit(
                self._execute_subagent,
                subagent_id,
                context_gatherer,
                action_executor,
                verifier
            )
            self.futures[subagent_id] = future

        logger.info(f"Spawned {len(subagent_ids)} subagents in parallel")

        return subagent_ids

    def _execute_subagent(
        self,
        subagent_id: str,
        context_gatherer: Callable,
        action_executor: Callable,
        verifier: Callable
    ) -> SubagentResult:
        """Execute subagent (called in background thread)"""
        subagent = self.active_subagents[subagent_id]
        return subagent.execute(context_gatherer, action_executor, verifier)

    def wait_for_subagents(
        self,
        subagent_ids: List[str],
        timeout: float = 300
    ) -> Dict[str, SubagentResult]:
        """
        Wait for subagents to complete.

        Args:
            subagent_ids: List of subagent IDs to wait for
            timeout: Timeout in seconds

        Returns:
            Dict of subagent_id -> SubagentResult

        Raises:
            TimeoutError if timeout exceeded
        """
        results = {}
        start_time = time.time()

        logger.info(f"Waiting for {len(subagent_ids)} subagents (timeout={timeout}s)")

        for subagent_id in subagent_ids:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Subagents exceeded timeout ({timeout}s)")

            if subagent_id in self.futures:
                # Wait for this subagent's future
                remaining_time = timeout - (time.time() - start_time)
                try:
                    result = self.futures[subagent_id].result(timeout=remaining_time)
                    results[subagent_id] = result
                except TimeoutError:
                    logger.error(f"Subagent {subagent_id} timed out")
                    results[subagent_id] = SubagentResult(
                        subagent_id=subagent_id,
                        task=self.active_subagents[subagent_id].task,
                        success=False,
                        output=None,
                        error="Timeout exceeded"
                    )
            else:
                # Subagent not found or not started
                logger.warning(f"Subagent {subagent_id} not found")

        elapsed = time.time() - start_time
        logger.info(f"All subagents completed in {elapsed:.2f}s")

        return results

    def merge_subagent_results(self, results: Dict[str, SubagentResult]) -> Dict[str, Any]:
        """
        Merge results from multiple subagents.

        Returns only relevant information, NOT full context!

        Args:
            results: Dict of subagent_id -> SubagentResult

        Returns:
            Merged result with key findings and errors
        """
        merged = {
            "success": all(r.success for r in results.values()),
            "total_subagents": len(results),
            "successful_subagents": sum(1 for r in results.values() if r.success),
            "failed_subagents": sum(1 for r in results.values() if not r.success),
            "key_findings": [],
            "errors": [],
            "total_iterations": sum(r.iterations for r in results.values()),
            "total_duration": sum(r.duration_seconds for r in results.values())
        }

        for subagent_id, result in results.items():
            if result.success:
                # Extract only relevant info
                merged["key_findings"].append({
                    "subagent": subagent_id,
                    "task": result.task.get("goal", "unknown"),
                    "summary": result.output_summary,
                    "key_data": result.key_data
                })
            else:
                merged["errors"].append({
                    "subagent": subagent_id,
                    "task": result.task.get("goal", "unknown"),
                    "error": result.error
                })

        logger.info(
            f"Merged {len(results)} subagent results "
            f"({merged['successful_subagents']} successful, {merged['failed_subagents']} failed)"
        )

        return merged

    def get_statistics(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            "total_subagents_spawned": len(self.active_subagents),
            "max_parallel": self.max_parallel,
            "active_futures": len(self.futures),
            "completed_subagents": sum(
                1 for s in self.active_subagents.values()
                if s.status == "completed"
            ),
            "failed_subagents": sum(
                1 for s in self.active_subagents.values()
                if s.status == "failed"
            )
        }

    def cleanup(self):
        """Cleanup resources"""
        self.executor.shutdown(wait=True)
        logger.info("SubagentOrchestrator cleanup complete")


if __name__ == "__main__":
    # Example usage
    def example_context_gatherer(task, iteration_log):
        """Example context gatherer"""
        return {"task": task, "subagent": True}

    def example_action_executor(task, context):
        """Example action executor"""
        time.sleep(1)  # Simulate work
        return {
            "result": f"Completed task: {task.get('goal')}",
            "data": [1, 2, 3, 4, 5]
        }

    def example_verifier(output, context, task):
        """Example verifier"""
        return {
            "passed": True,
            "message": "Output is correct"
        }

    # Create orchestrator
    orchestrator = SubagentOrchestrator(max_parallel=3)

    # Define tasks
    tasks = [
        {"goal": "search emails for 'project X'"},
        {"goal": "search calendar for meetings"},
        {"goal": "search docs for specifications"},
        {"goal": "analyze previous implementations"},
        {"goal": "check dependencies"}
    ]

    print("=" * 60)
    print("SUBAGENT ORCHESTRATOR EXAMPLE")
    print("=" * 60)

    # Spawn subagents in parallel
    print(f"\nSpawning {len(tasks)} subagents...")
    subagent_ids = orchestrator.spawn_parallel(
        tasks=tasks,
        context_gatherer=example_context_gatherer,
        action_executor=example_action_executor,
        verifier=example_verifier
    )

    # Wait for results
    print("Waiting for subagents to complete...")
    results = orchestrator.wait_for_subagents(subagent_ids, timeout=30)

    # Merge results
    print("\nMerging results...")
    merged = orchestrator.merge_subagent_results(results)

    # Display results
    print("\n" + "=" * 60)
    print("MERGED RESULTS")
    print("=" * 60)
    print(json.dumps(merged, indent=2))

    # Show statistics
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    stats = orchestrator.get_statistics()
    print(json.dumps(stats, indent=2))

    # Cleanup
    orchestrator.cleanup()
    print("\n✅ Example complete")
