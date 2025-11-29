#!/usr/bin/env python3
"""
CLI Interface for Orchestration System
User-friendly command-line interface for processing prompts with full orchestration
"""

import argparse
import logging
import sys
import json
from typing import Optional
from pathlib import Path

from master_orchestrator import MasterOrchestrator
from claude_integration import ClaudeOrchestrator


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('orchestrator.log'),
            logging.StreamHandler()
        ]
    )


def process_prompt_local(
    prompt: str,
    min_confidence: float,
    max_iterations: int,
    output_file: Optional[str]
):
    """Process prompt using local orchestrator (no Claude API)"""
    print("\n" + "=" * 80)
    print("PROCESSING WITH LOCAL ORCHESTRATOR")
    print("=" * 80)

    orchestrator = MasterOrchestrator(
        min_confidence_score=min_confidence,
        max_refinement_iterations=max_iterations
    )

    print(f"\nPrompt: {prompt}\n")
    print("Processing...")

    result = orchestrator.process(prompt)

    # Display results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"\nStatus: {'✅ SUCCESS' if result.success else '❌ FAILED'}")
    print(f"Confidence Score: {result.confidence_score:.2f}%")
    print(f"Iterations: {result.iterations_performed}")
    print(f"Duration: {result.total_duration_seconds:.2f}s")

    if result.warnings:
        print(f"\n⚠️  Warnings: {len(result.warnings)}")
        for warning in result.warnings[:3]:
            print(f"   - {warning}")

    if result.errors:
        print(f"\n❌ Errors:")
        for error in result.errors:
            print(f"   - {error}")

    print(f"\nPrompt Analysis:")
    print(f"   Intent: {result.prompt_analysis.get('intent_type')}")
    print(f"   Complexity: {result.prompt_analysis.get('complexity')}")
    print(f"   Required Components: {result.prompt_analysis.get('required_components')}")

    print(f"\nQuality Metrics:")
    for metric, value in result.quality_metrics.items():
        if isinstance(value, dict):
            print(f"   {metric}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        else:
            print(f"   {metric}: {value}")

    # Save to file if requested
    if output_file:
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"\n💾 Results saved to: {output_path}")

    # Show statistics
    print("\n" + "=" * 80)
    print("ORCHESTRATOR STATISTICS")
    print("=" * 80)
    stats = orchestrator.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value:.2f}" if isinstance(value, float) else f"   {key}: {value}")

    print("\n" + "=" * 80)


def process_prompt_claude(
    prompt: str,
    model: str,
    min_confidence: float,
    max_iterations: int,
    max_tokens: int,
    temperature: float,
    output_file: Optional[str]
):
    """Process prompt using Claude API with orchestration"""
    print("\n" + "=" * 80)
    print(f"PROCESSING WITH CLAUDE ({model})")
    print("=" * 80)

    try:
        orchestrator = ClaudeOrchestrator(
            model=model,
            min_confidence_score=min_confidence,
            max_refinement_iterations=max_iterations
        )
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    print(f"\nPrompt: {prompt}\n")
    print("Processing...")

    response = orchestrator.process(
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )

    # Display results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"\nStatus: {'✅ SUCCESS' if response.success else '❌ FAILED'}")
    print(f"Confidence Score: {response.orchestration_result.confidence_score:.2f}%")
    print(f"Model: {response.claude_model}")
    print(f"Tokens: {response.total_tokens}")
    print(f"Cost: ${response.cost_estimate:.6f}")

    print(f"\n{'─' * 80}")
    print("CLAUDE RESPONSE:")
    print(f"{'─' * 80}")
    print(f"\n{response.response_text}\n")
    print(f"{'─' * 80}")

    print(f"\nOrchestration Metrics:")
    print(f"   Iterations: {response.orchestration_result.iterations_performed}")
    print(f"   Duration: {response.orchestration_result.total_duration_seconds:.2f}s")

    if response.orchestration_result.warnings:
        print(f"   Warnings: {len(response.orchestration_result.warnings)}")

    # Save to file if requested
    if output_file:
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(response.to_dict(), f, indent=2)
        print(f"\n💾 Results saved to: {output_path}")

    # Show statistics
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)
    stats = orchestrator.get_statistics()
    print(f"   Total Requests: {stats['total_requests']}")
    print(f"   Total Tokens: {stats['total_tokens']}")
    print(f"   Total Cost: ${stats['total_cost']:.6f}")

    print("\n" + "=" * 80)


def interactive_mode(use_claude: bool, model: str, min_confidence: float):
    """Run in interactive mode"""
    print("\n" + "=" * 80)
    print("INTERACTIVE MODE")
    print("=" * 80)
    print("\nType your prompts and press Enter. Type 'quit' or 'exit' to stop.\n")

    if use_claude:
        try:
            orchestrator = ClaudeOrchestrator(
                model=model,
                min_confidence_score=min_confidence
            )
            print(f"Using Claude ({model}) with orchestration\n")
        except ValueError as e:
            print(f"\n❌ Error: {e}")
            print("Falling back to local orchestrator\n")
            use_claude = False
            orchestrator = MasterOrchestrator(min_confidence_score=min_confidence)
    else:
        orchestrator = MasterOrchestrator(min_confidence_score=min_confidence)
        print("Using local orchestrator\n")

    while True:
        try:
            prompt = input("\n🤖 Enter prompt: ").strip()

            if not prompt:
                continue

            if prompt.lower() in ['quit', 'exit', 'q']:
                break

            print("\nProcessing...\n")

            if use_claude:
                response = orchestrator.process(prompt, max_tokens=2048)
                print(f"Confidence: {response.orchestration_result.confidence_score:.2f}%")
                print(f"\n{response.response_text}\n")
            else:
                result = orchestrator.process(prompt)
                print(f"Confidence: {result.confidence_score:.2f}%")
                if result.success:
                    print(f"Output: {result.output}")
                else:
                    print(f"❌ Processing failed: {result.errors}")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

    # Show final statistics
    print("\n" + "=" * 80)
    print("SESSION STATISTICS")
    print("=" * 80)
    stats = orchestrator.get_statistics()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"   {k}: {v}")
        else:
            print(f"   {key}: {value:.2f}" if isinstance(value, float) else f"   {key}: {value}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Orchestration System CLI - Process prompts with comprehensive validation and quality assurance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process prompt with local orchestrator
  python cli_interface.py "What is machine learning?"

  # Process prompt with Claude
  python cli_interface.py --claude "Write a Python function to sort a list"

  # Interactive mode
  python cli_interface.py --interactive

  # Save results to file
  python cli_interface.py --output results.json "Explain neural networks"

  # Adjust confidence threshold
  python cli_interface.py --min-confidence 98.0 "Implement a REST API"
        """
    )

    parser.add_argument(
        'prompt',
        nargs='?',
        help='Prompt to process (optional in interactive mode)'
    )

    parser.add_argument(
        '--claude', '-c',
        action='store_true',
        help='Use Claude API instead of local orchestrator'
    )

    parser.add_argument(
        '--model', '-m',
        default='claude-3-5-sonnet-20241022',
        help='Claude model to use (default: claude-3-5-sonnet-20241022)'
    )

    parser.add_argument(
        '--min-confidence',
        type=float,
        default=96.0,
        help='Minimum confidence score (0-100, default: 96.0)'
    )

    parser.add_argument(
        '--max-iterations',
        type=int,
        default=5,
        help='Maximum refinement iterations (default: 5)'
    )

    parser.add_argument(
        '--max-tokens',
        type=int,
        default=4096,
        help='Maximum tokens for Claude response (default: 4096)'
    )

    parser.add_argument(
        '--temperature',
        type=float,
        default=1.0,
        help='Temperature for Claude (0-1, default: 1.0)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file for results (JSON format)'
    )

    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Validate arguments
    if not args.interactive and not args.prompt:
        parser.error("Prompt is required unless using --interactive mode")

    # Run appropriate mode
    if args.interactive:
        interactive_mode(args.claude, args.model, args.min_confidence)
    elif args.claude:
        process_prompt_claude(
            args.prompt,
            args.model,
            args.min_confidence,
            args.max_iterations,
            args.max_tokens,
            args.temperature,
            args.output
        )
    else:
        process_prompt_local(
            args.prompt,
            args.min_confidence,
            args.max_iterations,
            args.output
        )


if __name__ == "__main__":
    main()
