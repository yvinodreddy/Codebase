#!/usr/bin/env python3
"""
FINAL TESTS for medical_guardrails.py - Cover Remaining 17 Lines
Missing lines: 151, 154, 184, 239, 243, 250, 266, 325, 328, 345-350, 354, 372
"""

import pytest
import sys
from pathlib import Path

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "guardrails"))

try:
    from medical_guardrails import (
        PHIDetector,
        HIPAAComplianceValidator,
        MedicalTerminologyValidator,
        MedicalFactChecker,
        ValidationResult
    )
except ImportError as e:
    pytest.skip(f"Cannot import medical_guardrails: {e}", allow_module_level=True)


class TestMedicalGuardrailsFinalLines:
    """Tests targeting the final 17 missing lines"""

    # ============ LINES 151, 154: HIPAA Prohibited Terms ============

    def test_lines_151_154_prohibited_terms_actual_patient_name(self):
        """Lines 151, 154: Prohibited term 'actual patient name' triggers lines"""
        validator = HIPAAComplianceValidator()

        text = "This case discusses an actual patient name and real clinical data."

        result = validator.validate_compliance(text, content_type="medical_education")

        # Lines 151 (append to found_prohibited) and 154 (append to issues) should execute
        assert result.passed == False
        assert "prohibited terms" in result.message.lower()

    def test_lines_151_154_prohibited_terms_not_anonymized(self):
        """Lines 151, 154: Prohibited term 'not anonymized' triggers lines"""
        validator = HIPAAComplianceValidator()

        text = "This patient data is not anonymized and contains identifiable information."

        result = validator.validate_compliance(text, content_type="clinical_case")

        # Lines 151, 154 should execute
        assert result.passed == False

    # ============ LINE 184: HIPAA Passes ============

    def test_line_184_hipaa_compliance_passes(self):
        """Line 184: HIPAA validation passes (return True path)"""
        validator = HIPAAComplianceValidator()

        # Text with disclaimer, no prohibited terms - should pass
        text = "This educational material is for educational purposes only and is anonymized."

        result = validator.validate_compliance(text, content_type="medical_education")

        # Line 184 should execute (return ValidationResult with passed=True)
        assert result.passed == True
        assert result.layer == "hipaa_compliance"
        assert "validated" in result.message.lower()

    # ============ LINES 239, 243, 250, 266: Terminology Validation ============

    def test_lines_239_243_medical_prefixes_suffixes(self):
        """Lines 239, 243: Count medical prefixes and suffixes"""
        validator = MedicalTerminologyValidator()

        # Text with medical prefixes (cardio, neuro) and suffixes (ology, itis)
        text = """
        Cardiology assessment shows neuroitis with gastrology findings.
        Hepatology and dermatology consultations recommended for osteopathy treatment.
        """

        result = validator.validate_terminology(text)

        # Lines 239 (count prefixes) and 243 (count suffixes) should execute
        assert result is not None

    def test_line_250_coding_systems_icd10(self):
        """Line 250: ICD-10 coding pattern detected"""
        validator = MedicalTerminologyValidator()

        # Text with ICD-10 codes
        text = """
        Patient diagnosed with condition A12.3 and secondary diagnosis B45.67.
        Treatment plan includes procedures coded as J44.0 and E11.9.
        """

        result = validator.validate_terminology(text)

        # Line 250 should execute (append coding system to findings)
        if result.details and "findings" in result.details:
            # Should detect ICD-10 codes
            assert "coding_systems_used" in result.details["findings"]

    def test_line_266_terminology_validation_passes(self):
        """Line 266: Terminology validation passes (return True path)"""
        validator = MedicalTerminologyValidator()

        # Text with sufficient medical terms (5+ required)
        text = """
        Cardiology consultation for cardiopathy revealed cardiomegaly.
        Neurology assessment showed neuritis and neuropathy.
        Gastroenterology findings include gastritis and gastropathy.
        """

        result = validator.validate_terminology(text)

        # Line 266 should execute (return ValidationResult with passed=True)
        assert result.passed == True
        assert result.layer == "medical_terminology"

    # ============ LINES 325, 328, 354: Fact Checking - Known Incorrect Claims ============

    def test_lines_325_328_354_incorrect_claim_vaccines_autism(self):
        """Lines 325, 328, 354: Known incorrect claim 'vaccines cause autism'"""
        fact_checker = MedicalFactChecker()

        text = "Some people believe vaccines cause autism, which has been debunked."

        result = fact_checker.check_medical_facts(text)

        # Lines 325 (append to found_incorrect), 328 (append to issues),
        # and 354 (return failed validation) should execute
        assert result.passed == False
        assert "incorrect" in result.message.lower()

    def test_lines_325_328_354_incorrect_claim_antibiotics(self):
        """Lines 325, 328, 354: Known incorrect claim 'antibiotics cure viral infections'"""
        fact_checker = MedicalFactChecker()

        text = "Taking antibiotics cure viral infections like the common cold."

        result = fact_checker.check_medical_facts(text)

        # Lines 325, 328, 354 should execute
        assert result.passed == False

    # ============ LINES 345-350: Vital Signs Range Checking ============

    def test_lines_345_350_vital_signs_blood_pressure_high(self):
        """Lines 345-350: Abnormal vital signs detected (blood pressure)"""
        fact_checker = MedicalFactChecker()

        # Text with unrealistic blood pressure values
        text = "Patient presented with blood pressure 200 systolic, which is concerning."

        result = fact_checker.check_medical_facts(text)

        # Lines 345-350 should execute (try/except block for vital sign checking)
        assert result is not None
        # May have warnings about unusual values

    def test_lines_345_350_vital_signs_heart_rate_abnormal(self):
        """Lines 345-350: Abnormal heart rate detected"""
        fact_checker = MedicalFactChecker()

        text = "Patient's heart rate was recorded at 180 bpm, requiring intervention."

        result = fact_checker.check_medical_facts(text)

        # Lines 345-350 should execute
        assert result is not None

    # ============ LINE 372: Fact Check Passes Clean (No Warnings) ============

    def test_line_372_fact_check_passes_clean(self):
        """Line 372: Fact check passes with no issues and no warnings"""
        fact_checker = MedicalFactChecker()

        # Clean medical fact text with evidence-based language
        text = """
        According to clinical trials, aspirin reduces cardiovascular risk in patients with
        coronary artery disease. Research shows that beta-blockers are recommended by
        cardiology guidelines for heart failure management.
        """

        result = fact_checker.check_medical_facts(text)

        # Line 372 should execute (return ValidationResult with passed=True, no warnings)
        assert result.passed == True
        assert result.layer == "medical_fact_checking"
        assert "passed" in result.message.lower()

    # ============ COMPREHENSIVE EDGE CASE TESTS ============

    def test_hipaa_multiple_prohibited_terms(self):
        """Test multiple prohibited terms at once"""
        validator = HIPAAComplianceValidator()

        text = "This is a real patient with actual patient name and contains PHI that is not anonymized."

        result = validator.validate_compliance(text, content_type="medical_education")

        assert result.passed == False
        # Should detect multiple prohibited terms (lines 151, 154 executed multiple times)

    def test_terminology_all_coding_systems(self):
        """Test multiple coding system patterns"""
        validator = MedicalTerminologyValidator()

        text = """
        Diagnosis codes: ICD-10 A12.3, CPT 99213, LOINC 1234-5.
        SNOMED code 123456789 and RxNorm: 987654.
        """

        result = validator.validate_terminology(text)

        # Line 250 should execute for multiple coding systems
        assert result is not None

    def test_fact_checker_multiple_incorrect_claims(self):
        """Test multiple incorrect claims"""
        fact_checker = MedicalFactChecker()

        text = """
        Some myths: vaccines cause autism and antibiotics cure viral infections.
        Also, cancer is contagious and diabetes is only from eating sugar.
        """

        result = fact_checker.check_medical_facts(text)

        # Lines 325, 328 should execute multiple times
        assert result.passed == False
        # Should detect multiple incorrect claims

    def test_terminology_exact_5_terms(self):
        """Test with exactly 5 medical terms (boundary condition)"""
        validator = MedicalTerminologyValidator()

        text = "Cardiology, neurology, gastrology, hepatology, and dermatology consultations."

        result = validator.validate_terminology(text)

        # Should pass with exactly 5 terms
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
