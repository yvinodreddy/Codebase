"""
Comprehensive Test Suite for Guardrail System
Tests all 7 layers with medical-specific scenarios
"""

import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from guardrails.multi_layer_system import MultiLayerGuardrailSystem
from guardrails.azure_content_safety import (
    AzureContentSafetyValidator,
    PromptShieldsValidator,
    GroundednessDetector
)
from guardrails.medical_guardrails import (
    PHIDetector,
    HIPAAComplianceValidator,
    MedicalTerminologyValidator,
    MedicalFactChecker
)
from guardrails.crewai_guardrails import (
    medical_knowledge_extraction_guardrail,
    clinical_case_synthesis_guardrail,
    medical_dialogue_guardrail,
    compliance_validation_guardrail,
    podcast_script_guardrail,
    quality_assurance_guardrail
)


# ==========================================
# FIXTURES
# ==========================================

@pytest.fixture
def guardrail_system():
    """Create guardrail system instance."""
    return MultiLayerGuardrailSystem()


@pytest.fixture
def phi_detector():
    """Create PHI detector instance."""
    return PHIDetector()


@pytest.fixture
def hipaa_validator():
    """Create HIPAA validator instance."""
    return HIPAAComplianceValidator()


@pytest.fixture
def terminology_validator():
    """Create terminology validator instance."""
    return MedicalTerminologyValidator()


@pytest.fixture
def fact_checker():
    """Create fact checker instance."""
    return MedicalFactChecker()


# ==========================================
# LAYER 3 TESTS: PHI DETECTION
# ==========================================

class TestPHIDetection:
    """Test PHI detection functionality."""

    def test_no_phi_in_clean_text(self, phi_detector):
        """Test that clean medical text passes PHI detection."""
        clean_text = "This anonymized case discusses diabetes management and cardiovascular health."
        result = phi_detector.detect_phi(clean_text)
        assert result.passed is True

    def test_detect_email_address(self, phi_detector):
        """Test detection of email addresses (PHI)."""
        text_with_email = "Patient email: john.doe@hospital.com for follow-up."
        result = phi_detector.detect_phi(text_with_email)
        assert result.passed is False
        assert "email" in str(result.details)

    def test_detect_phone_number(self, phi_detector):
        """Test detection of phone numbers (PHI)."""
        text_with_phone = "Contact patient at 555-123-4567"
        result = phi_detector.detect_phi(text_with_phone)
        assert result.passed is False
        assert "phone" in str(result.details)

    def test_detect_ssn(self, phi_detector):
        """Test detection of SSN (PHI)."""
        text_with_ssn = "Patient SSN: 123-45-6789"
        result = phi_detector.detect_phi(text_with_ssn)
        assert result.passed is False
        assert "ssn" in str(result.details)

    def test_detect_medical_record_number(self, phi_detector):
        """Test detection of medical record numbers (PHI)."""
        text_with_mrn = "Medical Record Number: MRN123456"
        result = phi_detector.detect_phi(text_with_mrn)
        assert result.passed is False


# ==========================================
# LAYER 7 TESTS: HIPAA COMPLIANCE
# ==========================================

class TestHIPAACompliance:
    """Test HIPAA compliance validation."""

    def test_educational_content_with_disclaimer(self, hipaa_validator):
        """Test that educational content with disclaimer passes."""
        content = """
        This is an anonymized educational case for medical training purposes.
        This is not medical advice. Always consult with a healthcare provider.
        """
        result = hipaa_validator.validate_compliance(content, "medical_education")
        assert result.passed is True

    def test_clinical_case_without_anonymization(self, hipaa_validator):
        """Test that clinical case without anonymization fails."""
        content = """
        This case presents a real patient with diabetes.
        Treatment recommendations follow.
        """
        result = hipaa_validator.validate_compliance(content, "clinical_case")
        assert result.passed is False

    def test_prohibited_terms_detected(self, hipaa_validator):
        """Test detection of prohibited terms."""
        content = """
        This is the actual patient name and real patient data.
        Not anonymized.
        """
        result = hipaa_validator.validate_compliance(content)
        assert result.passed is False


# ==========================================
# LAYER 4 TESTS: MEDICAL TERMINOLOGY
# ==========================================

class TestMedicalTerminology:
    """Test medical terminology validation."""

    def test_sufficient_medical_terminology(self, terminology_validator):
        """Test that content with sufficient medical terms passes."""
        medical_content = """
        The patient presented with cardiology issues including arrhythmia.
        Neurological examination revealed no deficits.
        Gastroenterology consultation recommended for hepatitis screening.
        Dermatology noted no concerning lesions.
        Hematology workup was within normal limits.
        """
        result = terminology_validator.validate_terminology(medical_content)
        assert result.passed is True

    def test_insufficient_medical_terminology(self, terminology_validator):
        """Test that content without medical terms fails."""
        non_medical_content = """
        The person felt sick and went to the hospital.
        The doctor said everything was okay.
        """
        result = terminology_validator.validate_terminology(non_medical_content)
        assert result.passed is False


# ==========================================
# LAYER 7 TESTS: MEDICAL FACT CHECKING
# ==========================================

class TestMedicalFactChecking:
    """Test medical fact-checking functionality."""

    def test_factually_correct_content(self, fact_checker):
        """Test that factually correct content passes."""
        correct_content = """
        According to current clinical guidelines, diabetes management includes
        monitoring blood glucose levels. Evidence-based research shows that
        lifestyle modifications improve outcomes. Studies indicate regular
        exercise benefits cardiovascular health.
        """
        result = fact_checker.check_medical_facts(correct_content)
        assert result.passed is True

    def test_detect_known_incorrect_claim(self, fact_checker):
        """Test detection of known incorrect medical claims."""
        incorrect_content = """
        Vaccines cause autism according to recent studies.
        Antibiotics cure viral infections effectively.
        """
        result = fact_checker.check_medical_facts(incorrect_content)
        assert result.passed is False

    def test_no_evidence_based_language(self, fact_checker):
        """Test warning for lack of evidence-based language."""
        content_without_evidence = """
        Diabetes is managed with insulin.
        Heart disease requires treatment.
        """
        result = fact_checker.check_medical_facts(content_without_evidence)
        # Should pass but with warnings
        assert result.passed is True
        if result.details:
            assert "warnings" in result.details


# ==========================================
# INTEGRATION TESTS: MULTI-LAYER SYSTEM
# ==========================================

class TestMultiLayerSystem:
    """Test complete multi-layer guardrail system."""

    def test_safe_medical_input(self, guardrail_system):
        """Test that safe medical input passes all layers."""
        safe_input = "What are the current guidelines for diabetes management?"
        result = guardrail_system.process_with_guardrails(
            user_input=safe_input,
            content_type="medical_query"
        )
        assert result["success"] is True
        assert result["blocked_at"] is None

    def test_input_with_phi(self, guardrail_system):
        """Test that input with PHI is blocked at Layer 3."""
        phi_input = "Patient John Doe, email john@email.com, has diabetes."
        result = guardrail_system.process_with_guardrails(
            user_input=phi_input
        )
        assert result["success"] is False
        assert "layer_3" in result["blocked_at"]

    def test_safe_medical_output(self, guardrail_system):
        """Test that safe medical output passes all layers."""
        safe_input = "Generate diabetes educational content"
        safe_output = """
        This anonymized educational content discusses diabetes management
        for educational purposes. This is not medical advice.

        Diabetes management includes:
        - Cardiology monitoring for cardiovascular complications
        - Nephrology assessment for kidney function
        - Ophthalmology screening for retinopathy
        - Neurology evaluation for neuropathy
        - Endocrinology consultation for metabolic control

        According to current clinical guidelines and evidence-based research,
        comprehensive diabetes care improves patient outcomes.
        """
        result = guardrail_system.process_with_guardrails(
            user_input=safe_input,
            output=safe_output,
            content_type="medical_education"
        )
        assert result["success"] is True

    def test_output_with_incorrect_medical_facts(self, guardrail_system):
        """Test that output with incorrect medical facts is blocked."""
        safe_input = "Generate medical information"
        incorrect_output = """
        Medical information shows that vaccines cause autism.
        Antibiotics cure viral infections like the common cold.
        """
        result = guardrail_system.process_with_guardrails(
            user_input=safe_input,
            output=incorrect_output,
            content_type="medical_education"
        )
        assert result["success"] is False
        assert "layer_7" in result["blocked_at"]


# ==========================================
# CREWAI GUARDRAIL TESTS
# ==========================================

class TestCrewAIGuardrails:
    """Test CrewAI-specific guardrail functions."""

    def test_medical_knowledge_extraction_guardrail(self):
        """Test medical knowledge extraction guardrail."""
        safe_output = """
        Medical knowledge extraction results:
        - Patient demographics: Anonymized
        - Conditions: Type 2 diabetes, hypertension, hyperlipidemia
        - Medications: Metformin, lisinopril, atorvastatin
        - Observations: HbA1c 7.2%, BP 130/85, LDL 110 mg/dL

        This is anonymized educational content for medical training purposes.
        """
        # Simulate TaskOutput
        class MockTaskOutput:
            def __str__(self):
                return safe_output

        passed, result = medical_knowledge_extraction_guardrail(MockTaskOutput())
        assert passed is True

    def test_clinical_case_synthesis_guardrail(self):
        """Test clinical case synthesis guardrail."""
        safe_case = """
        Anonymized Clinical Case Presentation

        This is a de-identified educational case for medical training.

        Chief Complaint: 65-year-old patient with dyspnea on exertion
        History: Type 2 diabetes mellitus, hypertension, hyperlipidemia
        Medications: Metformin, lisinopril, atorvastatin

        This case is for educational purposes only and does not constitute
        medical advice. Always consult with a healthcare provider.
        """

        class MockTaskOutput:
            def __str__(self):
                return safe_case

        passed, result = clinical_case_synthesis_guardrail(MockTaskOutput())
        assert passed is True

    def test_medical_dialogue_guardrail(self):
        """Test medical dialogue guardrail."""
        safe_dialogue = """
        Doctor-Patient Dialogue (Anonymized Educational Content)

        Doctor: Good morning. How are you feeling today?
        Patient: I've been managing my diabetes better with the new medication.
        Doctor: That's excellent. According to your recent HbA1c results,
                your blood sugar control has improved significantly.
        Patient: Thank you for the guidance.

        This is educational content, not medical advice.
        """

        class MockTaskOutput:
            def __str__(self):
                return safe_dialogue

        passed, result = medical_dialogue_guardrail(MockTaskOutput())
        assert passed is True

    def test_podcast_script_guardrail(self):
        """Test podcast script guardrail."""
        safe_script = """
        Medical Education Podcast Script

        Introduction:
        Welcome to our educational podcast on diabetes management.
        This content is for educational purposes and is not medical advice.

        [Host]: Today we discuss an anonymized case study about diabetes care.
        [Expert]: According to evidence-based guidelines, comprehensive
                 diabetes management includes regular monitoring...

        Disclaimer: This podcast provides educational information only.
        Always consult your healthcare provider for personalized medical advice.
        """

        class MockTaskOutput:
            def __str__(self):
                return safe_script

        passed, result = podcast_script_guardrail(MockTaskOutput())
        assert passed is True


# ==========================================
# PERFORMANCE TESTS
# ==========================================

class TestPerformance:
    """Test guardrail system performance and statistics."""

    def test_statistics_tracking(self, guardrail_system):
        """Test that statistics are properly tracked."""
        initial_stats = guardrail_system.get_statistics()
        initial_total = initial_stats["total_requests"]

        # Process a request
        guardrail_system.process_with_guardrails(
            user_input="Test medical query about diabetes management"
        )

        updated_stats = guardrail_system.get_statistics()
        assert updated_stats["total_requests"] == initial_total + 1

    def test_reset_statistics(self, guardrail_system):
        """Test statistics reset functionality."""
        # Process some requests
        guardrail_system.process_with_guardrails(
            user_input="Test query 1"
        )
        guardrail_system.process_with_guardrails(
            user_input="Test query 2"
        )

        # Reset
        guardrail_system.reset_statistics()

        stats = guardrail_system.get_statistics()
        assert stats["total_requests"] == 0
        assert stats["successful"] == 0


# ==========================================
# RUN TESTS
# ==========================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
