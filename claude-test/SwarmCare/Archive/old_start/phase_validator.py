#!/usr/bin/env python3
"""
SWARMCARE PHASE VALIDATOR
Validates phases for dependency satisfaction and integration readiness
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict

# Phase dependency graph
PHASE_DEPENDENCIES = {
    0: [],  # Foundation - no dependencies
    1: [0],  # RAG Heat - requires Foundation
    2: [0],  # SWARMCARE Agents - requires Foundation
    3: [1, 2],  # Workflows - requires RAG + Agents
    4: [0],  # Frontend - requires Foundation
    5: [],  # Audio - can run independently
    6: [0, 1, 2, 3, 4],  # HIPAA - requires most core features
    7: [0, 1, 2, 3, 4, 5, 6],  # Testing - requires all main phases
    8: [0, 1, 2, 3, 4, 5, 6, 7],  # Deployment - requires everything
    9: [],  # Documentation - can run independently
    10: [3],  # Business - requires Workflows
    11: [7],  # Research - requires Testing
    # Extended phases (12-28) - most can run after core
    12: [1, 2, 3],  # Real-time Clinical Decision Support
    13: [1, 2],  # Predictive Analytics
    14: [1, 2],  # Multi-modal AI
    15: [1, 2],  # Advanced Medical NLP
    16: [2, 12],  # Explainable AI
    17: [1, 2, 13],  # Population Health
    18: [1, 2],  # Clinical Trial Matching
    19: [2, 5],  # Voice AI
    20: [6],  # Security Certifications
    21: [12],  # Closed-loop Clinical Automation
    22: [13],  # Continuous Learning
    23: [14],  # FDA Clearance
    24: [15],  # Automated Coding
    25: [16],  # Patient-facing XAI
    26: [17],  # Public Health Integration
    27: [18],  # Trial Lifecycle
    28: [19],  # Ultra-fast Voice AI
}

class PhaseValidator:
    def __init__(self, collected_dir: str):
        self.collected_dir = Path(collected_dir)
        self.phases: Dict[int, Dict] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def load_phases(self) -> bool:
        """Load all phase manifests"""
        print(f"Loading phases from: {self.collected_dir}")

        if not self.collected_dir.exists():
            self.errors.append(f"Collected directory not found: {self.collected_dir}")
            return False

        for i in range(29):  # phase_00 to phase_28
            phase_name = f"phase_{i:02d}"
            phase_dir = self.collected_dir / phase_name
            manifest_file = phase_dir / "MANIFEST.json"

            if not phase_dir.exists():
                self.errors.append(f"Missing phase directory: {phase_name}")
                continue

            if not manifest_file.exists():
                self.errors.append(f"Missing manifest for {phase_name}")
                continue

            try:
                with open(manifest_file, 'r') as f:
                    manifest = json.load(f)
                    self.phases[i] = manifest
            except Exception as e:
                self.errors.append(f"Failed to load manifest for {phase_name}: {e}")

        print(f"Loaded {len(self.phases)} phases")
        return len(self.errors) == 0

    def validate_completeness(self) -> bool:
        """Check if all 29 phases are present"""
        print("\n=== Validating Completeness ===")

        missing = []
        for i in range(29):
            if i not in self.phases:
                missing.append(i)

        if missing:
            self.errors.append(f"Missing phases: {missing}")
            print(f"✗ Missing {len(missing)} phases: {missing}")
            return False

        print(f"✓ All 29 phases present")
        return True

    def validate_dependencies(self) -> bool:
        """Validate dependency graph is satisfied"""
        print("\n=== Validating Dependencies ===")

        available_phases = set(self.phases.keys())
        issues = []

        for phase_id, dependencies in PHASE_DEPENDENCIES.items():
            if phase_id not in available_phases:
                continue  # Already caught by completeness check

            missing_deps = [dep for dep in dependencies if dep not in available_phases]

            if missing_deps:
                issues.append(f"Phase {phase_id} missing dependencies: {missing_deps}")

        if issues:
            for issue in issues:
                self.errors.append(issue)
                print(f"✗ {issue}")
            return False

        print(f"✓ All dependencies satisfied")
        return True

    def validate_integration_readiness(self) -> bool:
        """Check if phases are marked ready for integration"""
        print("\n=== Validating Integration Readiness ===")

        not_ready = []

        for phase_id, manifest in self.phases.items():
            ready = manifest.get('ready_for_integration', False)
            if not ready:
                not_ready.append(phase_id)

        if not_ready:
            self.warnings.append(f"Phases not marked ready: {not_ready}")
            print(f"⚠ {len(not_ready)} phases not marked ready: {not_ready}")
            return False

        print(f"✓ All phases ready for integration")
        return True

    def validate_file_structure(self) -> bool:
        """Validate each phase has proper file structure"""
        print("\n=== Validating File Structure ===")

        issues = []

        for phase_id, manifest in self.phases.items():
            phase_name = f"phase_{phase_id:02d}"
            phase_dir = self.collected_dir / phase_name

            # Check for expected directories
            expected_dirs = ['backend', 'frontend', 'tests', 'docs']
            has_files = False

            for exp_dir in expected_dirs:
                dir_path = phase_dir / exp_dir
                if dir_path.exists():
                    file_count = len(list(dir_path.rglob('*.*')))
                    if file_count > 0:
                        has_files = True

            if not has_files:
                issues.append(f"Phase {phase_id} has no files in expected directories")

        if issues:
            for issue in issues:
                self.warnings.append(issue)
                print(f"⚠ {issue}")

        if not issues:
            print(f"✓ All phases have proper file structure")

        return True

    def check_conflicts(self) -> Tuple[bool, List[str]]:
        """Check for potential file conflicts between phases"""
        print("\n=== Checking for Conflicts ===")

        file_map = defaultdict(list)

        # Build map of files to phases
        for phase_id in self.phases.keys():
            phase_name = f"phase_{phase_id:02d}"
            phase_dir = self.collected_dir / phase_name

            for file_path in phase_dir.rglob('*.*'):
                if file_path.name in ['MANIFEST.json', 'PHASE_PROMPT.md']:
                    continue

                # Get relative path from phase_dir
                rel_path = file_path.relative_to(phase_dir)
                file_map[str(rel_path)].append(phase_id)

        # Find duplicates
        conflicts = []
        for file_path, phases in file_map.items():
            if len(phases) > 1:
                conflicts.append(f"{file_path} appears in phases: {phases}")

        if conflicts:
            print(f"⚠ Found {len(conflicts)} potential conflicts:")
            for conflict in conflicts[:10]:  # Show first 10
                print(f"  - {conflict}")
                self.warnings.append(conflict)
        else:
            print(f"✓ No file conflicts detected")

        return len(conflicts) == 0, conflicts

    def generate_report(self) -> Dict:
        """Generate validation report"""
        return {
            "timestamp": "2025-10-26T00:00:00Z",
            "total_phases": len(self.phases),
            "expected_phases": 29,
            "validation_passed": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "phases": list(self.phases.keys()),
        }

    def validate_all(self) -> bool:
        """Run all validations"""
        print("\n" + "="*60)
        print("SWARMCARE PHASE VALIDATION")
        print("="*60)

        if not self.load_phases():
            return False

        results = [
            self.validate_completeness(),
            self.validate_dependencies(),
            self.validate_integration_readiness(),
            self.validate_file_structure(),
        ]

        self.check_conflicts()

        # Summary
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        print(f"Phases Validated: {len(self.phases)}/29")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")

        if self.errors:
            print("\nERRORS:")
            for error in self.errors:
                print(f"  ✗ {error}")

        if self.warnings:
            print("\nWARNINGS:")
            for warning in self.warnings[:10]:  # Show first 10
                print(f"  ⚠ {warning}")

        passed = all(results) and len(self.errors) == 0

        print("\n" + "="*60)
        if passed:
            print("✓ VALIDATION PASSED - Ready for Integration")
        else:
            print("✗ VALIDATION FAILED - Fix errors before integration")
        print("="*60 + "\n")

        return passed


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 phase_validator.py <collected_phases_dir>")
        sys.exit(1)

    collected_dir = sys.argv[1]

    validator = PhaseValidator(collected_dir)
    success = validator.validate_all()

    # Write report
    report = validator.generate_report()
    report_file = Path(collected_dir).parent / "validation_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to: {report_file}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
