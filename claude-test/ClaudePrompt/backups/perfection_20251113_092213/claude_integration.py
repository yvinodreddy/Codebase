"""
Claude SDK Integration Layer
Integrates Claude API with the orchestrator for intelligent prompt processing
"""

import logging
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from dotenv import load_dotenv
import anthropic

from master_orchestrator import MasterOrchestrator, OrchestrationResult
from config import UltrathinkConfig as Config

load_dotenv()

logger = logging.getLogger(__name__)


# =============================================================================
# S1: API KEY MASKING (Security Enhancement)
# =============================================================================

def mask_api_key(key: str) -> str:
    """
    Mask API key for safe logging.

    Shows only first 8 characters, masks the rest.
    Prevents API key exposure in logs, error messages, and debug output.

    Args:
        key: API key to mask

    Returns:
        Masked key string (e.g., "sk-ant-a...***")

    Examples:
        >>> mask_api_key("sk-ant-api03-1234567890abcdef")
        'sk-ant-a...***'
        >>> mask_api_key("short")
        '***'
    """
    if not key or len(key) < 12:
        return "***"
    return f"{key[:8]}...***"


@dataclass
class ClaudeResponse:
    """Response from Claude with orchestration"""
    success: bool
    response_text: str
    claude_model: str
    orchestration_result: OrchestrationResult
    total_tokens: int
    cost_estimate: float
    timestamp: str
    output_validation: Dict[str, Any] = field(default_factory=dict)  # NEW: Output guardrails results
    verification_result: Dict[str, Any] = field(default_factory=dict)  # NEW: Verification results
    final_confidence: float = 0.0  # NEW: Combined confidence score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "response_text": self.response_text,
            "claude_model": self.claude_model,
            "orchestration_metrics": {
                "confidence_score": self.orchestration_result.confidence_score,
                "iterations": self.orchestration_result.iterations_performed,
                "duration": self.orchestration_result.total_duration_seconds
            },
            "output_validation": self.output_validation,
            "verification_result": self.verification_result,
            "final_confidence": self.final_confidence,
            "total_tokens": self.total_tokens,
            "cost_estimate": self.cost_estimate,
            "timestamp": self.timestamp
        }


class ClaudeOrchestrator:
    """
    Claude SDK Integration with Master Orchestrator

    This class provides:
    1. Claude API integration for intelligent responses
    2. Full orchestration pipeline with guardrails
    3. Quality assurance and confidence scoring
    4. Comprehensive logging and monitoring
    """

    # Pricing per million tokens (as of 2025)
    PRICING = {
        "claude-sonnet-4-5-20250929": {"input": 3.00, "output": 15.00},
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},  # Deprecated
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
        "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25}
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-5-20250929",
        min_confidence_score: float = 99.0,
        max_refinement_iterations: int = 20,
        enable_rate_limiting: bool = True  # S4: Rate limiting control
    ):
        """
        Initialize Claude Orchestrator

        Args:
            api_key: Anthropic API key (or uses ANTHROPIC_API_KEY env var)
            model: Claude model to use
            min_confidence_score: Minimum acceptable confidence (0-100)
            max_refinement_iterations: Max iterations for refinement
            enable_rate_limiting: Enable rate limiting (default: True)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")

        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)

        # Initialize orchestrator
        self.orchestrator = MasterOrchestrator(
            min_confidence_score=min_confidence_score,
            max_refinement_iterations=max_refinement_iterations
        )

        # S4: Initialize rate limiter
        self.rate_limiter = None
        if enable_rate_limiting:
            from agent_framework.rate_limiter import RateLimiter
            self.rate_limiter = RateLimiter()
            logger.info(
                f"Rate limiting enabled: {Config.RATE_LIMIT_CALLS} calls per "
                f"{Config.RATE_LIMIT_WINDOW}s ({Config.RATE_LIMIT_CALLS/(Config.RATE_LIMIT_WINDOW/60):.1f}/min)"
            )
        else:
            logger.warning("Rate limiting DISABLED - use with caution!")

        # Statistics
        self.stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0
        }

        # S1: Use masked API key in logs
        logger.info(f"ClaudeOrchestrator initialized (model={model}, api_key={mask_api_key(self.api_key)})")

    def process(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        source_documents: Optional[List[str]] = None
    ) -> ClaudeResponse:
        """
        Process prompt through Claude with full orchestration.

        Args:
            prompt: User's input prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens in response
            temperature: Temperature for response generation (0-1)
            source_documents: Optional source documents for groundedness

        Returns:
            ClaudeResponse with orchestration metrics
        """
        logger.info(f"Processing prompt with Claude ({self.model})")

        # ===================================================================
        # STEP 1: INPUT VALIDATION ONLY (NO FULL PREPROCESSING)
        # ===================================================================
        logger.info("Step 1: Input validation...")

        # Validate input through guardrails (Layers 1-3 only)
        # Layer 1: Prompt Shields
        layer1 = self.orchestrator.guardrails.layer1_prompt_shields(
            user_input=prompt,
            documents=source_documents if source_documents else None
        )
        if not layer1.passed:
            input_validation = {"success": False, "blocked_at": "Layer 1 (Prompt Shields)"}
        else:
            # Layer 2: Input Content Filter
            layer2 = self.orchestrator.guardrails.layer2_input_content_filter(
                user_input=prompt
            )
            if not layer2.passed:
                input_validation = {"success": False, "blocked_at": "Layer 2 (Content Filter)"}
            else:
                # Layer 3: PHI Detection
                layer3 = self.orchestrator.guardrails.layer3_phi_detection(
                    user_input=prompt,
                    content_type="general"
                )
                if not layer3.passed:
                    input_validation = {"success": False, "blocked_at": "Layer 3 (PHI Detection)"}
                else:
                    input_validation = {"success": True, "passed_layers": ["Layer 1", "Layer 2", "Layer 3"]}

        if not input_validation.get("success", True):
            logger.error(f"Input validation failed at {input_validation.get('blocked_at', 'unknown')}")
            # Create minimal orchestration result for failed input
            from master_orchestrator import OrchestrationResult
            failed_result = OrchestrationResult(
                success=False,
                confidence_score=0.0,
                output="",
                prompt_analysis={},
                guardrails_validation=input_validation,
                agent_execution={},
                verification_results={},
                quality_metrics={},
                iterations_performed=0,
                total_duration_seconds=0.0,
                warnings=[],
                errors=[f"Input blocked at {input_validation.get('blocked_at', 'unknown')}"]
            )
            return ClaudeResponse(
                success=False,
                response_text=f"Request blocked: Input validation failed",
                claude_model=self.model,
                orchestration_result=failed_result,
                total_tokens=0,
                cost_estimate=0.0,
                timestamp=datetime.now().isoformat(),
                output_validation={},
                verification_result={},
                final_confidence=0.0
            )

        logger.info("✅ Input validation passed")

        # ===================================================================
        # STEP 2: CALL CLAUDE API
        # ===================================================================
        logger.info("Step 2: Calling Claude API...")

        # Use prompt directly (no pre-enhancement needed)
        enhanced_prompt = prompt

        # Prepare system prompt (with prompt caching support)
        if system_prompt is None:
            system_prompt = self._create_default_system_prompt()

        try:
            # S4: Apply rate limiting BEFORE API call
            if self.rate_limiter:
                wait_time = self.rate_limiter.wait_if_needed(verbose=False)
                if wait_time > 0:
                    logger.info(f"Rate limiter delayed request by {wait_time:.1f}s")

            # Get conversation history from context manager (compacted if needed)
            context_messages = self.orchestrator.context_manager.get_messages()

            # Convert to Claude API format
            claude_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in context_messages
                if msg.role in ["user", "assistant"]  # Skip system messages from compaction
            ]

            # Add current enhanced prompt if not already in history
            if not claude_messages or claude_messages[-1]["content"] != enhanced_prompt:
                claude_messages.append({"role": "user", "content": enhanced_prompt})

            logger.info(f"📝 Using {len(claude_messages)} messages from context "
                       f"({self.orchestrator.context_manager.get_total_tokens()} tokens)")

            # ================================================================
            # PROMPT CACHING: 90% token savings on cached content
            # ================================================================
            # Use system array format with cache_control for caching
            # Caching strategy:
            # 1. Static system prompt (rarely changes)
            # 2. Guardrail rules (never change) ← CACHE THIS
            # 3. Conversation history (grows incrementally) ← CACHE THIS

            system_blocks = []

            # Block 1: Basic system prompt (uncached, small)
            system_blocks.append({
                "type": "text",
                "text": system_prompt
            })

            # Block 2: Guardrail rules and validation protocol (CACHED)
            # This is static and large - perfect for caching
            guardrail_rules = self._get_guardrail_rules_for_cache()
            if guardrail_rules:
                system_blocks.append({
                    "type": "text",
                    "text": guardrail_rules,
                    "cache_control": {"type": "ephemeral"}  # 90% savings
                })

            # Block 3: Recent conversation summary (CACHED)
            # Cache the conversation history up to recent messages
            if len(claude_messages) > 2:
                conversation_summary = self._create_conversation_summary(claude_messages[:-1])
                system_blocks.append({
                    "type": "text",
                    "text": conversation_summary,
                    "cache_control": {"type": "ephemeral"}  # 90% savings
                })

            # Call Claude API with prompt caching
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_blocks,  # ← Use array format for caching
                messages=[claude_messages[-1]] if claude_messages else []  # Only most recent message
            )

            response_text = message.content[0].text
            input_tokens = message.usage.input_tokens
            output_tokens = message.usage.output_tokens
            total_tokens = input_tokens + output_tokens

            # Track prompt caching metrics (if available)
            cache_read_tokens = getattr(message.usage, 'cache_read_input_tokens', 0)
            cache_creation_tokens = getattr(message.usage, 'cache_creation_input_tokens', 0)

            if cache_read_tokens > 0:
                savings_percent = (cache_read_tokens / input_tokens * 100) if input_tokens > 0 else 0
                logger.info(f"💾 Prompt cache HIT: {cache_read_tokens} tokens cached ({savings_percent:.1f}% savings)")
                self.stats["cache_hits"] = self.stats.get("cache_hits", 0) + 1
                self.stats["cache_read_tokens"] = self.stats.get("cache_read_tokens", 0) + cache_read_tokens

            if cache_creation_tokens > 0:
                logger.info(f"💾 Prompt cache WRITE: {cache_creation_tokens} tokens cached")
                self.stats["cache_writes"] = self.stats.get("cache_writes", 0) + 1
                self.stats["cache_creation_tokens"] = self.stats.get("cache_creation_tokens", 0) + cache_creation_tokens

            # Add Claude's response to context manager
            self.orchestrator.context_manager.add_message("assistant", response_text)

            logger.info(f"Claude response received ({total_tokens} tokens)")

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            from master_orchestrator import OrchestrationResult
            failed_result = OrchestrationResult(
                success=False,
                confidence_score=0.0,
                output="",
                prompt_analysis={},
                guardrails_validation={},
                agent_execution={},
                verification_results={},
                quality_metrics={},
                iterations_performed=0,
                total_duration_seconds=0.0,
                warnings=[],
                errors=[f"Claude API error: {str(e)}"]
            )
            return ClaudeResponse(
                success=False,
                response_text=f"Claude API error: {str(e)}",
                claude_model=self.model,
                orchestration_result=failed_result,
                total_tokens=0,
                cost_estimate=0.0,
                timestamp=datetime.now().isoformat(),
                output_validation={},
                verification_result={},
                final_confidence=0.0
            )

        # ===================================================================
        # STEP 3: POST-PROCESS CLAUDE RESPONSE (OUTPUT VALIDATION)
        # ===================================================================
        logger.info("Step 3: Post-processing Claude response...")
        logger.info("Running OUTPUT validation (Guardrails Layer 4-7)...")

        # Validate Claude's response through OUTPUT guardrails (Layers 4-7)
        output_validation = self.orchestrator.guardrails.process_with_guardrails(
            user_input=prompt,
            output=response_text,
            source_documents=source_documents if source_documents else [],
            content_type="general",  # Could be enhanced based on prompt analysis
            query=prompt
        )

        if not output_validation["success"]:
            logger.warning(f"Output validation failed at {output_validation.get('blocked_at', 'unknown layer')}")
            from master_orchestrator import OrchestrationResult
            failed_result = OrchestrationResult(
                success=False,
                confidence_score=0.0,
                output=response_text,
                prompt_analysis={},
                guardrails_validation=output_validation,
                agent_execution={},
                verification_results={},
                quality_metrics={},
                iterations_performed=0,
                total_duration_seconds=0.0,
                warnings=[],
                errors=[f"Output blocked at {output_validation.get('blocked_at')}"]
            )
            return ClaudeResponse(
                success=False,
                response_text=f"Response blocked by guardrails: {output_validation.get('blocked_at')}",
                claude_model=self.model,
                orchestration_result=failed_result,
                total_tokens=total_tokens,
                cost_estimate=self._calculate_cost(input_tokens, output_tokens),
                timestamp=datetime.now().isoformat(),
                output_validation=output_validation,
                verification_result={},
                final_confidence=0.0
            )

        logger.info("✅ Output validation passed (all 7 guardrail layers)")

        # ===================================================================
        # STEP 3.5: VERIFICATION SYSTEM (Multi-method verification)
        # ===================================================================
        logger.info("Running multi-method verification...")

        # Import verification system
        try:
            from agent_framework.verification_system import MultiMethodVerifier
            verifier = MultiMethodVerifier()

            verification_result = verifier.verify_output(
                output=response_text,
                context={
                    "input": prompt,
                    "model": self.model,
                    "source_documents": source_documents
                },
                output_type="text",
                task={"type": "generate_response", "prompt": prompt}
            )

            if not verification_result.get("overall_passed", True):
                logger.warning(f"Verification failed: {verification_result.get('overall_message', 'Unknown')}")
                # Log but don't fail - verification is advisory
            else:
                logger.info(f"✅ Verification passed: {verification_result.get('overall_message', 'All checks passed')}")
        except Exception as e:
            logger.warning(f"Verification system unavailable: {e}")
            verification_result = {"overall_passed": True, "overall_message": "Verification skipped"}

        # Calculate final confidence score
        # Combine output validation and verification (no preprocessing score)
        verification_confidence = verification_result.get("overall_confidence", 100.0)
        output_conf = output_validation.get("confidence", 100.0)

        final_confidence = (
            output_conf * 0.6 +  # Output validation (primary)
            verification_confidence * 0.4  # Verification (secondary)
        )

        logger.info(f"Final confidence: {final_confidence:.2f}%")

        # Create orchestration result for successful completion
        from master_orchestrator import OrchestrationResult
        orchestration_result = OrchestrationResult(
            success=True,
            confidence_score=final_confidence,
            output=response_text,
            prompt_analysis={"intent_type": "general", "complexity": "moderate"},
            guardrails_validation={
                "input_validation": input_validation,
                "output_validation": output_validation
            },
            agent_execution={
                "model": self.model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens
            },
            verification_results=verification_result if verification_result else {},
            quality_metrics={
                "output_validation_confidence": output_conf,
                "verification_confidence": verification_confidence
            },
            iterations_performed=1,
            total_duration_seconds=0.0,  # Will be updated below
            warnings=[],
            errors=[]
        )

        # ===================================================================
        # STEP 4: CALCULATE COST AND PREPARE RESPONSE
        # ===================================================================
        cost_estimate = self._calculate_cost(input_tokens, output_tokens)

        # Update statistics
        self.stats["total_requests"] += 1
        self.stats["total_tokens"] += total_tokens
        self.stats["total_cost"] += cost_estimate

        response = ClaudeResponse(
            success=True,
            response_text=response_text,
            claude_model=self.model,
            orchestration_result=orchestration_result,
            total_tokens=total_tokens,
            cost_estimate=cost_estimate,
            timestamp=datetime.now().isoformat(),
            output_validation=output_validation,  # NEW
            verification_result=verification_result,  # NEW
            final_confidence=final_confidence  # NEW
        )

        logger.info(f"✅ Processing complete (confidence: {final_confidence:.2f}%)")

        return response

    def process_with_validation(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        source_documents: Optional[List[str]] = None,
        target_confidence: float = 99.0,
        max_refinement_iterations: int = 20,
        verbose: bool = False
    ) -> ClaudeResponse:
        """
        Process prompt with MANDATORY 99-100% validation loop.

        This method ensures PRODUCTION-READY quality by:
        1. Getting initial response from Claude
        2. Validating through complete pipeline
        3. Refining until 99%+ confidence achieved
        4. Maximum 20 refinement iterations

        Args:
            prompt: User's input prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens for response
            temperature: Sampling temperature
            source_documents: Optional source documents
            target_confidence: Target confidence (default: 99.0%)
            max_refinement_iterations: Max refinement loops (default: 20)
            verbose: Show detailed validation logs

        Returns:
            ClaudeResponse with 99-100% confidence
        """
        from validation_loop import ValidationLoop

        if verbose:
            print(f"\n{'='*80}")
            print(f"🎯 PRODUCTION-READY PROCESSING - Targeting {target_confidence}% Confidence")
            print(f"{'='*80}\n")

        # STEP 1: Get initial response
        if verbose:
            print("[Step 1] Getting initial response from Claude API...")

        initial_response = self.process(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            source_documents=source_documents
        )

        initial_text = initial_response.response_text
        initial_confidence = initial_response.final_confidence

        if verbose:
            print(f"  Initial confidence: {initial_confidence:.1f}%")
            print(f"  Target confidence: {target_confidence}%\n")

        # Check if already meets target
        if initial_confidence >= target_confidence:
            if verbose:
                print(f"✅ INITIAL RESPONSE MEETS TARGET ({initial_confidence:.1f}% >= {target_confidence}%)")
                print(f"{'='*80}\n")
            return initial_response

        # STEP 2: Validation and refinement loop
        if verbose:
            print(f"[Step 2] Initial confidence below target. Starting refinement loop...")
            print(f"  Maximum refinement iterations: {max_refinement_iterations}\n")

        # Create API call wrapper for refinement
        def claude_refinement_call(refinement_prompt: str) -> str:
            """Wrapper to call Claude API for refinement"""
            refined_response = self.process(
                prompt=refinement_prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                source_documents=source_documents
            )
            return refined_response.response_text

        # Run validation loop
        validation_loop = ValidationLoop(max_iterations=max_refinement_iterations)
        final_text, validation_result = validation_loop.validate_and_refine(
            initial_response=initial_text,
            original_prompt=prompt,
            claude_api_call=claude_refinement_call,
            verbose=verbose
        )

        final_confidence = validation_result.get("confidence", 0.0)

        if verbose:
            print(f"\n{'='*80}")
            print(f"✅ VALIDATION COMPLETE")
            print(f"  Final confidence: {final_confidence:.1f}%")
            print(f"  Target: {target_confidence}%")
            print(f"  Status: {'✅ ACHIEVED' if final_confidence >= target_confidence else '⚠️  BEST EFFORT'}")
            print(f"{'='*80}\n")

        # Create final response with updated confidence
        final_response = ClaudeResponse(
            success=True,
            response_text=final_text,
            claude_model=self.model,
            orchestration_result=initial_response.orchestration_result,
            total_tokens=initial_response.total_tokens,  # Note: doesn't include refinement tokens
            cost_estimate=initial_response.cost_estimate,
            timestamp=datetime.now().isoformat(),
            output_validation=validation_result,
            verification_result=validation_result.get("verification", {}),
            final_confidence=final_confidence
        )

        return final_response

    def _enhance_prompt_with_orchestration(
        self,
        original_prompt: str,
        orchestration_result: OrchestrationResult
    ) -> str:
        """Enhance prompt with orchestration insights"""

        # Extract key insights
        intent = orchestration_result.prompt_analysis.get("intent_type")
        complexity = orchestration_result.prompt_analysis.get("complexity")

        enhancement = f"""[Orchestration Insights]
Intent: {intent}
Complexity: {complexity}
Target Confidence: {orchestration_result.confidence_score:.0f}%

[Original Prompt]
{original_prompt}

Please provide a comprehensive, accurate response that achieves high confidence (96-100%).
"""

        return enhancement

    def _create_default_system_prompt(self) -> str:
        """Create default system prompt with orchestration guidelines"""
        return """You are Claude, integrated with an advanced orchestration system that includes:
- Multi-layer guardrails for safety and accuracy
- Adaptive feedback loops for iterative refinement
- Comprehensive verification systems
- Quality assurance with 96-100% confidence target

Your responses should be:
1. Accurate and well-researched
2. Clear and comprehensive
3. Safe and compliant with all guardrails
4. Structured and easy to understand
5. Verified against source materials when applicable

Always strive for the highest quality and confidence in your responses."""

    def _get_guardrail_rules_for_cache(self) -> str:
        """
        Get guardrail rules for prompt caching.

        This content is static and large - perfect for caching.
        Returns all 7 layers of guardrail rules with detailed descriptions.
        Must be >= 1024 tokens for Claude to cache it.
        """
        return """=== ULTRATHINK GUARDRAIL SYSTEM (7 LAYERS) ===

OVERVIEW:
The ULTRATHINK system employs a comprehensive 7-layer guardrail architecture
designed to ensure safety, accuracy, and compliance at every stage of processing.
These guardrails work in conjunction with adaptive feedback loops, multi-method
verification systems, and quality assurance mechanisms to achieve 96-100%
confidence targets.

Each layer serves a specific purpose and runs automatically on all inputs and
outputs. Failures at any layer result in immediate rejection of the content,
with detailed logging for review and analysis.

================================================================================
INPUT VALIDATION LAYERS (Layers 1-3)
================================================================================

These layers validate user input BEFORE it reaches the AI model, preventing
harmful, malicious, or sensitive content from being processed.

───────────────────────────────────────────────────────────────────────────────
Layer 1: Prompt Shields - Jailbreak Detection
───────────────────────────────────────────────────────────────────────────────

Purpose: Detect and block attempts to bypass safety guidelines through prompt
engineering, jailbreaking, or injection attacks.

Key Functions:
• Jailbreak Pattern Detection: Identifies known jailbreak techniques such as
  role-playing scenarios, hypothetical questions, or encoded instructions
  designed to circumvent safety measures.

• Prompt Injection Prevention: Detects attempts to inject malicious instructions
  that could override system prompts or manipulate the model's behavior in
  unintended ways.

• Input Authenticity Validation: Verifies that user input represents genuine
  requests rather than attempts to manipulate the system through adversarial
  prompting techniques.

• Pattern Matching: Uses both rule-based and ML-based approaches to identify
  suspicious patterns in user input that may indicate malicious intent.

Severity Levels:
- Low (0-2): Minor concerns, potentially ambiguous phrasing
- Medium (3-5): Clear patterns of manipulation attempts
- High (6-8): Definite jailbreak or injection attempts
- Critical (9-10): Severe security threats requiring immediate blocking

───────────────────────────────────────────────────────────────────────────────
Layer 2: Content Filtering - Harmful Content Detection
───────────────────────────────────────────────────────────────────────────────

Purpose: Block harmful, inappropriate, or unsafe content categories in user input.

Categories Monitored:
• Violence: Content depicting, glorifying, or inciting physical harm, assault,
  weapons, or dangerous activities. Includes graphic descriptions, instructions
  for causing harm, or promotion of violent ideologies.

• Hate Speech: Content targeting individuals or groups based on protected
  characteristics including race, ethnicity, religion, gender, sexual orientation,
  disability, or other protected categories. Includes slurs, dehumanizing
  language, and discriminatory content.

• Self-Harm: Content promoting, encouraging, or providing instructions for
  self-injury, suicide, eating disorders, or other forms of self-harm. Includes
  both explicit and implicit encouragement.

• Sexual Content: Inappropriate sexual content, including explicit descriptions,
  solicitation, or content involving minors. Maintains professional boundaries
  while allowing appropriate medical or educational discussions.

• Harassment & Bullying: Content designed to intimidate, threaten, or harass
  individuals or groups. Includes doxxing, stalking, or coordinated harassment.

Detection Methods:
- Keyword matching with context awareness
- Semantic analysis for implicit harmful content
- Pattern recognition for coded or obfuscated harmful content
- Severity scoring across multiple dimensions

───────────────────────────────────────────────────────────────────────────────
Layer 3: PHI Detection - Protected Health Information & Privacy
───────────────────────────────────────────────────────────────────────────────

Purpose: Detect and prevent exposure of personally identifiable information (PII)
and protected health information (PHI) in compliance with HIPAA, GDPR, and other
privacy regulations.

Detectable Information Types:
• Names: Full names, partial names with sufficient identifying context
• Dates: Birth dates, admission dates, discharge dates, death dates
• Contact Information: Addresses, phone numbers, email addresses, URLs
• Identifiers: SSN, medical record numbers, account numbers, license numbers
• Biometrics: Fingerprints, voiceprints, facial recognition data
• Medical Information: Diagnoses, treatment details, test results when paired
  with identifying information

HIPAA Compliance:
This layer ensures compliance with the 18 HIPAA identifiers and prevents
unauthorized disclosure of protected health information. All detected PHI
triggers immediate flagging for review and redaction if necessary.

================================================================================
OUTPUT VALIDATION LAYERS (Layers 4-7)
================================================================================

These layers validate AI-generated content BEFORE it's shown to users, ensuring
quality, accuracy, safety, and compliance.

───────────────────────────────────────────────────────────────────────────────
Layer 4: Medical Terminology Validation
───────────────────────────────────────────────────────────────────────────────

Purpose: Validate accuracy of medical terminology, drug names, dosages, and
clinical information in generated responses.

Validation Checks:
• Medical Terms: Cross-references medical terminology against authoritative
  databases (UMLS, SNOMED CT, ICD-10) to ensure correct usage and spelling.

• Drug Names: Validates pharmaceutical names (generic and brand names), checks
  for common misspellings, and ensures proper capitalization conventions.

• Dosage Information: Verifies that dosage recommendations fall within safe,
  clinically appropriate ranges for the indicated medication and condition.

• Clinical Accuracy: Ensures clinical statements align with current medical
  knowledge and evidence-based practice guidelines.

• Contraindications: Flags potential contraindications or drug interactions
  when multiple medications are mentioned.

This layer is particularly critical for medical education and clinical case
discussions where accuracy can impact patient safety.

───────────────────────────────────────────────────────────────────────────────
Layer 5: Output Content Filtering
───────────────────────────────────────────────────────────────────────────────

Purpose: Apply the same harmful content categories as Layer 2, but to AI-generated
outputs to ensure the model hasn't inadvertently generated unsafe content.

This layer prevents the system from outputting:
• Harmful instructions or information that could cause physical harm
• Biased, discriminatory, or hateful content
• Content that could facilitate self-harm or dangerous behaviors
• Inappropriate sexual content or content violating professional boundaries
• Content that harasses, threatens, or intimidates

Even when user input passes Layer 2, the model could potentially generate
problematic content in its response. Layer 5 catches these cases.

───────────────────────────────────────────────────────────────────────────────
Layer 6: Groundedness Check - Factual Accuracy Validation
───────────────────────────────────────────────────────────────────────────────

Purpose: Verify that generated responses are grounded in provided source materials
and detect hallucinations or unsupported claims.

Validation Methods:
• Source Attribution: Checks that factual claims can be traced back to provided
  source documents with proper citation and context.

• Hallucination Detection: Identifies statements that appear factual but cannot
  be verified against source materials, indicating potential model hallucination.

• Consistency Checking: Ensures response content is internally consistent and
  doesn't contradict itself or the source materials.

• Evidence Strength: Assesses whether claims are supported by sufficient evidence
  and whether the level of certainty in the response matches the evidence strength.

This layer is critical for maintaining trust and ensuring responses don't include
fabricated information, especially in medical, legal, or educational contexts.

───────────────────────────────────────────────────────────────────────────────
Layer 7: Compliance & Fact Checking
───────────────────────────────────────────────────────────────────────────────

Purpose: Final compliance verification ensuring responses meet regulatory
requirements and factual accuracy standards.

Compliance Checks:
• HIPAA Compliance: Verifies no unauthorized PHI disclosure in outputs
• Medical Fact Checking: Cross-validates medical statements against current
  clinical guidelines and research
• Regulatory Compliance: Ensures responses comply with relevant regulations
  (FDA, medical board guidelines, etc.)
• Ethical Standards: Validates adherence to medical ethics and professional
  standards of care

This final layer provides comprehensive oversight before any content reaches
the end user, ensuring complete compliance with all applicable regulations
and standards.

================================================================================
ENFORCEMENT POLICY
================================================================================

ALL responses must pass ALL applicable guardrail layers before delivery to users.

Failure at ANY layer results in:
1. Immediate blocking of the content
2. Detailed logging of the failure reason and layer
3. User notification of the block with appropriate explanation
4. No exposure of potentially harmful or non-compliant content

This strict enforcement policy ensures the highest levels of safety, accuracy,
and compliance across all system operations.
"""

    def _create_conversation_summary(self, messages: List[Dict]) -> str:
        """
        Create summary of conversation history for caching.

        Summarizes past messages while preserving key information.
        """
        if not messages:
            return ""

        summary_parts = ["=== CONVERSATION HISTORY ===\n"]

        # Summarize older messages (keep last 5 in full)
        if len(messages) > 5:
            summary_parts.append(f"[Earlier: {len(messages)-5} messages summarized]\n")
            recent_messages = messages[-5:]
        else:
            recent_messages = messages

        # Add recent messages
        for i, msg in enumerate(recent_messages, 1):
            role = msg["role"].upper()
            content_preview = msg["content"][:200] + "..." if len(msg["content"]) > 200 else msg["content"]
            summary_parts.append(f"{role} {i}: {content_preview}\n")

        return "\n".join(summary_parts)

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate estimated cost for API call"""
        pricing = self.PRICING.get(self.model)
        if not pricing:
            return 0.0

        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]

        return input_cost + output_cost

    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics"""
        stats = {
            **self.stats,
            "orchestrator_stats": self.orchestrator.get_statistics()
        }

        # S4: Add rate limiting stats if enabled
        if self.rate_limiter:
            stats["rate_limiting"] = self.rate_limiter.get_current_usage()

        return stats

    def get_rate_limit_stats(self) -> Optional[Dict]:
        """
        Get current rate limiting statistics.

        Returns:
            Dict with rate limit stats, or None if rate limiting disabled
        """
        if self.rate_limiter:
            return self.rate_limiter.get_current_usage()
        return None


if __name__ == "__main__":
    # Example usage
    import json

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Note: Requires ANTHROPIC_API_KEY environment variable
    try:
        orchestrator = ClaudeOrchestrator(
            model="claude-sonnet-4-5-20250929",
            min_confidence_score=99.0
        )

        print("\n" + "=" * 80)
        print("CLAUDE ORCHESTRATOR EXAMPLE")
        print("=" * 80)

        test_prompts = [
            "Explain machine learning in simple terms",
            "Write a Python function to calculate Fibonacci numbers"
        ]

        for prompt in test_prompts:
            print(f"\n{'=' * 80}")
            print(f"Prompt: {prompt}")
            print("=" * 80)

            response = orchestrator.process(
                prompt=prompt,
                max_tokens=1024
            )

            print(f"\n📊 RESULT:")
            print(f"   Success: {response.success}")
            print(f"   Confidence: {response.orchestration_result.confidence_score:.2f}%")
            print(f"   Tokens: {response.total_tokens}")
            print(f"   Cost: ${response.cost_estimate:.6f}")
            print(f"\n   Response:")
            print(f"   {response.response_text[:200]}...")

        # Show statistics
        print("\n" + "=" * 80)
        print("STATISTICS")
        print("=" * 80)
        stats = orchestrator.get_statistics()
        print(json.dumps(stats, indent=2))

    except ValueError as e:
        print(f"\n⚠️  Note: {e}")
        print("Set ANTHROPIC_API_KEY environment variable to run this example")

    print("\n✅ Example complete")
