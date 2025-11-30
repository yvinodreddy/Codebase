#!/usr/bin/env python3
"""
Production-grade validation script for dual retrieval results.

Validates search results to ensure 99% confidence through multi-layered checks.
Returns JSON with confidence score, acceptability, and refinement suggestions.
"""
import argparse
import json
import sys
import re
from typing import Dict, List, Tuple


class ResponseValidator:
    """Validates search results with production-grade quality checks."""

    TARGET_CONFIDENCE = 99.0
    MIN_RESULTS = 1
    MIN_CONTENT_LENGTH = 20

    def __init__(self):
        self.validation_checks = [
            self._check_has_results,
            self._check_content_quality,
            self._check_relevance_indicators,
            self._check_structure,
            self._check_completeness
        ]

    def validate(
        self,
        response_text: str,
        prompt: str,
        iteration: int
    ) -> Dict:
        """
        Run all validation checks and compute confidence score.

        Args:
            response_text: The search results text to validate
            prompt: Original search query
            iteration: Current iteration number

        Returns:
            {
                'iteration': int,
                'confidence': float,
                'target_confidence': float,
                'is_acceptable': bool,
                'suggestions': List[str],
                'guardrails': {...},
                'verification': {...}
            }
        """
        # Run all validation checks
        check_results = []
        suggestions = []

        for check_func in self.validation_checks:
            passed, confidence, suggestion = check_func(response_text, prompt)
            check_results.append({
                'name': check_func.__name__,
                'passed': passed,
                'confidence': confidence
            })
            if suggestion:
                suggestions.append(suggestion)

        # Compute overall confidence (average of all checks)
        overall_confidence = sum(r['confidence'] for r in check_results) / len(check_results)

        # Determine if acceptable
        is_acceptable = overall_confidence >= self.TARGET_CONFIDENCE

        return {
            'iteration': iteration,
            'confidence': round(overall_confidence, 1),
            'target_confidence': self.TARGET_CONFIDENCE,
            'is_acceptable': is_acceptable,
            'suggestions': suggestions[:3],  # Top 3 suggestions
            'guardrails': {
                'passed': all(r['passed'] for r in check_results),
                'confidence': round(overall_confidence, 1),
                'checks': check_results
            },
            'verification': {
                'passed': overall_confidence >= 90.0,
                'confidence': round(overall_confidence, 1)
            }
        }

    def _check_has_results(
        self,
        response_text: str,
        prompt: str
    ) -> Tuple[bool, float, str]:
        """Check if response has actual results."""
        # Look for result indicators
        has_total = "Total results:" in response_text
        has_no_results = "No results found" in response_text or "0 results" in response_text.lower()

        if has_no_results:
            return False, 0.0, "No results found - check database has data for this project"

        if not has_total:
            return False, 50.0, "Response missing 'Total results:' header"

        # Extract result count
        match = re.search(r"Total results:\s*(\d+)", response_text)
        if match:
            count = int(match.group(1))
            if count == 0:
                return False, 0.0, "Result count is 0 - ensure database has relevant data"
            elif count < self.MIN_RESULTS:
                return False, 60.0, f"Only {count} results found - need at least {self.MIN_RESULTS}"
            else:
                # More results = higher confidence
                confidence = min(100.0, 80.0 + (count * 2))
                return True, confidence, ""

        return False, 50.0, "Could not extract result count"

    def _check_content_quality(
        self,
        response_text: str,
        prompt: str
    ) -> Tuple[bool, float, str]:
        """Check quality of result content."""
        # Check content length
        if len(response_text) < self.MIN_CONTENT_LENGTH:
            return False, 30.0, "Response too short - insufficient content"

        # Look for numbered results (1., 2., etc.)
        numbered_results = re.findall(r"^\s*\d+\.\s+", response_text, re.MULTILINE)
        if not numbered_results:
            return False, 70.0, "Results not properly numbered"

        # Check for content indicators
        has_content_indicators = any(
            indicator in response_text
            for indicator in ['Title:', 'Description:', 'Code:', 'Score:', 'ID:', 'Content:']
        )

        if not has_content_indicators:
            return False, 75.0, "Results missing content structure (Title, Description, etc.)"

        # Quality score based on content richness
        # CRITICAL FIX (2025-11-30): Don't require code examples for database queries
        # Database messages are prompts, not code, so Title + Description = 100%
        confidence = 85.0

        has_title = 'Title:' in response_text
        has_description = 'Description:' in response_text
        has_code = 'Code:' in response_text or 'code_example' in response_text.lower()

        if has_title:
            confidence += 7.5  # Increased from 5 to 7.5
        if has_description:
            confidence += 7.5  # Increased from 5 to 7.5
        if has_code:
            confidence += 0.0  # Code is BONUS, not required (was +5)

        # If has both Title AND Description, give 100% (was 95%)
        # This allows database queries to reach 100% without code examples
        return True, min(100.0, confidence), ""

    def _check_relevance_indicators(
        self,
        response_text: str,
        prompt: str
    ) -> Tuple[bool, float, str]:
        """Check if results are relevant to the query."""
        # Extract query keywords
        query_keywords = set(
            word.lower()
            for word in re.findall(r'\w+', prompt)
            if len(word) > 3
        )

        if not query_keywords:
            return True, 100.0, ""  # Can't assess relevance without keywords

        # Count how many query keywords appear in results
        response_lower = response_text.lower()
        matching_keywords = sum(
            1 for keyword in query_keywords
            if keyword in response_lower
        )

        relevance_ratio = matching_keywords / len(query_keywords)

        if relevance_ratio < 0.3:
            return False, 60.0, f"Low relevance - only {matching_keywords}/{len(query_keywords)} query keywords found"
        elif relevance_ratio < 0.5:
            return True, 80.0, "Moderate relevance - consider refining results"
        else:
            confidence = 90.0 + (relevance_ratio * 10.0)
            return True, min(100.0, confidence), ""

    def _check_structure(
        self,
        response_text: str,
        prompt: str
    ) -> Tuple[bool, float, str]:
        """Check if response has proper structure."""
        required_sections = [
            ("SEARCH RESULTS", "Missing method indicator (KEYWORD/SEMANTIC)"),
            ("Total results:", "Missing result count"),
        ]

        missing_sections = []
        for section, error_msg in required_sections:
            if section not in response_text:
                missing_sections.append(error_msg)

        if missing_sections:
            confidence = max(50.0, 100.0 - (len(missing_sections) * 25.0))
            return False, confidence, missing_sections[0]

        # Check for proper formatting
        has_newlines = '\n' in response_text
        has_separators = any(sep in response_text for sep in ['---', '===', '━━━'])

        if not has_newlines:
            return False, 70.0, "Response lacks proper line breaks"

        confidence = 95.0
        if has_separators:
            confidence += 5.0

        return True, confidence, ""

    def _check_completeness(
        self,
        response_text: str,
        prompt: str
    ) -> Tuple[bool, float, str]:
        """Check if response is complete and not truncated."""
        # Check for truncation indicators
        truncation_indicators = [
            "...",
            "[truncated]",
            "[more]",
            "and more"
        ]

        is_truncated = any(
            indicator in response_text.lower()
            for indicator in truncation_indicators
        )

        # Check if response ends abruptly
        ends_properly = response_text.rstrip().endswith(('.', '!', '?', '"', '}', ']'))

        if is_truncated and not ends_properly:
            return False, 75.0, "Response appears truncated - ensure full results returned"

        if is_truncated:
            return True, 85.0, "Response may be truncated but ends properly"

        if not ends_properly:
            return True, 90.0, "Response may be incomplete (doesn't end with punctuation)"

        return True, 100.0, ""


def main():
    """Main entry point for validation script."""
    parser = argparse.ArgumentParser(
        description="Validate search results to ensure production-grade quality"
    )
    parser.add_argument(
        'response_text',
        nargs='?',  # Make optional (can come from stdin)
        help="The search results text to validate (or use --stdin)"
    )
    parser.add_argument(
        '--stdin',
        action='store_true',
        help="Read response text from stdin instead of argument"
    )
    parser.add_argument(
        '--prompt',
        required=True,
        help="Original search query"
    )
    parser.add_argument(
        '--iteration',
        type=int,
        default=1,
        help="Current iteration number"
    )

    args = parser.parse_args()

    # Get response text from stdin if --stdin flag is used
    if args.stdin:
        response_text = sys.stdin.read()
    elif args.response_text:
        response_text = args.response_text
    else:
        print(json.dumps({
            'error': 'Must provide response_text argument or use --stdin flag',
            'confidence': 0,
            'is_acceptable': False
        }))
        sys.exit(1)

    # Validate
    validator = ResponseValidator()
    result = validator.validate(
        response_text=response_text,
        prompt=args.prompt,
        iteration=args.iteration
    )

    # Output as JSON
    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result['is_acceptable'] else 1)


if __name__ == '__main__':
    main()
