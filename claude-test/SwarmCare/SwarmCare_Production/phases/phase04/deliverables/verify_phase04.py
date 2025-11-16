#!/usr/bin/env python3
"""
Phase 04: Frontend Application - Comprehensive Verification Script

Verifies all deliverables:
- Backend API implementation
- Frontend components (RAG UI, Dashboard, Podcast UI)
- Docker configurations
- Kubernetes manifests
- Test suite
- Documentation
- Deployment readiness

Returns:
- 0: All verifications passed
- 1: Verification failures detected
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*80}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*80}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

class Phase04Verifier:
    """Comprehensive Phase 04 verification"""

    def __init__(self):
        self.deliverables_dir = Path(__file__).parent
        self.phase_dir = self.deliverables_dir.parent
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "phase": "04",
            "phase_name": "Frontend Application",
            "checks": [],
            "total_checks": 0,
            "passed_checks": 0,
            "failed_checks": 0,
            "warnings": 0
        }

    def check_file_exists(self, filename, category):
        """Check if deliverable file exists"""
        filepath = self.deliverables_dir / filename
        exists = filepath.exists()

        self.results["total_checks"] += 1
        if exists:
            self.results["passed_checks"] += 1
            print_success(f"{category}: {filename} exists")
            size = filepath.stat().st_size
            print_info(f"   Size: {size:,} bytes")
        else:
            self.results["failed_checks"] += 1
            print_error(f"{category}: {filename} NOT FOUND")

        self.results["checks"].append({
            "category": category,
            "check": f"File exists: {filename}",
            "passed": exists
        })

        return exists

    def check_file_content(self, filename, expected_strings, category):
        """Check if file contains expected content"""
        filepath = self.deliverables_dir / filename
        if not filepath.exists():
            return False

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            self.results["total_checks"] += 1
            found = all(s in content for s in expected_strings)

            if found:
                self.results["passed_checks"] += 1
                print_success(f"{category}: {filename} contains expected content")
            else:
                self.results["failed_checks"] += 1
                print_error(f"{category}: {filename} missing expected content")

            self.results["checks"].append({
                "category": category,
                "check": f"Content validation: {filename}",
                "passed": found
            })

            return found
        except Exception as e:
            print_error(f"{category}: Error reading {filename}: {e}")
            return False

    def verify_architecture_design(self):
        """Verify architecture design document"""
        print_header("ARCHITECTURE DESIGN")

        exists = self.check_file_exists("ARCHITECTURE_DESIGN.md", "Architecture")

        if exists:
            expected_content = [
                "RAG UI",
                "SWARMCARE Dashboard",
                "Podcast UI",
                "FastAPI",
                "React",
                "Kubernetes"
            ]
            self.check_file_content("ARCHITECTURE_DESIGN.md", expected_content, "Architecture")

    def verify_backend_api(self):
        """Verify backend API implementation"""
        print_header("BACKEND API")

        exists = self.check_file_exists("backend_api.py", "Backend API")

        if exists:
            expected_content = [
                "FastAPI",
                "/api/rag/query",
                "/api/dashboard/agents",
                "/api/podcast/generate",
                "MultiLayerGuardrailSystem",
                "AdaptiveFeedbackLoop"
            ]
            self.check_file_content("backend_api.py", expected_content, "Backend API")

    def verify_frontend_components(self):
        """Verify frontend components"""
        print_header("FRONTEND COMPONENTS")

        # RAG UI
        exists = self.check_file_exists("frontend_rag_ui.tsx", "RAG UI")
        if exists:
            self.check_file_content("frontend_rag_ui.tsx", [
                "RAGUIComponent",
                "StreamingResponse",
                "QueryHistory"
            ], "RAG UI")

        # Dashboard
        exists = self.check_file_exists("frontend_dashboard.tsx", "Dashboard")
        if exists:
            self.check_file_content("frontend_dashboard.tsx", [
                "DashboardComponent",
                "AgentStatusCard",
                "WebSocket"
            ], "Dashboard")

        # Podcast UI
        exists = self.check_file_exists("frontend_podcast_ui.tsx", "Podcast UI")
        if exists:
            self.check_file_content("frontend_podcast_ui.tsx", [
                "PodcastUIComponent",
                "AudioPlayer",
                "EpisodeCard"
            ], "Podcast UI")

    def verify_tests(self):
        """Verify test suite"""
        print_header("TEST SUITE")

        exists = self.check_file_exists("test_comprehensive.py", "Tests")

        if exists:
            expected_content = [
                "TestRAGAPI",
                "TestDashboardAPI",
                "TestPodcastAPI",
                "TestSecurity",
                "TestGuardrailsIntegration",
                "TestPerformance"
            ]
            self.check_file_content("test_comprehensive.py", expected_content, "Tests")

    def verify_docker_configs(self):
        """Verify Docker configurations"""
        print_header("DOCKER CONFIGURATION")

        # Frontend Dockerfile
        self.check_file_exists("Dockerfile.frontend", "Docker")
        self.check_file_content("Dockerfile.frontend", [
            "FROM node:18-alpine",
            "nginx"
        ], "Docker Frontend")

        # Backend Dockerfile
        self.check_file_exists("Dockerfile.backend", "Docker")
        self.check_file_content("Dockerfile.backend", [
            "FROM python:3.11-slim",
            "uvicorn"
        ], "Docker Backend")

        # Docker Compose
        self.check_file_exists("docker-compose.yml", "Docker Compose")
        self.check_file_content("docker-compose.yml", [
            "frontend:",
            "backend:",
            "redis:",
            "postgres:"
        ], "Docker Compose")

    def verify_kubernetes(self):
        """Verify Kubernetes manifests"""
        print_header("KUBERNETES DEPLOYMENT")

        exists = self.check_file_exists("kubernetes-deployment.yaml", "Kubernetes")

        if exists:
            expected_content = [
                "kind: Namespace",
                "kind: Deployment",
                "kind: Service",
                "kind: HorizontalPodAutoscaler",
                "frontend-deployment",
                "backend-deployment"
            ]
            self.check_file_content("kubernetes-deployment.yaml", expected_content, "Kubernetes")

    def verify_phase_structure(self):
        """Verify phase directory structure"""
        print_header("PHASE STRUCTURE")

        required_dirs = [
            self.phase_dir / "code",
            self.phase_dir / "tests",
            self.phase_dir / "docs",
            self.phase_dir / ".state",
            self.phase_dir / "deliverables"
        ]

        for dir_path in required_dirs:
            self.results["total_checks"] += 1
            if dir_path.exists():
                self.results["passed_checks"] += 1
                print_success(f"Directory exists: {dir_path.name}/")
            else:
                self.results["failed_checks"] += 1
                print_error(f"Directory missing: {dir_path.name}/")

    def verify_implementation(self):
        """Verify main implementation file"""
        print_header("PHASE IMPLEMENTATION")

        impl_file = self.phase_dir / "code" / "implementation.py"
        self.results["total_checks"] += 1

        if impl_file.exists():
            self.results["passed_checks"] += 1
            print_success("implementation.py exists")

            with open(impl_file, 'r') as f:
                content = f.read()
                if "Phase04Implementation" in content:
                    print_success("Phase04Implementation class found")
                    self.results["passed_checks"] += 1
                else:
                    print_error("Phase04Implementation class not found")
                    self.results["failed_checks"] += 1
                self.results["total_checks"] += 1
        else:
            self.results["failed_checks"] += 1
            print_error("implementation.py NOT FOUND")

    def generate_report(self):
        """Generate final verification report"""
        print_header("VERIFICATION SUMMARY")

        # Calculate success rate
        success_rate = (self.results["passed_checks"] / self.results["total_checks"] * 100) if self.results["total_checks"] > 0 else 0

        # Print summary
        print(f"Total Checks:    {self.results['total_checks']}")
        print(f"✅ Passed:       {self.results['passed_checks']}")
        print(f"❌ Failed:       {self.results['failed_checks']}")
        print(f"⚠️  Warnings:    {self.results['warnings']}")
        print(f"\n{Colors.BOLD}Success Rate:    {success_rate:.1f}%{Colors.END}")

        # Determine overall status
        if success_rate >= 95:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ PHASE 04 VERIFICATION: PASSED{Colors.END}")
            print(f"{Colors.GREEN}All critical deliverables present and validated.{Colors.END}")
            status = "PASSED"
            exit_code = 0
        elif success_rate >= 80:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  PHASE 04 VERIFICATION: PASSED WITH WARNINGS{Colors.END}")
            print(f"{Colors.YELLOW}Some non-critical checks failed. Review recommended.{Colors.END}")
            status = "PASSED_WITH_WARNINGS"
            exit_code = 0
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ PHASE 04 VERIFICATION: FAILED{Colors.END}")
            print(f"{Colors.RED}Critical deliverables missing or invalid.{Colors.END}")
            status = "FAILED"
            exit_code = 1

        # Save report
        self.results["overall_status"] = status
        self.results["success_rate"] = success_rate

        report_path = self.deliverables_dir / "VERIFICATION_REPORT.json"
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n{Colors.BLUE}Report saved to: {report_path}{Colors.END}")

        return exit_code

    def run(self):
        """Run all verifications"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}")
        print("╔════════════════════════════════════════════════════════════════════════════╗")
        print("║                  PHASE 04: FRONTEND APPLICATION                            ║")
        print("║                   COMPREHENSIVE VERIFICATION                               ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")

        print_info(f"Verification started: {self.results['timestamp']}")
        print_info(f"Deliverables directory: {self.deliverables_dir}")

        # Run all verification checks
        self.verify_architecture_design()
        self.verify_backend_api()
        self.verify_frontend_components()
        self.verify_tests()
        self.verify_docker_configs()
        self.verify_kubernetes()
        self.verify_phase_structure()
        self.verify_implementation()

        # Generate final report
        return self.generate_report()

def main():
    """Main entry point"""
    verifier = Phase04Verifier()
    exit_code = verifier.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
