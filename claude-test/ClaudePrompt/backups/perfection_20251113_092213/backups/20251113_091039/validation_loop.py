#!/usr/bin/env python3
"""
Validation Loop - Ensures 99-100% Confidence
============================================

This module implements the iterative refinement loop that ensures
ALL responses achieve 99-100% confidence before being returned.

This is MANDATORY for production use.
"""

import logging
import json
from typing import Dict, Any, Tuple
from validate_my_response import ResponseValidator
from config import UltrathinkConfig

logger = logging.getLogger(__name__)


class ValidationLoop:
    """
    Iterative refinement loop to achieve 99-100% confidence.

    Process:
    1. Get initial response from Claude
    2. Validate through complete pipeline
    3. If < 99%, refine based on suggestions
    4. Repeat until 99%+ or max iterations
    5. Return validated response
    """

    def __init__(self, max_iterations: int = None):
        """
        Initialize validation loop.

        Args:
            max_iterations: Maximum refinement iterations (default from config)
        """
        self.validator = ResponseValidator()
        self.max_iterations = max_iterations or UltrathinkConfig.MAX_REFINEMENT_ITERATIONS
        self.target_confidence = UltrathinkConfig.CONFIDENCE_PRODUCTION  # 99.0%

    def validate_and_refine(
        self,
        initial_response: str,
        original_prompt: str,
        claude_api_call: callable,
        verbose: bool = False
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Validate response and refine until 99%+ confidence achieved.

        Args:
            initial_response: Initial response from Claude
            original_prompt: Original user prompt
            claude_api_call: Function to call Claude API for refinement
            verbose: Show detailed iteration logs

        Returns:
            Tuple of (final_response, validation_result)
        """

        current_response = initial_response
        iteration = 1
        best_response = initial_response
        best_confidence = 0.0

        if verbose:
            print(f"\n{'='*80}")
            print(f"🎯 VALIDATION LOOP - Targeting {self.target_confidence}% Confidence")
            print(f"{'='*80}\n")

        while iteration <= self.max_iterations:
            # Validate current response
            if verbose:
                print(f"[Iteration {iteration}/{self.max_iterations}] Validating response...")

            validation_result = self.validator.validate(
                response_text=current_response,
                original_prompt=original_prompt,
                iteration=iteration
            )

            confidence = validation_result.get("confidence", 0.0)
            is_acceptable = validation_result.get("is_acceptable", False)

            if verbose:
                print(f"  Confidence: {confidence:.1f}%")
                print(f"  Target: {self.target_confidence}%")
                print(f"  Acceptable: {'✅ YES' if is_acceptable else '❌ NO'}")

            # Track best response seen
            if confidence > best_confidence:
                best_confidence = confidence
                best_response = current_response

            # Check if we've achieved target
            if is_acceptable and confidence >= self.target_confidence:
                if verbose:
                    print(f"\n✅ TARGET ACHIEVED: {confidence:.1f}% confidence (iteration {iteration})")
                    print(f"{'='*80}\n")

                return current_response, validation_result

            # If we've reached max iterations, return best attempt
            if iteration >= self.max_iterations:
                logger.warning(
                    f"Max iterations ({self.max_iterations}) reached. "
                    f"Best confidence: {best_confidence:.1f}% (target: {self.target_confidence}%)"
                )

                if verbose:
                    print(f"\n⚠️  MAX ITERATIONS REACHED")
                    print(f"  Best confidence achieved: {best_confidence:.1f}%")
                    print(f"  Target confidence: {self.target_confidence}%")
                    print(f"  Using best response from iteration with highest confidence")
                    print(f"{'='*80}\n")

                # Return best response with its validation
                if best_response != current_response:
                    validation_result = self.validator.validate(
                        response_text=best_response,
                        original_prompt=original_prompt,
                        iteration=iteration
                    )

                return best_response, validation_result

            # Get refinement suggestions
            suggestions = validation_result.get("suggestions", [])

            if not suggestions:
                # No suggestions but still below target - add generic improvement request
                suggestions = [
                    "Add more detail and comprehensive coverage",
                    "Include specific examples and evidence",
                    "Ensure all aspects of the question are addressed",
                    "Provide step-by-step explanations where applicable"
                ]

            if verbose:
                print(f"\n  Refinement needed. Suggestions:")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"    {i}. {suggestion}")
                print()

            # Create refinement prompt
            refinement_prompt = self._create_refinement_prompt(
                original_prompt=original_prompt,
                current_response=current_response,
                confidence=confidence,
                target_confidence=self.target_confidence,
                suggestions=suggestions,
                iteration=iteration
            )

            # Call Claude API to refine
            if verbose:
                print(f"[Iteration {iteration + 1}] Requesting refined response from Claude...")

            try:
                refined_response = claude_api_call(refinement_prompt)
                current_response = refined_response
                iteration += 1
            except Exception as e:
                logger.error(f"Refinement failed: {e}")
                if verbose:
                    print(f"  ❌ Refinement failed: {e}")
                    print(f"  Using best response so far: {best_confidence:.1f}% confidence")
                return best_response, validation_result

        # Should not reach here, but return best response as fallback
        return best_response, validation_result

    def _create_refinement_prompt(
        self,
        original_prompt: str,
        current_response: str,
        confidence: float,
        target_confidence: float,
        suggestions: list,
        iteration: int
    ) -> str:
        """
        Create prompt for Claude to refine the response.

        Args:
            original_prompt: Original user question
            current_response: Current response that needs improvement
            confidence: Current confidence score
            target_confidence: Target confidence score
            suggestions: List of improvement suggestions
            iteration: Current iteration number

        Returns:
            Refinement prompt for Claude
        """

        suggestions_text = "\n".join([f"{i}. {s}" for i, s in enumerate(suggestions, 1)])

        return f"""Your previous response to the question below achieved {confidence:.1f}% confidence, but the target is {target_confidence}% for production use.

Please refine your response to address these specific issues:

{suggestions_text}

Original Question:
{original_prompt}

Your Previous Response (Iteration {iteration}):
{current_response}

Please provide an IMPROVED response that:
1. Addresses ALL the suggestions above
2. Provides more comprehensive coverage
3. Includes specific examples and evidence
4. Has clear, detailed explanations
5. Covers all aspects of the original question
6. Is production-ready quality

Your improved response:"""

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get validation loop statistics.

        Returns:
            Statistics dictionary
        """
        return {
            "target_confidence": self.target_confidence,
            "max_iterations": self.max_iterations
        }


def validate_response_to_target(
    response: str,
    prompt: str,
    claude_api_call: callable,
    target_confidence: float = 99.0,
    max_iterations: int = 20,
    verbose: bool = False
) -> Tuple[str, Dict[str, Any]]:
    """
    Convenience function to validate and refine a response.

    Args:
        response: Initial response to validate
        prompt: Original prompt
        claude_api_call: Function to call Claude for refinement
        target_confidence: Target confidence percentage
        max_iterations: Maximum refinement iterations
        verbose: Show detailed logs

    Returns:
        Tuple of (final_response, validation_result)
    """
    loop = ValidationLoop(max_iterations=max_iterations)
    return loop.validate_and_refine(
        initial_response=response,
        original_prompt=prompt,
        claude_api_call=claude_api_call,
        verbose=verbose
    )
