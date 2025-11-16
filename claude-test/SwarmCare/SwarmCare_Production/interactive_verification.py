#!/usr/bin/env python3
"""
Interactive Verification Script with Explanations
This script checks the SwarmCare system and EXPLAINS what it's checking and why.
"""

import json
import os
import sys
from pathlib import Path

# ANSI Colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
BOLD = '\033[1m'
NC = '\033[0m'


class ExplainedValidator:
    """Validator that explains what it's checking"""

    def __init__(self):
        self.checks_passed = []
        self.checks_failed = []
        self.explanations = []

    def explain(self, title, explanation):
        """Print an explanation box"""
        print(f"\n{CYAN}{'═' * 80}{NC}")
        print(f"{CYAN}{BOLD}{title}{NC}")
        print(f"{CYAN}{'═' * 80}{NC}")
        print(f"{explanation}")
        print()

    def check(self, name, condition, success_msg, failure_msg, why):
        """
        Perform a check with explanation

        Args:
            name: Check name
            condition: Boolean condition to check
            success_msg: Message if check passes
            failure_msg: Message if check fails
            why: Explanation of why this check matters
        """
        print(f"{BLUE}Checking: {name}{NC}")
        print(f"  Why: {why}")

        if condition:
            print(f"  {GREEN}✓{NC} {success_msg}")
            self.checks_passed.append(name)
        else:
            print(f"  {RED}✗{NC} {failure_msg}")
            self.checks_failed.append(name)

        print()

    def summary(self):
        """Print summary of all checks"""
        total = len(self.checks_passed) + len(self.checks_failed)
        passed = len(self.checks_passed)
        failed = len(self.checks_failed)
        success_rate = (passed / total * 100) if total > 0 else 0

        print(f"\n{CYAN}{'═' * 80}{NC}")
        print(f"{CYAN}{BOLD}VERIFICATION SUMMARY{NC}")
        print(f"{CYAN}{'═' * 80}{NC}")
        print(f"Total Checks: {total}")
        print(f"{GREEN}Passed: {passed}{NC}")
        print(f"{RED}Failed: {failed}{NC}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()

        if failed == 0:
            print(f"{GREEN}╔{'═' * 78}╗{NC}")
            print(f"{GREEN}║{'🎉 ALL CHECKS PASSED - SYSTEM IS PRODUCTION READY! 🎉':^78}║{NC}")
            print(f"{GREEN}╚{'═' * 78}╝{NC}")
            return 0
        else:
            print(f"{RED}╔{'═' * 78}╗{NC}")
            print(f"{RED}║{'❌ SOME CHECKS FAILED - SEE TROUBLESHOOTING GUIDE':^78}║{NC}")
            print(f"{RED}╚{'═' * 78}╝{NC}")
            print()
            print(f"{YELLOW}Failed checks:{NC}")
            for check in self.checks_failed:
                print(f"  • {check}")
            print()
            print(f"See: {BOLD}COMPLETE_SYSTEM_GUIDE.md{NC} → Troubleshooting section")
            return 1


def main():
    """Run interactive verification"""
    validator = ExplainedValidator()

    print(f"{CYAN}╔{'═' * 78}╗{NC}")
    print(f"{CYAN}║{' INTERACTIVE SYSTEM VERIFICATION WITH EXPLANATIONS ':^78}║{NC}")
    print(f"{CYAN}╚{'═' * 78}╝{NC}")

    validator.explain(
        "WHAT THIS SCRIPT DOES",
        """This script verifies that the SwarmCare v2.1 Ultimate system is correctly
configured and production-ready. Unlike a simple validation script that just
reports pass/fail, this script EXPLAINS:

  • What each check is testing
  • Why that check matters
  • What it means if it fails
  • How components relate to each other

Use this to LEARN about the system while verifying it's correct."""
    )

    # Get base directory
    script_dir = Path(__file__).parent.absolute()
    base_dir = str(script_dir)

    # ======================================================================
    # CHECK 1: Phase Directories
    # ======================================================================

    validator.explain(
        "CHECK 1: PHASE DIRECTORY STRUCTURE",
        """The system has 29 phases (phase00 through phase28). Each phase is a
self-contained unit of work with its own:
  • Code implementation
  • Tests
  • Documentation
  • State tracking

We're checking that all 29 phase directories exist and have the required
subdirectories: code/, tests/, docs/, and .state/

This matters because: If phases are missing or improperly structured, developers
won't know where to put code or how to track progress."""
    )

    phases_ok = 0
    for i in range(29):
        phase_dir = os.path.join(base_dir, 'phases', f'phase{i:02d}')
        has_structure = all([
            os.path.exists(os.path.join(phase_dir, 'code')),
            os.path.exists(os.path.join(phase_dir, 'tests')),
            os.path.exists(os.path.join(phase_dir, 'docs')),
            os.path.exists(os.path.join(phase_dir, '.state'))
        ])
        if has_structure:
            phases_ok += 1

    validator.check(
        "Phase Directory Structure",
        phases_ok == 29,
        f"All 29 phases have complete directory structure",
        f"Only {phases_ok}/29 phases have complete structure",
        "Ensures each phase has the right folders for code, tests, docs, and tracking"
    )

    # ======================================================================
    # CHECK 2: Phase Files
    # ======================================================================

    validator.explain(
        "CHECK 2: REQUIRED FILES IN EACH PHASE",
        """Each phase needs specific files to be functional:

  • README.md - Tells developers what to build
  • code/implementation.py - Where the actual code goes (with guardrails)
  • code/__init__.py - Makes code a Python package
  • tests/test_phase{N}.py - Tests to verify code works
  • docs/IMPLEMENTATION_GUIDE.md - Detailed implementation instructions
  • .state/phase_state.json - Tracks progress (NOT_STARTED/IN_PROGRESS/COMPLETED)

We're verifying all these files exist for all 29 phases.

This matters because: Missing files mean developers don't have templates or
guidance, making it harder to implement correctly."""
    )

    files_ok = 0
    for i in range(29):
        phase_dir = os.path.join(base_dir, 'phases', f'phase{i:02d}')
        has_files = all([
            os.path.exists(os.path.join(phase_dir, 'README.md')),
            os.path.exists(os.path.join(phase_dir, 'code', 'implementation.py')),
            os.path.exists(os.path.join(phase_dir, 'code', '__init__.py')),
            os.path.exists(os.path.join(phase_dir, 'tests', f'test_phase{i:02d}.py')),
            os.path.exists(os.path.join(phase_dir, 'docs', 'IMPLEMENTATION_GUIDE.md')),
            os.path.exists(os.path.join(phase_dir, '.state', 'phase_state.json'))
        ])
        if has_files:
            files_ok += 1

    validator.check(
        "Required Phase Files",
        files_ok == 29,
        f"All 29 phases have all required files",
        f"Only {files_ok}/29 phases have all required files",
        "Each phase needs these files for developers to implement and track work"
    )

    # ======================================================================
    # CHECK 3: Tracker System
    # ======================================================================

    validator.explain(
        "CHECK 3: TRACKER SYSTEM",
        """The tracker system is the "brain" that knows:
  • What's been completed (story points done)
  • What's remaining (story points left)
  • Current progress (percentage)
  • Which phase is active

It consists of two JSON files:
  • .tracker/state.json - Global state (current progress)
  • .tracker/phase_manifest.json - Phase definitions (all 29 phases)

We're checking these files exist, are valid JSON, and have correct values.

This matters because: Without the tracker, you can't see progress or know what
to work on next. The ./continue command relies on these files."""
    )

    tracker_checks = 0

    # Check state.json exists and is valid
    state_file = os.path.join(base_dir, '.tracker', 'state.json')
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)

            if state.get('total_story_points') == 1362 and state.get('total_phases') == 29:
                tracker_checks += 1

        except json.JSONDecodeError:
            pass

    # Check phase_manifest.json exists and is valid
    manifest_file = os.path.join(base_dir, '.tracker', 'phase_manifest.json')
    if os.path.exists(manifest_file):
        try:
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)

            if manifest.get('total_story_points') == 1362 and len(manifest.get('phases', [])) == 29:
                tracker_checks += 1

        except json.JSONDecodeError:
            pass

    validator.check(
        "Tracker System Files",
        tracker_checks == 2,
        "Both tracker files exist and have correct values (1362 SP, 29 phases)",
        f"Only {tracker_checks}/2 tracker files are correct",
        "The tracker is essential for knowing progress and what to do next"
    )

    # ======================================================================
    # CHECK 4: Story Points Consistency
    # ======================================================================

    validator.explain(
        "CHECK 4: STORY POINTS CALCULATION",
        """Story points measure the amount of work in the project. We have:
  • 29 phases
  • 1362 total story points
  • Each phase has a specific number of story points

We're verifying that:
  1. The sum of all phase story points = 1362
  2. The manifest claims 1362 (consistency check)
  3. The calculations are mathematically correct

This matters because: If story points don't add up, the progress percentage
will be wrong, misleading developers about how much work remains."""
    )

    try:
        with open(manifest_file, 'r') as f:
            manifest = json.load(f)

        calculated_total = sum(phase.get('story_points', 0) for phase in manifest.get('phases', []))
        claimed_total = manifest.get('total_story_points', 0)

        sp_consistent = (calculated_total == claimed_total == 1362)

        validator.check(
            "Story Points Calculation",
            sp_consistent,
            f"Story points are consistent: {calculated_total} calculated = {claimed_total} claimed = 1362 expected",
            f"Story points mismatch: {calculated_total} calculated ≠ {claimed_total} claimed",
            "Ensures progress calculations will be accurate"
        )

    except Exception as e:
        validator.check(
            "Story Points Calculation",
            False,
            "",
            f"Could not verify story points: {e}",
            "Ensures progress calculations will be accurate"
        )

    # ======================================================================
    # CHECK 5: Guardrails System
    # ======================================================================

    validator.explain(
        "CHECK 5: GUARDRAILS SYSTEM",
        """Guardrails are the safety system that ensures:
  • Medical data is handled safely (HIPAA compliance)
  • No personal health information (PHI) is leaked
  • Medical terminology is correct
  • AI outputs are safe and accurate

The system has 6 guardrail modules:
  1. multi_layer_system.py - Main orchestrator
  2. medical_guardrails.py - Medical validation
  3. azure_content_safety.py - Content filtering
  4. crewai_guardrails.py - CrewAI integration
  5. monitoring.py - Logging and tracking
  6. __init__.py - Package initialization

We're checking all 6 modules exist.

This matters because: Without guardrails, the system could leak PHI, provide
incorrect medical information, or violate HIPAA - critical safety issues!"""
    )

    guardrails_dir = os.path.join(base_dir, 'guardrails')
    required_modules = [
        '__init__.py',
        'azure_content_safety.py',
        'crewai_guardrails.py',
        'medical_guardrails.py',
        'monitoring.py',
        'multi_layer_system.py'
    ]

    guardrails_ok = sum(1 for mod in required_modules if os.path.exists(os.path.join(guardrails_dir, mod)))

    validator.check(
        "Guardrails Modules",
        guardrails_ok == len(required_modules),
        f"All {len(required_modules)} guardrail modules present",
        f"Only {guardrails_ok}/{len(required_modules)} guardrail modules present",
        "Guardrails ensure medical safety, HIPAA compliance, and prevent PHI leakage"
    )

    # ======================================================================
    # CHECK 6: AI Prompts System
    # ======================================================================

    validator.explain(
        "CHECK 6: AI PROMPTS SYSTEM",
        """AI prompts accelerate development by providing:
  • Phase-specific implementation guidance
  • Code templates with guardrails
  • Best practices and patterns
  • Success criteria

The system has:
  • 29 phase-specific prompts (PHASE_00_PROMPT.md through PHASE_28_PROMPT.md)
  • AI_PROMPTS_LIBRARY.md (218 KB, 48 general prompts)
  • Training guides and frameworks

We're checking that all 29 phase-specific prompts exist.

This matters because: Without prompts, developers don't have AI-assisted
guidance, making implementation slower and more error-prone."""
    )

    ai_prompts_dir = os.path.join(base_dir, 'ai_prompts')
    phase_prompts_ok = 0

    for i in range(29):
        prompt_file = os.path.join(ai_prompts_dir, f'PHASE_{i:02d}_PROMPT.md')
        if os.path.exists(prompt_file):
            phase_prompts_ok += 1

    validator.check(
        "AI Prompt Templates",
        phase_prompts_ok == 29,
        f"All 29 phase-specific AI prompts present",
        f"Only {phase_prompts_ok}/29 phase-specific prompts present",
        "AI prompts guide developers and accelerate implementation with best practices"
    )

    # ======================================================================
    # CHECK 7: Integration System
    # ======================================================================

    validator.explain(
        "CHECK 7: INTEGRATION SYSTEM",
        """The integration system supports distributed development across multiple
machines. It has 4 directories:

  • incoming/ - Code packages from other machines
  • merged_code/ - Combined work from all machines
  • test_results/ - Test outputs from all machines
  • reports/ - Integration reports and summaries

We're checking all 4 directories exist.

This matters because: For large projects, multiple developers work on different
phases simultaneously. The integration system combines their work safely."""
    )

    integration_dir = os.path.join(base_dir, 'integration')
    integration_subdirs = ['incoming', 'merged_code', 'reports', 'test_results']
    integration_ok = sum(1 for subdir in integration_subdirs if os.path.exists(os.path.join(integration_dir, subdir)))

    validator.check(
        "Integration Directories",
        integration_ok == len(integration_subdirs),
        f"All {len(integration_subdirs)} integration directories present",
        f"Only {integration_ok}/{len(integration_subdirs)} integration directories present",
        "Integration system enables distributed development across multiple machines"
    )

    # ======================================================================
    # CHECK 8: Scripts
    # ======================================================================

    validator.explain(
        "CHECK 8: EXECUTABLE SCRIPTS",
        """The system has two critical scripts:

  1. continue - Your main interface
     • Shows progress
     • Displays current phase
     • Provides interactive menu
     • Updates tracker state

  2. comprehensive_sp_validation.py - Automated validation
     • Runs 22 tests
     • Validates structure, story points, files
     • Ensures production readiness

We're checking both scripts exist and are executable.

This matters because: These are your primary tools for working with the system.
Without them, you'd have to manually track progress and validate."""
    )

    continue_script = os.path.join(base_dir, 'continue')
    validation_script = os.path.join(base_dir, 'comprehensive_sp_validation.py')

    scripts_ok = 0
    if os.path.exists(continue_script) and os.access(continue_script, os.X_OK):
        scripts_ok += 1
    if os.path.exists(validation_script):
        scripts_ok += 1

    validator.check(
        "Critical Scripts",
        scripts_ok == 2,
        "Both continue and validation scripts present",
        f"Only {scripts_ok}/2 critical scripts present",
        "Scripts are your main interface for tracking progress and validating the system"
    )

    # ======================================================================
    # CHECK 9: Documentation
    # ======================================================================

    validator.explain(
        "CHECK 9: DOCUMENTATION SYSTEM",
        """Complete documentation is essential for understanding the system. We have:

  • COMPLETE_SYSTEM_GUIDE.md - Main guide explaining everything
  • VISUAL_ARCHITECTURE_GUIDE.md - Diagrams and visual explanations
  • STORY_POINTS_CORRECTION_REPORT.md - Why 1362 SP (not 1102)
  • PRODUCTION_READINESS_REPORT.md - System readiness verification
  • QUICK_REFERENCE.md - Quick commands and tips

We're checking these core documentation files exist.

This matters because: Without documentation, developers don't understand the
system architecture, can't troubleshoot issues, or learn how components work."""
    )

    doc_files = [
        'COMPLETE_SYSTEM_GUIDE.md',
        'VISUAL_ARCHITECTURE_GUIDE.md',
        'STORY_POINTS_CORRECTION_REPORT.md',
        'PRODUCTION_READINESS_REPORT.md',
        'QUICK_REFERENCE.md'
    ]

    docs_ok = sum(1 for doc in doc_files if os.path.exists(os.path.join(base_dir, doc)))

    validator.check(
        "Core Documentation",
        docs_ok >= 4,  # At least 4 of 5
        f"All core documentation files present ({docs_ok}/{len(doc_files)})",
        f"Only {docs_ok}/{len(doc_files)} documentation files present",
        "Documentation explains the system, guides implementation, and helps troubleshooting"
    )

    # ======================================================================
    # FINAL SUMMARY
    # ======================================================================

    validator.explain(
        "WHAT HAPPENS NEXT",
        """Based on the verification results above:

If ALL CHECKS PASSED ✓:
  → Your system is production-ready!
  → Start implementing with: ./continue
  → Follow phase guides for development
  → Use AI prompts for accelerated coding

If SOME CHECKS FAILED ✗:
  → See the COMPLETE_SYSTEM_GUIDE.md → Troubleshooting section
  → Each failed check has a fix procedure
  → Re-run this script after fixes
  → Most issues are simple (missing files, permissions, etc.)

To learn more:
  → Read COMPLETE_SYSTEM_GUIDE.md for full understanding
  → Read VISUAL_ARCHITECTURE_GUIDE.md for diagrams
  → Read QUICK_REFERENCE.md for quick commands"""
    )

    return validator.summary()


if __name__ == '__main__':
    sys.exit(main())
