#!/usr/bin/env python3
"""
Validate Explanations Script
Validates the quality and correctness of generated explanations.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any


class ExplanationValidator:
    """Validates explanation data quality and structure."""

    def __init__(self):
        self.results = {
            "shap": {"passed": [], "failed": []},
            "lime": {"passed": [], "failed": []},
            "attention": {"passed": [], "failed": []},
            "decision": {"passed": [], "failed": []}
        }

    def validate_shap_values(self, explanations: List[Dict]) -> bool:
        """Validate SHAP values structure and consistency."""
        print("\n[SHAP Validation]")

        if not explanations:
            print("  ✗ FAIL: No SHAP explanations found")
            self.results["shap"]["failed"].append("No explanations found")
            return False

        passed = True

        for i, exp in enumerate(explanations):
            # Check required fields
            if "shap_values" not in exp:
                print(f"  ✗ FAIL: Missing shap_values in explanation {i}")
                self.results["shap"]["failed"].append(f"Explanation {i}: Missing shap_values")
                passed = False
                continue

            # Check that SHAP values are numeric
            shap_values = exp["shap_values"]
            if not isinstance(shap_values, dict):
                print(f"  ✗ FAIL: shap_values must be a dictionary in explanation {i}")
                self.results["shap"]["failed"].append(f"Explanation {i}: Invalid shap_values type")
                passed = False
                continue

            # Validate each feature value
            for feature, value in shap_values.items():
                if not isinstance(value, (int, float)):
                    print(f"  ✗ FAIL: Non-numeric SHAP value for '{feature}' in explanation {i}")
                    self.results["shap"]["failed"].append(f"Explanation {i}: Non-numeric value for {feature}")
                    passed = False
                    break

            # Check base value
            if "base_value" not in exp:
                print(f"  ✗ FAIL: Missing base_value in explanation {i}")
                self.results["shap"]["failed"].append(f"Explanation {i}: Missing base_value")
                passed = False
            elif not isinstance(exp["base_value"], (int, float)):
                print(f"  ✗ FAIL: base_value must be numeric in explanation {i}")
                self.results["shap"]["failed"].append(f"Explanation {i}: Invalid base_value type")
                passed = False

        if passed:
            print(f"  ✓ PASS: All {len(explanations)} SHAP explanations valid")
            self.results["shap"]["passed"].append(f"All {len(explanations)} explanations valid")

        return passed

    def validate_lime_local_model(self, explanations: List[Dict], threshold: float = 0.85) -> bool:
        """Validate LIME local model R² scores."""
        print("\n[LIME Validation]")

        if not explanations:
            print("  ✗ FAIL: No LIME explanations found")
            self.results["lime"]["failed"].append("No explanations found")
            return False

        passed = True

        for i, exp in enumerate(explanations):
            # Check required fields
            if "local_model_r2" not in exp:
                print(f"  ✗ FAIL: Missing local_model_r2 in explanation {i}")
                self.results["lime"]["failed"].append(f"Explanation {i}: Missing local_model_r2")
                passed = False
                continue

            r2_score = exp["local_model_r2"]

            # Validate R² is numeric
            if not isinstance(r2_score, (int, float)):
                print(f"  ✗ FAIL: local_model_r2 must be numeric in explanation {i}")
                self.results["lime"]["failed"].append(f"Explanation {i}: Invalid R² type")
                passed = False
                continue

            # Validate R² is in valid range
            if r2_score < 0 or r2_score > 1:
                print(f"  ✗ FAIL: local_model_r2 must be between 0 and 1 in explanation {i} (got {r2_score})")
                self.results["lime"]["failed"].append(f"Explanation {i}: R² out of range ({r2_score})")
                passed = False
                continue

            # Check R² threshold
            if r2_score < threshold:
                print(f"  ✗ FAIL: local_model_r2 ({r2_score:.3f}) < threshold ({threshold}) in explanation {i}")
                self.results["lime"]["failed"].append(f"Explanation {i}: R² below threshold ({r2_score:.3f})")
                passed = False
                continue

            # Check lime_explanation structure
            if "lime_explanation" not in exp:
                print(f"  ✗ FAIL: Missing lime_explanation in explanation {i}")
                self.results["lime"]["failed"].append(f"Explanation {i}: Missing lime_explanation")
                passed = False
                continue

        if passed:
            print(f"  ✓ PASS: All {len(explanations)} LIME explanations have R² > {threshold}")
            self.results["lime"]["passed"].append(f"All {len(explanations)} explanations valid with R² > {threshold}")

        return passed

    def validate_attention_weights(self, visualizations: List[Dict], expected_heads: int = 8) -> bool:
        """Validate attention weights for all heads."""
        print("\n[Attention Validation]")

        if not visualizations:
            print("  ✗ FAIL: No attention visualizations found")
            self.results["attention"]["failed"].append("No visualizations found")
            return False

        passed = True

        for i, viz in enumerate(visualizations):
            # Check required fields
            if "attention_weights" not in viz:
                print(f"  ✗ FAIL: Missing attention_weights in visualization {i}")
                self.results["attention"]["failed"].append(f"Visualization {i}: Missing attention_weights")
                passed = False
                continue

            attention_weights = viz["attention_weights"]

            # Validate structure
            if not isinstance(attention_weights, dict):
                print(f"  ✗ FAIL: attention_weights must be a dictionary in visualization {i}")
                self.results["attention"]["failed"].append(f"Visualization {i}: Invalid attention_weights type")
                passed = False
                continue

            # Check number of heads
            num_heads = len(attention_weights)
            if num_heads != expected_heads:
                print(f"  ✗ FAIL: Expected {expected_heads} heads, got {num_heads} in visualization {i}")
                self.results["attention"]["failed"].append(f"Visualization {i}: Wrong number of heads ({num_heads})")
                passed = False
                continue

            # Validate each head's weights
            for head_name, weights in attention_weights.items():
                if not isinstance(weights, list):
                    print(f"  ✗ FAIL: Weights for {head_name} must be a list in visualization {i}")
                    self.results["attention"]["failed"].append(f"Visualization {i}: Invalid weights for {head_name}")
                    passed = False
                    break

                # Check all weights are numeric
                if not all(isinstance(w, (int, float)) for w in weights):
                    print(f"  ✗ FAIL: All weights must be numeric for {head_name} in visualization {i}")
                    self.results["attention"]["failed"].append(f"Visualization {i}: Non-numeric weights in {head_name}")
                    passed = False
                    break

        if passed:
            print(f"  ✓ PASS: All {len(visualizations)} attention visualizations have {expected_heads} valid heads")
            self.results["attention"]["passed"].append(f"All {len(visualizations)} visualizations valid")

        return passed

    def validate_decision_confidence(self, explanations: List[Dict], min_confidence: float = 0.7) -> bool:
        """Validate decision confidence scores."""
        print("\n[Decision Validation]")

        if not explanations:
            print("  ✗ FAIL: No decision explanations found")
            self.results["decision"]["failed"].append("No explanations found")
            return False

        passed = True

        for i, exp in enumerate(explanations):
            # Check required fields
            required_fields = ["decision", "confidence", "reasoning", "recommendations"]
            for field in required_fields:
                if field not in exp:
                    print(f"  ✗ FAIL: Missing {field} in explanation {i}")
                    self.results["decision"]["failed"].append(f"Explanation {i}: Missing {field}")
                    passed = False
                    continue

            if "confidence" not in exp:
                continue

            confidence = exp["confidence"]

            # Validate confidence is numeric
            if not isinstance(confidence, (int, float)):
                print(f"  ✗ FAIL: Confidence must be numeric in explanation {i}")
                self.results["decision"]["failed"].append(f"Explanation {i}: Invalid confidence type")
                passed = False
                continue

            # Validate confidence range
            if confidence < 0 or confidence > 1:
                print(f"  ✗ FAIL: Confidence must be between 0 and 1 in explanation {i} (got {confidence})")
                self.results["decision"]["failed"].append(f"Explanation {i}: Confidence out of range ({confidence})")
                passed = False
                continue

            # Check minimum confidence threshold
            if confidence < min_confidence:
                print(f"  ⚠ WARNING: Low confidence ({confidence:.3f}) in explanation {i}")

            # Validate reasoning is a list with content
            if not isinstance(exp.get("reasoning"), list) or len(exp["reasoning"]) == 0:
                print(f"  ✗ FAIL: Reasoning must be a non-empty list in explanation {i}")
                self.results["decision"]["failed"].append(f"Explanation {i}: Invalid reasoning")
                passed = False
                continue

            # Validate recommendations is a list with content
            if not isinstance(exp.get("recommendations"), list) or len(exp["recommendations"]) == 0:
                print(f"  ✗ FAIL: Recommendations must be a non-empty list in explanation {i}")
                self.results["decision"]["failed"].append(f"Explanation {i}: Invalid recommendations")
                passed = False
                continue

        if passed:
            print(f"  ✓ PASS: All {len(explanations)} decision explanations valid")
            self.results["decision"]["passed"].append(f"All {len(explanations)} explanations valid")

        return passed

    def generate_report(self) -> Dict[str, Any]:
        """Generate validation report."""
        total_passed = sum(len(v["passed"]) for v in self.results.values())
        total_failed = sum(len(v["failed"]) for v in self.results.values())

        return {
            "summary": {
                "total_checks": total_passed + total_failed,
                "passed": total_passed,
                "failed": total_failed,
                "overall_status": "PASS" if total_failed == 0 else "FAIL"
            },
            "details": self.results
        }


def main():
    parser = argparse.ArgumentParser(
        description="Validate explanation quality and correctness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --shap shap_explanations.json --lime lime_explanations.json
  %(prog)s --attention attention_visualizations.json --decision decision_explanations.json
  %(prog)s --all explanations_dir/ --report validation_report.json
        """
    )

    parser.add_argument('--shap', type=str, help='SHAP explanations JSON file')
    parser.add_argument('--lime', type=str, help='LIME explanations JSON file')
    parser.add_argument('--attention', type=str, help='Attention visualizations JSON file')
    parser.add_argument('--decision', type=str, help='Decision explanations JSON file')
    parser.add_argument('--all', type=str, help='Directory containing all explanation files')
    parser.add_argument('--report', type=str, help='Output file for validation report (JSON)')
    parser.add_argument('--lime-threshold', type=float, default=0.85,
                       help='Minimum R² threshold for LIME (default: 0.85)')
    parser.add_argument('--attention-heads', type=int, default=8,
                       help='Expected number of attention heads (default: 8)')

    args = parser.parse_args()

    # Determine file paths
    if args.all:
        base_dir = Path(args.all)
        shap_file = base_dir / "shap_explanations.json"
        lime_file = base_dir / "lime_explanations.json"
        attention_file = base_dir / "attention_visualizations.json"
        decision_file = base_dir / "decision_explanations.json"
    else:
        shap_file = Path(args.shap) if args.shap else None
        lime_file = Path(args.lime) if args.lime else None
        attention_file = Path(args.attention) if args.attention else None
        decision_file = Path(args.decision) if args.decision else None

    validator = ExplanationValidator()
    all_passed = True

    print("=" * 60)
    print("EXPLANATION VALIDATION")
    print("=" * 60)

    # Validate SHAP
    if shap_file and shap_file.exists():
        try:
            with open(shap_file, 'r') as f:
                shap_data = json.load(f)
            if not validator.validate_shap_values(shap_data):
                all_passed = False
        except Exception as e:
            print(f"\n✗ Error validating SHAP file: {e}")
            all_passed = False

    # Validate LIME
    if lime_file and lime_file.exists():
        try:
            with open(lime_file, 'r') as f:
                lime_data = json.load(f)
            if not validator.validate_lime_local_model(lime_data, args.lime_threshold):
                all_passed = False
        except Exception as e:
            print(f"\n✗ Error validating LIME file: {e}")
            all_passed = False

    # Validate Attention
    if attention_file and attention_file.exists():
        try:
            with open(attention_file, 'r') as f:
                attention_data = json.load(f)
            if not validator.validate_attention_weights(attention_data, args.attention_heads):
                all_passed = False
        except Exception as e:
            print(f"\n✗ Error validating attention file: {e}")
            all_passed = False

    # Validate Decision
    if decision_file and decision_file.exists():
        try:
            with open(decision_file, 'r') as f:
                decision_data = json.load(f)
            if not validator.validate_decision_confidence(decision_data):
                all_passed = False
        except Exception as e:
            print(f"\n✗ Error validating decision file: {e}")
            all_passed = False

    # Generate report
    report = validator.generate_report()

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total checks: {report['summary']['total_checks']}")
    print(f"Passed: {report['summary']['passed']}")
    print(f"Failed: {report['summary']['failed']}")
    print(f"Overall status: {report['summary']['overall_status']}")
    print("=" * 60)

    # Save report if requested
    if args.report:
        report_path = Path(args.report)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nValidation report saved to: {report_path.absolute()}")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
