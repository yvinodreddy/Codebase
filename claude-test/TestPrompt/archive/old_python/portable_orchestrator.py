#!/usr/bin/env python3
"""
Portable Orchestration Wrapper
Works from ANY directory - just run: orchestrate "your prompt"

This wrapper makes the orchestration system available globally while
working in any directory. It automatically handles paths and configuration.
"""

import sys
import os
from pathlib import Path
import argparse
import json

# Get the orchestration home from environment or use script location
ORCHESTRATION_HOME = Path(os.environ.get('ORCHESTRATION_HOME', Path(__file__).parent))
sys.path.insert(0, str(ORCHESTRATION_HOME))

try:
    from master_orchestrator import MasterOrchestrator
    from claude_integration import ClaudeOrchestrator
except ImportError as e:
    print(f"❌ Error: Cannot import orchestration modules from {ORCHESTRATION_HOME}")
    print(f"   {e}")
    print(f"\n💡 Set ORCHESTRATION_HOME environment variable to the TestPrompt directory")
    sys.exit(1)


def get_current_context():
    """Gather context about current working directory"""
    cwd = Path.cwd()
    context = {
        "working_directory": str(cwd),
        "directory_name": cwd.name,
        "is_git_repo": (cwd / ".git").exists(),
        "has_python": any((cwd / f).exists() for f in ["setup.py", "pyproject.toml", "requirements.txt"]),
        "has_nodejs": any((cwd / f).exists() for f in ["package.json", "package-lock.json"]),
        "has_dotnet": any(cwd.glob("*.csproj")),
        "readme_exists": any((cwd / f).exists() for f in ["README.md", "README.txt", "README"]),
    }

    # List immediate directory contents
    try:
        contents = [f.name for f in cwd.iterdir() if not f.name.startswith('.')][:20]
        context["directory_contents"] = contents
    except:
        context["directory_contents"] = []

    return context


def main():
    parser = argparse.ArgumentParser(
        description="Portable Orchestration - Run from ANY directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  orchestrate "explain this codebase"
  orchestrate "fix all bugs" --claude
  orchestrate "write tests" --min-confidence 98
  orchestrate "refactor code" --context auto

The orchestrator automatically:
  ✓ Analyzes your current directory
  ✓ Routes through all guardrails
  ✓ Applies all agent framework components
  ✓ Targets 96-100% confidence
  ✓ Refines until quality threshold is met
        """
    )

    parser.add_argument(
        'prompt',
        nargs='?',
        help='The prompt to process'
    )

    parser.add_argument(
        '--claude', '-c',
        action='store_true',
        help='Use Claude API (requires ANTHROPIC_API_KEY)'
    )

    parser.add_argument(
        '--min-confidence',
        type=float,
        default=96.0,
        help='Minimum confidence threshold (default: 96.0)'
    )

    parser.add_argument(
        '--context',
        choices=['auto', 'minimal', 'full'],
        default='auto',
        help='Context gathering mode (default: auto)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Save results to JSON file'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    parser.add_argument(
        '--show-dir',
        action='store_true',
        help='Show current directory context and exit'
    )

    args = parser.parse_args()

    # Show directory context
    if args.show_dir:
        context = get_current_context()
        print(json.dumps(context, indent=2))
        return 0

    # Validate prompt
    if not args.prompt:
        parser.print_help()
        return 1

    # Gather context if requested
    context_info = None
    if args.context in ['auto', 'full']:
        context_info = get_current_context()
        if args.verbose:
            print(f"📁 Working directory: {context_info['working_directory']}")

    # Enhance prompt with directory context
    enhanced_prompt = args.prompt
    if context_info and args.context == 'auto':
        enhanced_prompt = f"""Working in directory: {context_info['directory_name']}
Directory type: {'Git repo' if context_info['is_git_repo'] else 'Regular directory'}
Project type: {', '.join([k.replace('has_', '') for k, v in context_info.items() if k.startswith('has_') and v])}

User Request: {args.prompt}"""

    print("\n" + "="*80)
    print(" PORTABLE ORCHESTRATION SYSTEM")
    print(f" Working Directory: {Path.cwd()}")
    print(f" Orchestration Home: {ORCHESTRATION_HOME}")
    print(f" Mode: {'Claude API' if args.claude else 'Local Orchestrator'}")
    print(f" Confidence Threshold: {args.min_confidence}%")
    print("="*80 + "\n")

    try:
        if args.claude:
            # Use Claude API
            if not os.getenv('ANTHROPIC_API_KEY'):
                print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
                print("   Set it in your .bashrc or .env file")
                return 1

            orchestrator = ClaudeOrchestrator(min_confidence_score=args.min_confidence)

            print("🔄 Processing with Claude API...\n")
            response = orchestrator.process(enhanced_prompt)

            print("="*80)
            print(" CLAUDE RESPONSE")
            print("="*80)
            print(response.response_text)
            print("\n" + "="*80)
            print(" ORCHESTRATION METRICS")
            print("="*80)
            print(f"Confidence: {response.orchestration_result.confidence_score:.2f}%")
            print(f"Tokens Used: {response.total_tokens:,} (Input: {response.input_tokens:,}, Output: {response.output_tokens:,})")
            print(f"Cost Estimate: ${response.cost_estimate:.6f}")
            print(f"Duration: {response.orchestration_result.total_duration_seconds:.2f}s")

            # Save if requested
            if args.output:
                output_data = {
                    "prompt": args.prompt,
                    "enhanced_prompt": enhanced_prompt,
                    "response": response.response_text,
                    "confidence": response.orchestration_result.confidence_score,
                    "tokens": response.total_tokens,
                    "cost": response.cost_estimate,
                    "context": context_info
                }
                with open(args.output, 'w') as f:
                    json.dump(output_data, f, indent=2)
                print(f"\n💾 Results saved to: {args.output}")

        else:
            # Use local orchestrator
            orchestrator = MasterOrchestrator(min_confidence_score=args.min_confidence)

            print("🔄 Processing with local orchestrator...\n")
            result = orchestrator.process(enhanced_prompt, context=context_info)

            print("="*80)
            print(f" {'✅ SUCCESS' if result.success else '❌ FAILED'}")
            print("="*80)
            print(f"Confidence Score: {result.confidence_score:.2f}%")
            print(f"Iterations: {result.iterations_performed}")
            print(f"Duration: {result.total_duration_seconds:.2f}s")

            if result.output:
                print("\n" + "="*80)
                print(" OUTPUT")
                print("="*80)
                print(result.output)

            if result.warnings:
                print(f"\n⚠️  Warnings ({len(result.warnings)}):")
                for warning in result.warnings[:3]:
                    print(f"   - {warning}")

            if result.errors:
                print(f"\n❌ Errors ({len(result.errors)}):")
                for error in result.errors:
                    print(f"   - {error}")

            # Verbose details
            if args.verbose:
                print("\n" + "="*80)
                print(" DETAILED METRICS")
                print("="*80)
                print(f"Intent: {result.prompt_analysis.get('intent_type')}")
                print(f"Complexity: {result.prompt_analysis.get('complexity')}")
                print(f"Components: {result.prompt_analysis.get('required_components')}")

                if result.quality_metrics.get('confidence_breakdown'):
                    print("\nConfidence Breakdown:")
                    for component, score in result.quality_metrics['confidence_breakdown'].items():
                        print(f"  {component}: {score:.2f}")

            # Save if requested
            if args.output:
                output_data = {
                    "prompt": args.prompt,
                    "enhanced_prompt": enhanced_prompt,
                    "success": result.success,
                    "confidence": result.confidence_score,
                    "output": result.output,
                    "iterations": result.iterations_performed,
                    "duration": result.total_duration_seconds,
                    "prompt_analysis": result.prompt_analysis,
                    "quality_metrics": result.quality_metrics,
                    "warnings": result.warnings,
                    "errors": result.errors,
                    "context": context_info
                }
                with open(args.output, 'w') as f:
                    json.dump(output_data, f, indent=2, default=str)
                print(f"\n💾 Results saved to: {args.output}")

        print("\n" + "="*80 + "\n")
        return 0 if (args.claude or result.success) else 1

    except Exception as e:
        print(f"\n❌ Error during orchestration: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
