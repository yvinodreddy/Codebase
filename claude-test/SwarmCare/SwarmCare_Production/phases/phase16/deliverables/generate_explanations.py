#!/usr/bin/env python3
"""
Generate Explanations Script
Generates SHAP, LIME, attention, and decision explanations for SwarmCare models.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))

try:
    from implementation import (
        generate_shap_explanations,
        generate_lime_explanations,
        generate_attention_visualizations,
        generate_decision_explanations
    )
except ImportError as e:
    print(f"Warning: Could not import from implementation.py: {e}")
    print("Using mock implementation for demonstration purposes.")

    def generate_shap_explanations(model, count):
        return [{
            "patient_id": f"P{1000+i}",
            "prediction": "High Risk" if i % 2 == 0 else "Low Risk",
            "shap_values": {
                "age": 0.15 + (i * 0.01),
                "blood_pressure": -0.08 + (i * 0.005),
                "heart_rate": 0.12 - (i * 0.003),
                "respiratory_rate": 0.06 + (i * 0.002)
            },
            "base_value": 0.5,
            "timestamp": datetime.now().isoformat()
        } for i in range(count)]

    def generate_lime_explanations(model, count):
        return [{
            "patient_id": f"P{1000+i}",
            "prediction": "High Risk" if i % 2 == 0 else "Low Risk",
            "lime_explanation": {
                "age > 65": 0.25,
                "bp_systolic > 140": 0.18,
                "heart_rate < 60": -0.12,
                "oxygen_sat < 95": 0.15
            },
            "local_model_r2": 0.89 + (i * 0.001),
            "timestamp": datetime.now().isoformat()
        } for i in range(count)]

    def generate_attention_visualizations(model, count):
        return [{
            "patient_id": f"P{1000+i}",
            "attention_weights": {
                f"head_{j}": [0.1 + (j * 0.02) for _ in range(10)]
                for j in range(8)
            },
            "layer": "transformer_layer_4",
            "timestamp": datetime.now().isoformat()
        } for i in range(count)]

    def generate_decision_explanations(model, count):
        return [{
            "patient_id": f"P{1000+i}",
            "decision": "Immediate Intervention Required" if i % 3 == 0 else "Monitor Closely",
            "confidence": 0.85 + (i * 0.01),
            "reasoning": [
                "Elevated vital signs detected",
                "Pattern matches high-risk profile",
                "Historical trend indicates deterioration"
            ],
            "recommendations": [
                "Increase monitoring frequency",
                "Consult specialist",
                "Review medication"
            ],
            "timestamp": datetime.now().isoformat()
        } for i in range(count)]


def main():
    parser = argparse.ArgumentParser(
        description="Generate explanations for SwarmCare model predictions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --model swarmcare_v1 --count 10 --output explanations/
  %(prog)s --model ensemble --count 5 --output ./data/
        """
    )

    parser.add_argument(
        '--model',
        type=str,
        default='swarmcare_v1',
        help='Model name to generate explanations for (default: swarmcare_v1)'
    )

    parser.add_argument(
        '--count',
        type=int,
        default=10,
        help='Number of explanations to generate (default: 10)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='.',
        help='Output directory for explanation files (default: current directory)'
    )

    args = parser.parse_args()

    # Validate arguments
    if args.count <= 0:
        print("Error: --count must be a positive integer", file=sys.stderr)
        sys.exit(1)

    # Create output directory
    output_dir = Path(args.output)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Generating explanations for model: {args.model}")
    print(f"Count: {args.count}")
    print(f"Output directory: {output_dir.absolute()}\n")

    results = {}

    try:
        # Generate SHAP explanations
        print("Generating SHAP explanations...")
        shap_explanations = generate_shap_explanations(args.model, args.count)
        shap_file = output_dir / "shap_explanations.json"
        with open(shap_file, 'w') as f:
            json.dump(shap_explanations, f, indent=2)
        results['shap'] = str(shap_file.absolute())
        print(f"  ✓ Saved to {shap_file}")

        # Generate LIME explanations
        print("Generating LIME explanations...")
        lime_explanations = generate_lime_explanations(args.model, args.count)
        lime_file = output_dir / "lime_explanations.json"
        with open(lime_file, 'w') as f:
            json.dump(lime_explanations, f, indent=2)
        results['lime'] = str(lime_file.absolute())
        print(f"  ✓ Saved to {lime_file}")

        # Generate attention visualizations
        print("Generating attention visualizations...")
        attention_count = max(1, args.count // 2)  # Generate fewer attention visualizations
        attention_viz = generate_attention_visualizations(args.model, attention_count)
        attention_file = output_dir / "attention_visualizations.json"
        with open(attention_file, 'w') as f:
            json.dump(attention_viz, f, indent=2)
        results['attention'] = str(attention_file.absolute())
        print(f"  ✓ Saved to {attention_file}")

        # Generate decision explanations
        print("Generating decision explanations...")
        decision_explanations = generate_decision_explanations(args.model, args.count)
        decision_file = output_dir / "decision_explanations.json"
        with open(decision_file, 'w') as f:
            json.dump(decision_explanations, f, indent=2)
        results['decision'] = str(decision_file.absolute())
        print(f"  ✓ Saved to {decision_file}")

        # Save summary
        summary = {
            "model": args.model,
            "count": args.count,
            "timestamp": datetime.now().isoformat(),
            "files": results
        }
        summary_file = output_dir / "generation_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"\n✓ All explanations generated successfully!")
        print(f"Summary saved to {summary_file}")

    except Exception as e:
        print(f"\nError generating explanations: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
