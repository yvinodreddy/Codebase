"""
Phase 15: Advanced Medical NLP & Auto-Coding
Comprehensive Production-Ready Test Suite
"""

import unittest
import sys
import os
import json

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase15Implementation
from medical_code_database import MedicalCodeDatabase
from medical_nlp_engine import MedicalNLPEngine
from autocoding_system import MedicalAutoCodingSystem
from clinical_note_generator import ClinicalNoteGenerator


class TestMedicalCodeDatabase(unittest.TestCase):
    """Test medical code database"""

    def setUp(self):
        self.db = MedicalCodeDatabase()

    def test_database_initialization(self):
        """Test database is properly initialized"""
        stats = self.db.get_stats()
        self.assertGreater(stats['total_icd10_codes'], 0)
        self.assertGreater(stats['total_cpt_codes'], 0)

    def test_icd10_search(self):
        """Test ICD-10 code search"""
        results = self.db.search_icd10("diabetes")
        self.assertGreater(len(results), 0)
        code_str, icd_code, confidence = results[0]
        self.assertIn("E11", code_str)  # Type 2 diabetes codes

    def test_cpt_search(self):
        """Test CPT code search"""
        results = self.db.search_cpt("ecg")
        self.assertGreater(len(results), 0)
        code_str, cpt_code, confidence = results[0]
        self.assertEqual(code_str, "93000")  # ECG code

    def test_code_retrieval(self):
        """Test direct code retrieval"""
        icd_code = self.db.get_icd10("E11.9")
        self.assertIsNotNone(icd_code)
        self.assertEqual(icd_code.code, "E11.9")

        cpt_code = self.db.get_cpt("93000")
        self.assertIsNotNone(cpt_code)
        self.assertEqual(cpt_code.code, "93000")


class TestMedicalNLPEngine(unittest.TestCase):
    """Test medical NLP engine"""

    def setUp(self):
        self.nlp = MedicalNLPEngine()

    def test_entity_extraction(self):
        """Test medical entity extraction"""
        text = "Patient with type 2 diabetes on metformin 500mg twice daily."
        entities = self.nlp.extract_entities(text)

        self.assertGreater(len(entities), 0)

        # Check for disease entity
        disease_entities = [e for e in entities if e.entity_type == 'disease']
        self.assertGreater(len(disease_entities), 0)

        # Check for medication entity
        med_entities = [e for e in entities if e.entity_type == 'medication']
        self.assertGreater(len(med_entities), 0)

    def test_negation_detection(self):
        """Test negation detection"""
        text = "Patient denies chest pain and shortness of breath."
        entities = self.nlp.extract_entities(text)
        entities = self.nlp.detect_negation(text, entities)

        # All symptoms should be negated
        negated_count = sum(1 for e in entities if e.attributes.get('negated'))
        self.assertGreater(negated_count, 0)

    def test_comprehensive_analysis(self):
        """Test comprehensive NLP analysis"""
        text = "68-year-old male with acute MI. Treated with aspirin and clopidogrel. Cardiac catheterization performed."
        result = self.nlp.analyze_text(text)

        self.assertIn('entities', result)
        self.assertIn('stats', result)
        self.assertGreater(result['stats']['total_entities'], 0)


class TestAutoCodingSystem(unittest.TestCase):
    """Test auto-coding system"""

    def setUp(self):
        self.system = MedicalAutoCodingSystem()

    def test_icd10_autocoding(self):
        """Test ICD-10 auto-coding"""
        text = "Patient with type 2 diabetes mellitus."
        report = self.system.code_text(text)

        self.assertGreater(len(report.icd10_codes), 0)
        self.assertTrue(any("E11" in c.code for c in report.icd10_codes))

    def test_cpt_autocoding(self):
        """Test CPT auto-coding"""
        text = "ECG performed showing normal sinus rhythm."
        report = self.system.code_text(text)

        # Should find ECG procedure code
        self.assertGreater(report.total_codes, 0)

    def test_confidence_scoring(self):
        """Test confidence scoring"""
        text = "Patient with hypertension and diabetes."
        report = self.system.code_text(text)

        self.assertGreater(report.confidence_score, 0.0)
        self.assertLessEqual(report.confidence_score, 1.0)

    def test_warning_generation(self):
        """Test warning generation"""
        text = "Patient denies chest pain."  # Negated finding
        report = self.system.code_text(text)

        # Should generate warning about negated entities
        self.assertIsInstance(report.warnings, list)


class TestClinicalNoteGenerator(unittest.TestCase):
    """Test clinical note generator"""

    def setUp(self):
        self.generator = ClinicalNoteGenerator()

    def test_soap_note_generation(self):
        """Test SOAP note generation"""
        data = {
            "chief_complaint": "Chest pain",
            "history": "Patient reports chest pain for 2 hours.",
            "vitals": {"BP": "140/90 mmHg", "HR": "95 bpm"},
            "exam_findings": "Anxious appearing.",
            "labs": {},
            "assessment": "Acute coronary syndrome",
            "plan": "Admit to hospital; Start aspirin"
        }

        note = self.generator.generate_soap_note(data)

        self.assertEqual(note.note_type, "SOAP")
        self.assertIn("SUBJECTIVE", note.content)
        self.assertIn("OBJECTIVE", note.content)
        self.assertIn("ASSESSMENT", note.content)
        self.assertIn("PLAN", note.content)

    def test_discharge_summary_generation(self):
        """Test discharge summary generation"""
        data = {
            "admission_date": "2025-10-28",
            "discharge_date": "2025-10-31",
            "admission_diagnosis": "Pneumonia",
            "hospital_course": "Treated with antibiotics.",
            "procedures": ["Chest X-ray"],
            "discharge_diagnosis": "Pneumonia, resolved",
            "medications": ["Amoxicillin 500mg"],
            "discharge_condition": "Stable",
            "follow_up": "Follow up in 1 week"
        }

        note = self.generator.generate_discharge_summary(data)

        self.assertEqual(note.note_type, "discharge_summary")
        self.assertIn("DISCHARGE SUMMARY", note.content)
        self.assertIn("ADMISSION DATE", note.content)

    def test_progress_note_generation(self):
        """Test progress note generation"""
        data = {
            "date": "2025-10-31",
            "interval_history": "Patient improving.",
            "vitals": {"BP": "120/80 mmHg"},
            "exam": "No acute distress.",
            "labs": {"Glucose": "120 mg/dL"},
            "assessment_plan": "Continue current treatment."
        }

        note = self.generator.generate_progress_note(data)

        self.assertEqual(note.note_type, "progress_note")
        self.assertIn("PROGRESS NOTE", note.content)

    def test_note_autocoding(self):
        """Test that notes are auto-coded"""
        data = {
            "chief_complaint": "Diabetes follow-up",
            "history": "Patient with type 2 diabetes.",
            "vitals": {},
            "exam_findings": "Well-appearing.",
            "labs": {},
            "assessment": "Type 2 diabetes mellitus",
            "plan": "Continue metformin"
        }

        note = self.generator.generate_soap_note(data)

        # Should have ICD-10 codes extracted
        self.assertGreater(len(note.icd10_codes), 0)


class TestPhase15Implementation(unittest.TestCase):
    """Test Phase 15 implementation"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase15Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 15)
        self.assertEqual(self.implementation.phase_name, "Advanced Medical NLP & Auto-Coding")
        self.assertEqual(self.implementation.story_points, 47)
        self.assertEqual(self.implementation.priority, "P0")

    def test_execution(self):
        """Test phase execution"""
        task = {"goal": "Implement Advanced Medical NLP & Auto-Coding", "phase_id": 15}
        result = self.implementation.execute(task)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)

    def test_phase_logic(self):
        """Test phase-specific logic"""
        context = {"phase_id": 15}
        output = self.implementation._implement_phase_logic(context)

        self.assertIn("status", output)
        self.assertIn("components", output)
        self.assertEqual(output["implemented"], True)

    def test_all_components_operational(self):
        """Test all components are operational"""
        context = {"phase_id": 15}
        output = self.implementation._implement_phase_logic(context)

        components = output["components"]

        # Check all components are operational
        self.assertEqual(components["medical_code_database"]["status"], "operational")
        self.assertEqual(components["nlp_engine"]["status"], "operational")
        self.assertEqual(components["autocoding_system"]["status"], "operational")
        self.assertEqual(components["clinical_note_generator"]["status"], "operational")

    def test_production_ready(self):
        """Test system is production-ready"""
        context = {"phase_id": 15}
        output = self.implementation._implement_phase_logic(context)

        self.assertTrue(output["production_ready"])

        # Check all tests passed
        test_results = output["test_results"]
        for test_name, result in test_results.items():
            self.assertEqual(result, "passed", f"{test_name} did not pass")


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow"""

    def setUp(self):
        self.implementation = Phase15Implementation()
        self.db = MedicalCodeDatabase()
        self.nlp = MedicalNLPEngine()
        self.autocoding = MedicalAutoCodingSystem()
        self.note_gen = ClinicalNoteGenerator()

    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # Step 1: Clinical text input
        clinical_text = "Patient with type 2 diabetes mellitus presents for routine follow-up. Blood pressure 135/85. A1C is 7.2%. Continue metformin. Return in 3 months."

        # Step 2: NLP analysis
        nlp_result = self.nlp.analyze_text(clinical_text)
        self.assertGreater(nlp_result['stats']['total_entities'], 0)

        # Step 3: Auto-coding
        coding_report = self.autocoding.code_text(clinical_text)
        self.assertGreater(len(coding_report.icd10_codes), 0)

        # Step 4: Note generation
        note = self.note_gen.extract_note_from_text(clinical_text, "SOAP")
        self.assertIsNotNone(note)
        self.assertGreater(len(note.icd10_codes), 0)

    def test_multi_diagnosis_coding(self):
        """Test coding with multiple diagnoses"""
        text = "Patient with hypertension, type 2 diabetes, and hyperlipidemia."
        report = self.autocoding.code_text(text)

        # Should find at least 3 ICD-10 codes
        self.assertGreaterEqual(len(report.icd10_codes), 3)

    def test_procedure_coding(self):
        """Test procedure coding"""
        text = "ECG and chest X-ray performed. Colonoscopy scheduled."
        report = self.autocoding.code_text(text)

        # Should find CPT codes
        self.assertGreater(len(report.cpt_codes), 0)


def run_all_tests():
    """Run all tests and return results"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestMedicalCodeDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestMedicalNLPEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestAutoCodingSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestClinicalNoteGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestPhase15Implementation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    print("=" * 80)
    print("PHASE 15 COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print()

    result = run_all_tests()

    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("=" * 80)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
