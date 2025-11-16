#!/usr/bin/env python3
"""
SwarmCare Documentation Verification Script
Phase 09: Production-Ready Documentation Verification

Verifies all documentation components:
- Technical documentation
- User guides
- Tutorials
- API documentation
- Deployment documentation

Usage:
    python3 verify_documentation.py
    python3 verify_documentation.py --verbose
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

try:
    from implementation import Phase09Implementation
    IMPLEMENTATION_AVAILABLE = True
except ImportError as e:
    print(f"❌ Failed to import implementation: {e}")
    IMPLEMENTATION_AVAILABLE = False


class DocumentationVerifier:
    """Comprehensive documentation verification"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "phase": "Phase 09: Documentation",
            "verification_passed": False,
            "documentation_types": {},
            "generation_tools": {},
            "summary": {}
        }

    def log(self, message):
        """Log message if verbose"""
        if self.verbose:
            print(f"  {message}")

    def verify_all(self) -> bool:
        """Verify all documentation components"""
        print("=" * 80)
        print("SWARMCARE DOCUMENTATION VERIFICATION")
        print("=" * 80)
        print(f"Started: {self.results['timestamp']}")
        print("=" * 80)
        print()

        if not IMPLEMENTATION_AVAILABLE:
            print("❌ Implementation not available")
            return False

        # Initialize phase
        try:
            phase = Phase09Implementation()
            self.log("Phase initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize phase: {e}")
            return False

        # Verify each documentation type
        all_passed = True

        # 1. Technical Documentation
        if not self._verify_technical_docs(phase):
            all_passed = False

        # 2. User Guides
        if not self._verify_user_guides(phase):
            all_passed = False

        # 3. Tutorials
        if not self._verify_tutorials(phase):
            all_passed = False

        # 4. API Documentation
        if not self._verify_api_docs(phase):
            all_passed = False

        # 5. Deployment Documentation
        if not self._verify_deployment_docs(phase):
            all_passed = False

        # 6. Generation Tools
        if not self._verify_generation_tools(phase):
            all_passed = False

        # Summary
        self._print_summary(all_passed)

        self.results["verification_passed"] = all_passed
        return all_passed

    def _verify_technical_docs(self, phase) -> bool:
        """Verify technical documentation"""
        print("Verifying Technical Documentation...")

        try:
            tech_docs = phase._init_technical_docs()

            checks = [
                (tech_docs["status"] == "initialized", "Status"),
                (len(tech_docs["components"]) >= 8, "Components"),
                ("Markdown" in tech_docs["formats"], "Formats"),
                (tech_docs["auto_generated"] == True, "Auto-generation"),
            ]

            all_passed = all(check[0] for check in checks)

            if all_passed:
                print("  ✅ Technical Documentation: VERIFIED")
                self.results["documentation_types"]["technical"] = {
                    "passed": True,
                    "components": len(tech_docs["components"])
                }
            else:
                failed = [check[1] for check in checks if not check[0]]
                print(f"  ❌ Technical Documentation: FAILED - {', '.join(failed)}")
                self.results["documentation_types"]["technical"] = {
                    "passed": False,
                    "error": f"Failed checks: {', '.join(failed)}"
                }

            return all_passed

        except Exception as e:
            print(f"  ❌ Technical Documentation: Exception: {e}")
            return False

    def _verify_user_guides(self, phase) -> bool:
        """Verify user guides"""
        print("Verifying User Guides...")

        try:
            user_guides = phase._init_user_guides()

            checks = [
                (user_guides["status"] == "initialized", "Status"),
                (len(user_guides["components"]) >= 8, "Components"),
                ("Clinicians" in user_guides["target_audiences"], "Audiences"),
                (user_guides["accessibility"] == "WCAG 2.1 Level AA", "Accessibility"),
            ]

            all_passed = all(check[0] for check in checks)

            if all_passed:
                print("  ✅ User Guides: VERIFIED")
                self.results["documentation_types"]["user_guides"] = {
                    "passed": True,
                    "components": len(user_guides["components"])
                }
            else:
                failed = [check[1] for check in checks if not check[0]]
                print(f"  ❌ User Guides: FAILED - {', '.join(failed)}")
                self.results["documentation_types"]["user_guides"] = {
                    "passed": False,
                    "error": f"Failed checks: {', '.join(failed)}"
                }

            return all_passed

        except Exception as e:
            print(f"  ❌ User Guides: Exception: {e}")
            return False

    def _verify_tutorials(self, phase) -> bool:
        """Verify tutorials"""
        print("Verifying Tutorials...")

        try:
            tutorials = phase._init_tutorials()

            checks = [
                (tutorials["status"] == "initialized", "Status"),
                (len(tutorials["tutorial_categories"]) >= 8, "Categories"),
                ("Beginner" in tutorials["difficulty_levels"], "Difficulty levels"),
                (len(tutorials["delivery_methods"]) >= 5, "Delivery methods"),
            ]

            all_passed = all(check[0] for check in checks)

            if all_passed:
                print("  ✅ Tutorials: VERIFIED")
                self.results["documentation_types"]["tutorials"] = {
                    "passed": True,
                    "categories": len(tutorials["tutorial_categories"])
                }
            else:
                failed = [check[1] for check in checks if not check[0]]
                print(f"  ❌ Tutorials: FAILED - {', '.join(failed)}")
                self.results["documentation_types"]["tutorials"] = {
                    "passed": False,
                    "error": f"Failed checks: {', '.join(failed)}"
                }

            return all_passed

        except Exception as e:
            print(f"  ❌ Tutorials: Exception: {e}")
            return False

    def _verify_api_docs(self, phase) -> bool:
        """Verify API documentation"""
        print("Verifying API Documentation...")

        try:
            api_docs = phase._init_api_docs()

            checks = [
                (api_docs["status"] == "initialized", "Status"),
                (len(api_docs["components"]) >= 8, "Components"),
                (api_docs["api_specifications"]["openapi_version"] == "3.1.0", "OpenAPI version"),
                ("python" in api_docs["languages"], "Language support"),
            ]

            all_passed = all(check[0] for check in checks)

            if all_passed:
                print("  ✅ API Documentation: VERIFIED")
                self.results["documentation_types"]["api_docs"] = {
                    "passed": True,
                    "components": len(api_docs["components"])
                }
            else:
                failed = [check[1] for check in checks if not check[0]]
                print(f"  ❌ API Documentation: FAILED - {', '.join(failed)}")
                self.results["documentation_types"]["api_docs"] = {
                    "passed": False,
                    "error": f"Failed checks: {', '.join(failed)}"
                }

            return all_passed

        except Exception as e:
            print(f"  ❌ API Documentation: Exception: {e}")
            return False

    def _verify_deployment_docs(self, phase) -> bool:
        """Verify deployment documentation"""
        print("Verifying Deployment Documentation...")

        try:
            deployment = phase._init_deployment_docs()

            checks = [
                (deployment["status"] == "initialized", "Status"),
                (len(deployment["components"]) >= 10, "Components"),
                ("Kubernetes" in deployment["deployment_targets"], "Deployment targets"),
                ("terraform" in deployment["automation"], "Automation"),
            ]

            all_passed = all(check[0] for check in checks)

            if all_passed:
                print("  ✅ Deployment Documentation: VERIFIED")
                self.results["documentation_types"]["deployment"] = {
                    "passed": True,
                    "components": len(deployment["components"])
                }
            else:
                failed = [check[1] for check in checks if not check[0]]
                print(f"  ❌ Deployment Documentation: FAILED - {', '.join(failed)}")
                self.results["documentation_types"]["deployment"] = {
                    "passed": False,
                    "error": f"Failed checks: {', '.join(failed)}"
                }

            return all_passed

        except Exception as e:
            print(f"  ❌ Deployment Documentation: Exception: {e}")
            return False

    def _verify_generation_tools(self, phase) -> bool:
        """Verify documentation generation tools"""
        print("Verifying Generation Tools...")

        try:
            tools = phase._init_generation_tools()

            checks = [
                ("mkdocs" in tools["static_site_generators"], "MkDocs"),
                ("swagger_ui" in tools["api_doc_generators"], "Swagger UI"),
                ("mermaid" in tools["diagram_tools"], "Mermaid"),
                (tools["automation"]["auto_build_on_commit"] == True, "Auto-build"),
            ]

            all_passed = all(check[0] for check in checks)

            if all_passed:
                print("  ✅ Generation Tools: VERIFIED")
                self.results["generation_tools"] = {
                    "passed": True,
                    "count": len(tools)
                }
            else:
                failed = [check[1] for check in checks if not check[0]]
                print(f"  ❌ Generation Tools: FAILED - {', '.join(failed)}")
                self.results["generation_tools"] = {
                    "passed": False,
                    "error": f"Failed checks: {', '.join(failed)}"
                }

            return all_passed

        except Exception as e:
            print(f"  ❌ Generation Tools: Exception: {e}")
            return False

    def _print_summary(self, all_passed):
        """Print verification summary"""
        print()
        print("=" * 80)
        print("VERIFICATION SUMMARY")
        print("=" * 80)

        total = len(self.results["documentation_types"]) + (1 if self.results["generation_tools"] else 0)
        passed = sum(1 for item in self.results["documentation_types"].values() if item.get("passed", False))
        if self.results["generation_tools"].get("passed", False):
            passed += 1

        print(f"Total Components: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed / total * 100):.1f}%")
        print("=" * 80)

        if all_passed:
            print("✅ ALL DOCUMENTATION VERIFIED SUCCESSFULLY")
        else:
            print("❌ SOME DOCUMENTATION VERIFICATION FAILED")

        print("=" * 80)

    def save_report(self, filename="documentation_verification_report.json"):
        """Save verification report"""
        report_path = os.path.join(os.path.dirname(__file__), filename)
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nVerification report saved to: {report_path}")


def main():
    """Main verification entry point"""
    import argparse
    parser = argparse.ArgumentParser(description="Verify SwarmCare Documentation")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    args = parser.parse_args()

    verifier = DocumentationVerifier(verbose=args.verbose)
    success = verifier.verify_all()
    verifier.save_report()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
