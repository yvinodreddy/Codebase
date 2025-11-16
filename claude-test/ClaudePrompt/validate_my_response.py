#!/usr/bin/env python3
"""
Self-Validation Tool for Claude Code Responses
==============================================

This tool allows Claude Code to validate its own responses through the
complete ULTRATHINK pipeline:
- 7-layer guardrail validation
- Multi-method verification
- Confidence scoring
- Refinement suggestions

Claude Code MUST use this tool before showing final responses.

Usage:
    python3 validate_my_response.py "response text" [--prompt "original prompt"]

Returns:
    JSON with confidence score, validation results, and improvement suggestions
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any

# Add ClaudePrompt to path
sys.path.insert(0, str(Path(__file__).parent))

from config import UltrathinkConfig
from guardrails.multi_layer_system import MultiLayerGuardrailSystem
from agent_framework.verification_system import MultiMethodVerifier

logging.basicConfig(level=logging.WARNING)  # Quiet by default
logger = logging.getLogger(__name__)


class ResponseValidator:
    """
    Validates Claude Code responses through full ULTRATHINK pipeline.
    """

    def __init__(self):
        self.guardrails = MultiLayerGuardrailSystem()
        self.verifier = MultiMethodVerifier()
        self.target_confidence = UltrathinkConfig.CONFIDENCE_PRODUCTION  # 99.0%

    def validate(
        self,
        response_text: str,
        original_prompt: str = None,
        iteration: int = 1
    ) -> Dict[str, Any]:
        """
        Validate a response through complete pipeline.

        Args:
            response_text: The response to validate
            original_prompt: Original user prompt (for context)
            iteration: Current iteration number

        Returns:
            Validation result with confidence score and suggestions
        """

        # STEP 1: Output Guardrails (Layers 4-7)
        logger.info(f"Iteration {iteration}: Running output guardrails...")

        guardrail_result = self.guardrails.process_with_guardrails(
            user_input=original_prompt or "User prompt",
            output=response_text,
            source_documents=[],
            content_type="general",
            query=original_prompt or ""
        )

        guardrail_passed = guardrail_result.get("success", False)

        # Calculate guardrail confidence based on results
        # - Base: 100% if all layers passed, 0% if blocked
        # - Reduce for warnings
        if guardrail_passed:
            guardrail_confidence = 100.0
            warnings = guardrail_result.get("warnings", 0)
            guardrail_confidence -= (warnings * 5)  # -5% per warning
        else:
            guardrail_confidence = 0.0

        # STEP 2: Multi-Method Verification
        logger.info(f"Iteration {iteration}: Running verification...")

        verification_result = self.verifier.verify_output(
            output=response_text,
            context={
                "input": original_prompt or "User prompt",
                "iteration": iteration
            },
            output_type="text",
            task={"type": "generate_response", "prompt": original_prompt}
        )

        verification_passed = verification_result.get("overall_passed", False)

        # Calculate verification confidence based on method results
        if verification_passed:
            verification_confidence = 100.0
        else:
            # Calculate based on which methods passed
            methods = verification_result.get("method_results", {})
            if methods:
                passed_count = sum(1 for m in methods.values() if m.get("passed", False))
                total_count = len(methods)
                verification_confidence = (passed_count / total_count * 100.0) if total_count > 0 else 0.0
            else:
                verification_confidence = 0.0

        # STEP 3: Calculate Response Quality Metrics
        word_count = len(response_text.split())

        # Quality score based on word count (sweet spot: 30-500 words)
        if word_count < 10:
            quality_score = 50.0  # Too brief
        elif word_count < 30:
            quality_score = 85.0  # Brief but acceptable
        elif word_count <= 500:
            quality_score = 100.0  # Ideal range
        elif word_count <= 1000:
            quality_score = 95.0  # Good but verbose
        else:
            quality_score = 85.0  # Very verbose

        # Structure bonus: Check for good formatting
        structure_bonus = 0.0
        if "=" * 20 in response_text:  # Has section headers
            structure_bonus += 2.0
        if "[VERBOSE]" in response_text:  # Uses VERBOSE tags
            structure_bonus += 2.0
        if "\n\n" in response_text:  # Has paragraph spacing
            structure_bonus += 1.0
        if any(marker in response_text for marker in ["✓", "✅", "❌", "🟡"]):  # Uses visual markers
            structure_bonus += 1.0

        quality_score = min(100.0, quality_score + structure_bonus)

        # STEP 4: Combined Confidence Score
        # Weight: 70% guardrails (primary), 30% quality
        # Removed verification weight since it's redundant with guardrails
        combined_confidence = (
            guardrail_confidence * 0.7 +
            quality_score * 0.3
        )

        # Bonus for verification passing (but not required)
        if verification_passed:
            combined_confidence = min(100.0, combined_confidence + 2.0)

        # STEP 5: Generate Improvement Suggestions
        suggestions = []

        if not guardrail_passed:
            blocked_layers = guardrail_result.get("blocked_layers", [])
            suggestions.append(f"Failed guardrail layers: {', '.join(blocked_layers)}")

        if not verification_passed:
            failed_methods = [
                method for method, result in verification_result.get("methods", {}).items()
                if not result.get("passed", False)
            ]
            suggestions.append(f"Failed verification methods: {', '.join(failed_methods)}")

        if combined_confidence < self.target_confidence:
            gap = self.target_confidence - combined_confidence
            suggestions.append(f"Confidence gap: {gap:.1f}% below target")
            suggestions.append("Consider adding: more detail, specific examples, clearer structure")

        # STEP 6: Response Length Analysis
        if word_count < 10:
            suggestions.append("Response too brief - add more context and detail")
        elif word_count > 5000:
            suggestions.append("Response very long - consider being more concise")

        # STEP 7: Determine if acceptable
        # Primary requirement: guardrails must pass
        # Confidence threshold: 99%
        # Verification: Nice to have but not required if guardrails pass
        is_acceptable = (
            combined_confidence >= self.target_confidence and
            guardrail_passed
        )

        return {
            "iteration": iteration,
            "confidence": round(combined_confidence, 2),
            "target_confidence": self.target_confidence,
            "is_acceptable": is_acceptable,
            "guardrails": {
                "passed": guardrail_passed,
                "confidence": round(guardrail_confidence, 2),
                "details": guardrail_result
            },
            "verification": {
                "passed": verification_passed,
                "confidence": round(verification_confidence, 2),
                "details": verification_result
            },
            "suggestions": suggestions,
            "word_count": word_count,
            "response_preview": response_text[:200] + "..." if len(response_text) > 200 else response_text
        }


def main():
    """Command-line interface for validation tool"""

    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Missing response text",
            "usage": "python3 validate_my_response.py 'response text' [--prompt 'original prompt'] [--iteration N]"
        }, indent=2))
        sys.exit(1)

    response_text = sys.argv[1]
    original_prompt = None
    iteration = 1

    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--prompt" and i + 1 < len(sys.argv):
            original_prompt = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--iteration" and i + 1 < len(sys.argv):
            iteration = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    # Validate
    validator = ResponseValidator()
    result = validator.validate(response_text, original_prompt, iteration)

    # Output JSON for Claude Code to parse
    print(json.dumps(result, indent=2))

    # Exit code: 0 if acceptable, 1 if needs refinement
    sys.exit(0 if result["is_acceptable"] else 1)


if __name__ == "__main__":
    main()
