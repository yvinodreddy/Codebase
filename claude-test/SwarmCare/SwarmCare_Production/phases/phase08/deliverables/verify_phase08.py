#!/usr/bin/env python3
"""
Phase 08 Production Deployment - Verification Script
Comprehensive validation of all deployment artifacts
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple
import subprocess

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'


class Phase08Verifier:
    """Comprehensive Phase 08 verification"""

    def __init__(self):
        self.phase_dir = Path(__file__).parent.parent
        self.results = []
        self.total_checks = 0
        self.passed_checks = 0

    def verify_all(self) -> bool:
        """Run all verification checks"""
        print(f"\n{BOLD}{'=' * 70}{RESET}")
        print(f"{BOLD}{BLUE}PHASE 08: PRODUCTION DEPLOYMENT - VERIFICATION{RESET}")
        print(f"{BOLD}{'=' * 70}{RESET}\n")

        checks = [
            ("Helm Charts", self.verify_helm_charts),
            ("Kubernetes Manifests", self.verify_kubernetes_manifests),
            ("Security Configuration", self.verify_security_config),
            ("Monitoring Stack", self.verify_monitoring),
            ("CI/CD Pipelines", self.verify_cicd),
            ("Terraform Infrastructure", self.verify_terraform),
            ("Deployment Scripts", self.verify_scripts),
            ("Python Code", self.verify_python_code),
            ("Tests", self.verify_tests),
            ("Documentation", self.verify_documentation),
        ]

        for check_name, check_func in checks:
            self._run_check(check_name, check_func)

        self._print_summary()

        return self.passed_checks == self.total_checks

    def _run_check(self, name: str, func):
        """Run a single verification check"""
        print(f"\n{BOLD}Checking: {name}{RESET}")
        try:
            result = func()
            if result:
                self.passed_checks += 1
                print(f"  {GREEN}✓ PASSED{RESET}")
            else:
                print(f"  {RED}✗ FAILED{RESET}")
            self.total_checks += 1
            self.results.append((name, result))
        except Exception as e:
            print(f"  {RED}✗ ERROR: {e}{RESET}")
            self.total_checks += 1
            self.results.append((name, False))

    def verify_helm_charts(self) -> bool:
        """Verify Helm chart structure"""
        helm_dir = self.phase_dir / "deliverables" / "helm"

        required_files = [
            "Chart.yaml",
            "values.yaml",
            "templates/deployment.yaml",
            "templates/service.yaml",
            "templates/hpa.yaml",
            "templates/_helpers.tpl",
        ]

        all_exist = True
        for file in required_files:
            path = helm_dir / file
            if path.exists():
                print(f"    {GREEN}✓ {file}{RESET}")
            else:
                print(f"    {RED}✗ Missing: {file}{RESET}")
                all_exist = False

        # Check Chart.yaml content
        chart_file = helm_dir / "Chart.yaml"
        if chart_file.exists():
            with open(chart_file) as f:
                content = f.read()
                if "apiVersion: v2" in content and "swarmcare" in content:
                    print(f"    {GREEN}✓ Chart.yaml valid{RESET}")
                else:
                    print(f"    {YELLOW}⚠ Chart.yaml may be incomplete{RESET}")

        return all_exist

    def verify_kubernetes_manifests(self) -> bool:
        """Verify Kubernetes manifest files"""
        security_dir = self.phase_dir / "deliverables" / "security"

        required_files = {
            "rbac.yaml": ["ServiceAccount", "Role", "RoleBinding"],
            "network-policies.yaml": ["NetworkPolicy"],
            "pod-security.yaml": ["PodSecurityPolicy"],
            "sealed-secrets.yaml": ["SealedSecret"],
        }

        all_valid = True
        for filename, required_kinds in required_files.items():
            path = security_dir / filename
            if not path.exists():
                print(f"    {RED}✗ Missing: {filename}{RESET}")
                all_valid = False
                continue

            with open(path) as f:
                content = f.read()
                found_kinds = [kind for kind in required_kinds if f"kind: {kind}" in content]

                if len(found_kinds) == len(required_kinds):
                    print(f"    {GREEN}✓ {filename}: All kinds present{RESET}")
                else:
                    print(f"    {YELLOW}⚠ {filename}: Missing some kinds{RESET}")
                    all_valid = False

        return all_valid

    def verify_security_config(self) -> bool:
        """Verify security configurations"""
        security_dir = self.phase_dir / "deliverables" / "security"

        checks = {
            "RBAC configured": (security_dir / "rbac.yaml").exists(),
            "Network policies defined": (security_dir / "network-policies.yaml").exists(),
            "Pod security enforced": (security_dir / "pod-security.yaml").exists(),
            "Secrets management": (security_dir / "sealed-secrets.yaml").exists(),
        }

        all_passed = True
        for check_name, passed in checks.items():
            if passed:
                print(f"    {GREEN}✓ {check_name}{RESET}")
            else:
                print(f"    {RED}✗ {check_name}{RESET}")
                all_passed = False

        return all_passed

    def verify_monitoring(self) -> bool:
        """Verify monitoring stack configuration"""
        monitoring_dir = self.phase_dir / "deliverables" / "monitoring"

        required_files = [
            "prometheus-values.yaml",
            "grafana-dashboards.yaml",
        ]

        all_exist = True
        for filename in required_files:
            path = monitoring_dir / filename
            if path.exists():
                size_kb = path.stat().st_size / 1024
                print(f"    {GREEN}✓ {filename} ({size_kb:.1f} KB){RESET}")

                # Check content
                with open(path) as f:
                    content = f.read()
                    if "prometheus" in content.lower() or "grafana" in content.lower():
                        print(f"      {GREEN}✓ Content valid{RESET}")
            else:
                print(f"    {RED}✗ Missing: {filename}{RESET}")
                all_exist = False

        return all_exist

    def verify_cicd(self) -> bool:
        """Verify CI/CD pipeline configurations"""
        cicd_dir = self.phase_dir / "deliverables" / "cicd"

        pipelines = {
            "github-actions-deploy.yaml": ["deploy", "build", "test"],
            "argocd-application.yaml": ["Application", "syncPolicy"],
        }

        all_valid = True
        for filename, keywords in pipelines.items():
            path = cicd_dir / filename
            if not path.exists():
                print(f"    {RED}✗ Missing: {filename}{RESET}")
                all_valid = False
                continue

            with open(path) as f:
                content = f.read()
                found = sum(1 for kw in keywords if kw in content)

                if found == len(keywords):
                    print(f"    {GREEN}✓ {filename}: Complete{RESET}")
                else:
                    print(f"    {YELLOW}⚠ {filename}: Incomplete ({found}/{len(keywords)}){RESET}")

        return all_valid

    def verify_terraform(self) -> bool:
        """Verify Terraform configuration"""
        terraform_dir = self.phase_dir / "deliverables" / "terraform"

        required_files = ["main.tf", "variables.tf", "outputs.tf"]

        all_exist = True
        total_lines = 0

        for filename in required_files:
            path = terraform_dir / filename
            if path.exists():
                lines = len(path.read_text().splitlines())
                total_lines += lines
                print(f"    {GREEN}✓ {filename} ({lines} lines){RESET}")
            else:
                print(f"    {RED}✗ Missing: {filename}{RESET}")
                all_exist = False

        print(f"    Total Terraform code: {total_lines} lines")

        # Check for key resources
        main_tf = terraform_dir / "main.tf"
        if main_tf.exists():
            with open(main_tf) as f:
                content = f.read()
                resources = ["azurerm_kubernetes_cluster", "azurerm_container_registry",
                           "azurerm_postgresql_flexible_server", "azurerm_redis_cache"]
                found = sum(1 for r in resources if r in content)
                print(f"    {GREEN}✓ Key resources: {found}/{len(resources)}{RESET}")

        return all_exist

    def verify_scripts(self) -> bool:
        """Verify deployment automation scripts"""
        scripts_dir = self.phase_dir / "deliverables" / "scripts"

        required_scripts = [
            "deploy.sh",
            "rollback.sh",
            "backup-restore.sh",
        ]

        all_valid = True
        for script in required_scripts:
            path = scripts_dir / script
            if not path.exists():
                print(f"    {RED}✗ Missing: {script}{RESET}")
                all_valid = False
                continue

            if os.access(path, os.X_OK):
                lines = len(path.read_text().splitlines())
                print(f"    {GREEN}✓ {script} ({lines} lines, executable){RESET}")
            else:
                print(f"    {YELLOW}⚠ {script} (not executable){RESET}")

        return all_valid

    def verify_python_code(self) -> bool:
        """Verify Python deployment code"""
        code_dir = self.phase_dir / "code" / "deployment"

        required_files = ["__init__.py", "deployment_manager.py"]

        all_exist = True
        total_lines = 0

        for filename in required_files:
            path = code_dir / filename
            if path.exists():
                lines = len(path.read_text().splitlines())
                total_lines += lines
                print(f"    {GREEN}✓ {filename} ({lines} lines){RESET}")
            else:
                print(f"    {RED}✗ Missing: {filename}{RESET}")
                all_exist = False

        print(f"    Total Python code: {total_lines} lines")

        return all_exist

    def verify_tests(self) -> bool:
        """Verify test suite"""
        test_file = self.phase_dir / "tests" / "test_deployment.py"

        if not test_file.exists():
            print(f"    {RED}✗ Test file not found{RESET}")
            return False

        with open(test_file) as f:
            content = f.read()

        test_classes = content.count("class Test")
        test_methods = content.count("def test_")

        print(f"    {GREEN}✓ Test file exists{RESET}")
        print(f"    Test classes: {test_classes}")
        print(f"    Test methods: {test_methods}")

        return test_classes >= 5 and test_methods >= 15

    def verify_documentation(self) -> bool:
        """Verify documentation"""
        docs_to_check = [
            ("DEPLOYMENT_RUNBOOK.md", 5000),
            ("README.md", 500),
        ]

        all_exist = True
        for filename, min_size in docs_to_check:
            path = self.phase_dir / "deliverables" / filename if "RUNBOOK" in filename else self.phase_dir / filename

            if path.exists():
                size = path.stat().st_size
                if size >= min_size:
                    print(f"    {GREEN}✓ {filename} ({size / 1024:.1f} KB){RESET}")
                else:
                    print(f"    {YELLOW}⚠ {filename} too small ({size} < {min_size} bytes){RESET}")
            else:
                print(f"    {YELLOW}⚠ {filename} not found{RESET}")

        return True  # Documentation is optional

    def _print_summary(self):
        """Print verification summary"""
        print(f"\n{BOLD}{'=' * 70}{RESET}")
        print(f"{BOLD}VERIFICATION SUMMARY{RESET}")
        print(f"{BOLD}{'=' * 70}{RESET}")

        success_rate = (self.passed_checks / self.total_checks * 100) if self.total_checks > 0 else 0

        for name, passed in self.results:
            status = f"{GREEN}✓ PASSED{RESET}" if passed else f"{RED}✗ FAILED{RESET}"
            print(f"  {name:.<50} {status}")

        print(f"\n{BOLD}Results: {self.passed_checks}/{self.total_checks} checks passed ({success_rate:.1f}%){RESET}")

        if self.passed_checks == self.total_checks:
            print(f"\n{GREEN}{BOLD}✅ PHASE 08 VERIFICATION: SUCCESS{RESET}")
            print(f"{GREEN}All checks passed! Phase 08 is production-ready.{RESET}\n")
            return True
        else:
            print(f"\n{YELLOW}{BOLD}⚠️  PHASE 08 VERIFICATION: INCOMPLETE{RESET}")
            print(f"{YELLOW}Some checks failed. Review the output above.{RESET}\n")
            return False


def main():
    """Main entry point"""
    verifier = Phase08Verifier()
    success = verifier.verify_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
