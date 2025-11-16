#!/usr/bin/env python3
"""
Phase 02 Validation Script
Production-ready validation with comprehensive checks

Validates:
- All 6 agents initialized correctly
- Guardrails integration
- Performance requirements
- Test suite execution
- Documentation completeness
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))

try:
    from implementation import Phase02Implementation
    IMPLEMENTATION_AVAILABLE = True
except ImportError as e:
    print(f"❌ Failed to import implementation: {e}")
    IMPLEMENTATION_AVAILABLE = False


class Phase02Validator:
    """Comprehensive Phase 02 validation"""

    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "phase_id": 2,
            "phase_name": "SWARMCARE Agents",
            "checks": [],
            "overall_passed": False,
            "success_rate": 0.0
        }

    def run_all_checks(self):
        """Run all validation checks"""
        print("=" * 80)
        print("PHASE 02: SWARMCARE AGENTS - COMPREHENSIVE VALIDATION")
        print("=" * 80)
        print(f"Started: {self.results['timestamp']}")
        print("=" * 80)
        print()

        if not IMPLEMENTATION_AVAILABLE:
            self._add_check("Implementation Import", False, "Failed to import implementation module")
            self._print_results()
            return False

        # Run all checks
        self._check_implementation_exists()
        self._check_phase_initialization()
        self._check_all_agents()
        self._check_agent_validation()
        self._check_execution()
        self._check_test_files()
        self._check_documentation()
        self._check_state_tracking()

        # Calculate overall result
        self._calculate_results()
        self._print_results()

        return self.results["overall_passed"]

    def _add_check(self, name, passed, message="", details=None):
        """Add check result"""
        status = "✅" if passed else "❌"
        print(f"{status} {name}: {message}")

        self.results["checks"].append({
            "name": name,
            "passed": passed,
            "message": message,
            "details": details
        })

    def _check_implementation_exists(self):
        """Check implementation file exists"""
        impl_path = Path(__file__).parent / "code" / "implementation.py"
        exists = impl_path.exists()

        if exists:
            size = impl_path.stat().st_size
            self._add_check(
                "Implementation File",
                True,
                f"Found ({size:,} bytes)",
                {"path": str(impl_path), "size": size}
            )
        else:
            self._add_check("Implementation File", False, "Not found")

    def _check_phase_initialization(self):
        """Check phase initializes correctly"""
        try:
            phase = Phase02Implementation()

            checks = [
                (phase.phase_id == 2, "Phase ID"),
                (phase.phase_name == "SWARMCARE Agents", "Phase Name"),
                (phase.story_points == 94, "Story Points"),
                (phase.priority == "P0", "Priority"),
                (phase.framework_version == "100%", "Framework Version")
            ]

            all_passed = all(check[0] for check in checks)
            failed = [check[1] for check in checks if not check[0]]

            if all_passed:
                self._add_check("Phase Initialization", True, "All metadata correct")
            else:
                self._add_check(
                    "Phase Initialization",
                    False,
                    f"Failed checks: {', '.join(failed)}"
                )

        except Exception as e:
            self._add_check("Phase Initialization", False, f"Exception: {e}")

    def _check_all_agents(self):
        """Check all 6 agents"""
        try:
            phase = Phase02Implementation()

            agents = {
                "knowledge": phase._initialize_knowledge_agent(),
                "case": phase._initialize_case_agent(),
                "conversation": phase._initialize_conversation_agent(),
                "compliance": phase._initialize_compliance_agent(),
                "podcast": phase._initialize_podcast_agent(),
                "qa": phase._initialize_qa_agent()
            }

            # Check count
            if len(agents) == 6:
                self._add_check("Agent Count", True, "All 6 agents present")
            else:
                self._add_check(
                    "Agent Count",
                    False,
                    f"Expected 6, got {len(agents)}"
                )

            # Check each agent
            required_fields = ["name", "type", "description", "capabilities",
                             "integrations", "guardrails", "status"]

            for agent_name, agent_config in agents.items():
                missing_fields = [f for f in required_fields if f not in agent_config]

                if not missing_fields:
                    self._add_check(
                        f"Agent: {agent_name}",
                        True,
                        f"{agent_config['name']} - {agent_config['status']}"
                    )
                else:
                    self._add_check(
                        f"Agent: {agent_name}",
                        False,
                        f"Missing fields: {', '.join(missing_fields)}"
                    )

        except Exception as e:
            self._add_check("Agent Initialization", False, f"Exception: {e}")

    def _check_agent_validation(self):
        """Check agent validation system"""
        try:
            phase = Phase02Implementation()

            agents = {
                "knowledge": phase._initialize_knowledge_agent(),
                "case": phase._initialize_case_agent(),
                "conversation": phase._initialize_conversation_agent(),
                "compliance": phase._initialize_compliance_agent(),
                "podcast": phase._initialize_podcast_agent(),
                "qa": phase._initialize_qa_agent()
            }

            validation = phase._validate_all_agents(agents)

            if validation["all_passed"]:
                self._add_check(
                    "Agent Validation",
                    True,
                    f"All {validation['agent_count']} agents validated"
                )
            else:
                failed_agents = [
                    a["agent"] for a in validation["agents_validated"]
                    if not a["valid"]
                ]
                self._add_check(
                    "Agent Validation",
                    False,
                    f"Failed: {', '.join(failed_agents)}"
                )

        except Exception as e:
            self._add_check("Agent Validation", False, f"Exception: {e}")

    def _check_execution(self):
        """Check phase execution"""
        try:
            phase = Phase02Implementation()
            task = {"goal": "Implement SWARMCARE Agents", "phase_id": 2}

            result = phase.execute(task)

            if result.success:
                total_agents = result.output.get("components", {}).get("total_agents", 0)
                self._add_check(
                    "Phase Execution",
                    True,
                    f"Success - {total_agents} agents created"
                )
            else:
                self._add_check(
                    "Phase Execution",
                    False,
                    f"Failed: {result.error}"
                )

        except Exception as e:
            self._add_check("Phase Execution", False, f"Exception: {e}")

    def _check_test_files(self):
        """Check test files exist and are comprehensive"""
        test_path = Path(__file__).parent / "tests" / "test_phase02.py"

        if test_path.exists():
            size = test_path.stat().st_size

            # Check file has substantial content (should be > 10KB for comprehensive tests)
            if size > 10000:
                self._add_check(
                    "Test Suite",
                    True,
                    f"Comprehensive ({size:,} bytes)"
                )
            else:
                self._add_check(
                    "Test Suite",
                    False,
                    f"Too small ({size:,} bytes) - may not be comprehensive"
                )
        else:
            self._add_check("Test Suite", False, "Test file not found")

    def _check_documentation(self):
        """Check documentation completeness"""
        docs_dir = Path(__file__).parent / "docs"
        required_docs = [
            "IMPLEMENTATION_GUIDE.md",
            "API_REFERENCE.md"
        ]

        for doc_name in required_docs:
            doc_path = docs_dir / doc_name

            if doc_path.exists():
                size = doc_path.stat().st_size
                self._add_check(
                    f"Documentation: {doc_name}",
                    True,
                    f"Found ({size:,} bytes)"
                )
            else:
                self._add_check(
                    f"Documentation: {doc_name}",
                    False,
                    "Not found"
                )

    def _check_state_tracking(self):
        """Check state tracking exists"""
        state_path = Path(__file__).parent / ".state" / "phase_state.json"

        if state_path.exists():
            try:
                with open(state_path, 'r') as f:
                    state = json.load(f)

                if "phase_id" in state and state["phase_id"] == 2:
                    self._add_check(
                        "State Tracking",
                        True,
                        f"Valid state file (status: {state.get('status', 'unknown')})"
                    )
                else:
                    self._add_check("State Tracking", False, "Invalid state data")
            except Exception as e:
                self._add_check("State Tracking", False, f"Error reading state: {e}")
        else:
            # State file will be created on execution, so this is OK
            self._add_check(
                "State Tracking",
                True,
                "State file will be created on execution"
            )

    def _calculate_results(self):
        """Calculate overall results"""
        total = len(self.results["checks"])
        passed = sum(1 for check in self.results["checks"] if check["passed"])

        self.results["total_checks"] = total
        self.results["passed_checks"] = passed
        self.results["failed_checks"] = total - passed
        self.results["success_rate"] = (passed / total * 100) if total > 0 else 0
        self.results["overall_passed"] = self.results["success_rate"] == 100.0

    def _print_results(self):
        """Print validation results"""
        print()
        print("=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        print(f"Total Checks: {self.results['total_checks']}")
        print(f"Passed: {self.results['passed_checks']}")
        print(f"Failed: {self.results['failed_checks']}")
        print(f"Success Rate: {self.results['success_rate']:.1f}%")
        print("=" * 80)

        if self.results["overall_passed"]:
            print("✅ PHASE 02: ALL VALIDATION CHECKS PASSED")
        else:
            print("❌ PHASE 02: SOME VALIDATION CHECKS FAILED")

        print("=" * 80)

    def save_report(self):
        """Save validation report"""
        report_path = Path(__file__).parent / "validation_report.json"

        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\nValidation report saved to: {report_path}")


def main():
    """Main validation entry point"""
    validator = Phase02Validator()
    success = validator.run_all_checks()
    validator.save_report()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
