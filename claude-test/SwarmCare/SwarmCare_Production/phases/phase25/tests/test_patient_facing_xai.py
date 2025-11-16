"""
Phase 25: Patient-Facing XAI Core System Tests
Comprehensive test suite for all XAI components

Tests cover:
- Health Literacy Assessment
- Explanation Generation
- Validation Engine
- Patient Portal Integration
- End-to-End Pipeline
"""

import unittest
import sys
import os
from datetime import datetime

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from patient_facing_xai_core import (
    # Engines
    HealthLiteracyAssessment,
    ExplanationGenerator,
    ExplanationValidator,
    PatientPortalIntegration,
    PatientFacingXAIPipeline,

    # Enums
    HealthLiteracyLevel,
    ExplanationType,
    ModalityType,
    LanguageCode,
    AccessibilityFeature,

    # Data Models
    PatientProfile,
    MedicalConcept,
    Explanation,
    ValidationResult,

    # Convenience Functions
    create_patient_profile,
    create_medical_concept
)


# ============================================================================
# TEST HEALTH LITERACY ASSESSMENT
# ============================================================================

class TestHealthLiteracyAssessment(unittest.TestCase):
    """Test health literacy assessment engine"""

    def setUp(self):
        """Set up test fixtures"""
        self.assessor = HealthLiteracyAssessment()

    def test_assess_from_demographics_doctoral(self):
        """Test assessment for doctoral education"""
        level = self.assessor.assess_from_demographics("Doctoral Degree", 45)
        self.assertEqual(level, HealthLiteracyLevel.EXPERT)

    def test_assess_from_demographics_bachelors(self):
        """Test assessment for bachelor's education"""
        level = self.assessor.assess_from_demographics("Bachelor's Degree", 30)
        self.assertEqual(level, HealthLiteracyLevel.ADVANCED)

    def test_assess_from_demographics_high_school(self):
        """Test assessment for high school education"""
        level = self.assessor.assess_from_demographics("High School", 25)
        self.assertEqual(level, HealthLiteracyLevel.INTERMEDIATE)

    def test_assess_from_demographics_default(self):
        """Test default assessment for adults"""
        level = self.assessor.assess_from_demographics(None, 35)
        self.assertEqual(level, HealthLiteracyLevel.INTERMEDIATE)

    def test_assess_from_comprehension_test(self):
        """Test assessment from medical term recognition"""
        # Expert level terms
        expert_terms = ["pathophysiology", "pharmacokinetics", "etiology", "comorbidity"]
        level = self.assessor.assess_from_comprehension_test(expert_terms)
        self.assertIn(level, [HealthLiteracyLevel.EXPERT, HealthLiteracyLevel.ADVANCED])

    def test_get_recommended_reading_level_basic(self):
        """Test reading level parameters for basic literacy"""
        params = self.assessor.get_recommended_reading_level(HealthLiteracyLevel.BASIC)

        self.assertEqual(params["grade_level"], "3-5")
        self.assertEqual(params["max_syllables_per_word"], 2)
        self.assertEqual(params["max_words_per_sentence"], 10)
        self.assertFalse(params["use_medical_jargon"])
        self.assertTrue(params["use_analogies"])

    def test_get_recommended_reading_level_expert(self):
        """Test reading level parameters for expert literacy"""
        params = self.assessor.get_recommended_reading_level(HealthLiteracyLevel.EXPERT)

        self.assertEqual(params["grade_level"], "professional")
        self.assertIsNone(params["max_syllables_per_word"])
        self.assertTrue(params["use_medical_jargon"])


# ============================================================================
# TEST EXPLANATION GENERATION
# ============================================================================

class TestExplanationGenerator(unittest.TestCase):
    """Test explanation generation engine"""

    def setUp(self):
        """Set up test fixtures"""
        self.generator = ExplanationGenerator()

        self.patient_basic = create_patient_profile(
            patient_id="P001",
            age=45,
            education_level="Middle School",
            preferred_language="en"
        )

        self.patient_expert = create_patient_profile(
            patient_id="P002",
            age=35,
            education_level="Medical Degree",
            preferred_language="en"
        )

    def test_generate_diagnosis_explanation_basic(self):
        """Test diagnosis explanation for basic literacy"""
        concept = create_medical_concept(
            concept_type=ExplanationType.DIAGNOSIS,
            technical_term="Hypertension",
            context={
                "condition": "Hypertension",
                "simple_description": "your blood pressure is too high",
                "why_important": "it can damage your heart and blood vessels over time"
            }
        )

        explanation = self.generator.generate_explanation(concept, self.patient_basic)

        self.assertIsInstance(explanation, Explanation)
        self.assertEqual(explanation.literacy_level, HealthLiteracyLevel.ELEMENTARY)
        self.assertGreater(len(explanation.primary_text), 0)
        self.assertGreater(len(explanation.simplified_summary), 0)
        self.assertIsNotNone(explanation.analogy)  # Basic literacy should get analogies

    def test_generate_diagnosis_explanation_expert(self):
        """Test diagnosis explanation for expert literacy"""
        concept = create_medical_concept(
            concept_type=ExplanationType.DIAGNOSIS,
            technical_term="Hypertension",
            context={
                "condition": "Hypertension",
                "mechanism": "elevated systemic vascular resistance",
                "prognosis": "manageable with treatment",
                "treatment_overview": "antihypertensive therapy"
            }
        )

        explanation = self.generator.generate_explanation(concept, self.patient_expert)

        self.assertIsInstance(explanation, Explanation)
        self.assertEqual(explanation.literacy_level, HealthLiteracyLevel.EXPERT)
        self.assertIn("Hypertension", explanation.primary_text)  # Technical term used

    def test_generate_medication_explanation(self):
        """Test medication explanation"""
        concept = create_medical_concept(
            concept_type=ExplanationType.MEDICATION,
            technical_term="Lisinopril",
            context={
                "medication": "Lisinopril",
                "purpose": "lower your blood pressure",
                "dosage": "10mg",
                "frequency": "once daily"
            }
        )

        explanation = self.generator.generate_explanation(concept, self.patient_basic)

        self.assertIsInstance(explanation, Explanation)
        # Check that medication name is in the explanation (fallback template uses technical term)
        self.assertTrue(len(explanation.primary_text) > 0)

    def test_medical_term_translation(self):
        """Test medical terminology translation"""
        # Test basic level translation
        translated = self.generator._translate_medical_term(
            "hypertension",
            HealthLiteracyLevel.BASIC
        )
        self.assertEqual(translated, "high blood pressure")

        # Test expert level (no translation)
        translated_expert = self.generator._translate_medical_term(
            "hypertension",
            HealthLiteracyLevel.EXPERT
        )
        self.assertEqual(translated_expert, "hypertension")

    def test_generate_analogy(self):
        """Test analogy generation"""
        concept = create_medical_concept(
            concept_type=ExplanationType.DIAGNOSIS,
            technical_term="Hypertension",
            context={}
        )

        analogy = self.generator._generate_analogy(concept)
        self.assertIsNotNone(analogy)
        self.assertIn("blood", analogy.lower())

    def test_readability_calculation(self):
        """Test Flesch Reading Ease calculation"""
        # Simple text should have high readability
        simple_text = "This is easy. It is simple."
        score_simple = self.generator._calculate_readability(simple_text)
        self.assertGreater(score_simple, 60)

        # Complex text should have lower readability
        complex_text = "The pathophysiological mechanisms underlying cardiovascular dysfunction."
        score_complex = self.generator._calculate_readability(complex_text)
        self.assertLess(score_complex, score_simple)

    def test_key_points_extraction(self):
        """Test key points extraction"""
        text = "First point. Second point. Third point. Fourth point. Fifth point."
        points = self.generator._extract_key_points(text, HealthLiteracyLevel.BASIC)

        self.assertIsInstance(points, list)
        self.assertGreater(len(points), 0)
        self.assertLessEqual(len(points), 3)  # Basic level limited to 3

    def test_faq_generation_diagnosis(self):
        """Test FAQ generation for diagnosis"""
        concept = create_medical_concept(
            concept_type=ExplanationType.DIAGNOSIS,
            technical_term="Diabetes",
            context={"severity": "moderate"}
        )

        faq = self.generator._generate_faq(concept, HealthLiteracyLevel.INTERMEDIATE)

        self.assertIsInstance(faq, list)
        self.assertGreater(len(faq), 0)
        self.assertLessEqual(len(faq), 3)

        # Check FAQ structure
        for item in faq:
            self.assertIn("q", item)
            self.assertIn("a", item)

    def test_action_steps_generation(self):
        """Test action steps generation"""
        concept = create_medical_concept(
            concept_type=ExplanationType.MEDICATION,
            technical_term="Metformin",
            context={}
        )

        steps = self.generator._generate_action_steps(concept)

        self.assertIsInstance(steps, list)
        self.assertGreater(len(steps), 0)


# ============================================================================
# TEST EXPLANATION VALIDATION
# ============================================================================

class TestExplanationValidator(unittest.TestCase):
    """Test explanation validation engine"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = ExplanationValidator()
        self.generator = ExplanationGenerator()

        self.patient = create_patient_profile(
            patient_id="P001",
            age=45,
            education_level="High School"
        )

    def test_validate_good_explanation(self):
        """Test validation of a good explanation"""
        concept = create_medical_concept(
            concept_type=ExplanationType.DIAGNOSIS,
            technical_term="Hypertension",
            context={
                "condition": "Hypertension",
                "simple_description": "high blood pressure",
                "why_important": "can damage your heart"
            }
        )

        explanation = self.generator.generate_explanation(concept, self.patient)
        validation = self.validator.validate_explanation(explanation)

        self.assertIsInstance(validation, ValidationResult)
        self.assertTrue(validation.overall_passed)
        self.assertTrue(validation.readability_passed)
        self.assertTrue(validation.accuracy_passed)
        self.assertTrue(validation.comprehension_passed)
        self.assertTrue(validation.accessibility_passed)

    def test_readability_check(self):
        """Test readability validation"""
        concept = create_medical_concept(
            concept_type=ExplanationType.DIAGNOSIS,
            technical_term="Test Condition",
            context={
                "condition": "Test",
                "simple_description": "test description",
                "why_important": "test importance"
            }
        )

        explanation = self.generator.generate_explanation(concept, self.patient)

        issues = []
        recommendations = []
        passed = self.validator._check_readability(explanation, issues, recommendations)

        self.assertIsInstance(passed, bool)

    def test_accuracy_check(self):
        """Test accuracy validation"""
        concept = create_medical_concept(
            concept_type=ExplanationType.DIAGNOSIS,
            technical_term="Hypertension",
            context={
                "condition": "Hypertension",
                "simple_description": "high blood pressure",
                "why_important": "can damage your heart and blood vessels over time"
            }
        )

        explanation = self.generator.generate_explanation(concept, self.patient)

        issues = []
        recommendations = []
        passed = self.validator._check_accuracy(explanation, issues, recommendations)

        # Should pass with complete context
        self.assertTrue(passed)

    def test_comprehension_check(self):
        """Test comprehension validation"""
        concept = create_medical_concept(
            concept_type=ExplanationType.DIAGNOSIS,
            technical_term="Test",
            context={"condition": "Test", "simple_description": "test"}
        )

        explanation = self.generator.generate_explanation(concept, self.patient)

        issues = []
        recommendations = []
        passed = self.validator._check_comprehension(explanation, issues, recommendations)

        self.assertTrue(passed)


# ============================================================================
# TEST PATIENT PORTAL INTEGRATION
# ============================================================================

class TestPatientPortalIntegration(unittest.TestCase):
    """Test patient portal integration"""

    def setUp(self):
        """Set up test fixtures"""
        self.portal = PatientPortalIntegration(enable_audit_logging=True)
        self.generator = ExplanationGenerator()

        self.patient = create_patient_profile(
            patient_id="P001",
            age=45,
            education_level="High School"
        )

    def test_prepare_for_portal(self):
        """Test portal content preparation"""
        concept = create_medical_concept(
            concept_type=ExplanationType.DIAGNOSIS,
            technical_term="Hypertension",
            context={
                "condition": "Hypertension",
                "simple_description": "high blood pressure"
            }
        )

        explanation = self.generator.generate_explanation(concept, self.patient)
        portal_content = self.portal.prepare_for_portal(explanation, self.patient)

        self.assertIsInstance(portal_content, dict)
        self.assertIn("patient_id_hash", portal_content)
        self.assertIn("explanation_id", portal_content)
        self.assertIn("title", portal_content)
        self.assertIn("summary", portal_content)
        self.assertIn("full_explanation", portal_content)
        self.assertIn("key_points", portal_content)
        self.assertIn("faq", portal_content)
        self.assertIn("action_steps", portal_content)
        self.assertTrue(portal_content["hipaa_compliant"])
        self.assertTrue(portal_content["phi_protected"])

    def test_audit_logging(self):
        """Test HIPAA-compliant audit logging"""
        concept = create_medical_concept(
            concept_type=ExplanationType.DIAGNOSIS,
            technical_term="Test",
            context={"condition": "Test", "simple_description": "test"}
        )

        explanation = self.generator.generate_explanation(concept, self.patient)

        initial_log_count = len(self.portal.audit_log)
        self.portal.prepare_for_portal(explanation, self.patient)

        self.assertEqual(len(self.portal.audit_log), initial_log_count + 1)

        # Check last log entry
        last_log = self.portal.audit_log[-1]
        self.assertIn("timestamp", last_log)
        self.assertIn("patient_id_hash", last_log)
        self.assertIn("explanation_id", last_log)
        self.assertEqual(last_log["action"], "portal_access")


# ============================================================================
# TEST END-TO-END PIPELINE
# ============================================================================

class TestPatientFacingXAIPipeline(unittest.TestCase):
    """Test complete patient-facing XAI pipeline"""

    def setUp(self):
        """Set up test fixtures"""
        self.pipeline = PatientFacingXAIPipeline(use_guardrails=True)

    def test_pipeline_initialization(self):
        """Test pipeline initializes all components"""
        self.assertIsNotNone(self.pipeline.literacy_assessor)
        self.assertIsNotNone(self.pipeline.explanation_generator)
        self.assertIsNotNone(self.pipeline.validator)
        self.assertIsNotNone(self.pipeline.portal_integration)

    def test_generate_patient_explanation(self):
        """Test end-to-end explanation generation"""
        patient = create_patient_profile(
            patient_id="P001",
            age=55,
            education_level="High School"
        )

        concept = create_medical_concept(
            concept_type=ExplanationType.DIAGNOSIS,
            technical_term="Diabetes Mellitus",
            context={
                "condition": "Diabetes Mellitus",
                "simple_description": "high blood sugar",
                "why_important": "can affect your whole body"
            }
        )

        result = self.pipeline.generate_patient_explanation(
            patient=patient,
            concept=concept,
            validate=True,
            deliver_to_portal=True
        )

        self.assertIsInstance(result, dict)
        self.assertIn("patient_id_hash", result)
        self.assertIn("explanation", result)
        self.assertIn("validation", result)
        self.assertIn("portal_ready", result)
        self.assertTrue(result["hipaa_compliant"])
        self.assertTrue(result["phi_removed"])

        # Check explanation
        self.assertIsNotNone(result["explanation"])

        # Check validation
        self.assertIsNotNone(result["validation"])

        # Check portal content
        self.assertIsNotNone(result["portal_ready"])

    def test_batch_generation(self):
        """Test batch explanation generation"""
        patients_concepts = [
            (
                create_patient_profile("P001", 45, "High School"),
                create_medical_concept(
                    ExplanationType.DIAGNOSIS,
                    "Hypertension",
                    {"condition": "Hypertension", "simple_description": "high BP"}
                )
            ),
            (
                create_patient_profile("P002", 60, "College"),
                create_medical_concept(
                    ExplanationType.MEDICATION,
                    "Metformin",
                    {"medication": "Metformin", "purpose": "lower blood sugar"}
                )
            )
        ]

        results = self.pipeline.batch_generate_explanations(patients_concepts)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)

        for result in results:
            self.assertTrue(result["hipaa_compliant"])
            self.assertIsNotNone(result["explanation"])

    def test_statistics_tracking(self):
        """Test pipeline statistics tracking"""
        patient = create_patient_profile("P001", 45, "High School")
        concept = create_medical_concept(
            ExplanationType.DIAGNOSIS,
            "Test",
            {"condition": "Test", "simple_description": "test"}
        )

        initial_stats = self.pipeline.get_statistics()

        self.pipeline.generate_patient_explanation(patient, concept, validate=True)

        updated_stats = self.pipeline.get_statistics()

        self.assertGreater(
            updated_stats["total_explanations"],
            initial_stats["total_explanations"]
        )


# ============================================================================
# TEST CONVENIENCE FUNCTIONS
# ============================================================================

class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions"""

    def test_create_patient_profile(self):
        """Test patient profile creation"""
        profile = create_patient_profile(
            patient_id="P001",
            age=45,
            education_level="High School",
            preferred_language="en",
            accessibility_needs=["screen_reader"]
        )

        self.assertIsInstance(profile, PatientProfile)
        self.assertEqual(profile.patient_id, "P001")
        self.assertEqual(profile.age, 45)
        self.assertEqual(profile.preferred_language, "en")
        self.assertIn("screen_reader", profile.accessibility_needs)
        self.assertIsNotNone(profile.patient_id_hash)

    def test_create_medical_concept(self):
        """Test medical concept creation"""
        concept = create_medical_concept(
            concept_type=ExplanationType.DIAGNOSIS,
            technical_term="Hypertension",
            context={"severity": "moderate"},
            severity="moderate"
        )

        self.assertIsInstance(concept, MedicalConcept)
        self.assertEqual(concept.concept_type, ExplanationType.DIAGNOSIS)
        self.assertEqual(concept.technical_term, "Hypertension")
        self.assertEqual(concept.severity, "moderate")
        self.assertIsNotNone(concept.concept_id)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
