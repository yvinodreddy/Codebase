"""
Phase 18: Clinical Trial Matching
Comprehensive Test Suite

Tests all components:
- DataValidator
- EligibilityChecker
- TrialMatcher
- Phase18Implementation
- Integration tests
- HIPAA compliance tests
"""

import unittest
import sys
import os
from datetime import datetime

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import (
    Phase18Implementation,
    DataValidator,
    EligibilityChecker,
    TrialMatcher,
    Patient,
    ClinicalTrial,
    MatchResult,
    TrialPhase,
    TrialStatus
)


class TestDataValidator(unittest.TestCase):
    """Test DataValidator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = DataValidator()

    def test_valid_patient_data(self):
        """Test validation of valid patient data"""
        patient = Patient(
            patient_id="P001",
            age=45,
            gender='M',
            diagnoses=['Lung Cancer'],
            conditions=['Hypertension'],
            medications=['Lisinopril'],
            allergies=[],
            comorbidities=[],
            biomarkers={'PDL1': 50.0},
            performance_status=1,
            smoking_status='Former'
        )

        valid, message = self.validator.validate_patient_data(patient)
        self.assertTrue(valid)
        self.assertEqual(message, "Validation passed")

    def test_invalid_age(self):
        """Test validation rejects invalid age"""
        patient = Patient(
            patient_id="P002",
            age=150,  # Invalid
            gender='F',
            diagnoses=['Breast Cancer'],
            conditions=[],
            medications=[],
            allergies=[],
            comorbidities=[],
            biomarkers={},
            performance_status=0,
            smoking_status='Never'
        )

        valid, message = self.validator.validate_patient_data(patient)
        self.assertFalse(valid)
        self.assertIn("age", message.lower())

    def test_invalid_gender(self):
        """Test validation rejects invalid gender"""
        patient = Patient(
            patient_id="P003",
            age=50,
            gender='X',  # Invalid
            diagnoses=['Cancer'],
            conditions=[],
            medications=[],
            allergies=[],
            comorbidities=[],
            biomarkers={},
            performance_status=0,
            smoking_status='Never'
        )

        valid, message = self.validator.validate_patient_data(patient)
        self.assertFalse(valid)
        self.assertIn("gender", message.lower())

    def test_invalid_performance_status(self):
        """Test validation rejects invalid ECOG score"""
        patient = Patient(
            patient_id="P004",
            age=60,
            gender='M',
            diagnoses=['Cancer'],
            conditions=[],
            medications=[],
            allergies=[],
            comorbidities=[],
            biomarkers={},
            performance_status=10,  # Invalid (max is 5)
            smoking_status='Never'
        )

        valid, message = self.validator.validate_patient_data(patient)
        self.assertFalse(valid)
        self.assertIn("performance status", message.lower())

    def test_missing_patient_id(self):
        """Test validation rejects missing patient ID"""
        patient = Patient(
            patient_id="",  # Missing
            age=45,
            gender='F',
            diagnoses=['Cancer'],
            conditions=[],
            medications=[],
            allergies=[],
            comorbidities=[],
            biomarkers={},
            performance_status=1,
            smoking_status='Never'
        )

        valid, message = self.validator.validate_patient_data(patient)
        self.assertFalse(valid)
        self.assertIn("patient id", message.lower())

    def test_anonymize_patient_id(self):
        """Test patient ID anonymization (HIPAA compliance)"""
        patient_id = "PATIENT_12345"
        anonymized = self.validator.anonymize_patient_id(patient_id)

        # Check hash is created
        self.assertIsNotNone(anonymized)
        self.assertEqual(len(anonymized), 16)

        # Check original ID is not in hash
        self.assertNotIn(patient_id, anonymized)

        # Check consistency (same input = same output)
        anonymized2 = self.validator.anonymize_patient_id(patient_id)
        self.assertEqual(anonymized, anonymized2)

        # Check uniqueness (different input = different output)
        anonymized3 = self.validator.anonymize_patient_id("DIFFERENT_ID")
        self.assertNotEqual(anonymized, anonymized3)

    def test_valid_trial_data(self):
        """Test validation of valid trial data"""
        trial = ClinicalTrial(
            nct_id="NCT12345678",
            title="Test Trial",
            phase="Phase 2",
            status="Recruiting",
            condition="Lung Cancer",
            intervention="Pembrolizumab",
            sponsor="NCI",
            location="Mayo Clinic",
            eligibility_criteria={},
            enrollment_target=100,
            start_date="2024-01-01"
        )

        valid, message = self.validator.validate_trial_data(trial)
        self.assertTrue(valid)
        self.assertEqual(message, "Validation passed")

    def test_invalid_nct_id_format(self):
        """Test validation rejects invalid NCT ID"""
        trial = ClinicalTrial(
            nct_id="INVALID123",  # Invalid format
            title="Test Trial",
            phase="Phase 1",
            status="Recruiting",
            condition="Cancer",
            intervention="Drug",
            sponsor="Sponsor",
            location="Location",
            eligibility_criteria={},
            enrollment_target=50,
            start_date="2024-01-01"
        )

        valid, message = self.validator.validate_trial_data(trial)
        self.assertFalse(valid)
        self.assertIn("NCT ID", message)

    def test_invalid_trial_phase(self):
        """Test validation rejects invalid trial phase"""
        trial = ClinicalTrial(
            nct_id="NCT11111111",
            title="Test Trial",
            phase="Phase 10",  # Invalid
            status="Recruiting",
            condition="Cancer",
            intervention="Drug",
            sponsor="Sponsor",
            location="Location",
            eligibility_criteria={},
            enrollment_target=50,
            start_date="2024-01-01"
        )

        valid, message = self.validator.validate_trial_data(trial)
        self.assertFalse(valid)
        self.assertIn("phase", message.lower())


class TestEligibilityChecker(unittest.TestCase):
    """Test EligibilityChecker class"""

    def setUp(self):
        """Set up test fixtures"""
        self.checker = EligibilityChecker()

    def test_age_eligibility_met(self):
        """Test age eligibility when criteria are met"""
        eligible, reason = self.checker.check_age_eligibility(
            patient_age=45,
            criteria={'min_age': 18, 'max_age': 75}
        )

        self.assertTrue(eligible)
        self.assertIn("requirement met", reason.lower())

    def test_age_too_young(self):
        """Test age eligibility when patient is too young"""
        eligible, reason = self.checker.check_age_eligibility(
            patient_age=15,
            criteria={'min_age': 18, 'max_age': 75}
        )

        self.assertFalse(eligible)
        self.assertIn("too young", reason.lower())

    def test_age_too_old(self):
        """Test age eligibility when patient is too old"""
        eligible, reason = self.checker.check_age_eligibility(
            patient_age=80,
            criteria={'min_age': 18, 'max_age': 75}
        )

        self.assertFalse(eligible)
        self.assertIn("too old", reason.lower())

    def test_gender_eligibility_all(self):
        """Test gender eligibility when all genders accepted"""
        eligible, reason = self.checker.check_gender_eligibility(
            patient_gender='M',
            criteria={'gender': 'All'}
        )

        self.assertTrue(eligible)
        self.assertIn("all genders", reason.lower())

    def test_gender_eligibility_match(self):
        """Test gender eligibility when gender matches"""
        eligible, reason = self.checker.check_gender_eligibility(
            patient_gender='F',
            criteria={'gender': 'F'}
        )

        self.assertTrue(eligible)

    def test_gender_eligibility_mismatch(self):
        """Test gender eligibility when gender doesn't match"""
        eligible, reason = self.checker.check_gender_eligibility(
            patient_gender='M',
            criteria={'gender': 'F'}
        )

        self.assertFalse(eligible)
        self.assertIn("mismatch", reason.lower())

    def test_condition_match_exact(self):
        """Test condition matching with exact match"""
        match, reason = self.checker.check_condition_match(
            patient_conditions=['Lung Cancer'],
            trial_condition='Lung Cancer'
        )

        self.assertTrue(match)

    def test_condition_match_partial(self):
        """Test condition matching with partial match"""
        match, reason = self.checker.check_condition_match(
            patient_conditions=['Non-Small Cell Lung Cancer'],
            trial_condition='Lung Cancer'
        )

        self.assertTrue(match)

    def test_condition_no_match(self):
        """Test condition matching with no match"""
        match, reason = self.checker.check_condition_match(
            patient_conditions=['Breast Cancer'],
            trial_condition='Lung Cancer'
        )

        self.assertFalse(match)

    def test_performance_status_acceptable(self):
        """Test performance status when acceptable"""
        eligible, reason = self.checker.check_performance_status(
            patient_ps=1,
            criteria={'max_ecog': 2}
        )

        self.assertTrue(eligible)

    def test_performance_status_too_high(self):
        """Test performance status when too high"""
        eligible, reason = self.checker.check_performance_status(
            patient_ps=4,
            criteria={'max_ecog': 2}
        )

        self.assertFalse(eligible)

    def test_biomarker_eligibility_met(self):
        """Test biomarker eligibility when criteria met"""
        eligible, met, failed = self.checker.check_biomarker_eligibility(
            patient_biomarkers={'PDL1': 50.0, 'EGFR': 2.0},
            required_biomarkers={
                'PDL1': {'min': 1.0, 'max': 100.0},
                'EGFR': {'min': 0.0, 'max': 10.0}
            }
        )

        self.assertTrue(eligible)
        self.assertEqual(len(met), 2)
        self.assertEqual(len(failed), 0)

    def test_biomarker_missing(self):
        """Test biomarker eligibility when biomarker missing"""
        eligible, met, failed = self.checker.check_biomarker_eligibility(
            patient_biomarkers={'PDL1': 50.0},
            required_biomarkers={
                'PDL1': {'min': 1.0, 'max': 100.0},
                'ALK': {'min': 0.0, 'max': 5.0}
            }
        )

        self.assertFalse(eligible)
        self.assertEqual(len(failed), 1)
        self.assertIn("ALK", failed[0])

    def test_exclusion_criteria_medication(self):
        """Test exclusion criteria for medications"""
        patient = Patient(
            patient_id="P001",
            age=50,
            gender='M',
            diagnoses=[],
            conditions=[],
            medications=['Warfarin', 'Aspirin'],
            allergies=[],
            comorbidities=[],
            biomarkers={},
            performance_status=1,
            smoking_status='Never'
        )

        eligible, reasons = self.checker.check_exclusion_criteria(
            patient,
            exclusions={'medications': ['Warfarin']}
        )

        self.assertFalse(eligible)
        self.assertEqual(len(reasons), 1)
        self.assertIn("Warfarin", reasons[0])

    def test_exclusion_criteria_smoking(self):
        """Test exclusion criteria for smoking status"""
        patient = Patient(
            patient_id="P002",
            age=50,
            gender='M',
            diagnoses=[],
            conditions=[],
            medications=[],
            allergies=[],
            comorbidities=[],
            biomarkers={},
            performance_status=1,
            smoking_status='Current'
        )

        eligible, reasons = self.checker.check_exclusion_criteria(
            patient,
            exclusions={'smoking': 'current'}
        )

        self.assertFalse(eligible)
        self.assertIn("smoker", reasons[0].lower())


class TestTrialMatcher(unittest.TestCase):
    """Test TrialMatcher class"""

    def setUp(self):
        """Set up test fixtures"""
        self.matcher = TrialMatcher()
        self.sample_trials = self._create_sample_trials()

    def _create_sample_trials(self):
        """Create sample trials for testing"""
        return [
            ClinicalTrial(
                nct_id="NCT10000001",
                title="Lung Cancer Study",
                phase="Phase 2",
                status="Recruiting",
                condition="Lung Cancer",
                intervention="Pembrolizumab",
                sponsor="NCI",
                location="Mayo Clinic, Rochester, MN",
                eligibility_criteria={
                    'min_age': 18,
                    'max_age': 75,
                    'gender': 'All',
                    'max_ecog': 2,
                    'biomarkers': {},
                    'exclusions': {}
                },
                enrollment_target=100,
                start_date="2024-01-01"
            ),
            ClinicalTrial(
                nct_id="NCT10000002",
                title="Breast Cancer Study",
                phase="Phase 3",
                status="Recruiting",
                condition="Breast Cancer",
                intervention="Chemotherapy",
                sponsor="NCI",
                location="MD Anderson, Houston, TX",
                eligibility_criteria={
                    'min_age': 21,
                    'max_age': 80,
                    'gender': 'F',
                    'max_ecog': 1,
                    'biomarkers': {},
                    'exclusions': {}
                },
                enrollment_target=150,
                start_date="2024-02-01"
            )
        ]

    def test_load_trials(self):
        """Test loading trials into database"""
        count = self.matcher.load_trials(self.sample_trials)

        self.assertEqual(count, 2)
        self.assertEqual(len(self.matcher.trials_database), 2)

    def test_search_trials_by_condition(self):
        """Test searching trials by condition"""
        self.matcher.load_trials(self.sample_trials)

        results = self.matcher.search_trials(condition="Lung Cancer")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].nct_id, "NCT10000001")

    def test_search_trials_by_status(self):
        """Test searching trials by status"""
        self.matcher.load_trials(self.sample_trials)

        results = self.matcher.search_trials(status="Recruiting")

        self.assertEqual(len(results), 2)

    def test_match_patient_to_trials(self):
        """Test matching patient to trials"""
        self.matcher.load_trials(self.sample_trials)

        patient = Patient(
            patient_id="P001",
            age=45,
            gender='M',
            diagnoses=['Lung Cancer'],
            conditions=['Lung Cancer'],
            medications=[],
            allergies=[],
            comorbidities=[],
            biomarkers={},
            performance_status=1,
            smoking_status='Never'
        )

        matches = self.matcher.match_patient_to_trials(patient, min_score=0.70)

        self.assertGreater(len(matches), 0)
        self.assertIsInstance(matches[0], MatchResult)

    def test_generate_matching_report(self):
        """Test generating matching report"""
        patient = Patient(
            patient_id="P001",
            age=50,
            gender='F',
            diagnoses=['Breast Cancer'],
            conditions=['Breast Cancer'],
            medications=[],
            allergies=[],
            comorbidities=[],
            biomarkers={},
            performance_status=0,
            smoking_status='Never'
        )

        matches = [
            MatchResult(
                patient_id="hashed_id",
                nct_id="NCT10000002",
                trial_title="Breast Cancer Study",
                match_score=0.95,
                eligibility_met=True,
                matched_criteria=["Age", "Gender", "Condition"],
                failed_criteria=[],
                recommendation="Highly Recommended"
            )
        ]

        report = self.matcher.generate_matching_report(patient, matches)

        self.assertIn('patient_id', report)
        self.assertIn('total_matches', report)
        self.assertIn('summary', report)
        self.assertEqual(report['total_matches'], 1)
        self.assertEqual(report['summary']['highly_recommended'], 1)


class TestPhase18Implementation(unittest.TestCase):
    """Test Phase18Implementation class"""

    def setUp(self):
        """Set up test fixtures"""
        self.impl = Phase18Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.impl.phase_id, 18)
        self.assertEqual(self.impl.phase_name, "Clinical Trial Matching")
        self.assertEqual(self.impl.story_points, 38)
        self.assertEqual(self.impl.priority, "P1")
        self.assertTrue(self.impl.is_initialized)

    def test_validator_initialized(self):
        """Test validator is properly initialized"""
        self.assertIsNotNone(self.impl.validator)

    def test_trial_matcher_initialized(self):
        """Test trial matcher is properly initialized"""
        self.assertIsNotNone(self.impl.trial_matcher)

    def test_eligibility_checker_initialized(self):
        """Test eligibility checker is properly initialized"""
        self.assertIsNotNone(self.impl.eligibility_checker)

    def test_generate_sample_trials(self):
        """Test generating sample trials"""
        trials = self.impl.generate_sample_trials(n_trials=5)

        self.assertEqual(len(trials), 5)
        self.assertIsInstance(trials[0], ClinicalTrial)
        self.assertTrue(trials[0].nct_id.startswith("NCT"))

    def test_generate_sample_patient(self):
        """Test generating sample patient"""
        patient = self.impl.generate_sample_patient("TEST_P001")

        self.assertIsInstance(patient, Patient)
        self.assertEqual(patient.patient_id, "TEST_P001")
        self.assertGreater(patient.age, 0)
        self.assertIn(patient.gender, ['M', 'F', 'Other'])

    def test_run_matching_demo(self):
        """Test running matching demonstration"""
        results = self.impl.run_matching_demo()

        self.assertIn('phase_info', results)
        self.assertIn('execution_summary', results)
        self.assertIn('matching_report', results)
        self.assertEqual(results['status'], 'SUCCESS')

    def test_get_stats(self):
        """Test getting implementation statistics"""
        stats = self.impl.get_stats()

        self.assertEqual(stats['phase_id'], 18)
        self.assertEqual(stats['phase_name'], "Clinical Trial Matching")
        self.assertEqual(stats['story_points'], 38)
        self.assertIn('features', stats)


class TestIntegration(unittest.TestCase):
    """Integration tests"""

    def test_end_to_end_matching_workflow(self):
        """Test complete end-to-end matching workflow"""
        impl = Phase18Implementation()

        # Generate data
        trials = impl.generate_sample_trials(n_trials=10)
        patient = impl.generate_sample_patient("INTEGRATION_TEST_001")

        # Load trials
        count = impl.trial_matcher.load_trials(trials)
        self.assertGreater(count, 0)

        # Search trials
        matching_trials = impl.trial_matcher.search_trials(
            condition="Lung Cancer"
        )
        self.assertGreater(len(matching_trials), 0)

        # Match patient
        matches = impl.trial_matcher.match_patient_to_trials(
            patient,
            trials=matching_trials,
            min_score=0.50
        )

        # Generate report
        report = impl.trial_matcher.generate_matching_report(patient, matches)

        # Verify report structure
        self.assertIn('patient_id', report)
        self.assertIn('total_matches', report)
        self.assertIn('summary', report)

    def test_hipaa_compliance_workflow(self):
        """Test HIPAA compliance in workflow"""
        impl = Phase18Implementation()
        patient = impl.generate_sample_patient("HIPAA_TEST_001")

        # Original ID
        original_id = patient.patient_id

        # Anonymize
        anonymized_id = impl.validator.anonymize_patient_id(original_id)

        # Verify anonymization
        self.assertNotEqual(original_id, anonymized_id)
        self.assertNotIn(original_id, anonymized_id)

        # Match patient (which internally anonymizes)
        trials = impl.generate_sample_trials(5)
        impl.trial_matcher.load_trials(trials)
        matches = impl.trial_matcher.match_patient_to_trials(patient)

        # Verify all matches use anonymized ID
        for match in matches:
            self.assertNotEqual(match.patient_id, original_id)


def run_tests():
    """Run all tests and return summary"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestEligibilityChecker))
    suite.addTests(loader.loadTestsFromTestCase(TestTrialMatcher))
    suite.addTests(loader.loadTestsFromTestCase(TestPhase18Implementation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Calculate statistics
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    passed = total_tests - failures - errors - skipped
    success_rate = (passed / total_tests * 100) if total_tests > 0 else 0

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests Run: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    print(f"Skipped: {skipped}")
    print(f"Success Rate: {success_rate:.2f}%")
    print("=" * 80)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
