#!/usr/bin/env python3
"""
Comprehensive Story Points Validation Script
Validates that all story points are correctly configured across the entire system
Version: 2.1
Date: 2025-10-27
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI Colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
NC = '\033[0m'

# Expected values
EXPECTED_TOTAL_SP = 1362
EXPECTED_PHASE_COUNT = 29
EXPECTED_PHASE_20_28_SP = 391  # Enhanced version

# Phase SP breakdown
EXPECTED_PHASE_SP = {
    0: 37, 1: 60, 2: 94, 3: 76, 4: 47, 5: 21, 6: 47, 7: 68, 8: 47, 9: 21,
    10: 26, 11: 21, 12: 55, 13: 62, 14: 76, 15: 47, 16: 34, 17: 43, 18: 38,
    19: 51, 20: 42, 21: 38, 22: 46, 23: 52, 24: 48, 25: 35, 26: 40, 27: 45,
    28: 45
}

class ValidationResult:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []

    def add_pass(self, test_name: str, details: str = ""):
        self.passed.append((test_name, details))

    def add_fail(self, test_name: str, details: str):
        self.failed.append((test_name, details))

    def add_warning(self, test_name: str, details: str):
        self.warnings.append((test_name, details))

    def is_success(self) -> bool:
        return len(self.failed) == 0


def print_header():
    print(f"{CYAN}╔{'═'*78}╗{NC}")
    print(f"{CYAN}║{'SWARMCARE v2.1 - COMPREHENSIVE STORY POINTS VALIDATION':^78}║{NC}")
    print(f"{CYAN}╚{'═'*78}╝{NC}")
    print()


def validate_phase_manifest(manifest_path: str, result: ValidationResult):
    """Validate phase_manifest.json"""
    print(f"{BLUE}[1/7] Validating phase_manifest.json...{NC}")

    if not os.path.exists(manifest_path):
        result.add_fail("Phase Manifest", f"File not found: {manifest_path}")
        return

    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Check version
        if manifest.get('version') == '2.1':
            result.add_pass("Manifest Version", "v2.1 ✓")
        else:
            result.add_fail("Manifest Version", f"Expected v2.1, got {manifest.get('version')}")

        # Check total phases
        if manifest.get('total_phases') == EXPECTED_PHASE_COUNT:
            result.add_pass("Total Phases", f"{EXPECTED_PHASE_COUNT} phases ✓")
        else:
            result.add_fail("Total Phases", f"Expected {EXPECTED_PHASE_COUNT}, got {manifest.get('total_phases')}")

        # Check total story points
        if manifest.get('total_story_points') == EXPECTED_TOTAL_SP:
            result.add_pass("Total Story Points", f"{EXPECTED_TOTAL_SP} SP ✓")
        else:
            result.add_fail("Total Story Points",
                          f"Expected {EXPECTED_TOTAL_SP} SP, got {manifest.get('total_story_points')} SP")

        # Validate individual phases
        phases = manifest.get('phases', [])
        if len(phases) == EXPECTED_PHASE_COUNT:
            result.add_pass("Phase Count", f"{len(phases)} phase definitions ✓")
        else:
            result.add_fail("Phase Count", f"Expected {EXPECTED_PHASE_COUNT} phases, got {len(phases)}")

        # Calculate actual total
        actual_total = sum(phase.get('story_points', 0) for phase in phases)
        if actual_total == EXPECTED_TOTAL_SP:
            result.add_pass("Calculated Total SP", f"{actual_total} SP matches manifest ✓")
        else:
            result.add_fail("Calculated Total SP",
                          f"Sum of phases ({actual_total} SP) doesn't match manifest ({manifest.get('total_story_points')} SP)")

        # Validate phase 20-28 (Enhanced version)
        phase_20_28_sp = sum(phase.get('story_points', 0) for phase in phases if 20 <= phase.get('phase_id', -1) <= 28)
        if phase_20_28_sp == EXPECTED_PHASE_20_28_SP:
            result.add_pass("Phase 20-28 SP", f"{phase_20_28_sp} SP (Enhanced) ✓")
        else:
            result.add_fail("Phase 20-28 SP",
                          f"Expected {EXPECTED_PHASE_20_28_SP} SP (Enhanced), got {phase_20_28_sp} SP")

        # Validate each phase SP value
        mismatches = []
        for phase in phases:
            phase_id = phase.get('phase_id')
            actual_sp = phase.get('story_points')
            expected_sp = EXPECTED_PHASE_SP.get(phase_id)

            if actual_sp != expected_sp:
                mismatches.append(f"Phase {phase_id}: expected {expected_sp} SP, got {actual_sp} SP")

        if mismatches:
            result.add_fail("Individual Phase SP", "; ".join(mismatches))
        else:
            result.add_pass("Individual Phase SP", "All 29 phases have correct SP values ✓")

    except json.JSONDecodeError as e:
        result.add_fail("Manifest JSON", f"Invalid JSON: {e}")
    except Exception as e:
        result.add_fail("Manifest Validation", f"Error: {e}")


def validate_state_json(state_path: str, result: ValidationResult):
    """Validate state.json"""
    print(f"{BLUE}[2/7] Validating state.json...{NC}")

    if not os.path.exists(state_path):
        result.add_fail("State File", f"File not found: {state_path}")
        return

    try:
        with open(state_path, 'r') as f:
            state = json.load(f)

        # Check version
        if state.get('version') == '2.1':
            result.add_pass("State Version", "v2.1 ✓")
        else:
            result.add_fail("State Version", f"Expected v2.1, got {state.get('version')}")

        # Check total_story_points
        if state.get('total_story_points') == EXPECTED_TOTAL_SP:
            result.add_pass("State Total SP", f"{EXPECTED_TOTAL_SP} SP ✓")
        else:
            result.add_fail("State Total SP",
                          f"Expected {EXPECTED_TOTAL_SP} SP, got {state.get('total_story_points')} SP")

        # Check total_phases
        if state.get('total_phases') == EXPECTED_PHASE_COUNT:
            result.add_pass("State Total Phases", f"{EXPECTED_PHASE_COUNT} phases ✓")
        else:
            result.add_fail("State Total Phases",
                          f"Expected {EXPECTED_PHASE_COUNT}, got {state.get('total_phases')}")

        # Validate story_points_remaining at initialization
        sp_completed = state.get('story_points_completed', 0)
        sp_remaining = state.get('story_points_remaining', 0)

        if sp_completed + sp_remaining == EXPECTED_TOTAL_SP:
            result.add_pass("SP Accounting", f"Completed ({sp_completed}) + Remaining ({sp_remaining}) = {EXPECTED_TOTAL_SP} ✓")
        else:
            total = sp_completed + sp_remaining
            result.add_fail("SP Accounting",
                          f"Completed ({sp_completed}) + Remaining ({sp_remaining}) = {total}, expected {EXPECTED_TOTAL_SP}")

    except json.JSONDecodeError as e:
        result.add_fail("State JSON", f"Invalid JSON: {e}")
    except Exception as e:
        result.add_fail("State Validation", f"Error: {e}")


def validate_continue_script(script_path: str, result: ValidationResult):
    """Validate continue script"""
    print(f"{BLUE}[3/7] Validating continue script...{NC}")

    if not os.path.exists(script_path):
        result.add_fail("Continue Script", f"File not found: {script_path}")
        return

    try:
        with open(script_path, 'r') as f:
            content = f.read()

        # Check for 1362 SP references
        sp_1362_count = content.count('1362')
        if sp_1362_count >= 4:  # Should appear at least 4 times
            result.add_pass("Continue Script SP", f"Found {sp_1362_count} references to 1362 SP ✓")
        else:
            result.add_fail("Continue Script SP", f"Expected at least 4 references to 1362 SP, found {sp_1362_count}")

        # Check for old 1102 references (should be gone)
        sp_1102_count = content.count('1102')
        if sp_1102_count == 0:
            result.add_pass("Continue Script (old refs)", "No 1102 SP references ✓")
        else:
            result.add_fail("Continue Script (old refs)", f"Found {sp_1102_count} outdated 1102 SP references")

        # Check for 29 phases reference
        if '29 phases' in content or '29 PHASES' in content:
            result.add_pass("Continue Script Phases", "29 phases reference found ✓")
        else:
            result.add_warning("Continue Script Phases", "Could not find '29 phases' reference")

    except Exception as e:
        result.add_fail("Continue Script Read", f"Error: {e}")


def validate_phase_directories(phases_dir: str, result: ValidationResult):
    """Validate phase directories"""
    print(f"{BLUE}[4/7] Validating phase directories...{NC}")

    if not os.path.exists(phases_dir):
        result.add_fail("Phases Directory", f"Directory not found: {phases_dir}")
        return

    try:
        phase_dirs = [d for d in os.listdir(phases_dir) if d.startswith('phase') and os.path.isdir(os.path.join(phases_dir, d))]
        phase_dirs.sort()

        if len(phase_dirs) == EXPECTED_PHASE_COUNT:
            result.add_pass("Phase Directories", f"{len(phase_dirs)} directories (phase00-phase28) ✓")
        else:
            result.add_fail("Phase Directories", f"Expected {EXPECTED_PHASE_COUNT} directories, found {len(phase_dirs)}")

        # Check for expected phase names
        expected_dirs = [f'phase{i:02d}' for i in range(EXPECTED_PHASE_COUNT)]
        missing = set(expected_dirs) - set(phase_dirs)
        extra = set(phase_dirs) - set(expected_dirs)

        if not missing and not extra:
            result.add_pass("Phase Directory Names", "All expected directories present ✓")
        else:
            if missing:
                result.add_fail("Missing Directories", f"Missing: {', '.join(missing)}")
            if extra:
                result.add_warning("Extra Directories", f"Extra: {', '.join(extra)}")

    except Exception as e:
        result.add_fail("Phase Directory Check", f"Error: {e}")


def validate_documentation(doc_path: str, result: ValidationResult):
    """Validate documentation"""
    print(f"{BLUE}[5/7] Validating documentation...{NC}")

    if not os.path.exists(doc_path):
        result.add_warning("Documentation", f"File not found: {doc_path}")
        return

    try:
        with open(doc_path, 'r') as f:
            content = f.read()

        # Check for 1362 SP references
        sp_1362_count = content.count('1362')
        if sp_1362_count >= 1:
            result.add_pass("Documentation SP", f"Found {sp_1362_count} references to 1362 SP ✓")
        else:
            result.add_fail("Documentation SP", "Expected at least 1 reference to 1362 SP")

        # Check for old 1102 references
        sp_1102_count = content.count('1102')
        if sp_1102_count == 0:
            result.add_pass("Documentation (old refs)", "No 1102 SP references ✓")
        else:
            result.add_fail("Documentation (old refs)", f"Found {sp_1102_count} outdated 1102 SP references")

        # Check for phase 20-28 enhanced references
        if '391' in content or 'Enhanced' in content:
            result.add_pass("Documentation Enhancement", "Enhanced version documented ✓")
        else:
            result.add_warning("Documentation Enhancement", "Enhanced version may not be documented")

    except Exception as e:
        result.add_fail("Documentation Read", f"Error: {e}")


def validate_ai_prompts_guardrails(base_dir: str, result: ValidationResult):
    """Validate AI prompts and guardrails"""
    print(f"{BLUE}[6/7] Validating AI prompts and guardrails...{NC}")

    ai_prompts_dir = os.path.join(base_dir, 'ai_prompts')
    guardrails_dir = os.path.join(base_dir, 'guardrails')

    # Check ai_prompts
    if os.path.exists(ai_prompts_dir):
        files = os.listdir(ai_prompts_dir)
        if len(files) >= 10:
            result.add_pass("AI Prompts", f"{len(files)} prompt files present ✓")
        else:
            result.add_warning("AI Prompts", f"Only {len(files)} files, expected more")
    else:
        result.add_fail("AI Prompts", "Directory not found")

    # Check guardrails
    if os.path.exists(guardrails_dir):
        py_files = [f for f in os.listdir(guardrails_dir) if f.endswith('.py')]
        if len(py_files) >= 5:
            result.add_pass("Guardrails", f"{len(py_files)} Python modules present ✓")
        else:
            result.add_warning("Guardrails", f"Only {len(py_files)} Python files")
    else:
        result.add_fail("Guardrails", "Directory not found")


def validate_integration_structure(base_dir: str, result: ValidationResult):
    """Validate integration directory structure"""
    print(f"{BLUE}[7/7] Validating integration structure...{NC}")

    integration_dir = os.path.join(base_dir, 'integration')

    if not os.path.exists(integration_dir):
        result.add_fail("Integration Dir", "Directory not found")
        return

    expected_subdirs = ['incoming', 'merged_code', 'reports', 'test_results']
    present = []
    missing = []

    for subdir in expected_subdirs:
        subdir_path = os.path.join(integration_dir, subdir)
        if os.path.exists(subdir_path):
            present.append(subdir)
        else:
            missing.append(subdir)

    if len(present) == len(expected_subdirs):
        result.add_pass("Integration Structure", f"All {len(present)} subdirectories present ✓")
    else:
        result.add_fail("Integration Structure", f"Missing: {', '.join(missing)}")


def print_results(result: ValidationResult):
    """Print validation results"""
    print()
    print(f"{CYAN}{'═'*80}{NC}")
    print(f"{CYAN}VALIDATION RESULTS{NC}")
    print(f"{CYAN}{'═'*80}{NC}")
    print()

    # Passed tests
    if result.passed:
        print(f"{GREEN}✅ PASSED ({len(result.passed)} tests):{NC}")
        for test, details in result.passed:
            print(f"  {GREEN}✓{NC} {test}: {details}" if details else f"  {GREEN}✓{NC} {test}")
        print()

    # Warnings
    if result.warnings:
        print(f"{YELLOW}⚠️  WARNINGS ({len(result.warnings)}):{NC}")
        for test, details in result.warnings:
            print(f"  {YELLOW}⚠{NC}  {test}: {details}")
        print()

    # Failed tests
    if result.failed:
        print(f"{RED}❌ FAILED ({len(result.failed)} tests):{NC}")
        for test, details in result.failed:
            print(f"  {RED}✗{NC} {test}: {details}")
        print()

    # Summary
    print(f"{CYAN}{'═'*80}{NC}")
    print(f"{CYAN}SUMMARY{NC}")
    print(f"{CYAN}{'═'*80}{NC}")
    total_tests = len(result.passed) + len(result.failed)
    success_rate = (len(result.passed) / total_tests * 100) if total_tests > 0 else 0

    print(f"Total Tests: {total_tests}")
    print(f"{GREEN}Passed: {len(result.passed)}{NC}")
    print(f"{RED}Failed: {len(result.failed)}{NC}")
    print(f"{YELLOW}Warnings: {len(result.warnings)}{NC}")
    print(f"Success Rate: {success_rate:.1f}%")
    print()

    if result.is_success():
        print(f"{GREEN}╔{'═'*78}╗{NC}")
        print(f"{GREEN}║{'🎉 ALL VALIDATIONS PASSED - 100% PRODUCTION READY! 🎉':^78}║{NC}")
        print(f"{GREEN}╚{'═'*78}╝{NC}")
        return 0
    else:
        print(f"{RED}╔{'═'*78}╗{NC}")
        print(f"{RED}║{'❌ VALIDATION FAILED - ISSUES NEED TO BE FIXED':^78}║{NC}")
        print(f"{RED}╚{'═'*78}╝{NC}")
        return 1


def main():
    # Determine base directory
    script_dir = Path(__file__).parent.absolute()
    base_dir = str(script_dir)

    print_header()
    print(f"Base Directory: {base_dir}")
    print()

    result = ValidationResult()

    # Run all validations
    validate_phase_manifest(os.path.join(base_dir, '.tracker', 'phase_manifest.json'), result)
    validate_state_json(os.path.join(base_dir, '.tracker', 'state.json'), result)
    validate_continue_script(os.path.join(base_dir, 'continue'), result)
    validate_phase_directories(os.path.join(base_dir, 'phases'), result)
    validate_documentation(os.path.join(base_dir, '..', 'CORRECTED_AND_COMPLETE.md'), result)
    validate_ai_prompts_guardrails(base_dir, result)
    validate_integration_structure(base_dir, result)

    # Print results
    exit_code = print_results(result)

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
