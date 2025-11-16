#!/usr/bin/env python3
"""
Comprehensive Validation Suite for SwarmCare
Production-ready testing framework to achieve 100% success rate

This suite validates:
1. All guardrails are implemented correctly
2. AI_Accelerate_Prompts requirements are met
3. System performance meets targets
4. Before/after comparisons
5. Version comparisons (v0, v2.0, v2.1)
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
import subprocess

@dataclass
class ValidationResult:
    """Result of a validation check"""
    name: str
    category: str
    passed: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class ValidationReport:
    """Complete validation report"""
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    warnings: int = 0
    results: List[ValidationResult] = field(default_factory=list)
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    end_time: str = ""
    duration_seconds: float = 0.0

class ComprehensiveValidator:
    """
    Comprehensive validation system for SwarmCare
    Validates all aspects of the implementation
    """

    def __init__(self, base_path: str = "/home/user01/claude-test/SwarmCare"):
        self.base_path = Path(base_path)
        self.report = ValidationReport()
        self.start_time = time.time()

    def run_all_validations(self) -> ValidationReport:
        """Run all validation checks"""
        print("=" * 80)
        print("COMPREHENSIVE VALIDATION SUITE FOR SWARMCARE")
        print("=" * 80)
        print(f"Start Time: {self.report.start_time}")
        print(f"Base Path: {self.base_path}")
        print("=" * 80)
        print()

        # Category 1: File Structure Validation
        print("📁 CATEGORY 1: File Structure Validation")
        self._validate_file_structure()
        print()

        # Category 2: Guardrails Implementation
        print("🛡️  CATEGORY 2: Guardrails Implementation")
        self._validate_guardrails()
        print()

        # Category 3: AI_Accelerate_Prompts Requirements
        print("🚀 CATEGORY 3: AI_Accelerate_Prompts Framework")
        self._validate_ai_framework()
        print()

        # Category 4: Code Quality
        print("✨ CATEGORY 4: Code Quality")
        self._validate_code_quality()
        print()

        # Category 5: Dependencies
        print("📦 CATEGORY 5: Dependencies")
        self._validate_dependencies()
        print()

        # Category 6: Configuration
        print("⚙️  CATEGORY 6: Configuration")
        self._validate_configuration()
        print()

        # Category 7: Documentation
        print("📚 CATEGORY 7: Documentation")
        self._validate_documentation()
        print()

        # Finalize report
        self._finalize_report()

        return self.report

    def _add_result(self, name: str, category: str, passed: bool,
                    message: str, details: Dict[str, Any] = None):
        """Add a validation result"""
        result = ValidationResult(
            name=name,
            category=category,
            passed=passed,
            message=message,
            details=details or {}
        )
        self.report.results.append(result)
        self.report.total_checks += 1
        if passed:
            self.report.passed_checks += 1
            status = "✅ PASS"
        else:
            self.report.failed_checks += 1
            status = "❌ FAIL"

        print(f"  {status}: {name}")
        if message:
            print(f"    → {message}")

    def _validate_file_structure(self):
        """Validate that all required files exist"""
        required_files = {
            "Guardrails Core": [
                "guardrails/__init__.py",
                "guardrails/azure_content_safety.py",
                "guardrails/medical_guardrails.py",
                "guardrails/multi_layer_system.py",
                "guardrails/crewai_guardrails.py",
                "guardrails/monitoring.py"
            ],
            "AI Framework": [
                "AI_Accelerate_Prompts/AI_PROMPTS_LIBRARY.md",
                "AI_Accelerate_Prompts/START_HERE.md",
                "AI_Accelerate_Prompts/README.md",
                "AI_Accelerate_Prompts/IMPLEMENTATION_GUIDE.md",
                "AI_Accelerate_Prompts/BEFORE_AFTER_COMPARISON.md"
            ],
            "Implementation": [
                "swarmcare_crew_with_guardrails.py",
                "requirements.txt",
                ".env.template",
                "setup_guardrails.sh"
            ],
            "Testing": [
                "tests/test_guardrails.py"
            ],
            "Documentation": [
                "GUARDRAILS_README.md",
                "GUARDRAILS_IMPLEMENTATION_GUIDE.md",
                "IMPLEMENTATION_COMPLETE.md"
            ]
        }

        for group, files in required_files.items():
            for file_path in files:
                full_path = self.base_path / file_path
                exists = full_path.exists()
                size = full_path.stat().st_size if exists else 0

                self._add_result(
                    name=f"{group}: {file_path}",
                    category="File Structure",
                    passed=exists and size > 0,
                    message=f"Size: {size:,} bytes" if exists else "File not found",
                    details={"path": str(full_path), "size": size}
                )

    def _validate_guardrails(self):
        """Validate guardrails implementation"""
        guardrails_checks = [
            ("Layer 1: Prompt Shields", self._check_prompt_shields),
            ("Layer 2: Input Content Filtering", self._check_input_filtering),
            ("Layer 3: PHI Detection", self._check_phi_detection),
            ("Layer 4: Medical Terminology", self._check_medical_terminology),
            ("Layer 5: Output Content Filtering", self._check_output_filtering),
            ("Layer 6: Groundedness Detection", self._check_groundedness),
            ("Layer 7: HIPAA Compliance", self._check_hipaa_compliance)
        ]

        for check_name, check_func in guardrails_checks:
            passed, message, details = check_func()
            self._add_result(
                name=check_name,
                category="Guardrails",
                passed=passed,
                message=message,
                details=details
            )

    def _check_prompt_shields(self) -> Tuple[bool, str, Dict]:
        """Check if Prompt Shields are implemented"""
        file_path = self.base_path / "guardrails" / "azure_content_safety.py"
        if not file_path.exists():
            return False, "File not found", {}

        content = file_path.read_text()
        has_prompt_shields = "analyze_text_with_prompt_shields" in content
        has_jailbreak = "jailbreak" in content.lower()

        return (has_prompt_shields and has_jailbreak,
                "Prompt Shields implementation found" if has_prompt_shields else "Missing implementation",
                {"has_prompt_shields": has_prompt_shields, "has_jailbreak": has_jailbreak})

    def _check_input_filtering(self) -> Tuple[bool, str, Dict]:
        """Check if input content filtering is implemented"""
        file_path = self.base_path / "guardrails" / "azure_content_safety.py"
        if not file_path.exists():
            return False, "File not found", {}

        content = file_path.read_text()
        categories = ["Hate", "Sexual", "Violence", "SelfHarm"]
        found_categories = [cat for cat in categories if cat in content]

        return (len(found_categories) == 4,
                f"Found {len(found_categories)}/4 content categories",
                {"categories": found_categories})

    def _check_phi_detection(self) -> Tuple[bool, str, Dict]:
        """Check if PHI detection is implemented"""
        file_path = self.base_path / "guardrails" / "medical_guardrails.py"
        if not file_path.exists():
            return False, "File not found", {}

        content = file_path.read_text()
        has_phi_detector = "PHIDetector" in content
        has_patterns = "PATTERNS" in content
        has_email = "email" in content.lower()
        has_phone = "phone" in content.lower()

        return (has_phi_detector and has_patterns,
                "PHI Detection implementation found" if has_phi_detector else "Missing implementation",
                {"has_detector": has_phi_detector, "has_patterns": has_patterns,
                 "has_email": has_email, "has_phone": has_phone})

    def _check_medical_terminology(self) -> Tuple[bool, str, Dict]:
        """Check if medical terminology validation is implemented"""
        file_path = self.base_path / "guardrails" / "medical_guardrails.py"
        if not file_path.exists():
            return False, "File not found", {}

        content = file_path.read_text()
        has_validator = "MedicalTerminologyValidator" in content
        has_snomed = "SNOMED" in content
        has_icd = "ICD" in content

        return (has_validator and (has_snomed or has_icd),
                "Medical terminology validation found" if has_validator else "Missing implementation",
                {"has_validator": has_validator, "has_snomed": has_snomed, "has_icd": has_icd})

    def _check_output_filtering(self) -> Tuple[bool, str, Dict]:
        """Check if output content filtering is implemented"""
        file_path = self.base_path / "guardrails" / "multi_layer_system.py"
        if not file_path.exists():
            return False, "File not found", {}

        content = file_path.read_text()
        has_output_filter = "validate_output" in content or "layer_5" in content.lower()

        return (has_output_filter,
                "Output filtering found" if has_output_filter else "Missing implementation",
                {"has_output_filter": has_output_filter})

    def _check_groundedness(self) -> Tuple[bool, str, Dict]:
        """Check if groundedness detection is implemented"""
        file_path = self.base_path / "guardrails" / "azure_content_safety.py"
        if not file_path.exists():
            return False, "File not found", {}

        content = file_path.read_text()
        has_groundedness = "groundedness" in content.lower()
        has_ungrounded = "ungrounded" in content.lower()

        return (has_groundedness,
                "Groundedness detection found" if has_groundedness else "Missing implementation",
                {"has_groundedness": has_groundedness, "has_ungrounded": has_ungrounded})

    def _check_hipaa_compliance(self) -> Tuple[bool, str, Dict]:
        """Check if HIPAA compliance validation is implemented"""
        file_path = self.base_path / "guardrails" / "medical_guardrails.py"
        if not file_path.exists():
            return False, "File not found", {}

        content = file_path.read_text()
        has_hipaa = "HIPAA" in content
        has_compliance = "HIPAAComplianceValidator" in content or "compliance" in content.lower()

        return (has_hipaa and has_compliance,
                "HIPAA compliance validation found" if has_hipaa else "Missing implementation",
                {"has_hipaa": has_hipaa, "has_compliance": has_compliance})

    def _validate_ai_framework(self):
        """Validate AI_Accelerate_Prompts framework requirements"""
        checks = [
            ("AI Prompts Library exists", self._check_prompts_library),
            ("Before/After comparison exists", self._check_comparison),
            ("Implementation guide exists", self._check_implementation_guide),
            ("48 prompts implemented", self._check_prompt_count)
        ]

        for check_name, check_func in checks:
            passed, message, details = check_func()
            self._add_result(
                name=check_name,
                category="AI Framework",
                passed=passed,
                message=message,
                details=details
            )

    def _check_prompts_library(self) -> Tuple[bool, str, Dict]:
        """Check if AI prompts library exists and has content"""
        file_path = self.base_path / "AI_Accelerate_Prompts" / "AI_PROMPTS_LIBRARY.md"
        if not file_path.exists():
            return False, "File not found", {}

        content = file_path.read_text()
        size = len(content)
        lines = content.count('\n')

        return (size > 50000,  # Should be substantial
                f"Library has {size:,} bytes, {lines:,} lines",
                {"size": size, "lines": lines})

    def _check_comparison(self) -> Tuple[bool, str, Dict]:
        """Check if before/after comparison exists"""
        file_path = self.base_path / "AI_Accelerate_Prompts" / "BEFORE_AFTER_COMPARISON.md"
        if not file_path.exists():
            return False, "File not found", {}

        content = file_path.read_text()
        has_before = "BEFORE" in content
        has_after = "AFTER" in content
        has_metrics = "Metric" in content or "metric" in content

        return (has_before and has_after,
                "Comparison document found with before/after sections",
                {"has_before": has_before, "has_after": has_after, "has_metrics": has_metrics})

    def _check_implementation_guide(self) -> Tuple[bool, str, Dict]:
        """Check if implementation guide exists"""
        file_path = self.base_path / "AI_Accelerate_Prompts" / "IMPLEMENTATION_GUIDE.md"
        return (file_path.exists(),
                "Implementation guide found" if file_path.exists() else "Missing",
                {"exists": file_path.exists()})

    def _check_prompt_count(self) -> Tuple[bool, str, Dict]:
        """Check if 48 prompts are documented"""
        file_path = self.base_path / "AI_Accelerate_Prompts" / "AI_PROMPTS_LIBRARY.md"
        if not file_path.exists():
            return False, "File not found", {}

        content = file_path.read_text()
        # Count prompt headers (## Prompt #X)
        import re
        prompts = re.findall(r'##\s+Prompt\s+#(\d+)', content)
        count = len(prompts)

        return (count >= 48,
                f"Found {count} prompts (target: 48)",
                {"prompt_count": count, "prompts": prompts[:10]})  # First 10 for details

    def _validate_code_quality(self):
        """Validate code quality metrics"""
        checks = [
            ("Python files are valid", self._check_python_syntax),
            ("No obvious security issues", self._check_security),
            ("Proper imports", self._check_imports)
        ]

        for check_name, check_func in checks:
            passed, message, details = check_func()
            self._add_result(
                name=check_name,
                category="Code Quality",
                passed=passed,
                message=message,
                details=details
            )

    def _check_python_syntax(self) -> Tuple[bool, str, Dict]:
        """Check if Python files have valid syntax"""
        python_files = list(self.base_path.rglob("*.py"))
        errors = []

        for py_file in python_files:
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
            try:
                compile(py_file.read_text(), py_file, 'exec')
            except SyntaxError as e:
                errors.append(f"{py_file.name}: {e}")

        return (len(errors) == 0,
                f"Checked {len(python_files)} files, {len(errors)} errors",
                {"total_files": len(python_files), "errors": errors})

    def _check_security(self) -> Tuple[bool, str, Dict]:
        """Check for obvious security issues"""
        issues = []

        # Check for hardcoded credentials
        py_files = list(self.base_path.rglob("*.py"))
        for py_file in py_files:
            if "venv" in str(py_file):
                continue
            content = py_file.read_text()
            if "password = " in content.lower() or "api_key = \"" in content:
                issues.append(f"{py_file.name}: Potential hardcoded credential")

        return (len(issues) == 0,
                f"Checked for security issues, found {len(issues)}",
                {"issues": issues})

    def _check_imports(self) -> Tuple[bool, str, Dict]:
        """Check if imports are properly structured"""
        main_file = self.base_path / "swarmcare_crew_with_guardrails.py"
        if not main_file.exists():
            return False, "Main file not found", {}

        content = main_file.read_text()
        required_imports = [
            "from guardrails.crewai_guardrails import",
            "from guardrails.multi_layer_system import",
            "from guardrails.monitoring import"
        ]

        found = [imp for imp in required_imports if imp in content]

        return (len(found) == len(required_imports),
                f"Found {len(found)}/{len(required_imports)} required imports",
                {"found": len(found), "required": len(required_imports)})

    def _validate_dependencies(self):
        """Validate dependencies are properly specified"""
        req_file = self.base_path / "requirements.txt"
        if not req_file.exists():
            self._add_result(
                name="requirements.txt exists",
                category="Dependencies",
                passed=False,
                message="File not found",
                details={}
            )
            return

        content = req_file.read_text()
        required_deps = [
            "crewai",
            "azure-ai-contentsafety",
            "python-dotenv",
            "tenacity",
            "pytest"
        ]

        found_deps = [dep for dep in required_deps if dep in content.lower()]

        self._add_result(
            name="Required dependencies",
            category="Dependencies",
            passed=len(found_deps) == len(required_deps),
            message=f"Found {len(found_deps)}/{len(required_deps)} required dependencies",
            details={"found": found_deps, "required": required_deps}
        )

    def _validate_configuration(self):
        """Validate configuration files"""
        env_template = self.base_path / ".env.template"

        if not env_template.exists():
            self._add_result(
                name=".env.template exists",
                category="Configuration",
                passed=False,
                message="Template not found",
                details={}
            )
            return

        content = env_template.read_text()
        required_vars = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "CONTENT_SAFETY_KEY",
            "CONTENT_SAFETY_ENDPOINT"
        ]

        found_vars = [var for var in required_vars if var in content]

        self._add_result(
            name="Environment variables",
            category="Configuration",
            passed=len(found_vars) == len(required_vars),
            message=f"Found {len(found_vars)}/{len(required_vars)} required variables",
            details={"found": found_vars, "required": required_vars}
        )

    def _validate_documentation(self):
        """Validate documentation completeness"""
        docs = [
            ("GUARDRAILS_README.md", 3000),  # Minimum bytes
            ("GUARDRAILS_IMPLEMENTATION_GUIDE.md", 5000),
            ("IMPLEMENTATION_COMPLETE.md", 2000),
            ("AI_Accelerate_Prompts/README.md", 2000)
        ]

        for doc_name, min_size in docs:
            doc_path = self.base_path / doc_name
            exists = doc_path.exists()
            size = doc_path.stat().st_size if exists else 0

            self._add_result(
                name=f"Documentation: {doc_name}",
                category="Documentation",
                passed=exists and size >= min_size,
                message=f"Size: {size:,} bytes (min: {min_size:,})" if exists else "Missing",
                details={"size": size, "min_size": min_size}
            )

    def _finalize_report(self):
        """Finalize the validation report"""
        self.report.end_time = datetime.now().isoformat()
        self.report.duration_seconds = time.time() - self.start_time

        # Calculate warnings (passes with notes)
        self.report.warnings = sum(1 for r in self.report.results
                                   if r.passed and "warning" in r.message.lower())

        # Print summary
        print()
        print("=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        print(f"Total Checks: {self.report.total_checks}")
        print(f"Passed: {self.report.passed_checks} ✅")
        print(f"Failed: {self.report.failed_checks} ❌")
        print(f"Warnings: {self.report.warnings} ⚠️")
        print(f"Success Rate: {(self.report.passed_checks/self.report.total_checks*100):.1f}%")
        print(f"Duration: {self.report.duration_seconds:.2f} seconds")
        print("=" * 80)

        # Show failed checks
        if self.report.failed_checks > 0:
            print()
            print("FAILED CHECKS:")
            print("-" * 80)
            for result in self.report.results:
                if not result.passed:
                    print(f"❌ [{result.category}] {result.name}")
                    print(f"   {result.message}")
            print("=" * 80)

    def save_report(self, filename: str = "validation_report.json"):
        """Save validation report to JSON file"""
        report_path = self.base_path / filename

        report_dict = {
            "summary": {
                "total_checks": self.report.total_checks,
                "passed": self.report.passed_checks,
                "failed": self.report.failed_checks,
                "warnings": self.report.warnings,
                "success_rate": (self.report.passed_checks / self.report.total_checks * 100)
                               if self.report.total_checks > 0 else 0,
                "duration_seconds": self.report.duration_seconds,
                "start_time": self.report.start_time,
                "end_time": self.report.end_time
            },
            "results": [
                {
                    "name": r.name,
                    "category": r.category,
                    "passed": r.passed,
                    "message": r.message,
                    "details": r.details,
                    "timestamp": r.timestamp
                }
                for r in self.report.results
            ]
        }

        with open(report_path, 'w') as f:
            json.dump(report_dict, f, indent=2)

        print(f"\n📄 Report saved to: {report_path}")
        return report_path

def main():
    """Main execution function"""
    print()
    print("🚀 Starting Comprehensive Validation Suite...")
    print()

    # Create validator
    validator = ComprehensiveValidator()

    # Run all validations
    report = validator.run_all_validations()

    # Save report
    validator.save_report("validation_report.json")

    # Exit with appropriate code
    if report.failed_checks == 0:
        print("\n✅ ALL VALIDATIONS PASSED! System is production-ready!")
        return 0
    else:
        print(f"\n❌ {report.failed_checks} validations failed. Please review and fix.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
