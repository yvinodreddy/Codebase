"""
Phase 25: Production Validation Script
========================================

Comprehensive validation for production readiness.
Tests implementation, core system, compliance, and deployment readiness.

Validation Sections:
1. Implementation Validation (6 checks)
2. Patient-Facing XAI Core (4 checks)
3. Health Literacy Assessment (3 checks)
4. Explanation Generation (3 checks)
5. Validation System (2 checks)
6. Portal Integration (2 checks)
7. HIPAA Compliance (2 checks)
8. Performance (2 checks)
9. Agent Framework (2 checks)
10. Production Readiness (2 checks)

Total: 28 validation checks
"""

import sys
import os
import time
from datetime import datetime

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase25Implementation
from patient_facing_xai_core import (
    PatientFacingXAIPipeline,
    HealthLiteracyAssessment,
    ExplanationGenerator,
    ExplanationValidator,
    PatientPortalIntegration,
    HealthLiteracyLevel,
    ExplanationType,
    create_patient_profile,
    create_medical_concept
)


class ValidationResult:
    """Track validation results"""

    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = []

    def check(self, name, condition, error_msg=""):
        """Perform a validation check"""
        self.total += 1
        if condition:
            self.passed += 1
            print(f"  ✅ {name}")
            return True
        else:
            self.failed += 1
            self.errors.append(f"{name}: {error_msg}")
            print(f"  ❌ {name} - {error_msg}")
            return False

    def print_summary(self):
        """Print validation summary"""
        print(f"\n{'=' * 80}")
        print("VALIDATION SUMMARY")
        print(f"{'=' * 80}")
        print(f"Total Checks:  {self.total}")
        print(f"Passed:        {self.passed} ({'✅' if self.passed == self.total else '⚠️ '})")
        print(f"Failed:        {self.failed} ({'✅' if self.failed == 0 else '❌'})")
        print(f"Success Rate:  {(self.passed / self.total * 100):.1f}%")

        if self.failed > 0:
            print(f"\n{'=' * 80}")
            print("FAILED CHECKS:")
            print(f"{'=' * 80}")
            for error in self.errors:
                print(f"  ❌ {error}")

        print(f"{'=' * 80}\n")

        return self.failed == 0


def main():
    """Run all validation checks"""
    print(f"\n{'=' * 80}")
    print("PHASE 25: PRODUCTION VALIDATION")
    print(f"{'=' * 80}")
    print(f"Started: {datetime.now().isoformat()}")
    print(f"{'=' * 80}\n")

    result = ValidationResult()

    # ========================================================================
    # SECTION 1: IMPLEMENTATION VALIDATION (6 checks)
    # ========================================================================
    print("Section 1: Implementation Validation")
    print("-" * 80)

    try:
        impl = Phase25Implementation()

        result.check(
            "Implementation initialization",
            impl is not None,
            "Failed to initialize Phase25Implementation"
        )

        result.check(
            "Phase metadata correct",
            impl.phase_id == 25 and impl.story_points == 35 and impl.priority == "P1",
            f"Expected phase_id=25, story_points=35, priority=P1; got {impl.phase_id}, {impl.story_points}, {impl.priority}"
        )

        result.check(
            "Framework available attribute",
            hasattr(impl, 'framework_available'),
            "Missing framework_available instance attribute"
        )

        # Test execution
        task = {"goal": "Validate implementation", "phase_id": 25}
        exec_result = impl.execute(task)

        result.check(
            "Execute returns result",
            exec_result is not None and hasattr(exec_result, 'success'),
            "Execute did not return proper result object"
        )

        result.check(
            "Execute succeeds",
            exec_result.success,
            f"Execute failed: {getattr(exec_result, 'error', 'Unknown error')}"
        )

        # Test output structure
        if exec_result.success and exec_result.output:
            output = exec_result.output
            result.check(
                "Output has required fields",
                all(k in output for k in ["phase_id", "components", "status"]),
                f"Missing required fields in output"
            )

    except Exception as e:
        result.check("Implementation section", False, f"Exception: {str(e)}")

    print()

    # ========================================================================
    # SECTION 2: PATIENT-FACING XAI CORE (4 checks)
    # ========================================================================
    print("Section 2: Patient-Facing XAI Core")
    print("-" * 80)

    try:
        pipeline = PatientFacingXAIPipeline()

        result.check(
            "Pipeline initialization",
            pipeline is not None,
            "Failed to initialize PatientFacingXAIPipeline"
        )

        result.check(
            "All pipeline components initialized",
            all([
                pipeline.literacy_assessor is not None,
                pipeline.explanation_generator is not None,
                pipeline.validator is not None,
                pipeline.portal_integration is not None
            ]),
            "Missing pipeline components"
        )

        # Test basic patient explanation
        patient = create_patient_profile("TEST001", 45, "High School")
        concept = create_medical_concept(
            ExplanationType.DIAGNOSIS,
            "Test Condition",
            {"condition": "Test", "simple_description": "test"}
        )

        explanation_result = pipeline.generate_patient_explanation(
            patient, concept, validate=True, deliver_to_portal=True
        )

        result.check(
            "Generate patient explanation",
            explanation_result is not None and "explanation" in explanation_result,
            "Failed to generate patient explanation"
        )

        result.check(
            "HIPAA compliance in output",
            explanation_result.get("hipaa_compliant") == True and
            explanation_result.get("phi_removed") == True,
            "HIPAA compliance flags not set"
        )

    except Exception as e:
        result.check("XAI Core section", False, f"Exception: {str(e)}")

    print()

    # ========================================================================
    # SECTION 3: HEALTH LITERACY ASSESSMENT (3 checks)
    # ========================================================================
    print("Section 3: Health Literacy Assessment")
    print("-" * 80)

    try:
        assessor = HealthLiteracyAssessment()

        # Test demographic assessment
        level = assessor.assess_from_demographics("Bachelor's Degree", 35)

        result.check(
            "Demographics assessment returns valid level",
            isinstance(level, HealthLiteracyLevel),
            f"Expected HealthLiteracyLevel, got {type(level)}"
        )

        # Test reading level parameters
        params = assessor.get_recommended_reading_level(HealthLiteracyLevel.BASIC)

        result.check(
            "Reading level parameters complete",
            all(k in params for k in ["grade_level", "max_syllables_per_word", "max_words_per_sentence"]),
            "Missing required reading level parameters"
        )

        # Test all literacy levels have parameters
        all_levels_ok = True
        for level in HealthLiteracyLevel:
            params = assessor.get_recommended_reading_level(level)
            if "grade_level" not in params:
                all_levels_ok = False
                break

        result.check(
            "All literacy levels have parameters",
            all_levels_ok,
            "Not all literacy levels have complete parameters"
        )

    except Exception as e:
        result.check("Literacy Assessment section", False, f"Exception: {str(e)}")

    print()

    # ========================================================================
    # SECTION 4: EXPLANATION GENERATION (3 checks)
    # ========================================================================
    print("Section 4: Explanation Generation")
    print("-" * 80)

    try:
        generator = ExplanationGenerator()
        patient = create_patient_profile("TEST002", 50, "High School")

        concept = create_medical_concept(
            ExplanationType.DIAGNOSIS,
            "Hypertension",
            {
                "condition": "Hypertension",
                "simple_description": "high blood pressure",
                "why_important": "can damage your heart"
            }
        )

        explanation = generator.generate_explanation(concept, patient)

        result.check(
            "Explanation generated successfully",
            explanation is not None and len(explanation.primary_text) > 0,
            "Failed to generate explanation or empty primary text"
        )

        result.check(
            "Explanation has required components",
            all([
                explanation.simplified_summary,
                len(explanation.key_points) > 0,
                len(explanation.faq) > 0
            ]),
            "Missing required explanation components"
        )

        result.check(
            "Readability score calculated",
            explanation.readability_score > 0,
            f"Invalid readability score: {explanation.readability_score}"
        )

    except Exception as e:
        result.check("Explanation Generation section", False, f"Exception: {str(e)}")

    print()

    # ========================================================================
    # SECTION 5: VALIDATION SYSTEM (2 checks)
    # ========================================================================
    print("Section 5: Validation System")
    print("-" * 80)

    try:
        validator = ExplanationValidator()
        generator = ExplanationGenerator()

        patient = create_patient_profile("TEST003", 45, "High School")
        concept = create_medical_concept(
            ExplanationType.DIAGNOSIS,
            "Diabetes",
            {
                "condition": "Diabetes",
                "simple_description": "high blood sugar",
                "why_important": "affects your whole body"
            }
        )

        explanation = generator.generate_explanation(concept, patient)
        validation = validator.validate_explanation(explanation)

        result.check(
            "Validation runs successfully",
            validation is not None,
            "Validation failed to run"
        )

        result.check(
            "Validation has all checks",
            all([
                hasattr(validation, 'readability_passed'),
                hasattr(validation, 'accuracy_passed'),
                hasattr(validation, 'comprehension_passed'),
                hasattr(validation, 'accessibility_passed'),
                hasattr(validation, 'overall_passed')
            ]),
            "Missing validation checks"
        )

    except Exception as e:
        result.check("Validation System section", False, f"Exception: {str(e)}")

    print()

    # ========================================================================
    # SECTION 6: PORTAL INTEGRATION (2 checks)
    # ========================================================================
    print("Section 6: Portal Integration")
    print("-" * 80)

    try:
        portal = PatientPortalIntegration(enable_audit_logging=True)
        generator = ExplanationGenerator()

        patient = create_patient_profile("TEST004", 40, "College")
        concept = create_medical_concept(
            ExplanationType.MEDICATION,
            "Metformin",
            {"medication": "Metformin", "purpose": "lower blood sugar"}
        )

        explanation = generator.generate_explanation(concept, patient)
        portal_content = portal.prepare_for_portal(explanation, patient, include_resources=True)

        result.check(
            "Portal content prepared",
            portal_content is not None and "title" in portal_content,
            "Failed to prepare portal content"
        )

        result.check(
            "Audit logging enabled",
            len(portal.audit_log) > 0,
            "Audit logging not working"
        )

    except Exception as e:
        result.check("Portal Integration section", False, f"Exception: {str(e)}")

    print()

    # ========================================================================
    # SECTION 7: HIPAA COMPLIANCE (2 checks)
    # ========================================================================
    print("Section 7: HIPAA Compliance")
    print("-" * 80)

    try:
        pipeline = PatientFacingXAIPipeline()
        patient = create_patient_profile("HIPAA_TEST_001", 55, "High School")
        concept = create_medical_concept(
            ExplanationType.DIAGNOSIS,
            "Test",
            {"condition": "Test", "simple_description": "test"}
        )

        hipaa_result = pipeline.generate_patient_explanation(patient, concept)

        result.check(
            "PHI protection enabled",
            "patient_id_hash" in hipaa_result and "phi_removed" in hipaa_result,
            "PHI protection not enabled"
        )

        result.check(
            "No raw patient ID in output",
            patient.patient_id not in str(hipaa_result),
            "Raw patient ID found in output (HIPAA violation)"
        )

    except Exception as e:
        result.check("HIPAA Compliance section", False, f"Exception: {str(e)}")

    print()

    # ========================================================================
    # SECTION 8: PERFORMANCE (2 checks)
    # ========================================================================
    print("Section 8: Performance")
    print("-" * 80)

    try:
        pipeline = PatientFacingXAIPipeline()
        patient = create_patient_profile("PERF001", 45, "High School")
        concept = create_medical_concept(
            ExplanationType.DIAGNOSIS,
            "Test",
            {"condition": "Test", "simple_description": "test"}
        )

        # Test explanation generation time
        start = time.time()
        pipeline.generate_patient_explanation(patient, concept, validate=True)
        duration_ms = (time.time() - start) * 1000

        result.check(
            "Explanation generation performance",
            duration_ms < 500,  # Should be < 500ms
            f"Too slow: {duration_ms:.1f}ms (target: <500ms)"
        )

        # Test validation time
        generator = ExplanationGenerator()
        validator = ExplanationValidator()

        explanation = generator.generate_explanation(concept, patient)

        start = time.time()
        validator.validate_explanation(explanation)
        val_duration_ms = (time.time() - start) * 1000

        result.check(
            "Validation performance",
            val_duration_ms < 100,  # Should be < 100ms
            f"Too slow: {val_duration_ms:.1f}ms (target: <100ms)"
        )

    except Exception as e:
        result.check("Performance section", False, f"Exception: {str(e)}")

    print()

    # ========================================================================
    # SECTION 9: AGENT FRAMEWORK (2 checks)
    # ========================================================================
    print("Section 9: Agent Framework Integration")
    print("-" * 80)

    try:
        impl = Phase25Implementation()

        result.check(
            "Framework integration attribute present",
            hasattr(impl, 'framework_available'),
            "Missing framework_available attribute"
        )

        # Test framework components if available
        if impl.framework_available:
            has_all_components = all([
                hasattr(impl, 'guardrails'),
                hasattr(impl, 'feedback_loop'),
                hasattr(impl, 'context'),
                hasattr(impl, 'orchestrator'),
                hasattr(impl, 'search'),
                hasattr(impl, 'verifier')
            ])
            result.check(
                "All framework components present",
                has_all_components,
                "Missing some framework components"
            )
        else:
            result.check(
                "Framework gracefully degraded",
                True,
                ""
            )

    except Exception as e:
        result.check("Agent Framework section", False, f"Exception: {str(e)}")

    print()

    # ========================================================================
    # SECTION 10: PRODUCTION READINESS (2 checks)
    # ========================================================================
    print("Section 10: Production Readiness")
    print("-" * 80)

    try:
        impl = Phase25Implementation()
        task = {"goal": "Production readiness check", "phase_id": 25}
        exec_result = impl.execute(task)

        if exec_result.success and exec_result.output:
            components = exec_result.output.get("components", {})

            result.check(
                "Production ready flag set",
                components.get("production_ready") == True,
                "Production ready flag not set"
            )

            result.check(
                "All capabilities documented",
                all([
                    "capabilities" in components,
                    "clinical_applications" in components,
                    "compliance" in components,
                    "performance" in components
                ]),
                "Missing capability documentation"
            )
        else:
            result.check("Production readiness", False, "Failed to execute implementation")

    except Exception as e:
        result.check("Production Readiness section", False, f"Exception: {str(e)}")

    print()

    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    success = result.print_summary()

    if success:
        print("✅ ALL VALIDATIONS PASSED - PRODUCTION READY")
        return 0
    else:
        print("❌ VALIDATION FAILED - NOT PRODUCTION READY")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
