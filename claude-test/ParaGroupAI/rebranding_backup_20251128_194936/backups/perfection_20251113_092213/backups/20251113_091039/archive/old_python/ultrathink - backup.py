#!/usr/bin/env python3
"""
ULTRATHINK - The ONE Unified Command

This is THE ONLY command you need. It does EVERYTHING:
- Takes your prompt (any size: 1 line or 500 lines)
- Applies your 5 ULTRATHINK directives
- Routes through ALL 8 agent framework components
- Routes through ALL 7 guardrail layers
- Targets 99-100% confidence
- Works everywhere (Claude Code, generates for Web)

USAGE:
    ultrathink "your prompt"
    ultrathink "your prompt" --web
    ultrathink --file large-prompt.txt
    ultrathink --help
"""

import sys
import os
from pathlib import Path
import argparse

# Setup
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from master_orchestrator import MasterOrchestrator
    from claude_integration import ClaudeOrchestrator
except ImportError as e:
    print(f"\n❌ ERROR: Cannot find orchestration system")
    print(f"   Make sure you're running from: {SCRIPT_DIR}")
    print(f"   Error: {e}\n")
    sys.exit(1)


def print_header():
    """Show what this tool does"""
    print("\n" + "="*80)
    print("🔥 ULTRATHINK - Unified Orchestration System")
    print("="*80)
    print("Your prompt → ULTRATHINK directives → Agent Framework → Guardrails → Result")
    print("="*80 + "\n")


def show_how_it_works():
    """Explain the flow in simple terms"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    HOW ULTRATHINK WORKS (Simple Flow)                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

YOUR PROMPT
    ↓
STAGE 1: ULTRATHINK DIRECTIVES APPLIED
    • TAKE FULL CONTROL - Autonomous execution activated
    • PRODUCTION-READY - 99%+ confidence required
    • 100% SUCCESS RATE - Multi-method verification
    • FAIL FAST, FIX FASTER - Rapid iteration
    • PARALLEL EVERYTHING - Concurrent processing
    ↓
STAGE 2: PROMPT ANALYSIS
    • What are you asking? (question, code, task, etc.)
    • How complex is it? (simple, moderate, complex)
    • Which components needed? (search, code gen, etc.)
    ↓
STAGE 3: AGENT FRAMEWORK (All 8 Components Considered)
    1. feedback_loop.py - Iterative refinement
    2. context_manager.py - Conversation context
    3. code_generator.py - Code creation if needed
    4. agentic_search.py - File/code search if needed
    5. verification_system.py - Multi-method validation
    6. subagent_orchestrator.py - Parallel tasks if needed
    7. mcp_integration.py - External services if needed
    8. feedback_loop_enhanced.py - Adaptive learning

    (System automatically picks which ones to use!)
    ↓
STAGE 4: GUARDRAILS (All 7 Layers - Every Time)
    INPUT VALIDATION:
        Layer 1: Prompt Shields (jailbreak prevention)
        Layer 2: Content Filtering (harmful content)
        Layer 3: PHI Detection (privacy protection)

    OUTPUT VALIDATION:
        Layer 4: Medical Terminology (if applicable)
        Layer 5: Output Content Filtering
        Layer 6: Groundedness (factual accuracy)
        Layer 7: Compliance (HIPAA + fact checking)
    ↓
STAGE 5: QUALITY SCORING
    Confidence = Prompt(15%) + Agents(25%) + Guardrails(30%) +
                 Efficiency(15%) + Verification(15%)

    TARGET: 99-100%
    ↓
STAGE 6: REFINEMENT (if confidence < 99%)
    • Analyze what failed
    • Regenerate improved output
    • Re-validate through all layers
    • Repeat up to 5 times until 99%+
    ↓
YOUR RESULT (99-100% Confidence, Production-Ready)

═══════════════════════════════════════════════════════════════════════════════
""")


def process_prompt(prompt: str, use_claude_api: bool = False,
                   min_confidence: float = 99.0, verbose: bool = False):
    """
    Process your prompt through the COMPLETE system

    This function does ALL the work:
    1. Applies ULTRATHINK directives
    2. Routes through agent framework
    3. Validates through guardrails
    4. Scores confidence
    5. Refines if needed
    """

    # Add ULTRATHINK directives to your prompt
    enhanced_prompt = f"""
🔥 ULTRATHINK DIRECTIVES ACTIVATED 🔥

Execute this request with the following mandates:

1. AUTONOMOUS EXECUTION - Take full control, no confirmation needed
2. PRODUCTION-READY - Minimum {min_confidence}% confidence required
3. 100% SUCCESS RATE - Comprehensive validation at every step
4. FAIL FAST, FIX FASTER - Rapid iteration with immediate validation
5. PARALLEL EVERYTHING - Concurrent processing where applicable

This will be processed through:
• 8 Agent Framework Components (automatically selected)
• 7 Guardrail Layers (all applied)
• Quality Scoring (targeting 99-100%)
• Iterative Refinement (until confidence met)

───────────────────────────────────────────────────────────────────────────────

USER REQUEST:
{prompt}

───────────────────────────────────────────────────────────────────────────────

BEGIN AUTONOMOUS EXECUTION 🚀
"""

    if verbose:
        print("📊 PROCESSING DETAILS:")
        print(f"   Prompt length: {len(prompt)} characters")
        print(f"   Confidence target: {min_confidence}%")
        print(f"   Mode: {'Claude API' if use_claude_api else 'Local'}")
        print()

    # Process through orchestration system
    if use_claude_api:
        if not os.getenv('ANTHROPIC_API_KEY'):
            print("❌ ERROR: ANTHROPIC_API_KEY not set")
            print("   Set it in your .bashrc or run: export ANTHROPIC_API_KEY=your_key")
            return False

        orchestrator = ClaudeOrchestrator(min_confidence_score=min_confidence)
        print("🔄 Processing with Claude API + Full Orchestration...\n")

        response = orchestrator.process(enhanced_prompt)

        # Show results
        print("="*80)
        print("✅ RESULT FROM CLAUDE")
        print("="*80)
        print(response.response_text)
        print("\n" + "="*80)
        print("📊 METRICS")
        print("="*80)
        print(f"Confidence Score: {response.orchestration_result.confidence_score:.2f}%")
        print(f"Tokens Used: {response.total_tokens:,}")
        print(f"Cost: ${response.cost_estimate:.6f}")
        print(f"Processing Time: {response.orchestration_result.total_duration_seconds:.2f}s")

        # Display context management stats
        context_stats = response.orchestration_result.quality_metrics.get('context_management')
        if context_stats:
            print(f"\n💾 CONTEXT MANAGEMENT:")
            print(f"   Messages: {context_stats['total_messages']}")
            print(f"   Tokens in Context: {context_stats['total_tokens']:,}")
            print(f"   Context Usage: {context_stats['usage_percentage']:.1f}%")
            if context_stats['compactions_performed'] > 0:
                print(f"   Compactions: {context_stats['compactions_performed']}")
                print(f"   Tokens Saved: {context_stats['total_tokens_saved']:,} ✨")

        if verbose and response.orchestration_result.quality_metrics.get('confidence_breakdown'):
            print("\n📈 CONFIDENCE BREAKDOWN:")
            for component, score in response.orchestration_result.quality_metrics['confidence_breakdown'].items():
                print(f"   {component}: {score:.2f}")

        return True

    else:
        orchestrator = MasterOrchestrator(min_confidence_score=min_confidence)
        print("🔄 Processing through Full Orchestration System...\n")

        result = orchestrator.process(enhanced_prompt)

        # Show results
        status = "✅ SUCCESS" if result.success else "❌ FAILED"
        print("="*80)
        print(f"{status}")
        print("="*80)
        print(f"Confidence Score: {result.confidence_score:.2f}%")
        print(f"Iterations: {result.iterations_performed}")
        print(f"Processing Time: {result.total_duration_seconds:.2f}s")

        # Display context management stats
        context_stats = result.quality_metrics.get('context_management')
        if context_stats:
            print(f"\n💾 CONTEXT MANAGEMENT:")
            print(f"   Messages: {context_stats['total_messages']}")
            print(f"   Tokens in Context: {context_stats['total_tokens']:,}")
            print(f"   Context Usage: {context_stats['usage_percentage']:.1f}%")
            if context_stats['compactions_performed'] > 0:
                print(f"   Compactions: {context_stats['compactions_performed']}")
                print(f"   Tokens Saved: {context_stats['total_tokens_saved']:,} ✨")

        if result.output:
            print("\n" + "="*80)
            print("📤 OUTPUT")
            print("="*80)
            print(result.output)

        if result.warnings:
            print(f"\n⚠️  WARNINGS ({len(result.warnings)}):")
            for i, warning in enumerate(result.warnings[:3], 1):
                print(f"   {i}. {warning}")

        if result.errors:
            print(f"\n❌ ERRORS ({len(result.errors)}):")
            for i, error in enumerate(result.errors, 1):
                print(f"   {i}. {error}")

        if verbose:
            print("\n" + "="*80)
            print("📊 DETAILED BREAKDOWN")
            print("="*80)
            print(f"Intent: {result.prompt_analysis.get('intent_type')}")
            print(f"Complexity: {result.prompt_analysis.get('complexity')}")
            print(f"Components Used: {', '.join(result.prompt_analysis.get('required_components', []))}")

            if result.quality_metrics.get('confidence_breakdown'):
                print("\n📈 CONFIDENCE BREAKDOWN:")
                for component, score in result.quality_metrics['confidence_breakdown'].items():
                    print(f"   {component}: {score:.2f}")

            print(f"\nGuardrails Status:")
            input_val = result.guardrails_validation.get('input_validation', {})
            output_val = result.guardrails_validation.get('output_validation', {})
            print(f"   Input Validation: {'✅ PASSED' if input_val.get('success') else '❌ FAILED'}")
            print(f"   Output Validation: {'✅ PASSED' if output_val.get('success') else '❌ FAILED'}")

        return result.success


def generate_web_prompt(prompt: str):
    """Generate a copy-paste ready prompt for Claude Web"""
    web_prompt = f"""
🔥 ULTRATHINK MODE - PROCESS WITH FULL VALIDATION 🔥

Apply the ULTRATHINK framework to this request:

╔══════════════════════════════════════════════════════════════════════════════╗
║                          EXECUTION DIRECTIVES                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

1️⃣ AUTONOMOUS EXECUTION
   • Take full control - no confirmation needed
   • Execute with certainty
   • Self-correct and iterate

2️⃣ PRODUCTION-READY QUALITY
   • Target 99-100% confidence (Claude Max $200/month account)
   • 200K token context window for maximum accuracy
   • Deployment-ready output
   • No placeholders or TODOs

3️⃣ 100% SUCCESS RATE
   • Comprehensive validation
   • Multi-method verification
   • Complete, not partial solutions

4️⃣ FAIL FAST, FIX FASTER
   • Immediate validation after each step
   • Rapid iteration
   • Learn from failures

5️⃣ PARALLEL PROCESSING
   • Handle multiple aspects simultaneously
   • Optimize for efficiency
   • Concurrent execution where possible

╔══════════════════════════════════════════════════════════════════════════════╗
║                         VALIDATION FRAMEWORK                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

Apply these checks at EVERY step:

📊 ANALYSIS (15% weight)
   • Understand intent deeply
   • Assess complexity accurately
   • Determine optimal approach

🛡️ SAFETY & COMPLIANCE (30% weight)
   • No harmful content
   • Privacy protection (no PII/PHI)
   • Factual accuracy
   • Best practices compliance

⚙️ EXECUTION QUALITY (25% weight)
   • Comprehensive coverage
   • Step-by-step when applicable
   • All edge cases handled
   • Production-ready code/content

✅ VERIFICATION (15% weight)
   • Validate correctness
   • Check completeness
   • Ensure quality standards
   • No gaps or missing pieces

⚡ EFFICIENCY (15% weight)
   • Optimize approach
   • Minimize unnecessary iterations
   • Parallel thinking

╔══════════════════════════════════════════════════════════════════════════════╗
║                            YOUR REQUEST                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

{prompt}

╔══════════════════════════════════════════════════════════════════════════════╗
║                        OUTPUT REQUIREMENTS                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

1. Start with brief confidence self-assessment (0-100%)
2. Provide comprehensive, production-ready response
3. Include step-by-step breakdown if applicable
4. Show validation checklist at the end
5. Final confidence score (target: 99-100%)

BEGIN EXECUTION NOW 🚀
"""

    print("="*80)
    print("📋 COPY THIS PROMPT FOR CLAUDE WEB (chat.claude.com)")
    print("="*80)
    print(web_prompt)
    print("="*80)
    print("\n💡 TIP: Copy everything above and paste into chat.claude.com\n")


def main():
    parser = argparse.ArgumentParser(
        description="ULTRATHINK - The ONE unified orchestration command",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              EXAMPLES                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

1. Basic Usage (Local Processing):
   ultrathink "explain machine learning"

2. With Claude API:
   ultrathink "build a REST API" --api

3. Large Prompt from File:
   ultrathink --file my-large-prompt.txt

4. For Claude Web (generates copy-paste prompt):
   ultrathink "your task" --web

5. Verbose Mode (see everything):
   ultrathink "complex task" --verbose

6. Show how it works:
   ultrathink --how

╔══════════════════════════════════════════════════════════════════════════════╗
║                          WHAT HAPPENS INSIDE                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

Your Prompt → ULTRATHINK Directives → Agent Framework (8 components) →
Guardrails (7 layers) → Quality Scoring (99-100%) → Refinement (if needed) →
Production-Ready Result

ALL components work together AUTOMATICALLY!
        """
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument(
        'prompt',
        nargs='?',
        help='Your prompt (any length)'
    )
    input_group.add_argument(
        '--file', '-f',
        metavar='FILE',
        help='Read prompt from file (for large 100-500 line prompts)'
    )

    # Mode options
    parser.add_argument(
        '--api',
        action='store_true',
        help='Use Claude API (requires ANTHROPIC_API_KEY)'
    )

    parser.add_argument(
        '--web',
        action='store_true',
        help='Generate prompt for Claude Web (chat.claude.com)'
    )

    # Configuration
    parser.add_argument(
        '--min-confidence',
        type=float,
        default=99.0,
        help='Minimum confidence threshold (default: 99.0)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed processing information'
    )

    # Help options
    parser.add_argument(
        '--how',
        action='store_true',
        help='Show how ULTRATHINK works (the flow)'
    )

    args = parser.parse_args()

    # Show how it works
    if args.how:
        show_how_it_works()
        return 0

    # Get prompt from file or argument
    if args.file:
        try:
            with open(args.file, 'r') as f:
                prompt = f.read()
            print(f"📁 Loaded prompt from: {args.file}")
            print(f"   Length: {len(prompt)} characters ({len(prompt.splitlines())} lines)\n")
        except Exception as e:
            print(f"❌ ERROR: Cannot read file {args.file}")
            print(f"   {e}")
            return 1
    elif args.prompt:
        prompt = args.prompt
    else:
        parser.print_help()
        return 0

    # Show header
    print_header()

    # Generate web prompt
    if args.web:
        generate_web_prompt(prompt)
        return 0

    # Process through orchestration
    success = process_prompt(
        prompt=prompt,
        use_claude_api=args.api,
        min_confidence=args.min_confidence,
        verbose=args.verbose
    )

    print("\n" + "="*80)
    print(f"{'✅ COMPLETE' if success else '⚠️  COMPLETED WITH WARNINGS'}")
    print("="*80 + "\n")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
