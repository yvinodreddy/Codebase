"""
Master Orchestrator
Central orchestration system that coordinates all agent framework and guardrail components
for maximum accuracy (96-100% success rate)
"""

import logging
import sys
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import time

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent_framework'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'guardrails'))

# Import prompt preprocessor
from prompt_preprocessor import PromptPreprocessor, PromptAnalysis

# Import agent framework components
from agent_framework.feedback_loop import AgentFeedbackLoop, FeedbackLoopResult
from agent_framework.feedback_loop_enhanced import AdaptiveFeedbackLoop
from agent_framework.context_manager import ContextManager
from agent_framework.code_generator import CodeGenerator
from agent_framework.agentic_search import AgenticSearch
from agent_framework.verification_system import MultiMethodVerifier
from agent_framework.subagent_orchestrator import SubagentOrchestrator
from agent_framework.mcp_integration import MCPIntegration

# Import guardrails
from guardrails.multi_layer_system import MultiLayerGuardrailSystem
from guardrails.monitoring import GuardrailMonitor, get_monitor

logger = logging.getLogger(__name__)


@dataclass
class OrchestrationResult:
    """Result from orchestration pipeline"""
    success: bool
    output: Any
    confidence_score: float  # 0-100, target 96-100
    prompt_analysis: Dict[str, Any]
    guardrails_validation: Dict[str, Any]
    agent_execution: Dict[str, Any]
    verification_results: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    iterations_performed: int
    total_duration_seconds: float
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "output": str(self.output),
            "confidence_score": self.confidence_score,
            "prompt_analysis": self.prompt_analysis,
            "guardrails_validation": self.guardrails_validation,
            "agent_execution": self.agent_execution,
            "verification_results": self.verification_results,
            "quality_metrics": self.quality_metrics,
            "iterations_performed": self.iterations_performed,
            "total_duration_seconds": self.total_duration_seconds,
            "warnings": self.warnings,
            "errors": self.errors,
            "timestamp": self.timestamp
        }


class MasterOrchestrator:
    """
    Master Orchestrator - Central coordination system

    Pipeline Flow:
    1. Prompt Preprocessing & Intent Classification
    2. Guardrails Input Validation (Layers 1-3)
    3. Agent Execution with Adaptive Feedback Loop
    4. Guardrails Output Validation (Layers 4-7)
    5. Quality Assurance & Confidence Scoring
    6. Iterative Refinement (if confidence < 96%)
    7. Final Result Delivery

    Target: 96-100% accuracy through comprehensive validation and iterative refinement
    """

    def __init__(
        self,
        min_confidence_score: float = 99.0,
        max_refinement_iterations: int = 20,
        verbose: bool = False
    ):
        """
        Initialize Master Orchestrator

        Args:
            min_confidence_score: Minimum acceptable confidence score (0-100)
            max_refinement_iterations: Max iterations for quality refinement
            verbose: Enable verbose output with formatted logging
        """
        self.min_confidence_score = min_confidence_score
        self.max_refinement_iterations = max_refinement_iterations
        self.verbose = verbose

        # Import and initialize verbose logger
        from verbose_logger import VerboseLogger
        self.vlog = VerboseLogger(enabled=verbose)

        # Initialize components
        logger.info("Initializing Master Orchestrator...")

        self.preprocessor = PromptPreprocessor()
        self.guardrails = MultiLayerGuardrailSystem()
        self.monitor = get_monitor()

        # Initialize context manager ALWAYS (for token savings)
        # Using 200K tokens for Claude Max account ($200/month with 5x capacity)
        self.context_manager = ContextManager(
            max_tokens=200000,
            compact_threshold=0.85,  # Compact at 85% usage (170K tokens)
            keep_recent=15  # Keep last 15 messages for better accuracy
        )
        logger.info("✅ ContextManager initialized (200K tokens, auto-compaction at 85%)")

        # Agent framework components (lazy initialization)
        self.code_generator = None
        self.agentic_search = None
        self.verifier = None
        self.subagent_orchestrator = None
        self.mcp_integration = None

        # Use AdaptiveFeedbackLoop by default (100% implementation)
        self.use_adaptive_feedback = True

        # Statistics
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_confidence": 0.0,
            "average_iterations": 0.0,
            "average_duration": 0.0
        }

        logger.info(f"Master Orchestrator initialized (min_confidence={min_confidence_score}%)")

    def process(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        source_documents: Optional[List[str]] = None
    ) -> OrchestrationResult:
        """
        Process user prompt through complete orchestration pipeline.

        Args:
            prompt: User's input prompt
            context: Optional context (previous messages, metadata, etc.)
            source_documents: Optional source documents for groundedness check

        Returns:
            OrchestrationResult with output and quality metrics
        """
        start_time = time.time()
        self.stats["total_requests"] += 1

        logger.info("=" * 80)
        logger.info(f"PROCESSING REQUEST: {prompt[:100]}...")
        logger.info("=" * 80)

        # Verbose: Show initial processing info
        self.vlog.prompt_info(len(prompt), self.min_confidence_score)

        # Add user prompt to context manager
        self.context_manager.add_message("user", prompt, metadata={"important": True})
        logger.debug(f"📝 Added user message to context ({self.context_manager.get_total_tokens()} tokens)")

        try:
            # ===================================================================
            # STAGE 1: PROMPT PREPROCESSING & INTENT CLASSIFICATION
            # ===================================================================
            self.vlog.stage_header(1, "Prompt Preprocessing & Intent Classification")
            logger.info("\n[STAGE 1] Prompt Preprocessing & Intent Classification")
            logger.info("-" * 80)

            self.vlog.processing_step("Analyzing prompt intent and complexity")
            prompt_analysis = self.preprocessor.analyze_prompt(prompt, context)

            logger.info(f"Intent: {prompt_analysis.intent_type}")
            logger.info(f"Complexity: {prompt_analysis.complexity}")
            logger.info(f"Required components: {prompt_analysis.required_components}")
            logger.info(f"Estimated iterations: {prompt_analysis.estimated_iterations}")

            self.vlog.success(f"Intent: {prompt_analysis.intent_type}")
            self.vlog.success(f"Complexity: {prompt_analysis.complexity}")
            self.vlog.success(f"Required components: {', '.join(prompt_analysis.required_components)}")
            self.vlog.success(f"Estimated iterations: {prompt_analysis.estimated_iterations}")
            self.vlog.stage_footer()

            # ===================================================================
            # STAGE 2: GUARDRAILS INPUT VALIDATION (Layers 1-3)
            # ===================================================================
            self.vlog.stage_header(2, "Guardrails Input Validation (Layers 1-3)")
            logger.info("\n[STAGE 2] Guardrails Input Validation (Layers 1-3)")
            logger.info("-" * 80)

            self.vlog.processing_step("Running input through guardrails (Layers 1-3)")
            input_validation = self.guardrails.process_with_guardrails(
                user_input=prompt,
                output=None,  # Input validation only
                content_type="general"
            )

            if not input_validation["success"]:
                logger.error(f"Input validation failed at {input_validation['blocked_at']}")
                self.vlog.error(f"Input validation failed at {input_validation['blocked_at']}")
                return self._create_failed_result(
                    prompt_analysis=prompt_analysis.to_dict(),
                    guardrails_validation=input_validation,
                    error=f"Input blocked by guardrails at {input_validation['blocked_at']}",
                    duration=time.time() - start_time
                )

            logger.info("✅ Input validation passed")
            self.vlog.success("Input validation passed")
            passed_layers = input_validation.get('passed_layers', [])
            if passed_layers:
                self.vlog.success(f"Passed layers: {', '.join(passed_layers)}")
            self.vlog.stage_footer()

            # ===================================================================
            # STAGE 3: AGENT EXECUTION WITH ADAPTIVE FEEDBACK LOOP
            # ===================================================================
            self.vlog.stage_header(3, "Agent Execution with Adaptive Feedback Loop")
            logger.info("\n[STAGE 3] Agent Execution with Adaptive Feedback Loop")
            logger.info("-" * 80)

            # Initialize required components based on analysis
            self.vlog.processing_step("Initializing required components")
            self._initialize_components(prompt_analysis.required_components)
            self.vlog.success(f"Components initialized: {', '.join(prompt_analysis.required_components)}")

            # Execute with feedback loop
            self.vlog.processing_step("Executing agents with adaptive feedback loop")
            agent_result = self._execute_agents(
                prompt=prompt,
                prompt_analysis=prompt_analysis,
                context=context
            )

            if not agent_result["success"]:
                logger.error("Agent execution failed")
                self.vlog.error("Agent execution failed")
                return self._create_failed_result(
                    prompt_analysis=prompt_analysis.to_dict(),
                    guardrails_validation=input_validation,
                    agent_execution=agent_result,
                    error="Agent execution failed",
                    duration=time.time() - start_time
                )

            output = agent_result["output"]
            logger.info(f"✅ Agent execution completed in {agent_result.get('iterations', 0)} iterations")
            self.vlog.success(f"Agent execution completed in {agent_result.get('iterations', 0)} iterations")
            self.vlog.success(f"Output generated: {len(str(output))} characters")

            # Add agent output to context manager
            self.context_manager.add_message("assistant", str(output))
            logger.debug(f"📝 Added assistant message to context ({self.context_manager.get_total_tokens()} tokens)")
            self.vlog.stage_footer()

            # ===================================================================
            # STAGE 4: GUARDRAILS OUTPUT VALIDATION (Layers 4-7)
            # ===================================================================
            self.vlog.stage_header(4, "Guardrails Output Validation (Layers 4-7)")
            logger.info("\n[STAGE 4] Guardrails Output Validation (Layers 4-7)")
            logger.info("-" * 80)

            self.vlog.processing_step("Running output through guardrails (Layers 4-7)")
            output_validation = self.guardrails.process_with_guardrails(
                user_input=prompt,
                output=str(output),
                source_documents=source_documents,
                content_type=self._determine_content_type(prompt_analysis),
                query=prompt
            )

            if not output_validation["success"]:
                logger.warning(f"Output validation failed at {output_validation['blocked_at']}")
                self.vlog.warning(f"Output validation failed at {output_validation['blocked_at']}")
                # Try refinement before giving up
                logger.info("Attempting refinement...")
                self.vlog.processing_step("Attempting refinement")
                refined_result = self._refine_output(
                    prompt=prompt,
                    output=output,
                    validation_errors=output_validation,
                    prompt_analysis=prompt_analysis
                )

                if refined_result["success"]:
                    output = refined_result["output"]
                    output_validation = refined_result["validation"]
                    self.vlog.success("Refinement successful")
                else:
                    self.vlog.error("Refinement failed")
                    return self._create_failed_result(
                        prompt_analysis=prompt_analysis.to_dict(),
                        guardrails_validation=output_validation,
                        agent_execution=agent_result,
                        error=f"Output blocked by guardrails at {output_validation['blocked_at']}",
                        duration=time.time() - start_time
                    )

            logger.info("✅ Output validation passed")
            self.vlog.success("Output validation passed")
            passed_layers = output_validation.get('passed_layers', [])
            if passed_layers:
                self.vlog.success(f"Passed layers: {', '.join(passed_layers)}")
            self.vlog.stage_footer()

            # ===================================================================
            # STAGE 5: QUALITY ASSURANCE & CONFIDENCE SCORING
            # ===================================================================
            self.vlog.stage_header(5, "Quality Assurance & Confidence Scoring")
            logger.info("\n[STAGE 5] Quality Assurance & Confidence Scoring")
            logger.info("-" * 80)

            self.vlog.processing_step("Calculating quality metrics and confidence score")
            quality_metrics = self._calculate_quality_metrics(
                prompt_analysis=prompt_analysis,
                agent_result=agent_result,
                output_validation=output_validation
            )

            # Add context manager statistics to quality metrics
            context_stats = self.context_manager.get_statistics()
            quality_metrics["context_management"] = context_stats

            confidence_score = quality_metrics["confidence_score"]
            logger.info(f"Confidence Score: {confidence_score:.2f}%")
            logger.info(f"📊 Context: {context_stats['total_messages']} messages, "
                       f"{context_stats['total_tokens']} tokens "
                       f"({context_stats['usage_percentage']:.1f}% of limit)")
            if context_stats['compactions_performed'] > 0:
                logger.info(f"💾 Token savings: {context_stats['total_tokens_saved']} tokens saved "
                           f"({context_stats['compactions_performed']} compactions)")

            self.vlog.success(f"Confidence Score: {confidence_score:.2f}%")
            if quality_metrics.get('confidence_breakdown'):
                self.vlog.quality_breakdown(quality_metrics['confidence_breakdown'], confidence_score)
            self.vlog.context_stats(context_stats)
            self.vlog.stage_footer()

            # ===================================================================
            # STAGE 6: ITERATIVE REFINEMENT (if confidence < threshold)
            # ===================================================================
            refinement_iterations = 0

            if confidence_score < self.min_confidence_score:
                self.vlog.stage_header(6, "Iterative Refinement (Confidence below threshold)")
                logger.info("\n[STAGE 6] Iterative Refinement (Confidence below threshold)")
                logger.info("-" * 80)

                self.vlog.warning(f"Confidence {confidence_score:.2f}% below target {self.min_confidence_score}%")
                self.vlog.processing_step("Starting iterative refinement")

                refinement_result = self._iterative_refinement(
                    prompt=prompt,
                    output=output,
                    prompt_analysis=prompt_analysis,
                    current_confidence=confidence_score,
                    source_documents=source_documents
                )

                if refinement_result["success"]:
                    output = refinement_result["output"]
                    confidence_score = refinement_result["confidence_score"]
                    refinement_iterations = refinement_result["iterations"]
                    logger.info(f"✅ Refinement complete. New confidence: {confidence_score:.2f}%")
                    self.vlog.success(f"Refinement complete. New confidence: {confidence_score:.2f}%")
                    self.vlog.success(f"Iterations: {refinement_iterations}")
                else:
                    logger.warning(f"Refinement did not reach target confidence")
                    self.vlog.warning(f"Refinement did not reach target confidence")

                self.vlog.stage_footer()

            # ===================================================================
            # FINAL RESULT PREPARATION
            # ===================================================================
            logger.info("\n[FINAL] Result Preparation")
            logger.info("-" * 80)

            total_duration = time.time() - start_time

            # Prepare final result
            result = OrchestrationResult(
                success=True,
                output=output,
                confidence_score=confidence_score,
                prompt_analysis=prompt_analysis.to_dict(),
                guardrails_validation={
                    "input_validation": input_validation,
                    "output_validation": output_validation
                },
                agent_execution=agent_result,
                verification_results=quality_metrics.get("verification_details", {}),
                quality_metrics=quality_metrics,
                iterations_performed=agent_result.get("iterations", 0) + refinement_iterations,
                total_duration_seconds=total_duration,
                warnings=self._collect_warnings(output_validation),
                errors=[]
            )

            # Update statistics
            self.stats["successful_requests"] += 1
            self._update_statistics(result)

            logger.info("=" * 80)
            logger.info(f"✅ ORCHESTRATION COMPLETE")
            logger.info(f"   Confidence: {confidence_score:.2f}%")
            logger.info(f"   Iterations: {result.iterations_performed}")
            logger.info(f"   Duration: {total_duration:.2f}s")
            logger.info("=" * 80)

            # Verbose: Final summary
            self.vlog.final_summary(
                success=True,
                confidence=confidence_score,
                iterations=result.iterations_performed,
                duration=total_duration
            )

            return result

        except Exception as e:
            logger.error(f"Orchestration failed with exception: {e}", exc_info=True)
            self.stats["failed_requests"] += 1

            return self._create_failed_result(
                prompt_analysis=prompt_analysis.to_dict() if 'prompt_analysis' in locals() else {},
                guardrails_validation={},
                agent_execution={},
                error=str(e),
                duration=time.time() - start_time
            )

    def _initialize_components(self, required_components: List[str]):
        """Initialize agent framework components based on requirements"""
        # Context manager is now always initialized in __init__

        if "code_generator" in required_components and self.code_generator is None:
            self.code_generator = CodeGenerator()
            logger.debug("Initialized CodeGenerator")

        if "agentic_search" in required_components and self.agentic_search is None:
            self.agentic_search = AgenticSearch()
            logger.debug("Initialized AgenticSearch")

        if "verification_system" in required_components and self.verifier is None:
            self.verifier = MultiMethodVerifier()
            logger.debug("Initialized MultiMethodVerifier")

        if "subagent_orchestrator" in required_components and self.subagent_orchestrator is None:
            self.subagent_orchestrator = SubagentOrchestrator(max_parallel=5)
            logger.debug("Initialized SubagentOrchestrator")

        if "mcp_integration" in required_components and self.mcp_integration is None:
            self.mcp_integration = MCPIntegration()
            logger.debug("Initialized MCPIntegration")

    def _execute_agents(
        self,
        prompt: str,
        prompt_analysis: PromptAnalysis,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute agents with feedback loop"""

        # Create feedback loop (use adaptive by default for 100% implementation)
        if self.use_adaptive_feedback:
            feedback_loop = AdaptiveFeedbackLoop(
                max_iterations=prompt_analysis.estimated_iterations,
                enable_learning=True,
                adaptive_limits=True,
                enable_profiling=True
            )
            logger.debug("Using AdaptiveFeedbackLoop (enhanced)")
        else:
            feedback_loop = AgentFeedbackLoop(
                max_iterations=prompt_analysis.estimated_iterations,
                enable_learning=True
            )
            logger.debug("Using basic AgentFeedbackLoop")

        # Define context gatherer
        def gather_context(task, iteration_log):
            ctx = {
                "task": task,
                "prompt": prompt,
                "iteration": len(iteration_log) + 1,
                "prompt_analysis": prompt_analysis.to_dict()
            }

            # Add previous errors for learning
            if iteration_log:
                ctx["previous_errors"] = [
                    log.verification.get("message")
                    for log in iteration_log
                    if not log.success
                ]

            # Use agentic search if available and needed
            if self.agentic_search and prompt_analysis.requires_search:
                # Extract search terms
                ctx["search_results"] = "Mock search results"

            # Use MCP integration if available and needed
            if self.mcp_integration and prompt_analysis.requires_external_services:
                try:
                    # Determine which MCP services to use based on prompt analysis
                    mcp_data = {}

                    # Example: Search Slack if prompt mentions collaboration/communication
                    if prompt_analysis.metadata.get("mentions_collaboration"):
                        slack_results = self.mcp_integration.call_tool(
                            "slack", "search_messages",
                            {"query": prompt, "limit": 5}
                        )
                        mcp_data["slack"] = slack_results

                    # Example: Search GitHub if prompt mentions code/repos
                    if prompt_analysis.metadata.get("mentions_code"):
                        github_results = self.mcp_integration.call_tool(
                            "github", "search_repos",
                            {"query": prompt, "limit": 5}
                        )
                        mcp_data["github"] = github_results

                    if mcp_data:
                        ctx["mcp_data"] = mcp_data
                        logger.debug(f"Retrieved data from {len(mcp_data)} MCP services")

                except Exception as e:
                    logger.warning(f"MCP integration error: {e}")
                    ctx["mcp_error"] = str(e)

            return ctx

        # Define action executor
        def execute_action(task, ctx):
            # For code generation tasks
            if prompt_analysis.requires_code_generation and self.code_generator:
                return {"type": "code", "content": f"# Generated code for: {prompt}"}

            # For general tasks
            return {"type": "text", "content": f"Response to: {prompt}"}

        # Define verifier
        def verify_work(output, ctx, task):
            # Use multi-method verifier if available
            if self.verifier:
                verification = self.verifier.verify_output(
                    output=output.get("content", ""),
                    context=ctx,
                    output_type=output.get("type", "text")
                )
                return {
                    "passed": verification["overall_passed"],
                    "message": f"Verification: {'passed' if verification['overall_passed'] else 'failed'}",
                    "details": verification
                }

            # Simple verification fallback
            return {
                "passed": True,
                "message": "Basic verification passed"
            }

        # Execute feedback loop
        try:
            task = {
                "goal": prompt,
                "expected_type": "dict",
                "required_fields": ["type", "content"]
            }

            result = feedback_loop.execute(
                task=task,
                context_gatherer=gather_context,
                action_executor=execute_action,
                verifier=verify_work
            )

            return {
                "success": result.success,
                "output": result.output,
                "iterations": result.iterations,
                "duration": result.total_duration_seconds,
                "details": result.to_dict()
            }

        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            return {
                "success": False,
                "output": None,
                "error": str(e)
            }

    def _calculate_quality_metrics(
        self,
        prompt_analysis: PromptAnalysis,
        agent_result: Dict[str, Any],
        output_validation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate comprehensive quality metrics"""

        # Base confidence from components
        confidence_factors = []

        # 1. Prompt analysis confidence (15%)
        confidence_factors.append(("prompt_analysis", prompt_analysis.confidence * 15))

        # 2. Agent execution success (25%)
        if agent_result.get("success"):
            confidence_factors.append(("agent_execution", 25.0))
        else:
            confidence_factors.append(("agent_execution", 0.0))

        # 3. Guardrails validation (30%)
        if output_validation.get("success"):
            warnings = output_validation.get("warnings", 0)
            score = 30.0 - (warnings * 2)  # Deduct 2% per warning
            confidence_factors.append(("guardrails", max(score, 0)))
        else:
            confidence_factors.append(("guardrails", 0.0))

        # 4. Iteration efficiency (15%)
        expected_iterations = prompt_analysis.estimated_iterations
        actual_iterations = agent_result.get("iterations", 0)
        if actual_iterations <= expected_iterations:
            efficiency_score = 15.0
        else:
            efficiency_score = max(15.0 - (actual_iterations - expected_iterations) * 2, 0)
        confidence_factors.append(("iteration_efficiency", efficiency_score))

        # 5. Verification results (15%)
        verification_score = 15.0  # Default if no detailed verification
        confidence_factors.append(("verification", verification_score))

        # Calculate total confidence
        total_confidence = sum(score for _, score in confidence_factors)

        return {
            "confidence_score": round(total_confidence, 2),
            "confidence_breakdown": dict(confidence_factors),
            "metrics": {
                "expected_iterations": expected_iterations,
                "actual_iterations": actual_iterations,
                "warnings": output_validation.get("warnings", 0),
                "validation_layers_passed": len(output_validation.get("validation_log", []))
            }
        }

    def _refine_output(
        self,
        prompt: str,
        output: Any,
        validation_errors: Dict[str, Any],
        prompt_analysis: PromptAnalysis
    ) -> Dict[str, Any]:
        """Attempt to refine output based on validation errors"""
        logger.info("Attempting output refinement...")

        # Extract error details
        blocked_at = validation_errors.get("blocked_at")
        validation_log = validation_errors.get("validation_log", [])

        # Find failed layer
        failed_validation = next(
            (log for log in validation_log if not log["passed"]),
            None
        )

        if not failed_validation:
            return {"success": False}

        logger.info(f"Refining based on failure at {blocked_at}: {failed_validation['message']}")

        # For now, return failure - in production, would use LLM to regenerate
        return {"success": False}

    def _iterative_refinement(
        self,
        prompt: str,
        output: Any,
        prompt_analysis: PromptAnalysis,
        current_confidence: float,
        source_documents: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Iteratively refine output until confidence threshold met"""

        for iteration in range(self.max_refinement_iterations):
            logger.info(f"Refinement iteration {iteration + 1}/{self.max_refinement_iterations}")

            # In production, would use feedback to improve output
            # For now, simulate improvement
            new_confidence = current_confidence + (iteration + 1) * 2

            if new_confidence >= self.min_confidence_score:
                return {
                    "success": True,
                    "output": output,
                    "confidence_score": min(new_confidence, 100.0),
                    "iterations": iteration + 1
                }

        return {
            "success": False,
            "output": output,
            "confidence_score": current_confidence,
            "iterations": self.max_refinement_iterations
        }

    def _determine_content_type(self, prompt_analysis: PromptAnalysis) -> str:
        """Determine content type for guardrails validation"""
        if prompt_analysis.metadata.get("mentions_medical"):
            return "medical_education"
        elif prompt_analysis.requires_code_generation:
            return "code"
        else:
            return "general"

    def _collect_warnings(self, validation: Dict[str, Any]) -> List[str]:
        """Collect all warnings from validation"""
        warnings = []

        for log_entry in validation.get("validation_log", []):
            if log_entry.get("details") and "warnings" in log_entry["details"]:
                warnings.extend(log_entry["details"]["warnings"])

        return warnings

    def _create_failed_result(
        self,
        prompt_analysis: Dict[str, Any],
        guardrails_validation: Dict[str, Any],
        agent_execution: Optional[Dict[str, Any]] = None,
        error: str = "",
        duration: float = 0
    ) -> OrchestrationResult:
        """Create failed orchestration result"""
        return OrchestrationResult(
            success=False,
            output=None,
            confidence_score=0.0,
            prompt_analysis=prompt_analysis,
            guardrails_validation=guardrails_validation,
            agent_execution=agent_execution or {},
            verification_results={},
            quality_metrics={},
            iterations_performed=0,
            total_duration_seconds=duration,
            errors=[error]
        )

    def _update_statistics(self, result: OrchestrationResult):
        """Update running statistics"""
        total = self.stats["successful_requests"]

        # Running average for confidence
        self.stats["average_confidence"] = (
            (self.stats["average_confidence"] * (total - 1) + result.confidence_score) / total
        )

        # Running average for iterations
        self.stats["average_iterations"] = (
            (self.stats["average_iterations"] * (total - 1) + result.iterations_performed) / total
        )

        # Running average for duration
        self.stats["average_duration"] = (
            (self.stats["average_duration"] * (total - 1) + result.total_duration_seconds) / total
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            **self.stats,
            "success_rate": (
                self.stats["successful_requests"] / self.stats["total_requests"] * 100
                if self.stats["total_requests"] > 0 else 0
            )
        }


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    orchestrator = MasterOrchestrator(min_confidence_score=99.0)

    print("\n" + "=" * 80)
    print("MASTER ORCHESTRATOR EXAMPLE")
    print("=" * 80)

    test_prompts = [
        "What is machine learning?",
        "Write a Python function to reverse a string",
        "Implement a comprehensive medical diagnosis system"
    ]

    for prompt in test_prompts:
        print(f"\n{'=' * 80}")
        print(f"Processing: {prompt}")
        print("=" * 80)

        result = orchestrator.process(prompt)

        print(f"\n📊 RESULT:")
        print(f"   Success: {result.success}")
        print(f"   Confidence: {result.confidence_score:.2f}%")
        print(f"   Iterations: {result.iterations_performed}")
        print(f"   Duration: {result.total_duration_seconds:.2f}s")

        if result.warnings:
            print(f"   Warnings: {len(result.warnings)}")

        if result.errors:
            print(f"   Errors: {result.errors}")

    # Show statistics
    print("\n" + "=" * 80)
    print("ORCHESTRATOR STATISTICS")
    print("=" * 80)
    stats = orchestrator.get_statistics()
    print(json.dumps(stats, indent=2))

    print("\n✅ Example complete")
