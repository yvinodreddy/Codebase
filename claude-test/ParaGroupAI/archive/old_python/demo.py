#!/usr/bin/env python3
"""
Comprehensive Orchestration System Demo
Demonstrates the full capabilities of the orchestration pipeline
"""

import logging
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

from prompt_preprocessor import PromptPreprocessor
from master_orchestrator import MasterOrchestrator


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def print_subsection(title: str):
    """Print formatted subsection header"""
    print("\n" + "-" * 80)
    print(f" {title}")
    print("-" * 80)


def demo_prompt_preprocessor():
    """Demonstrate prompt preprocessing capabilities"""
    print_section("1. PROMPT PREPROCESSOR DEMO")

    preprocessor = PromptPreprocessor()

    test_cases = [
        {
            "name": "Simple Question",
            "prompt": "What is machine learning?"
        },
        {
            "name": "Code Generation",
            "prompt": "Write a Python function to calculate the factorial of a number"
        },
        {
            "name": "Complex Multi-Step Task",
            "prompt": """Implement a comprehensive medical diagnosis system that includes:
            1. Patient data collection with PHI protection
            2. Symptom analysis using medical terminology
            3. Diagnosis suggestion with evidence-based recommendations
            4. Full HIPAA compliance validation
            5. Multi-layer guardrails for safety"""
        },
        {
            "name": "Search Task",
            "prompt": "Find all Python files in the project that contain class definitions"
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print_subsection(f"{i}. {test['name']}")
        print(f"Prompt: {test['prompt'][:100]}...")

        analysis = preprocessor.analyze_prompt(test['prompt'])

        print(f"\n📊 Analysis Results:")
        print(f"   Intent: {analysis.intent_type}")
        print(f"   Complexity: {analysis.complexity}")
        print(f"   Confidence: {analysis.confidence:.2f}")
        print(f"   Estimated Iterations: {analysis.estimated_iterations}")
        print(f"   Required Components: {', '.join(analysis.required_components)}")
        print(f"   Requires Search: {analysis.requires_search}")
        print(f"   Requires Code Gen: {analysis.requires_code_generation}")
        print(f"   Requires Parallel: {analysis.requires_parallel_processing}")

    # Show statistics
    print_subsection("Preprocessor Statistics")
    stats = preprocessor.get_statistics()
    print(f"   Total Prompts Analyzed: {stats['total_prompts']}")
    print(f"   Intent Distribution: {stats['intents']}")
    print(f"   Complexity Distribution: {stats['complexity_distribution']}")
    print(f"   Average Confidence: {stats['average_confidence']:.2f}")


def demo_master_orchestrator():
    """Demonstrate master orchestrator capabilities"""
    print_section("2. MASTER ORCHESTRATOR DEMO")

    orchestrator = MasterOrchestrator(
        min_confidence_score=96.0,
        max_refinement_iterations=5
    )

    test_cases = [
        {
            "name": "Simple Educational Query",
            "prompt": "Explain what an API is in simple terms",
            "description": "Tests basic question handling"
        },
        {
            "name": "Code Generation Task",
            "prompt": "Write a Python function to reverse a string",
            "description": "Tests code generation and verification"
        },
        {
            "name": "Complex Analysis",
            "prompt": "Analyze the differences between supervised and unsupervised learning, providing examples and use cases",
            "description": "Tests comprehensive analysis with multi-method verification"
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print_subsection(f"{i}. {test['name']}")
        print(f"Description: {test['description']}")
        print(f"Prompt: {test['prompt']}")
        print("\nProcessing through full orchestration pipeline...")

        result = orchestrator.process(test['prompt'])

        print(f"\n📊 Results:")
        print(f"   ✅ Success: {result.success}")
        print(f"   📈 Confidence Score: {result.confidence_score:.2f}%")
        print(f"   🔄 Iterations: {result.iterations_performed}")
        print(f"   ⏱️  Duration: {result.total_duration_seconds:.2f}s")

        if result.warnings:
            print(f"   ⚠️  Warnings: {len(result.warnings)}")
            for warning in result.warnings[:2]:
                print(f"      - {warning}")

        if result.errors:
            print(f"   ❌ Errors: {len(result.errors)}")
            for error in result.errors:
                print(f"      - {error}")

        print(f"\n   Pipeline Breakdown:")
        print(f"      Intent: {result.prompt_analysis.get('intent_type')}")
        print(f"      Complexity: {result.prompt_analysis.get('complexity')}")
        print(f"      Components Used: {result.prompt_analysis.get('required_components')}")

        print(f"\n   Guardrails:")
        input_val = result.guardrails_validation.get('input_validation', {})
        output_val = result.guardrails_validation.get('output_validation', {})
        print(f"      Input Validation: {'✅ Passed' if input_val.get('success') else '❌ Failed'}")
        print(f"      Output Validation: {'✅ Passed' if output_val.get('success') else '❌ Failed'}")

        print(f"\n   Quality Metrics:")
        for metric, value in result.quality_metrics.items():
            if metric == "confidence_breakdown":
                print(f"      Confidence Breakdown:")
                for component, score in value.items():
                    print(f"         {component}: {score:.2f}")
            elif metric != "verification_details":
                print(f"      {metric}: {value}")

    # Show orchestrator statistics
    print_subsection("Orchestrator Statistics")
    stats = orchestrator.get_statistics()
    print(f"   Total Requests: {stats['total_requests']}")
    print(f"   Successful: {stats['successful_requests']}")
    print(f"   Failed: {stats['failed_requests']}")
    print(f"   Success Rate: {stats.get('success_rate', 0):.2f}%")
    print(f"   Average Confidence: {stats['average_confidence']:.2f}%")
    print(f"   Average Iterations: {stats['average_iterations']:.2f}")
    print(f"   Average Duration: {stats['average_duration']:.2f}s")


def demo_confidence_scoring():
    """Demonstrate confidence scoring mechanism"""
    print_section("3. CONFIDENCE SCORING DEMO")

    print("\nThe system calculates confidence scores based on:")
    print("   • Prompt Analysis (15%)")
    print("   • Agent Execution (25%)")
    print("   • Guardrails Validation (30%)")
    print("   • Iteration Efficiency (15%)")
    print("   • Verification Results (15%)")
    print("\nTarget: 96-100% confidence score")

    orchestrator = MasterOrchestrator(min_confidence_score=96.0)

    prompts = [
        ("Very clear, simple prompt", "What is Python?"),
        ("Moderately complex prompt", "Explain object-oriented programming concepts"),
        ("Complex analytical prompt", "Compare and contrast different machine learning algorithms with examples")
    ]

    print_subsection("Confidence Score Comparison")

    for description, prompt in prompts:
        result = orchestrator.process(prompt)

        print(f"\n{description}:")
        print(f"   Prompt: {prompt}")
        print(f"   Confidence: {result.confidence_score:.2f}%")
        print(f"   Status: {'✅ Meets threshold (96%)' if result.confidence_score >= 96.0 else '⚠️ Below threshold'}")


def demo_error_handling():
    """Demonstrate error handling and recovery"""
    print_section("4. ERROR HANDLING & RECOVERY DEMO")

    orchestrator = MasterOrchestrator()

    test_cases = [
        {
            "name": "Empty Prompt",
            "prompt": "",
            "expected": "Should handle gracefully"
        },
        {
            "name": "Very Long Prompt",
            "prompt": "Test " * 1000,
            "expected": "Should process or truncate appropriately"
        },
        {
            "name": "Special Characters",
            "prompt": "Test @#$%^&*() prompt with special chars",
            "expected": "Should sanitize and process"
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print_subsection(f"{i}. {test['name']}")
        print(f"Expected: {test['expected']}")

        try:
            result = orchestrator.process(test['prompt'])
            print(f"Result: {'✅ Success' if result.success else '⚠️ Failed gracefully'}")
            if not result.success and result.errors:
                print(f"Errors: {result.errors}")
        except Exception as e:
            print(f"❌ Exception (should not happen): {e}")


def demo_performance():
    """Demonstrate performance characteristics"""
    print_section("5. PERFORMANCE DEMO")

    import time

    orchestrator = MasterOrchestrator()

    print_subsection("Processing Speed")

    prompts = [
        "What is AI?",
        "Explain neural networks",
        "Write a function to sort a list"
    ]

    total_start = time.time()
    durations = []

    for i, prompt in enumerate(prompts, 1):
        start = time.time()
        result = orchestrator.process(prompt)
        duration = time.time() - start
        durations.append(duration)

        print(f"\n{i}. \"{prompt[:40]}...\"")
        print(f"   Duration: {duration:.2f}s")
        print(f"   Iterations: {result.iterations_performed}")
        print(f"   Confidence: {result.confidence_score:.2f}%")

    total_duration = time.time() - total_start

    print(f"\n📊 Performance Summary:")
    print(f"   Total Duration: {total_duration:.2f}s")
    print(f"   Average Duration: {sum(durations)/len(durations):.2f}s")
    print(f"   Min Duration: {min(durations):.2f}s")
    print(f"   Max Duration: {max(durations):.2f}s")


def main():
    """Run complete demonstration"""
    # Setup logging
    logging.basicConfig(
        level=logging.WARNING,  # Set to WARNING to reduce noise in demo
        format='%(levelname)s: %(message)s'
    )

    print("\n" + "=" * 80)
    print(" COMPREHENSIVE ORCHESTRATION SYSTEM DEMONSTRATION")
    print(" Target Accuracy: 96-100%")
    print("=" * 80)

    print("\nThis demo showcases:")
    print("   ✓ Prompt preprocessing and intent classification")
    print("   ✓ Master orchestration pipeline")
    print("   ✓ Confidence scoring mechanism")
    print("   ✓ Error handling and recovery")
    print("   ✓ Performance characteristics")

    input("\nPress Enter to start the demonstration...")

    try:
        # Run all demos
        demo_prompt_preprocessor()
        input("\nPress Enter to continue to Master Orchestrator demo...")

        demo_master_orchestrator()
        input("\nPress Enter to continue to Confidence Scoring demo...")

        demo_confidence_scoring()
        input("\nPress Enter to continue to Error Handling demo...")

        demo_error_handling()
        input("\nPress Enter to continue to Performance demo...")

        demo_performance()

        # Final summary
        print_section("DEMO COMPLETE")
        print("\n✅ Demonstration completed successfully!")
        print("\nKey Takeaways:")
        print("   • Comprehensive 7-layer pipeline for maximum accuracy")
        print("   • Automatic intent classification and component selection")
        print("   • Confidence scoring targeting 96-100% accuracy")
        print("   • Robust error handling and recovery")
        print("   • Production-ready performance")
        print("\nNext Steps:")
        print("   1. Try the CLI: python cli_interface.py --help")
        print("   2. Run tests: python test_orchestration.py")
        print("   3. Read README.md for detailed documentation")
        print("   4. Integrate into your application")

        print("\n" + "=" * 80)

    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
