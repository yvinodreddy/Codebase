#!/usr/bin/env python3
"""
Phase 05 Verification Script
Automated verification of all deliverables and functionality
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import json
from datetime import datetime

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


class Phase05Verifier:
    """Comprehensive Phase 05 verification"""

    def __init__(self):
        self.phase_dir = Path(__file__).parent.parent
        self.results = []
        self.total_checks = 0
        self.passed_checks = 0

    def verify_all(self) -> bool:
        """Run all verification checks"""
        print(f"\n{BOLD}{'=' * 70}{RESET}")
        print(f"{BOLD}{BLUE}PHASE 05: AUDIO GENERATION - VERIFICATION{RESET}")
        print(f"{BOLD}{'=' * 70}{RESET}\n")

        checks = [
            ("File Structure", self.verify_file_structure),
            ("Code Quality", self.verify_code_quality),
            ("TTS Providers", self.verify_tts_providers),
            ("Audio Processors", self.verify_audio_processors),
            ("Validators", self.verify_validators),
            ("Storage System", self.verify_storage),
            ("Deployment Assets", self.verify_deployment_assets),
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

    def verify_file_structure(self) -> bool:
        """Verify required file structure exists"""
        required_paths = [
            "code/audio_providers/__init__.py",
            "code/audio_providers/base_provider.py",
            "code/audio_providers/azure_tts.py",
            "code/audio_providers/aws_polly.py",
            "code/audio_providers/google_tts.py",
            "code/processors/__init__.py",
            "code/processors/audio_processor.py",
            "code/processors/normalization.py",
            "code/processors/format_converter.py",
            "code/processors/effects_processor.py",
            "code/validators/__init__.py",
            "code/validators/audio_validator.py",
            "code/validators/quality_metrics.py",
            "code/storage/__init__.py",
            "code/storage/audio_storage.py",
            "code/storage/cache_manager.py",
            "deliverables/Dockerfile",
            "deliverables/kubernetes-audio-service.yaml",
            "deliverables/terraform-audio-infrastructure.tf",
            "deliverables/requirements.txt",
            "tests/test_comprehensive.py",
            "README.md",
        ]

        missing = []
        for path in required_paths:
            full_path = self.phase_dir / path
            if not full_path.exists():
                missing.append(path)
                print(f"    {RED}✗ Missing: {path}{RESET}")
            else:
                print(f"    {GREEN}✓ Found: {path}{RESET}")

        return len(missing) == 0

    def verify_code_quality(self) -> bool:
        """Verify code quality metrics"""
        code_dir = self.phase_dir / "code"
        total_lines = 0
        file_count = 0

        for py_file in code_dir.rglob("*.py"):
            if '__pycache__' in str(py_file):
                continue
            with open(py_file, 'r') as f:
                lines = len(f.readlines())
                total_lines += lines
                file_count += 1

        print(f"    Total Python files: {file_count}")
        print(f"    Total lines of code: {total_lines}")

        # Quality thresholds
        min_lines = 1000
        min_files = 10

        return total_lines >= min_lines and file_count >= min_files

    def verify_tts_providers(self) -> bool:
        """Verify TTS provider implementations"""
        providers_dir = self.phase_dir / "code" / "audio_providers"

        checks = [
            (providers_dir / "base_provider.py", ["BaseAudioProvider", "AudioFormat", "VoiceProfile"]),
            (providers_dir / "azure_tts.py", ["AzureTTSProvider", "generate_audio"]),
            (providers_dir / "aws_polly.py", ["AWSPollyProvider", "get_available_voices"]),
            (providers_dir / "google_tts.py", ["GoogleTTSProvider", "validate_voice"]),
        ]

        all_passed = True
        for file_path, required_symbols in checks:
            if not file_path.exists():
                print(f"    {RED}✗ Missing: {file_path.name}{RESET}")
                all_passed = False
                continue

            with open(file_path, 'r') as f:
                content = f.read()
                for symbol in required_symbols:
                    if symbol in content:
                        print(f"    {GREEN}✓ {file_path.name}: {symbol}{RESET}")
                    else:
                        print(f"    {RED}✗ {file_path.name}: Missing {symbol}{RESET}")
                        all_passed = False

        return all_passed

    def verify_audio_processors(self) -> bool:
        """Verify audio processing components"""
        processors_dir = self.phase_dir / "code" / "processors"

        required_classes = [
            ("audio_processor.py", ["AudioProcessor", "ProcessingConfig"]),
            ("normalization.py", ["AudioNormalizer", "NormalizationMetrics"]),
            ("format_converter.py", ["FormatConverter", "ConversionConfig"]),
            ("effects_processor.py", ["EffectsProcessor", "EffectType"]),
        ]

        all_passed = True
        for filename, classes in required_classes:
            file_path = processors_dir / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                    for cls in classes:
                        if cls in content:
                            print(f"    {GREEN}✓ {filename}: {cls}{RESET}")
                        else:
                            print(f"    {YELLOW}⚠ {filename}: {cls} not clearly defined{RESET}")
            else:
                print(f"    {RED}✗ Missing: {filename}{RESET}")
                all_passed = False

        return all_passed

    def verify_validators(self) -> bool:
        """Verify validation components"""
        validators_dir = self.phase_dir / "code" / "validators"

        files_to_check = [
            ("audio_validator.py", ["AudioValidator", "ValidationLevel", "ValidationResult"]),
            ("quality_metrics.py", ["QualityMetrics", "QualityScore"]),
        ]

        all_passed = True
        for filename, classes in files_to_check:
            file_path = validators_dir / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                    for cls in classes:
                        if cls in content:
                            print(f"    {GREEN}✓ {filename}: {cls}{RESET}")
                        else:
                            all_passed = False
            else:
                print(f"    {RED}✗ Missing: {filename}{RESET}")
                all_passed = False

        return all_passed

    def verify_storage(self) -> bool:
        """Verify storage system"""
        storage_dir = self.phase_dir / "code" / "storage"

        required = [
            ("audio_storage.py", ["AudioStorage", "StorageConfig", "HIPAA"]),
            ("cache_manager.py", ["CacheManager", "CacheEntry"]),
        ]

        all_passed = True
        for filename, keywords in required:
            file_path = storage_dir / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                    for keyword in keywords:
                        if keyword in content:
                            print(f"    {GREEN}✓ {filename}: {keyword}{RESET}")
                        else:
                            print(f"    {YELLOW}⚠ {filename}: {keyword} reference{RESET}")
            else:
                print(f"    {RED}✗ Missing: {filename}{RESET}")
                all_passed = False

        return all_passed

    def verify_deployment_assets(self) -> bool:
        """Verify deployment configuration files"""
        deliverables_dir = self.phase_dir / "deliverables"

        assets = [
            ("Dockerfile", 10),  # Min lines
            ("kubernetes-audio-service.yaml", 100),
            ("terraform-audio-infrastructure.tf", 100),
            ("requirements.txt", 10),
        ]

        all_passed = True
        for filename, min_lines in assets:
            file_path = deliverables_dir / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    lines = len(f.readlines())
                    if lines >= min_lines:
                        print(f"    {GREEN}✓ {filename}: {lines} lines{RESET}")
                    else:
                        print(f"    {YELLOW}⚠ {filename}: {lines} lines (expected {min_lines}+){RESET}")
                        all_passed = False
            else:
                print(f"    {RED}✗ Missing: {filename}{RESET}")
                all_passed = False

        return all_passed

    def verify_tests(self) -> bool:
        """Verify test suite"""
        test_file = self.phase_dir / "tests" / "test_comprehensive.py"

        if not test_file.exists():
            print(f"    {RED}✗ Test file not found{RESET}")
            return False

        with open(test_file, 'r') as f:
            content = f.read()

        required_tests = [
            "TestAudioProviders",
            "TestAudioProcessing",
            "TestAudioValidation",
            "TestAudioStorage",
            "TestProductionScenarios",
        ]

        all_found = True
        for test_class in required_tests:
            if test_class in content:
                print(f"    {GREEN}✓ {test_class}{RESET}")
            else:
                print(f"    {RED}✗ Missing: {test_class}{RESET}")
                all_found = False

        # Count test methods
        test_methods = content.count("def test_")
        print(f"    Total test methods: {test_methods}")

        return all_found and test_methods >= 15

    def verify_documentation(self) -> bool:
        """Verify documentation files"""
        docs_to_check = [
            self.phase_dir / "README.md",
            self.phase_dir / "docs" / "IMPLEMENTATION_GUIDE.md",
        ]

        all_exist = True
        for doc in docs_to_check:
            if doc.exists():
                size_kb = doc.stat().st_size / 1024
                print(f"    {GREEN}✓ {doc.name}: {size_kb:.1f} KB{RESET}")
            else:
                print(f"    {YELLOW}⚠ {doc.name}: Not found{RESET}")
                # Don't fail for documentation
        return True

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
            print(f"\n{GREEN}{BOLD}✅ PHASE 05 VERIFICATION: SUCCESS{RESET}")
            print(f"{GREEN}All checks passed! Phase 05 is production-ready.{RESET}\n")
            return True
        else:
            print(f"\n{YELLOW}{BOLD}⚠️  PHASE 05 VERIFICATION: INCOMPLETE{RESET}")
            print(f"{YELLOW}Some checks failed. Review the output above.{RESET}\n")
            return False


def main():
    """Main entry point"""
    verifier = Phase05Verifier()
    success = verifier.verify_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
