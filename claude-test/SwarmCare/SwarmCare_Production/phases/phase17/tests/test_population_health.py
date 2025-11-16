#!/usr/bin/env python3
"""
Phase 17: Population Health Management
Comprehensive test suite for population health core system
"""

import unittest
import sys
import os
from datetime import date, datetime, timedelta

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from population_health_core import (
    # Classes
    RiskStratificationEngine, CareGapsEngine, QualityMeasuresEngine,
    PopulationHealthPipeline,
    # Data classes
    PatientDemographics, Diagnosis, Medication, HealthcareEncounter,
    LabResult, RiskScore, CareGap, QualityMeasure, Intervention,
    # Enums
    RiskTier, CareGapType, QualityMeasureType, InterventionPriority,
    # Functions
    create_sample_patient
)


class TestRiskStratificationEngine(unittest.TestCase):
    """Test risk stratification engine"""

    def setUp(self):
        self.engine = RiskStratificationEngine()

    def test_initialization(self):
        """Test engine initializes correctly"""
        self.assertIsNotNone(self.engine)
        self.assertIsInstance(self.engine.HCC_WEIGHTS, dict)

    def test_hcc_risk_calculation(self):
        """Test HCC risk score calculation"""
        patient_data = create_sample_patient()

        risk_score = self.engine.calculate_hcc_risk(
            patient_data['patient_id'],
            patient_data['demographics'],
            patient_data['diagnoses'],
            patient_data['encounters']
        )

        self.assertIsInstance(risk_score, RiskScore)
        self.assertEqual(risk_score.patient_id, patient_data['patient_id'])
        self.assertGreater(risk_score.risk_score, 0)
        self.assertLessEqual(risk_score.risk_score, 100)
        self.assertIsInstance(risk_score.risk_tier, RiskTier)

    def test_age_sex_factor(self):
        """Test age-sex adjustment calculation"""
        # Test young patient
        young_score = self.engine._calculate_age_sex_factor(25, 'M')
        self.assertGreater(young_score, 0)

        # Test elderly patient
        elderly_score = self.engine._calculate_age_sex_factor(75, 'M')
        self.assertGreater(elderly_score, young_score)

    def test_utilization_factor(self):
        """Test healthcare utilization factor"""
        encounters = [
            HealthcareEncounter("ENC001", "inpatient", date.today(), None, "I50.9", 25000),
            HealthcareEncounter("ENC002", "ed", date.today(), None, "I50.9", 3500),
        ]

        score = self.engine._calculate_utilization_factor(encounters)
        self.assertGreater(score, 0)

    def test_risk_tier_determination(self):
        """Test risk tier assignment"""
        self.assertEqual(self.engine._determine_risk_tier(10), RiskTier.LOW)
        self.assertEqual(self.engine._determine_risk_tier(30), RiskTier.MEDIUM)
        self.assertEqual(self.engine._determine_risk_tier(50), RiskTier.HIGH)
        self.assertEqual(self.engine._determine_risk_tier(70), RiskTier.VERY_HIGH)
        self.assertEqual(self.engine._determine_risk_tier(90), RiskTier.CATASTROPHIC)

    def test_cost_projection(self):
        """Test annual cost projection"""
        encounters = [
            HealthcareEncounter("ENC001", "inpatient", date.today(), None, "I50.9", 25000)
        ]

        projected_cost = self.engine._project_annual_cost(50, encounters)
        self.assertGreater(projected_cost, 0)


class TestCareGapsEngine(unittest.TestCase):
    """Test care gaps identification engine"""

    def setUp(self):
        self.engine = CareGapsEngine()

    def test_initialization(self):
        """Test engine initializes correctly"""
        self.assertIsNotNone(self.engine)

    def test_identify_gaps(self):
        """Test comprehensive care gap identification"""
        patient_data = create_sample_patient()

        gaps = self.engine.identify_gaps(
            patient_data['patient_id'],
            patient_data['demographics'],
            patient_data['diagnoses'],
            patient_data['medications'],
            patient_data['encounters'],
            patient_data['lab_results']
        )

        self.assertIsInstance(gaps, list)
        self.assertGreater(len(gaps), 0)
        for gap in gaps:
            self.assertIsInstance(gap, CareGap)
            self.assertIsInstance(gap.gap_type, CareGapType)

    def test_preventive_screening_gaps(self):
        """Test preventive screening gap identification"""
        demographics = PatientDemographics("PATIENT-001", 55, "F")
        encounters = []

        gaps = self.engine._check_preventive_screenings("PATIENT-001", demographics, encounters)

        # Should find breast cancer screening gap
        self.assertGreater(len(gaps), 0)
        has_bcs = any("Breast Cancer" in gap.measure_name for gap in gaps)
        self.assertTrue(has_bcs)

    def test_chronic_disease_monitoring(self):
        """Test chronic disease monitoring gaps"""
        diagnoses = [
            Diagnosis("E11.9", "Type 2 Diabetes", date(2020, 1, 1), is_chronic=True)
        ]
        lab_results = []

        gaps = self.engine._check_chronic_disease_monitoring("PATIENT-001", diagnoses, lab_results)

        # Should find HbA1c gap for diabetic patient
        self.assertGreater(len(gaps), 0)
        has_hba1c = any("HbA1c" in gap.measure_name for gap in gaps)
        self.assertTrue(has_hba1c)

    def test_medication_adherence_gaps(self):
        """Test medication adherence gap detection"""
        medications = [
            Medication("Metformin", "00093-7214", date(2020, 1, 1), is_active=True, adherence_rate=0.65)
        ]

        gaps = self.engine._check_medication_adherence("PATIENT-001", medications)

        # Should find adherence gap (< 80%)
        self.assertGreater(len(gaps), 0)
        self.assertEqual(gaps[0].gap_type, CareGapType.MEDICATION_ADHERENCE)

    def test_vaccination_gaps(self):
        """Test vaccination gap identification"""
        demographics = PatientDemographics("PATIENT-001", 70, "M")
        encounters = []

        gaps = self.engine._check_vaccinations("PATIENT-001", demographics, encounters)

        # Should find both flu and pneumonia vaccine gaps
        self.assertGreater(len(gaps), 0)


class TestQualityMeasuresEngine(unittest.TestCase):
    """Test quality measures engine"""

    def setUp(self):
        self.engine = QualityMeasuresEngine()

    def test_initialization(self):
        """Test engine initializes correctly"""
        self.assertIsNotNone(self.engine)

    def test_hedis_measures_calculation(self):
        """Test HEDIS measures calculation"""
        population_data = [create_sample_patient() for _ in range(10)]

        measures = self.engine.calculate_hedis_measures(population_data)

        self.assertIsInstance(measures, list)
        self.assertGreater(len(measures), 0)
        for measure in measures:
            self.assertIsInstance(measure, QualityMeasure)
            self.assertEqual(measure.measure_type, QualityMeasureType.HEDIS)

    def test_diabetes_care_measure(self):
        """Test comprehensive diabetes care measure"""
        population_data = [create_sample_patient() for _ in range(5)]

        measure = self.engine._calculate_diabetes_care(population_data)

        self.assertEqual(measure.measure_id, "HEDIS_CDC")
        self.assertGreaterEqual(measure.denominator, 0)
        self.assertGreaterEqual(measure.numerator, 0)
        self.assertLessEqual(measure.numerator, measure.denominator)


class TestPopulationHealthPipeline(unittest.TestCase):
    """Test main population health pipeline"""

    def setUp(self):
        self.pipeline = PopulationHealthPipeline(use_guardrails=False)

    def test_initialization(self):
        """Test pipeline initializes correctly"""
        self.assertIsNotNone(self.pipeline)
        self.assertIsInstance(self.pipeline.risk_engine, RiskStratificationEngine)
        self.assertIsInstance(self.pipeline.gaps_engine, CareGapsEngine)
        self.assertIsInstance(self.pipeline.quality_engine, QualityMeasuresEngine)

    def test_analyze_patient(self):
        """Test single patient analysis"""
        patient_data = create_sample_patient()

        analysis = self.pipeline.analyze_patient(
            patient_data['patient_id'],
            patient_data['demographics'],
            patient_data['diagnoses'],
            patient_data['medications'],
            patient_data['encounters'],
            patient_data['lab_results']
        )

        self.assertIsInstance(analysis, dict)
        self.assertIn('risk_assessment', analysis)
        self.assertIn('care_gaps', analysis)
        self.assertIn('interventions', analysis)
        self.assertTrue(analysis['hipaa_compliant'])
        self.assertTrue(analysis['phi_removed'])

    def test_analyze_population(self):
        """Test population-level analysis"""
        population_data = [create_sample_patient() for _ in range(10)]

        # Modify patient IDs to be unique
        for i, patient in enumerate(population_data):
            patient['patient_id'] = f"PATIENT-{i+1:03d}"
            patient['demographics'].patient_id = f"PATIENT-{i+1:03d}"

        analysis = self.pipeline.analyze_population(population_data)

        self.assertIsInstance(analysis, dict)
        self.assertEqual(analysis['population_size'], 10)
        self.assertIn('metrics', analysis)
        self.assertIn('quality_measures', analysis)
        self.assertIn('cohorts', analysis)

    def test_generate_interventions(self):
        """Test intervention generation"""
        risk_score = RiskScore(
            patient_id="PATIENT-001",
            risk_tier=RiskTier.VERY_HIGH,
            risk_score=75.0,
            risk_model="HCC",
            contributing_factors=["Multiple chronic conditions"],
            projected_annual_cost=50000.0,
            confidence_score=0.85
        )

        care_gaps = [
            CareGap(
                gap_id="GAP-001",
                patient_id="PATIENT-001",
                gap_type=CareGapType.PREVENTIVE_SCREENING,
                measure_name="BCS",
                description="Mammogram overdue",
                due_date=date.today(),
                priority=InterventionPriority.HIGH,
                recommended_action="Schedule mammogram"
            )
        ]

        interventions = self.pipeline._generate_interventions("PATIENT-001", risk_score, care_gaps)

        self.assertIsInstance(interventions, list)
        self.assertGreater(len(interventions), 0)
        for intervention in interventions:
            self.assertIsInstance(intervention, Intervention)

    def test_hipaa_compliance(self):
        """Test HIPAA compliance in analysis"""
        patient_data = create_sample_patient()

        analysis = self.pipeline.analyze_patient(
            patient_data['patient_id'],
            patient_data['demographics'],
            patient_data['diagnoses'],
            patient_data['medications'],
            patient_data['encounters'],
            patient_data['lab_results']
        )

        # Check PHI protection
        self.assertIn('patient_id_hash', analysis)
        self.assertTrue(analysis['hipaa_compliant'])
        self.assertTrue(analysis['phi_removed'])

        # Ensure patient_id_hash is hashed
        self.assertEqual(len(analysis['patient_id_hash']), 16)


class TestDataClasses(unittest.TestCase):
    """Test data classes"""

    def test_patient_demographics(self):
        """Test PatientDemographics data class"""
        demographics = PatientDemographics("PATIENT-001", 65, "M", date(1959, 1, 1))

        self.assertEqual(demographics.patient_id, "PATIENT-001")
        self.assertEqual(demographics.age, 65)
        self.assertIsNotNone(demographics.patient_id_hash)
        self.assertEqual(len(demographics.patient_id_hash), 16)

    def test_diagnosis(self):
        """Test Diagnosis data class"""
        diagnosis = Diagnosis(
            "E11.9", "Type 2 Diabetes", date(2020, 1, 1),
            is_chronic=True, severity_weight=1.2
        )

        self.assertEqual(diagnosis.icd10_code, "E11.9")
        self.assertTrue(diagnosis.is_chronic)
        self.assertEqual(diagnosis.severity_weight, 1.2)

    def test_lab_result_abnormal(self):
        """Test LabResult abnormality detection"""
        # High HbA1c (abnormal)
        high_hba1c = LabResult("4548-4", "HbA1c", 9.5, "%", 4.0, 5.7)
        self.assertTrue(high_hba1c.is_abnormal)

        # Normal HbA1c
        normal_hba1c = LabResult("4548-4", "HbA1c", 5.2, "%", 4.0, 5.7)
        self.assertFalse(normal_hba1c.is_abnormal)


class TestIntegration(unittest.TestCase):
    """Integration tests"""

    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # Create pipeline
        pipeline = PopulationHealthPipeline(use_guardrails=False)

        # Create sample patient
        patient_data = create_sample_patient()

        # Analyze patient
        analysis = pipeline.analyze_patient(
            patient_data['patient_id'],
            patient_data['demographics'],
            patient_data['diagnoses'],
            patient_data['medications'],
            patient_data['encounters'],
            patient_data['lab_results']
        )

        # Verify complete analysis
        self.assertIn('risk_assessment', analysis)
        self.assertIn('care_gaps', analysis)
        self.assertIn('interventions', analysis)

        # Verify risk assessment
        risk = analysis['risk_assessment']
        self.assertIn('risk_score', risk)
        self.assertIn('risk_tier', risk)
        self.assertIn('projected_annual_cost', risk)

        # Verify care gaps
        self.assertGreater(len(analysis['care_gaps']), 0)

        # Verify interventions
        self.assertGreater(len(analysis['interventions']), 0)

        # Verify HIPAA compliance
        self.assertTrue(analysis['hipaa_compliant'])


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRiskStratificationEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestCareGapsEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestQualityMeasuresEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestPopulationHealthPipeline))
    suite.addTests(loader.loadTestsFromTestCase(TestDataClasses))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
