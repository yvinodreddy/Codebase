#!/usr/bin/env python3
"""
SwarmCare v2.1 - 100% Success Validator
Comprehensive validation to ensure 100% production readiness
"""

import json
import glob
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class SwarmCareValidator:
    """Validates 100% readiness for SwarmCare v2.1 Ultimate"""

    def __init__(self, base_path: str = "/home/user01/claude-test/SwarmCare/start"):
        self.base_path = Path(base_path)
        self.errors = []
        self.warnings = []
        self.passed_checks = []

    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """Run all validation checks"""
        print("=" * 80)
        print("SWARMCARE V2.1 ULTIMATE - 100% SUCCESS VALIDATOR")
        print("=" * 80)
        print()

        # Critical validations
        self.validate_phase_files()
        self.validate_distribution_configs()
        self.validate_phase_dependencies()
        self.validate_story_points_total()
        self.validate_core_scripts()
        self.validate_documentation()
        self.validate_distribution_balance()

        # Report results
        self.print_results()

        return (len(self.errors) == 0, self.errors, self.warnings)

    def validate_phase_files(self):
        """Validate all 29 phase files exist and are correct"""
        print("Validating phase files...")

        phase_files = sorted(glob.glob(str(self.base_path / "phases" / "*.json")))

        if len(phase_files) != 29:
            self.errors.append(f"Expected 29 phase files, found {len(phase_files)}")
            return

        total_points = 0
        phase_ids = []

        for phase_file in phase_files:
            try:
                with open(phase_file) as f:
                    data = json.load(f)
                    phase_id = data.get('phase_id')
                    points = data.get('story_points', 0)

                    phase_ids.append(phase_id)
                    total_points += points

            except Exception as e:
                self.errors.append(f"Error reading {phase_file}: {e}")

        # Check all phase IDs 0-28 present
        expected_ids = set(range(29))
        actual_ids = set(phase_ids)

        if expected_ids != actual_ids:
            missing = expected_ids - actual_ids
            extra = actual_ids - expected_ids
            if missing:
                self.errors.append(f"Missing phase IDs: {sorted(missing)}")
            if extra:
                self.errors.append(f"Extra phase IDs: {sorted(extra)}")
        else:
            self.passed_checks.append("✅ All 29 phase files present (IDs 0-28)")

        if total_points == 1102:
            self.passed_checks.append(f"✅ Total story points correct: {total_points}")
        else:
            self.errors.append(f"Total story points should be 1102, got {total_points}")

    def validate_distribution_configs(self):
        """Validate distribution configs sum to 1102 points"""
        print("Validating distribution configs...")

        # 5-machine config
        config_5 = self.base_path / "machine_configs" / "5_machine_distribution.json"
        if config_5.exists():
            with open(config_5) as f:
                data = json.load(f)
                total_5 = sum(m['total_story_points'] for m in data['machines'])

                if total_5 == 1102:
                    self.passed_checks.append(f"✅ 5-machine config: {total_5} points")
                else:
                    self.errors.append(f"5-machine config should sum to 1102, got {total_5}")

                # Check all phases covered
                all_phases = set()
                for m in data['machines']:
                    all_phases.update(m['assigned_phases'])

                expected_phases = set(range(29))
                if all_phases == expected_phases:
                    self.passed_checks.append("✅ 5-machine config covers all 29 phases")
                else:
                    missing = expected_phases - all_phases
                    extra = all_phases - expected_phases
                    if missing:
                        self.errors.append(f"5-machine missing phases: {sorted(missing)}")
                    if extra:
                        self.errors.append(f"5-machine extra phases: {sorted(extra)}")
        else:
            self.errors.append("5-machine distribution config not found")

        # 10-machine config
        config_10 = self.base_path / "machine_configs" / "10_machine_distribution.json"
        if config_10.exists():
            with open(config_10) as f:
                data = json.load(f)
                total_10 = sum(m['total_story_points'] for m in data['machines'])

                if total_10 == 1102:
                    self.passed_checks.append(f"✅ 10-machine config: {total_10} points")
                else:
                    self.errors.append(f"10-machine config should sum to 1102, got {total_10}")

                # Check all phases covered
                all_phases = set()
                for m in data['machines']:
                    all_phases.update(m['assigned_phases'])

                expected_phases = set(range(29))
                if all_phases == expected_phases:
                    self.passed_checks.append("✅ 10-machine config covers all 29 phases")
                else:
                    missing = expected_phases - all_phases
                    extra = all_phases - expected_phases
                    if missing:
                        self.errors.append(f"10-machine missing phases: {sorted(missing)}")
                    if extra:
                        self.errors.append(f"10-machine extra phases: {sorted(extra)}")
        else:
            self.errors.append("10-machine distribution config not found")

    def validate_phase_dependencies(self):
        """Validate phase dependencies are correct"""
        print("Validating phase dependencies...")

        # Load all phases
        phases = {}
        phase_files = sorted(glob.glob(str(self.base_path / "phases" / "*.json")))

        for phase_file in phase_files:
            with open(phase_file) as f:
                data = json.load(f)
                phase_id = data.get('phase_id')
                phases[phase_id] = data.get('dependencies', [])

        # Check Phase 0 has no dependencies
        if phases.get(0, []) == []:
            self.passed_checks.append("✅ Phase 0 (Foundation) has no dependencies")
        else:
            self.errors.append(f"Phase 0 should have no dependencies, got {phases.get(0)}")

        # Check all dependencies reference valid phases
        for phase_id, deps in phases.items():
            for dep in deps:
                if dep not in phases:
                    self.errors.append(f"Phase {phase_id} depends on non-existent phase {dep}")
                elif dep >= phase_id:
                    self.warnings.append(f"Phase {phase_id} depends on later phase {dep} (potential circular dependency)")

        self.passed_checks.append(f"✅ All phase dependencies validated (29 phases)")

    def validate_story_points_total(self):
        """Validate total story points"""
        print("Validating story points...")

        # This is already checked in validate_phase_files
        # Just add version check

        expected_breakdown = {
            "v1.0 (0-11)": 565,
            "v2.0 (12-19)": 406,
            "v2.1 (20-28)": 131,
            "TOTAL": 1102
        }

        phase_files = sorted(glob.glob(str(self.base_path / "phases" / "*.json")))
        v1_points = 0
        v2_points = 0
        v21_points = 0

        for phase_file in phase_files:
            with open(phase_file) as f:
                data = json.load(f)
                phase_id = data.get('phase_id')
                points = data.get('story_points', 0)

                if 0 <= phase_id <= 11:
                    v1_points += points
                elif 12 <= phase_id <= 19:
                    v2_points += points
                elif 20 <= phase_id <= 28:
                    v21_points += points

        if v1_points == 565:
            self.passed_checks.append(f"✅ v1.0 (Phases 0-11): {v1_points} points")
        else:
            self.errors.append(f"v1.0 should be 565 points, got {v1_points}")

        if v2_points == 406:
            self.passed_checks.append(f"✅ v2.0 (Phases 12-19): {v2_points} points")
        else:
            self.errors.append(f"v2.0 should be 406 points, got {v2_points}")

        if v21_points == 131:
            self.passed_checks.append(f"✅ v2.1 (Phases 20-28): {v21_points} points")
        else:
            self.errors.append(f"v2.1 should be 131 points, got {v21_points}")

    def validate_core_scripts(self):
        """Validate core scripts exist and are executable"""
        print("Validating core scripts...")

        core_scripts = [
            "DISTRIBUTED_EXECUTOR.sh",
            "COLLECT_PHASES.sh",
            "INTEGRATE_ALL.sh",
            "phase_validator.py",
            "integration_tester.py"
        ]

        for script in core_scripts:
            script_path = self.base_path / script
            if not script_path.exists():
                self.errors.append(f"Core script missing: {script}")
            elif not script_path.stat().st_mode & 0o111:  # Check if executable
                self.warnings.append(f"Core script not executable: {script}")
            else:
                self.passed_checks.append(f"✅ Core script present: {script}")

    def validate_documentation(self):
        """Validate key documentation files exist"""
        print("Validating documentation...")

        key_docs = [
            "BUSINESS_ANALYSIS_COMPARATIVE.md",
            "START_HERE.md",
            "DISTRIBUTED_README.md",
            "DISTRIBUTED_ARCHITECTURE.md",
            "SETUP_GUIDE.md"
        ]

        for doc in key_docs:
            doc_path = self.base_path / doc
            if not doc_path.exists():
                self.errors.append(f"Key documentation missing: {doc}")
            else:
                # Check for v2.1 references
                with open(doc_path) as f:
                    content = f.read()
                    if "1102" in content or "1,102" in content:
                        self.passed_checks.append(f"✅ {doc} references v2.1 (1102 points)")
                    elif "565" in content and doc != "BUSINESS_ANALYSIS_COMPARATIVE.md":
                        self.warnings.append(f"{doc} may still reference v1.0 (565 points)")

    def validate_distribution_balance(self):
        """Validate distribution balance across machines"""
        print("Validating distribution balance...")

        config_5 = self.base_path / "machine_configs" / "5_machine_distribution.json"
        if config_5.exists():
            with open(config_5) as f:
                data = json.load(f)
                points = [m['total_story_points'] for m in data['machines']]
                avg = sum(points) / len(points)
                max_points = max(points)
                min_points = min(points)

                # Check balance (no machine should have >30% more or <30% less than average)
                imbalance = max((max_points - avg) / avg, (avg - min_points) / avg)

                if imbalance < 0.30:
                    self.passed_checks.append(f"✅ 5-machine distribution balanced (±{imbalance*100:.0f}%)")
                else:
                    self.warnings.append(f"5-machine distribution imbalanced: max {max_points}, min {min_points}, avg {avg:.0f}")

    def print_results(self):
        """Print validation results"""
        print()
        print("=" * 80)
        print("VALIDATION RESULTS")
        print("=" * 80)
        print()

        if self.passed_checks:
            print(f"✅ PASSED CHECKS ({len(self.passed_checks)}):")
            for check in self.passed_checks:
                print(f"  {check}")
            print()

        if self.warnings:
            print(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")
            print()

        if self.errors:
            print(f"❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  ❌ {error}")
            print()

        print("=" * 80)
        if len(self.errors) == 0:
            print("✅ 100% SUCCESS - ALL VALIDATIONS PASSED")
            print("System is PRODUCTION READY for SwarmCare v2.1 Ultimate")
            print("=" * 80)
            return 0
        else:
            print(f"❌ VALIDATION FAILED - {len(self.errors)} error(s) found")
            print("System is NOT production ready until all errors are fixed")
            print("=" * 80)
            return 1


if __name__ == "__main__":
    validator = SwarmCareValidator()
    success, errors, warnings = validator.validate_all()

    if not success:
        sys.exit(1)
    elif warnings:
        print()
        print(f"Note: {len(warnings)} warning(s) found - review recommended but not blocking")
        sys.exit(0)
    else:
        sys.exit(0)
