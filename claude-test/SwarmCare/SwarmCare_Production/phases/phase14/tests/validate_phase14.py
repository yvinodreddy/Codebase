#!/usr/bin/env python3
"""
Phase 14: Comprehensive Validation Script
Production-ready validation for medical imaging system

Validates:
- Implementation completeness
- HIPAA compliance
- Performance benchmarks
- Integration with agent framework
- Production readiness
"""

import sys
import os
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

def print_section(title: str):
    """Print formatted section header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}")

def print_result(check: str, passed: bool, details: str = ""):
    """Print check result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {check}")
    if details:
        print(f"       {details}")

def validate_implementation() -> Tuple[int, int]:
    """Validate Phase 14 implementation"""
    print_section("IMPLEMENTATION VALIDATION")

    passed = 0
    total = 0

    # Check 1: Implementation file exists
    total += 1
    impl_path = Path(__file__).parent.parent / "code" / "implementation.py"
    if impl_path.exists():
        print_result("Implementation file exists", True, str(impl_path))
        passed += 1
    else:
        print_result("Implementation file exists", False, str(impl_path))

    # Check 2: Medical imaging core exists
    total += 1
    core_path = Path(__file__).parent.parent / "code" / "medical_imaging_core.py"
    if core_path.exists():
        print_result("Medical imaging core exists", True, str(core_path))
        passed += 1
    else:
        print_result("Medical imaging core exists", False, str(core_path))

    # Check 3: Implementation can be imported
    total += 1
    try:
        from implementation import Phase14Implementation
        print_result("Implementation imports successfully", True)
        passed += 1
    except Exception as e:
        print_result("Implementation imports successfully", False, str(e))

    # Check 4: Medical imaging core can be imported
    total += 1
    try:
        from medical_imaging_core import MedicalImagingPipeline
        print_result("Medical imaging core imports successfully", True)
        passed += 1
    except Exception as e:
        print_result("Medical imaging core imports successfully", False, str(e))

    # Check 5: Phase ID is correct
    total += 1
    try:
        from implementation import Phase14Implementation
        impl = Phase14Implementation()
        if impl.phase_id == 14:
            print_result("Phase ID is correct", True, f"Phase ID: {impl.phase_id}")
            passed += 1
        else:
            print_result("Phase ID is correct", False, f"Expected 14, got {impl.phase_id}")
    except Exception as e:
        print_result("Phase ID is correct", False, str(e))

    # Check 6: Story points are correct
    total += 1
    try:
        from implementation import Phase14Implementation
        impl = Phase14Implementation()
        if impl.story_points == 76:
            print_result("Story points are correct", True, f"Story Points: {impl.story_points}")
            passed += 1
        else:
            print_result("Story points are correct", False, f"Expected 76, got {impl.story_points}")
    except Exception as e:
        print_result("Story points are correct", False, str(e))

    return passed, total

def validate_medical_imaging() -> Tuple[int, int]:
    """Validate medical imaging capabilities"""
    print_section("MEDICAL IMAGING VALIDATION")

    passed = 0
    total = 0

    try:
        from medical_imaging_core import (
            MedicalImagingPipeline,
            DICOMProcessor,
            XRayAnalyzer,
            CTAnalyzer,
            MRIAnalyzer,
            ImagingModality,
            AbnormalityType
        )

        # Check 1: Pipeline initialization
        total += 1
        try:
            pipeline = MedicalImagingPipeline(use_guardrails=False)
            print_result("Pipeline initializes", True)
            passed += 1
        except Exception as e:
            print_result("Pipeline initializes", False, str(e))

        # Check 2: DICOM processor
        total += 1
        try:
            processor = DICOMProcessor()
            print_result("DICOM processor initializes", True)
            passed += 1
        except Exception as e:
            print_result("DICOM processor initializes", False, str(e))

        # Check 3: X-ray analyzer
        total += 1
        try:
            xray = XRayAnalyzer()
            print_result("X-ray analyzer initializes", True)
            passed += 1
        except Exception as e:
            print_result("X-ray analyzer initializes", False, str(e))

        # Check 4: CT analyzer
        total += 1
        try:
            ct = CTAnalyzer()
            print_result("CT analyzer initializes", True)
            passed += 1
        except Exception as e:
            print_result("CT analyzer initializes", False, str(e))

        # Check 5: MRI analyzer
        total += 1
        try:
            mri = MRIAnalyzer()
            print_result("MRI analyzer initializes", True)
            passed += 1
        except Exception as e:
            print_result("MRI analyzer initializes", False, str(e))

        # Check 6: Imaging modalities
        total += 1
        modalities = [m.value for m in ImagingModality]
        required_modalities = ["X-Ray", "CT Scan", "MRI"]
        if all(m in modalities for m in required_modalities):
            print_result("All required modalities supported", True, f"{len(modalities)} modalities")
            passed += 1
        else:
            print_result("All required modalities supported", False, f"Missing: {set(required_modalities) - set(modalities)}")

        # Check 7: Abnormality types
        total += 1
        abnormalities = [a.value for a in AbnormalityType]
        required_abnormalities = ["Fracture", "Pneumonia", "Tumor", "Normal"]
        if all(a in abnormalities for a in required_abnormalities):
            print_result("All required abnormality types supported", True, f"{len(abnormalities)} types")
            passed += 1
        else:
            print_result("All required abnormality types supported", False, f"Missing: {set(required_abnormalities) - set(abnormalities)}")

    except ImportError as e:
        print_result("Medical imaging modules available", False, str(e))

    return passed, total

def validate_hipaa_compliance() -> Tuple[int, int]:
    """Validate HIPAA compliance"""
    print_section("HIPAA COMPLIANCE VALIDATION")

    passed = 0
    total = 0

    try:
        from medical_imaging_core import DICOMProcessor, ImageMetadata
        import numpy as np

        processor = DICOMProcessor()

        # Check 1: PHI patterns defined
        total += 1
        if processor.phi_patterns:
            print_result("PHI detection patterns defined", True, f"{len(processor.phi_patterns)} patterns")
            passed += 1
        else:
            print_result("PHI detection patterns defined", False)

        # Check 2: Metadata anonymization
        total += 1
        img_array = np.random.randint(0, 255, (512, 512), dtype=np.uint8)
        metadata = processor._create_anonymous_metadata(Path("test.png"), img_array)

        if metadata.patient_id.startswith("ANON_"):
            print_result("Patient ID anonymized", True, f"Example: {metadata.patient_id[:12]}...")
            passed += 1
        else:
            print_result("Patient ID anonymized", False, f"Got: {metadata.patient_id}")

        # Check 3: PHI removed flag
        total += 1
        if metadata.phi_removed:
            print_result("PHI removed flag set", True)
            passed += 1
        else:
            print_result("PHI removed flag set", False)

        # Check 4: HIPAA compliant flag
        total += 1
        if metadata.hipaa_compliant:
            print_result("HIPAA compliant flag set", True)
            passed += 1
        else:
            print_result("HIPAA compliant flag set", False)

        # Check 5: Institution anonymized
        total += 1
        if metadata.institution == "ANONYMIZED":
            print_result("Institution anonymized", True)
            passed += 1
        else:
            print_result("Institution anonymized", False, f"Got: {metadata.institution}")

    except Exception as e:
        print_result("HIPAA validation error", False, str(e))

    return passed, total

def validate_performance() -> Tuple[int, int]:
    """Validate performance benchmarks"""
    print_section("PERFORMANCE VALIDATION")

    passed = 0
    total = 0

    try:
        from medical_imaging_core import MedicalImagingPipeline, DICOMProcessor
        import numpy as np
        import tempfile

        # Create test image
        temp_dir = tempfile.mkdtemp()
        image_path = os.path.join(temp_dir, "test.png")

        try:
            from PIL import Image
            img = Image.fromarray(np.random.randint(0, 255, (512, 512), dtype=np.uint8))
            img.save(image_path)
        except ImportError:
            with open(image_path, 'wb') as f:
                f.write(b'\x89PNG\r\n\x1a\n')

        pipeline = MedicalImagingPipeline(use_guardrails=False)

        # Check 1: Processing time
        total += 1
        start = time.time()
        result = pipeline.analyze_image(image_path, "XRAY")
        duration_ms = (time.time() - start) * 1000

        target_ms = 5000  # 5 seconds
        if result and duration_ms < target_ms:
            print_result(f"Processing time < {target_ms}ms", True, f"{duration_ms:.2f}ms")
            passed += 1
        else:
            print_result(f"Processing time < {target_ms}ms", False, f"{duration_ms:.2f}ms")

        # Check 2: Quality score calculation
        total += 1
        if result and result.quality_score > 0:
            print_result("Quality score calculated", True, f"{result.quality_score}/100")
            passed += 1
        else:
            print_result("Quality score calculated", False)

        # Check 3: Detections generated
        total += 1
        if result and len(result.detections) > 0:
            print_result("Abnormality detections generated", True, f"{len(result.detections)} detections")
            passed += 1
        else:
            print_result("Abnormality detections generated", False)

    except Exception as e:
        print_result("Performance validation error", False, str(e))

    return passed, total

def validate_framework_integration() -> Tuple[int, int]:
    """Validate agent framework integration"""
    print_section("FRAMEWORK INTEGRATION VALIDATION")

    passed = 0
    total = 0

    try:
        from implementation import Phase14Implementation

        impl = Phase14Implementation()

        # Check 1: Framework version
        total += 1
        if impl.framework_version == "100%":
            print_result("Framework version is 100%", True)
            passed += 1
        else:
            print_result("Framework version is 100%", False, f"Got: {impl.framework_version}")

        # Check 2: Execution method
        total += 1
        if hasattr(impl, 'execute'):
            print_result("Execute method exists", True)
            passed += 1
        else:
            print_result("Execute method exists", False)

        # Check 3: Context gathering
        total += 1
        if hasattr(impl, 'gather_context'):
            print_result("Context gathering method exists", True)
            passed += 1
        else:
            print_result("Context gathering method exists", False)

        # Check 4: Verification
        total += 1
        if hasattr(impl, 'verify_work'):
            print_result("Verification method exists", True)
            passed += 1
        else:
            print_result("Verification method exists", False)

        # Check 5: Full execution cycle
        total += 1
        try:
            task = {"goal": "Test execution", "phase_id": 14}
            result = impl.execute(task)
            if result and hasattr(result, 'success'):
                print_result("Full execution cycle works", True)
                passed += 1
            else:
                print_result("Full execution cycle works", False, "No result or success attribute")
        except Exception as e:
            print_result("Full execution cycle works", False, str(e))

    except Exception as e:
        print_result("Framework integration error", False, str(e))

    return passed, total

def validate_production_readiness() -> Tuple[int, int]:
    """Validate production readiness"""
    print_section("PRODUCTION READINESS VALIDATION")

    passed = 0
    total = 0

    # Check 1: State file exists
    total += 1
    state_path = Path(__file__).parent.parent / ".state" / "phase_state.json"
    if state_path.exists():
        print_result("Phase state file exists", True, str(state_path))
        passed += 1
    else:
        print_result("Phase state file exists", False, str(state_path))

    # Check 2: State file valid JSON
    total += 1
    try:
        with open(state_path, 'r') as f:
            state = json.load(f)
        print_result("State file is valid JSON", True)
        passed += 1
    except Exception as e:
        print_result("State file is valid JSON", False, str(e))

    # Check 3: Tests exist
    total += 1
    test_path = Path(__file__).parent / "test_phase14.py"
    if test_path.exists():
        print_result("Test file exists", True, str(test_path))
        passed += 1
    else:
        print_result("Test file exists", False, str(test_path))

    # Check 4: Medical imaging tests exist
    total += 1
    imaging_test_path = Path(__file__).parent / "test_medical_imaging.py"
    if imaging_test_path.exists():
        print_result("Medical imaging test file exists", True, str(imaging_test_path))
        passed += 1
    else:
        print_result("Medical imaging test file exists", False, str(imaging_test_path))

    # Check 5: Documentation exists
    total += 1
    doc_path = Path(__file__).parent.parent / "docs" / "IMPLEMENTATION_GUIDE.md"
    if doc_path.exists():
        print_result("Documentation exists", True, str(doc_path))
        passed += 1
    else:
        print_result("Documentation exists", False, str(doc_path))

    return passed, total

def main():
    """Run comprehensive validation"""
    print("\n" + "="*80)
    print("PHASE 14: COMPREHENSIVE VALIDATION SUITE")
    print("Multi-modal AI - Medical Imaging")
    print("="*80)

    total_passed = 0
    total_checks = 0

    # Run all validation sections
    p, t = validate_implementation()
    total_passed += p
    total_checks += t

    p, t = validate_medical_imaging()
    total_passed += p
    total_checks += t

    p, t = validate_hipaa_compliance()
    total_passed += p
    total_checks += t

    p, t = validate_performance()
    total_passed += p
    total_checks += t

    p, t = validate_framework_integration()
    total_passed += p
    total_checks += t

    p, t = validate_production_readiness()
    total_passed += p
    total_checks += t

    # Final summary
    print_section("VALIDATION SUMMARY")
    print(f"Total Checks: {total_checks}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_checks - total_passed}")
    print(f"Success Rate: {(total_passed/total_checks*100):.1f}%")

    if total_passed == total_checks:
        print("\n🎉 ✅ ALL VALIDATION CHECKS PASSED - PRODUCTION READY")
        return 0
    else:
        print(f"\n⚠️  {total_checks - total_passed} VALIDATION CHECKS FAILED - REVIEW REQUIRED")
        return 1

if __name__ == "__main__":
    exit(main())
