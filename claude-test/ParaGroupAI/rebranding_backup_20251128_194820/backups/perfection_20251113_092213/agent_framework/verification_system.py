"""
Multi-Method Verification System
Combines multiple verification approaches for robust output validation

Based on Anthropic's three verification methods:
1. Rules-based (best - clear rules, explain failures)
2. Visual feedback (for UI/visual tasks)
3. LLM as judge (for fuzzy criteria)
"""

import logging
import sys
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

# Add guardrails to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'guardrails'))

try:
    from multi_layer_system import MultiLayerGuardrailSystem
except ImportError:
    # Fallback if guardrails not available
    MultiLayerGuardrailSystem = None
    logging.warning("MultiLayerGuardrailSystem not available")

logger = logging.getLogger(__name__)


@dataclass
class VerificationResult:
    """Result from verification"""
    passed: bool
    method: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "passed": self.passed,
            "method": self.method,
            "message": self.message,
            "details": self.details,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp
        }


class MultiMethodVerifier:
    """
    Multi-method verification system.

    Anthropic's recommendation:
    "The best form of feedback is providing clearly defined rules for
    an output, then explaining which rules failed and why."

    This class combines:
    1. Rules-based verification (primary)
    2. Code verification (for code outputs)
    3. Visual verification (for UI outputs)
    4. LLM-as-judge (for fuzzy criteria)

    Example:
        >>> verifier = MultiMethodVerifier()
        >>> result = verifier.verify_output(
        ...     output=generated_code,
        ...     context={"input": user_request},
        ...     output_type="code"
        ... )
        >>> if result["overall_passed"]:
        ...     print("All verifications passed!")
    """

    def __init__(self):
        """Initialize multi-method verifier"""
        # Try to initialize guardrails
        if MultiLayerGuardrailSystem is not None:
            try:
                self.guardrails = MultiLayerGuardrailSystem()
            except Exception as e:
                logger.warning(f"Could not initialize guardrails: {e}")
                self.guardrails = None
        else:
            self.guardrails = None

        self.verification_log: List[Dict[str, Any]] = []

        logger.info("MultiMethodVerifier initialized")

    def verify_output(
        self,
        output: Any,
        context: Dict[str, Any],
        output_type: str = "text",
        task: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Verify output using multiple methods.

        Args:
            output: The output to verify
            context: Context including input, requirements, etc.
            output_type: Type of output ("text", "code", "ui", "data")
            task: Optional task information

        Returns:
            Dict with verification results from all applicable methods
        """
        logger.info(f"Verifying output (type={output_type})...")

        results = {}

        # Method 1: Rules-based (always)
        results["rules_based"] = self._verify_rules_based(output, context, task)

        # Method 2: Guardrails (if available and applicable)
        if self.guardrails and output_type in ["text", "code"]:
            results["guardrails"] = self._verify_with_guardrails(output, context)

        # Method 3: Code verification (if code output)
        if output_type == "code":
            results["code_verification"] = self._verify_code(output)

        # Method 4: Data validation (if data output)
        if output_type == "data":
            results["data_validation"] = self._verify_data(output, context)

        # Method 5: Visual feedback (if UI output)
        if output_type == "ui":
            results["visual"] = self._verify_visual(output, context)

        # Method 6: LLM as judge (if fuzzy validation requested)
        if context.get("fuzzy_validation") or context.get("use_llm_judge"):
            results["llm_judge"] = self._verify_with_llm_judge(output, context)

        # Combine results
        overall_passed = all(
            r.passed if isinstance(r, VerificationResult) else r.get("passed", False)
            for r in results.values()
        )

        all_recommendations = []
        for result in results.values():
            if isinstance(result, VerificationResult):
                all_recommendations.extend(result.recommendations)
            elif isinstance(result, dict):
                all_recommendations.extend(result.get("recommendations", []))

        verification_summary = {
            "overall_passed": overall_passed,
            "methods_used": list(results.keys()),
            "method_results": {
                k: v.to_dict() if isinstance(v, VerificationResult) else v
                for k, v in results.items()
            },
            "all_recommendations": all_recommendations,
            "timestamp": datetime.now().isoformat()
        }

        self.verification_log.append(verification_summary)

        logger.info(
            f"Verification complete: {'PASS' if overall_passed else 'FAIL'} "
            f"({len(results)} methods used)"
        )

        return verification_summary

    def _verify_rules_based(
        self,
        output: Any,
        context: Dict[str, Any],
        task: Optional[Dict[str, Any]]
    ) -> VerificationResult:
        """
        Rules-based verification (primary method).

        Anthropic: "The best form of feedback"
        """
        logger.debug("Running rules-based verification...")

        passed = True
        failed_rules = []
        recommendations = []

        # Define rules
        rules = self._get_verification_rules(context, task)

        # Check each rule
        for rule_name, rule_check in rules.items():
            rule_result = rule_check(output, context)

            if not rule_result["passed"]:
                passed = False
                failed_rules.append({
                    "rule": rule_name,
                    "reason": rule_result.get("reason", "Unknown"),
                    "how_to_fix": rule_result.get("how_to_fix", "")
                })

            if rule_result.get("recommendation"):
                recommendations.append(rule_result["recommendation"])

        if passed:
            message = f"All {len(rules)} rules passed"
        else:
            message = f"{len(failed_rules)} of {len(rules)} rules failed"

        return VerificationResult(
            passed=passed,
            method="rules_based",
            message=message,
            details={
                "total_rules": len(rules),
                "failed_rules": failed_rules
            },
            recommendations=recommendations
        )

    def _get_verification_rules(
        self,
        context: Dict[str, Any],
        task: Optional[Dict[str, Any]]
    ) -> Dict[str, callable]:
        """
        Get verification rules based on context.

        Each rule is a function that returns:
        {
            "passed": bool,
            "reason": str (if failed),
            "how_to_fix": str (if failed),
            "recommendation": str (optional)
        }
        """
        rules = {}

        # Rule 1: Output not empty
        def rule_not_empty(output, ctx):
            if output is None or (isinstance(output, str) and not output.strip()):
                return {
                    "passed": False,
                    "reason": "Output is empty",
                    "how_to_fix": "Generate non-empty output"
                }
            return {"passed": True}

        rules["not_empty"] = rule_not_empty

        # Rule 2: Output type matches expected
        if task and "expected_type" in task:
            expected_type = task["expected_type"]

            def rule_type_match(output, ctx):
                if expected_type == "dict" and not isinstance(output, dict):
                    return {
                        "passed": False,
                        "reason": f"Expected dict, got {type(output).__name__}",
                        "how_to_fix": "Return a dictionary"
                    }
                return {"passed": True}

            rules["type_match"] = rule_type_match

        # Rule 3: Required fields present (if dict output)
        if task and "required_fields" in task:
            required_fields = task["required_fields"]

            def rule_required_fields(output, ctx):
                if not isinstance(output, dict):
                    return {"passed": True}  # Only check dicts

                missing = [f for f in required_fields if f not in output]
                if missing:
                    return {
                        "passed": False,
                        "reason": f"Missing required fields: {missing}",
                        "how_to_fix": f"Add fields: {missing}"
                    }
                return {"passed": True}

            rules["required_fields"] = rule_required_fields

        # Rule 4: No sensitive data (basic check)
        def rule_no_sensitive_data(output, ctx):
            output_str = str(output).lower()

            sensitive_patterns = [
                "password:",
                "api_key:",
                "secret:",
                "ssn:",
                "credit_card:"
            ]

            found_patterns = [p for p in sensitive_patterns if p in output_str]

            if found_patterns:
                return {
                    "passed": False,
                    "reason": f"Potentially sensitive data found: {found_patterns}",
                    "how_to_fix": "Remove or redact sensitive information"
                }

            return {"passed": True}

        rules["no_sensitive_data"] = rule_no_sensitive_data

        return rules

    def _verify_with_guardrails(
        self,
        output: Any,
        context: Dict[str, Any]
    ) -> VerificationResult:
        """Verify using guardrails system"""
        if not self.guardrails:
            return VerificationResult(
                passed=True,
                method="guardrails",
                message="Guardrails not available (skipped)"
            )

        logger.debug("Running guardrails verification...")

        try:
            # Process through guardrails
            result = self.guardrails.process_with_guardrails(
                user_input=context.get("input", ""),
                output=str(output)
            )

            return VerificationResult(
                passed=result["success"],
                method="guardrails",
                message=f"Guardrails check: {'passed' if result['success'] else 'failed'}",
                details={
                    "blocked_at": result.get("blocked_at"),
                    "warnings": result.get("warnings", 0)
                }
            )

        except Exception as e:
            logger.error(f"Guardrails verification failed: {e}")
            return VerificationResult(
                passed=False,
                method="guardrails",
                message=f"Guardrails error: {e}"
            )

    def _verify_code(self, code: str) -> VerificationResult:
        """Verify code output"""
        logger.debug("Running code verification...")

        try:
            # Use code generator's verification
            try:
                from .code_generator import CodeGenerator
            except ImportError:
                from code_generator import CodeGenerator
            generator = CodeGenerator()
            result = generator.verify_code(code)

            return VerificationResult(
                passed=result.passed,
                method="code_verification",
                message=f"Code score: {result.score}/100",
                details={
                    "score": result.score,
                    "errors": result.errors,
                    "warnings": result.warnings
                },
                recommendations=result.recommendations
            )

        except Exception as e:
            logger.error(f"Code verification failed: {e}")
            return VerificationResult(
                passed=False,
                method="code_verification",
                message=f"Verification error: {e}"
            )

    def _verify_data(
        self,
        data: Any,
        context: Dict[str, Any]
    ) -> VerificationResult:
        """Verify data output (structure, completeness)"""
        logger.debug("Running data validation...")

        passed = True
        issues = []

        # Check data structure
        if not isinstance(data, (dict, list)):
            passed = False
            issues.append("Data should be dict or list")

        # Check if empty
        if not data:
            passed = False
            issues.append("Data is empty")

        # Check for expected schema
        expected_schema = context.get("expected_schema")
        if expected_schema and isinstance(data, dict):
            missing_keys = set(expected_schema.keys()) - set(data.keys())
            if missing_keys:
                passed = False
                issues.append(f"Missing keys: {missing_keys}")

        message = "Data validation passed" if passed else f"Data validation failed: {issues}"

        return VerificationResult(
            passed=passed,
            method="data_validation",
            message=message,
            details={"issues": issues}
        )

    def _verify_visual(
        self,
        output: Any,
        context: Dict[str, Any]
    ) -> VerificationResult:
        """
        Visual verification for UI outputs.

        In production, this would:
        1. Render the UI
        2. Take screenshot
        3. Use vision model to verify
        """
        logger.debug("Running visual verification...")

        # Placeholder implementation
        # In production, would use Playwright + vision model

        return VerificationResult(
            passed=True,
            method="visual",
            message="Visual verification not yet implemented",
            recommendations=["Implement screenshot-based verification for UI tasks"]
        )

    def _verify_with_llm_judge(
        self,
        output: Any,
        context: Dict[str, Any]
    ) -> VerificationResult:
        """
        LLM-as-judge verification for fuzzy criteria.

        Anthropic: Use this when you need fuzzy validation,
        but note it's expensive and less robust.
        """
        logger.debug("Running LLM-as-judge verification...")

        # Placeholder implementation
        # In production, would call LLM API with evaluation prompt

        evaluation_criteria = context.get("evaluation_criteria", [])

        return VerificationResult(
            passed=True,
            method="llm_judge",
            message="LLM-as-judge not yet implemented",
            details={"criteria": evaluation_criteria},
            recommendations=["Implement LLM-based evaluation for fuzzy criteria"]
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Get verification statistics"""
        if not self.verification_log:
            return {"error": "No verifications performed"}

        return {
            "total_verifications": len(self.verification_log),
            "passed": sum(1 for v in self.verification_log if v["overall_passed"]),
            "failed": sum(1 for v in self.verification_log if not v["overall_passed"]),
            "success_rate": sum(1 for v in self.verification_log if v["overall_passed"]) / len(self.verification_log),
            "methods_used": list(set(
                method
                for v in self.verification_log
                for method in v["methods_used"]
            ))
        }


if __name__ == "__main__":
    # Example usage
    import json

    verifier = MultiMethodVerifier()

    print("=" * 60)
    print("MULTI-METHOD VERIFIER EXAMPLE")
    print("=" * 60)

    # Example 1: Verify text output
    print("\n1. Verifying text output...")
    result = verifier.verify_output(
        output="This is a test output with proper content.",
        context={"input": "Generate test output"},
        output_type="text"
    )
    print(f"   Result: {'PASS' if result['overall_passed'] else 'FAIL'}")
    print(f"   Methods: {result['methods_used']}")

    # Example 2: Verify code output
    print("\n2. Verifying code output...")
    code = '''
def example_function():
    """Example function"""
    return "Hello, World!"
'''
    result = verifier.verify_output(
        output=code,
        context={"input": "Generate example function"},
        output_type="code"
    )
    print(f"   Result: {'PASS' if result['overall_passed'] else 'FAIL'}")
    print(f"   Methods: {result['methods_used']}")

    # Example 3: Verify with required fields
    print("\n3. Verifying dict output with requirements...")
    result = verifier.verify_output(
        output={"name": "Test", "value": 42},
        context={"input": "Generate data"},
        output_type="data",
        task={
            "expected_type": "dict",
            "required_fields": ["name", "value", "timestamp"]  # Missing timestamp!
        }
    )
    print(f"   Result: {'PASS' if result['overall_passed'] else 'FAIL'}")
    print(f"   Failed rules: {[r['rule'] for r in result['method_results']['rules_based']['details'].get('failed_rules', [])]}")

    # Show statistics
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    stats = verifier.get_statistics()
    print(json.dumps(stats, indent=2))

    print("\n✅ Example complete")
