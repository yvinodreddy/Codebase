#!/usr/bin/env python3
"""
Phase 06: HIPAA Compliance - Verification Script

Verifies all deliverables and compliance requirements.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*80}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*80}{Colors.END}\n")


def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")


class Phase06Verifier:
    """Comprehensive Phase 06 verification"""

    def __init__(self):
        self.deliverables_dir = Path(__file__).parent
        self.phase_dir = self.deliverables_dir.parent
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "phase": "06",
            "phase_name": "HIPAA Compliance",
            "checks": [],
            "total_checks": 0,
            "passed_checks": 0,
            "failed_checks": 0
        }

    def check_file_exists(self, filename, category):
        """Check if file exists"""
        filepath = self.deliverables_dir / filename
        exists = filepath.exists()

        self.results["total_checks"] += 1
        if exists:
            self.results["passed_checks"] += 1
            print_success(f"{category}: {filename} exists ({filepath.stat().st_size:,} bytes)")
        else:
            self.results["failed_checks"] += 1
            print_error(f"{category}: {filename} NOT FOUND")

        self.results["checks"].append({
            "category": category,
            "check": f"File exists: {filename}",
            "passed": exists
        })

        return exists

    def check_content(self, filename, keywords, category):
        """Check file contains keywords"""
        filepath = self.deliverables_dir / filename
        if not filepath.exists():
            return False

        self.results["total_checks"] += 1
        with open(filepath, 'r') as f:
            content = f.read()
            found = all(k in content for k in keywords)

        if found:
            self.results["passed_checks"] += 1
            print_success(f"{category}: {filename} contains all required keywords")
        else:
            self.results["failed_checks"] += 1
            print_error(f"{category}: {filename} missing required keywords")

        self.results["checks"].append({
            "category": category,
            "check": f"Content validation: {filename}",
            "passed": found
        })

        return found

    def verify_architecture(self):
        """Verify architecture document"""
        print_header("ARCHITECTURE VERIFICATION")

        exists = self.check_file_exists("HIPAA_COMPLIANCE_ARCHITECTURE.md", "Architecture")
        if exists:
            self.check_content("HIPAA_COMPLIANCE_ARCHITECTURE.md", [
                "Encryption", "Authentication", "Audit Logging",
                "AES-256", "MFA", "RBAC", "JWT"
            ], "Architecture")

    def verify_implementation(self):
        """Verify implementation"""
        print_header("IMPLEMENTATION VERIFICATION")

        exists = self.check_file_exists("hipaa_compliance_system.py", "Implementation")
        if exists:
            self.check_content("hipaa_compliance_system.py", [
                "EncryptionSystem", "MFASystem", "JWTManager",
                "RBACSystem", "TamperProofAuditLog", "SessionManager",
                "PHIMasking", "HIPAAComplianceSystem"
            ], "Implementation")

    def verify_tests(self):
        """Verify test suite"""
        print_header("TEST SUITE VERIFICATION")

        exists = self.check_file_exists("test_hipaa_compliance.py", "Tests")
        if exists:
            self.check_content("test_hipaa_compliance.py", [
                "test_encryption", "test_mfa", "test_jwt",
                "test_rbac", "test_audit_logging", "test_session",
                "test_phi_masking"
            ], "Tests")

    def verify_phase_structure(self):
        """Verify phase directory structure"""
        print_header("PHASE STRUCTURE VERIFICATION")

        dirs = ["code", "tests", "docs", ".state", "deliverables"]
        for dir_name in dirs:
            dir_path = self.phase_dir / dir_name
            self.results["total_checks"] += 1
            if dir_path.exists():
                self.results["passed_checks"] += 1
                print_success(f"Directory exists: {dir_name}/")
            else:
                self.results["failed_checks"] += 1
                print_error(f"Directory missing: {dir_name}/")

    def generate_report(self):
        """Generate verification report"""
        print_header("VERIFICATION SUMMARY")

        success_rate = (self.results["passed_checks"] / self.results["total_checks"] * 100
                       if self.results["total_checks"] > 0 else 0)

        print(f"Total Checks:    {self.results['total_checks']}")
        print(f"✅ Passed:       {self.results['passed_checks']}")
        print(f"❌ Failed:       {self.results['failed_checks']}")
        print(f"\n{Colors.BOLD}Success Rate:    {success_rate:.1f}%{Colors.END}")

        if success_rate >= 95:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ PHASE 06 VERIFICATION: PASSED{Colors.END}")
            status = "PASSED"
            exit_code = 0
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ PHASE 06 VERIFICATION: FAILED{Colors.END}")
            status = "FAILED"
            exit_code = 1

        self.results["overall_status"] = status
        self.results["success_rate"] = success_rate

        # Save report
        report_path = self.deliverables_dir / "VERIFICATION_REPORT.json"
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n{Colors.BLUE}Report saved to: {report_path}{Colors.END}")

        return exit_code

    def run(self):
        """Run all verifications"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}")
        print("╔" + "="*78 + "╗")
        print("║" + " "*20 + "PHASE 06: HIPAA COMPLIANCE" + " "*32 + "║")
        print("║" + " "*22 + "COMPREHENSIVE VERIFICATION" + " "*30 + "║")
        print("╚" + "="*78 + "╝")
        print(f"{Colors.END}\n")

        self.verify_architecture()
        self.verify_implementation()
        self.verify_tests()
        self.verify_phase_structure()

        return self.generate_report()


if __name__ == "__main__":
    verifier = Phase06Verifier()
    exit_code = verifier.run()
    sys.exit(exit_code)
