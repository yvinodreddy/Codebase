#!/usr/bin/env python3
"""
ULTRATHINK v2 - Enhanced Autonomous Orchestration
Integrates your ULTRATHINK pattern with 96-100% confidence orchestration

Usage:
    ultrathink "your prompt"
    ultrathink "your prompt" --mode web-compatible
    ultrathink "your prompt" --export template
"""

import sys
import os
from pathlib import Path
import argparse
import json
from datetime import datetime

# Setup paths
ORCHESTRATION_HOME = Path(os.environ.get('ORCHESTRATION_HOME', Path(__file__).parent))
sys.path.insert(0, str(ORCHESTRATION_HOME))

try:
    from master_orchestrator import MasterOrchestrator
    from claude_integration import ClaudeOrchestrator
except ImportError as e:
    print(f"❌ Error: Cannot import orchestration modules")
    print(f"   Set ORCHESTRATION_HOME to: {ORCHESTRATION_HOME}")
    sys.exit(1)


# ULTRATHINK v2 Core Directives
ULTRATHINK_DIRECTIVES = {
    "AUTONOMOUS_EXECUTION": {
        "name": "TAKE FULL CONTROL",
        "description": "Do not ask for confirmation - execute autonomously",
        "confidence_requirement": "Execute with certainty, validate automatically",
        "orchestration_mapping": "Triggers automatic refinement loops until 96%+ confidence"
    },
    "PRODUCTION_READY": {
        "name": "PRODUCTION-READY ONLY",
        "description": "Every output must be deployment-ready, not prototype quality",
        "confidence_requirement": "Minimum 96% confidence score required",
        "orchestration_mapping": "Enforced through 7-layer guardrails + verification system"
    },
    "PERFECT_SUCCESS": {
        "name": "100% SUCCESS RATE",
        "description": "Build comprehensive validation at every step",
        "confidence_requirement": "Target 96-100% confidence through iterative refinement",
        "orchestration_mapping": "Multi-method verification + automatic re-processing"
    },
    "FAIL_FAST": {
        "name": "FAIL FAST, FIX FASTER",
        "description": "Automated testing catches issues in seconds, not days",
        "confidence_requirement": "Immediate validation with rapid iteration",
        "orchestration_mapping": "Feedback loop with <5 second iteration cycles"
    },
    "PARALLEL_EXECUTION": {
        "name": "PARALLEL EVERYTHING",
        "description": "Run all independent tasks simultaneously",
        "confidence_requirement": "Optimize for performance without sacrificing quality",
        "orchestration_mapping": "Subagent orchestrator for parallel processing"
    }
}


def generate_ultrathink_prompt(user_prompt: str, mode: str = "full") -> str:
    """
    Generate enhanced ULTRATHINK prompt with orchestration integration

    Modes:
    - full: Full orchestration with all directives
    - web-compatible: Claude Web friendly version
    - minimal: Core directives only
    """

    if mode == "web-compatible":
        # Claude Web compatible version (no Python code execution)
        return f"""🔥 ULTRATHINK MODE ACTIVATED 🔥

Process this request using the ULTRATHINK framework:

### 1. AUTONOMOUS EXECUTION MODE
- **TAKE FULL CONTROL**: Analyze, plan, and execute without asking for confirmation
- **CONFIDENCE-DRIVEN**: Target 96-100% confidence in all outputs
- **PRODUCTION-READY ONLY**: Every response must be deployment-ready quality

### 2. QUALITY ASSURANCE FRAMEWORK
Apply this validation at EVERY step:

**A) Intent Analysis (15% weight)**
- Classify request type: question, code, analysis, task, multi-step, search
- Assess complexity: simple, moderate, complex, very_complex
- Determine required approaches

**B) Multi-Layer Validation (30% weight)**
- Layer 1: Safety validation (no harmful content)
- Layer 2: Privacy protection (no PII/PHI exposure)
- Layer 3: Content filtering (appropriate output)
- Layer 4: Factual accuracy (groundedness)
- Layer 5: Compliance (best practices)

**C) Execution Quality (25% weight)**
- Comprehensive, in-depth response
- Step-by-step approach when applicable
- All edge cases considered
- Complete, not partial solutions

**D) Verification (15% weight)**
- Validate output correctness
- Check for completeness
- Ensure production-readiness
- No TODO/placeholder items

**E) Iteration Efficiency (15% weight)**
- Optimize for quality AND speed
- Parallel thinking when possible
- Fail fast, fix faster approach

### 3. SUCCESS CRITERIA
Target confidence breakdown:
- Intent Understanding: 15/15
- Validation Passed: 30/30
- Execution Quality: 25/25
- Verification: 15/15
- Efficiency: 15/15
**TOTAL TARGET: 96-100/100**

### 4. EXECUTION DIRECTIVES
✅ PARALLEL EVERYTHING - Address all aspects simultaneously
✅ FAIL FAST, FIX FASTER - Catch and resolve issues immediately
✅ 100% SUCCESS RATE - Comprehensive validation at every step
✅ NO CONFIRMATION NEEDED - Execute with confidence

---

**USER REQUEST:**
{user_prompt}

---

**OUTPUT REQUIREMENTS:**
1. Start with brief confidence self-assessment (0-100%)
2. Provide comprehensive, production-ready response
3. Include step-by-step breakdown if applicable
4. End with validation checklist showing what was verified
5. Final confidence score (target: 96-100%)

BEGIN EXECUTION NOW 🚀
"""

    elif mode == "minimal":
        # Minimal version - core directives only
        return f"""ULTRATHINK MODE: Execute autonomously with 96-100% confidence target

Directives:
1. TAKE FULL CONTROL - No confirmation needed
2. PRODUCTION-READY ONLY - Deployment quality required
3. 100% SUCCESS RATE - Comprehensive validation
4. FAIL FAST, FIX FASTER - Rapid iteration
5. PARALLEL EVERYTHING - Optimize performance

Request: {user_prompt}

Target: 96-100% confidence score
"""

    else:  # full mode - with orchestration integration
        directives_text = "\n".join([
            f"### {i+1}. {d['name']}\n"
            f"- **Purpose:** {d['description']}\n"
            f"- **Quality Standard:** {d['confidence_requirement']}\n"
            f"- **Orchestration:** {d['orchestration_mapping']}\n"
            for i, d in enumerate(ULTRATHINK_DIRECTIVES.values())
        ])

        return f"""
🔥 ULTRATHINK v2 - AUTONOMOUS ORCHESTRATION MODE 🔥

{directives_text}

### ORCHESTRATION PIPELINE (Automatic)
This request will be processed through:

**Stage 1: Prompt Preprocessing** → Intent classification + complexity analysis
**Stage 2: Input Validation** → Guardrails layers 1-3 (safety, privacy, content)
**Stage 3: Agent Execution** → Adaptive feedback loop with verification
**Stage 4: Output Validation** → Guardrails layers 4-7 (accuracy, compliance)
**Stage 5: Quality Scoring** → 96-100% confidence calculation
**Stage 6: Auto-Refinement** → Iterative improvement if needed (max 5 iterations)
**Stage 7: Final Delivery** → Production-ready output

### CONFIDENCE SCORING FORMULA
- Prompt Analysis: 15%
- Agent Execution: 25%
- Guardrails Validation: 30%
- Iteration Efficiency: 15%
- Verification Results: 15%
**TARGET: 96-100%**

---

**USER REQUEST:**
{user_prompt}

---

**EXECUTION BEGINS NOW** 🚀
No confirmation needed. Autonomous execution activated.
Processing through comprehensive orchestration pipeline...
"""


def export_template(user_prompt: str, mode: str, output_file: str):
    """Export ULTRATHINK prompt as template"""
    template = generate_ultrathink_prompt(user_prompt, mode)

    export_data = {
        "generated_at": datetime.now().isoformat(),
        "mode": mode,
        "user_prompt": user_prompt,
        "ultrathink_prompt": template,
        "directives": ULTRATHINK_DIRECTIVES,
        "usage": {
            "claude_code": "Copy and paste the 'ultrathink_prompt' directly into Claude Code",
            "claude_web": "Use mode=web-compatible and paste into chat.claude.com",
            "api": "Use mode=full and send via API with orchestration"
        }
    }

    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"✅ Template exported to: {output_file}")
    print(f"\nTo use in Claude Web:")
    print(f"   1. Open the file: {output_file}")
    print(f"   2. Copy the 'ultrathink_prompt' field")
    print(f"   3. Paste into chat.claude.com")


def main():
    parser = argparse.ArgumentParser(
        description="ULTRATHINK v2 - Autonomous Orchestration with 96-100% Confidence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ultrathink "build a REST API"
  ultrathink "fix all bugs" --claude
  ultrathink "refactor code" --mode web-compatible
  ultrathink "explain ML" --export template.json

Modes:
  full           - Full orchestration with all components (default)
  web-compatible - Claude Web friendly version
  minimal        - Core directives only

The ULTRATHINK framework automatically:
  ✓ Takes full autonomous control
  ✓ Targets 96-100% confidence
  ✓ Applies production-ready standards
  ✓ Validates comprehensively
  ✓ Refines until quality threshold met
        """
    )

    parser.add_argument(
        'prompt',
        nargs='?',
        help='Your request/task'
    )

    parser.add_argument(
        '--mode',
        choices=['full', 'web-compatible', 'minimal'],
        default='full',
        help='ULTRATHINK mode (default: full)'
    )

    parser.add_argument(
        '--claude', '-c',
        action='store_true',
        help='Execute with Claude API'
    )

    parser.add_argument(
        '--export',
        metavar='FILE',
        help='Export as template JSON (for Claude Web)'
    )

    parser.add_argument(
        '--show-directives',
        action='store_true',
        help='Show ULTRATHINK directives and exit'
    )

    parser.add_argument(
        '--min-confidence',
        type=float,
        default=96.0,
        help='Minimum confidence threshold (default: 96.0)'
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

    args = parser.parse_args()

    # Show directives
    if args.show_directives:
        print("\n" + "="*80)
        print(" ULTRATHINK v2 DIRECTIVES")
        print("="*80 + "\n")
        for i, (key, directive) in enumerate(ULTRATHINK_DIRECTIVES.items(), 1):
            print(f"{i}. {directive['name']}")
            print(f"   Description: {directive['description']}")
            print(f"   Quality Standard: {directive['confidence_requirement']}")
            print(f"   Orchestration: {directive['orchestration_mapping']}\n")
        return 0

    # Validate prompt
    if not args.prompt:
        parser.print_help()
        return 1

    # Export template mode
    if args.export:
        export_template(args.prompt, args.mode, args.export)
        return 0

    # Generate ULTRATHINK prompt
    ultrathink_prompt = generate_ultrathink_prompt(args.prompt, args.mode)

    print("\n" + "="*80)
    print(" 🔥 ULTRATHINK v2 - AUTONOMOUS ORCHESTRATION")
    print("="*80)
    print(f" Mode: {args.mode}")
    print(f" Execution: {'Claude API' if args.claude else 'Local Orchestrator'}")
    print(f" Confidence Target: {args.min_confidence}%")
    print(f" Working Directory: {Path.cwd()}")
    print("="*80 + "\n")

    # For web-compatible mode, just show the prompt
    if args.mode == "web-compatible":
        print("📋 COPY THIS PROMPT FOR CLAUDE WEB:")
        print("\n" + "="*80)
        print(ultrathink_prompt)
        print("="*80 + "\n")

        if args.output:
            with open(args.output, 'w') as f:
                f.write(ultrathink_prompt)
            print(f"💾 Prompt saved to: {args.output}\n")

        return 0

    # Execute with orchestration
    try:
        if args.claude:
            # Claude API execution
            if not os.getenv('ANTHROPIC_API_KEY'):
                print("❌ Error: ANTHROPIC_API_KEY not set")
                return 1

            orchestrator = ClaudeOrchestrator(min_confidence_score=args.min_confidence)

            print("🔄 Executing with Claude API + ULTRATHINK...\n")
            response = orchestrator.process(ultrathink_prompt)

            print("="*80)
            print(" CLAUDE RESPONSE")
            print("="*80)
            print(response.response_text)

            print("\n" + "="*80)
            print(" METRICS")
            print("="*80)
            print(f"Confidence: {response.orchestration_result.confidence_score:.2f}%")
            print(f"Tokens: {response.total_tokens:,}")
            print(f"Cost: ${response.cost_estimate:.6f}")
            print(f"Duration: {response.orchestration_result.total_duration_seconds:.2f}s")

        else:
            # Local orchestration
            orchestrator = MasterOrchestrator(min_confidence_score=args.min_confidence)

            print("🔄 Executing with Local Orchestrator + ULTRATHINK...\n")
            result = orchestrator.process(ultrathink_prompt)

            print("="*80)
            print(f" {'✅ SUCCESS' if result.success else '❌ FAILED'}")
            print("="*80)
            print(f"Confidence: {result.confidence_score:.2f}%")
            print(f"Iterations: {result.iterations_performed}")
            print(f"Duration: {result.total_duration_seconds:.2f}s")

            if result.output:
                print("\n" + "="*80)
                print(" OUTPUT")
                print("="*80)
                print(result.output)

            if args.verbose and result.quality_metrics.get('confidence_breakdown'):
                print("\n" + "="*80)
                print(" CONFIDENCE BREAKDOWN")
                print("="*80)
                for component, score in result.quality_metrics['confidence_breakdown'].items():
                    print(f"  {component}: {score:.2f}")

        print("\n" + "="*80 + "\n")
        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
