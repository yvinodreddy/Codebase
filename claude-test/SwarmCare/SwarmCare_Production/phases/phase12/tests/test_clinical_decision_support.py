"""
Comprehensive Unit Tests for Phase 12: Clinical Decision Support System

Test Coverage:
- Sepsis Warning System (qSOFA, SIRS, Sepsis-3)
- Drug Interaction Checker
- Early Warning Scores (NEWS2, MEWS)
- Clinical Decision Support Engine
- HIPAA Audit Logging
- Edge cases and error handling
"""

import unittest
import sys
import os
from datetime import datetime

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from clinical_decision_support import (
    SepsisWarningSystem,
    DrugInteractionChecker,
    EarlyWarningScores,
    ClinicalDecisionSupportEngine,
    VitalSigns,
    LabValues,
    AlertSeverity,
    AlertType,
    assess_patient
)


class TestSepsisWarningSystem(unittest.TestCase):
    """Test cases for Sepsis Warning System"""

    def setUp(self):
        self.sepsis_system = SepsisWarningSystem()

    def test_qsofa_all_criteria_met(self):
        """Test qSOFA with all 3 criteria met"""
        vitals = VitalSigns(
            respiratory_rate=26,
            systolic_bp=95,
            consciousness_level='V'  # Not alert
        )
        score, criteria = self.sepsis_system.calculate_qsofa(vitals)
        self.assertEqual(score, 3)
        self.assertEqual(len(criteria), 3)

    def test_qsofa_two_criteria_met(self):
        """Test qSOFA with 2/3 criteria met"""
        vitals = VitalSigns(
            respiratory_rate=24,
            systolic_bp=98,
            consciousness_level='A'  # Alert
        )
        score, criteria = self.sepsis_system.calculate_qsofa(vitals)
        self.assertEqual(score, 2)
        self.assertEqual(len(criteria), 2)

    def test_qsofa_no_criteria_met(self):
        """Test qSOFA with normal vitals"""
        vitals = VitalSigns(
            respiratory_rate=16,
            systolic_bp=120,
            consciousness_level='A'
        )
        score, criteria = self.sepsis_system.calculate_qsofa(vitals)
        self.assertEqual(score, 0)
        self.assertEqual(len(criteria), 0)

    def test_sirs_all_criteria_met(self):
        """Test SIRS with all 4 criteria met"""
        vitals = VitalSigns(
            temperature_celsius=38.5,
            heart_rate=95,
            respiratory_rate=22
        )
        labs = LabValues(wbc_count=13.5)
        score, criteria = self.sepsis_system.calculate_sirs(vitals, labs)
        self.assertEqual(score, 4)
        self.assertEqual(len(criteria), 4)

    def test_sirs_low_temperature(self):
        """Test SIRS with hypothermia"""
        vitals = VitalSigns(
            temperature_celsius=35.5,
            heart_rate=85,
            respiratory_rate=18
        )
        labs = LabValues(wbc_count=7.0)
        score, criteria = self.sepsis_system.calculate_sirs(vitals, labs)
        self.assertGreaterEqual(score, 1)

    def test_septic_shock_detection(self):
        """Test detection of septic shock (qSOFA ≥2 + high lactate)"""
        vitals = VitalSigns(
            respiratory_rate=26,
            systolic_bp=88,
            consciousness_level='V'
        )
        labs = LabValues(lactate=4.5)

        alert = self.sepsis_system.detect_sepsis(vitals, labs, "PT001")

        self.assertIsNotNone(alert)
        self.assertEqual(alert.severity, AlertSeverity.CRITICAL)
        self.assertEqual(alert.alert_type, AlertType.SEPSIS)
        self.assertIn("SEPTIC SHOCK", alert.title)

    def test_high_risk_sepsis_detection(self):
        """Test detection of high-risk sepsis (qSOFA ≥2, no lactate)"""
        vitals = VitalSigns(
            respiratory_rate=26,
            systolic_bp=88,
            consciousness_level='A'
        )
        labs = LabValues()  # No lactate

        alert = self.sepsis_system.detect_sepsis(vitals, labs, "PT002")

        self.assertIsNotNone(alert)
        self.assertEqual(alert.severity, AlertSeverity.CRITICAL)

    def test_possible_sepsis_detection(self):
        """Test detection of possible sepsis (SIRS + high lactate)"""
        vitals = VitalSigns(
            temperature_celsius=38.8,
            heart_rate=110,
            respiratory_rate=22,
            systolic_bp=115
        )
        labs = LabValues(
            wbc_count=14.0,
            lactate=3.2
        )

        alert = self.sepsis_system.detect_sepsis(vitals, labs, "PT003")

        self.assertIsNotNone(alert)
        self.assertEqual(alert.severity, AlertSeverity.HIGH)

    def test_no_sepsis_normal_vitals(self):
        """Test that normal vitals don't trigger sepsis alert"""
        vitals = VitalSigns(
            temperature_celsius=37.0,
            heart_rate=75,
            respiratory_rate=16,
            systolic_bp=120
        )
        labs = LabValues(
            wbc_count=7.5,
            lactate=1.2
        )

        alert = self.sepsis_system.detect_sepsis(vitals, labs, "PT004")

        self.assertIsNone(alert)


class TestDrugInteractionChecker(unittest.TestCase):
    """Test cases for Drug Interaction Checker"""

    def setUp(self):
        self.drug_checker = DrugInteractionChecker()

    def test_warfarin_aspirin_interaction(self):
        """Test critical interaction: warfarin + aspirin"""
        medications = ["warfarin", "aspirin"]
        alerts = self.drug_checker.check_interactions(medications, "PT001")

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].severity, AlertSeverity.HIGH)
        self.assertEqual(alerts[0].alert_type, AlertType.DRUG_INTERACTION)
        self.assertIn("warfarin", alerts[0].title.lower())
        self.assertIn("aspirin", alerts[0].title.lower())

    def test_methotrexate_nsaid_interaction(self):
        """Test critical interaction: methotrexate + NSAIDs"""
        medications = ["methotrexate", "nsaids"]
        alerts = self.drug_checker.check_interactions(medications, "PT002")

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].severity, AlertSeverity.CRITICAL)
        self.assertIn("toxicity", alerts[0].description.lower())

    def test_ssri_mao_inhibitor_interaction(self):
        """Test critical interaction: SSRI + MAO inhibitor"""
        medications = ["ssri", "mao_inhibitor"]
        alerts = self.drug_checker.check_interactions(medications, "PT003")

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].severity, AlertSeverity.CRITICAL)
        self.assertIn("serotonin syndrome", alerts[0].description.lower())

    def test_multiple_interactions(self):
        """Test detection of multiple drug interactions"""
        medications = ["warfarin", "aspirin", "amiodarone"]
        alerts = self.drug_checker.check_interactions(medications, "PT004")

        # Should detect warfarin+aspirin and warfarin+amiodarone
        self.assertGreaterEqual(len(alerts), 2)

    def test_no_interaction_single_drug(self):
        """Test that single drug produces no interaction alerts"""
        medications = ["warfarin"]
        alerts = self.drug_checker.check_interactions(medications, "PT005")

        self.assertEqual(len(alerts), 0)

    def test_no_interaction_safe_combination(self):
        """Test safe drug combination produces no alerts"""
        medications = ["acetaminophen", "vitamin_d"]
        alerts = self.drug_checker.check_interactions(medications, "PT006")

        self.assertEqual(len(alerts), 0)

    def test_case_insensitive_checking(self):
        """Test that drug checking is case-insensitive"""
        medications = ["WARFARIN", "Aspirin"]
        alerts = self.drug_checker.check_interactions(medications, "PT007")

        self.assertEqual(len(alerts), 1)

    def test_statin_gemfibrozil_interaction(self):
        """Test critical interaction: statin + gemfibrozil"""
        medications = ["statins", "gemfibrozil"]
        alerts = self.drug_checker.check_interactions(medications, "PT008")

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].severity, AlertSeverity.CRITICAL)
        self.assertIn("rhabdomyolysis", alerts[0].description.lower())


class TestEarlyWarningScores(unittest.TestCase):
    """Test cases for Early Warning Score systems"""

    def setUp(self):
        self.ews = EarlyWarningScores()

    def test_news2_normal_vitals(self):
        """Test NEWS2 with normal vitals (score should be 0)"""
        vitals = VitalSigns(
            respiratory_rate=16,
            oxygen_saturation=98,
            systolic_bp=120,
            heart_rate=75,
            consciousness_level='A',
            temperature_celsius=37.0
        )
        score, components = self.ews.calculate_news2(vitals)

        self.assertEqual(score, 0)
        self.assertEqual(components['respiratory_rate'], 0)
        self.assertEqual(components['oxygen_saturation'], 0)
        self.assertEqual(components['consciousness'], 0)

    def test_news2_high_risk_vitals(self):
        """Test NEWS2 with high-risk vitals (score ≥7)"""
        vitals = VitalSigns(
            respiratory_rate=26,  # 3 points
            oxygen_saturation=90,  # 3 points
            systolic_bp=88,        # 3 points
            heart_rate=55,         # 1 point
            consciousness_level='V',  # 3 points
            temperature_celsius=35.0  # 3 points
        )
        score, components = self.ews.calculate_news2(vitals)

        self.assertGreaterEqual(score, 7)

    def test_news2_respiratory_rate_scoring(self):
        """Test NEWS2 respiratory rate scoring ranges"""
        # RR ≤8 = 3 points
        vitals1 = VitalSigns(respiratory_rate=8)
        score1, comp1 = self.ews.calculate_news2(vitals1)
        self.assertEqual(comp1['respiratory_rate'], 3)

        # RR 9-11 = 1 point
        vitals2 = VitalSigns(respiratory_rate=10)
        score2, comp2 = self.ews.calculate_news2(vitals2)
        self.assertEqual(comp2['respiratory_rate'], 1)

        # RR 12-20 = 0 points
        vitals3 = VitalSigns(respiratory_rate=16)
        score3, comp3 = self.ews.calculate_news2(vitals3)
        self.assertEqual(comp3['respiratory_rate'], 0)

        # RR ≥25 = 3 points
        vitals4 = VitalSigns(respiratory_rate=26)
        score4, comp4 = self.ews.calculate_news2(vitals4)
        self.assertEqual(comp4['respiratory_rate'], 3)

    def test_news2_oxygen_saturation_scoring(self):
        """Test NEWS2 oxygen saturation scoring"""
        # SpO2 ≤91 = 3 points
        vitals1 = VitalSigns(oxygen_saturation=90)
        score1, comp1 = self.ews.calculate_news2(vitals1)
        self.assertEqual(comp1['oxygen_saturation'], 3)

        # SpO2 92-93 = 2 points
        vitals2 = VitalSigns(oxygen_saturation=93)
        score2, comp2 = self.ews.calculate_news2(vitals2)
        self.assertEqual(comp2['oxygen_saturation'], 2)

        # SpO2 ≥96 = 0 points
        vitals3 = VitalSigns(oxygen_saturation=98)
        score3, comp3 = self.ews.calculate_news2(vitals3)
        self.assertEqual(comp3['oxygen_saturation'], 0)

    def test_news2_altered_consciousness(self):
        """Test NEWS2 consciousness scoring"""
        vitals_alert = VitalSigns(consciousness_level='A')
        score_alert, comp_alert = self.ews.calculate_news2(vitals_alert)
        self.assertEqual(comp_alert['consciousness'], 0)

        vitals_voice = VitalSigns(consciousness_level='V')
        score_voice, comp_voice = self.ews.calculate_news2(vitals_voice)
        self.assertEqual(comp_voice['consciousness'], 3)

    def test_mews_normal_vitals(self):
        """Test MEWS with normal vitals"""
        vitals = VitalSigns(
            respiratory_rate=12,  # 9-14 range = 0 points for MEWS
            heart_rate=75,
            systolic_bp=120,
            temperature_celsius=37.0,
            consciousness_level='A'
        )
        score, components = self.ews.calculate_mews(vitals)

        self.assertEqual(score, 0)

    def test_mews_high_score(self):
        """Test MEWS with abnormal vitals"""
        vitals = VitalSigns(
            respiratory_rate=32,   # 3 points
            heart_rate=135,        # 3 points
            systolic_bp=68,        # 3 points
            temperature_celsius=39.0,  # 2 points
            consciousness_level='P'    # 2 points
        )
        score, components = self.ews.calculate_mews(vitals)

        self.assertGreaterEqual(score, 10)

    def test_assess_patient_critical(self):
        """Test patient assessment with critical NEWS2 score"""
        vitals = VitalSigns(
            respiratory_rate=28,
            oxygen_saturation=89,
            systolic_bp=85,
            heart_rate=125,
            consciousness_level='V',
            temperature_celsius=38.5
        )

        alert = self.ews.assess_patient(vitals, "PT001")

        self.assertIsNotNone(alert)
        self.assertEqual(alert.severity, AlertSeverity.CRITICAL)
        self.assertEqual(alert.alert_type, AlertType.EARLY_WARNING)

    def test_assess_patient_high_risk(self):
        """Test patient assessment with elevated NEWS2 score"""
        vitals = VitalSigns(
            respiratory_rate=24,
            oxygen_saturation=93,
            systolic_bp=105,
            heart_rate=95,
            consciousness_level='A',
            temperature_celsius=38.2
        )

        alert = self.ews.assess_patient(vitals, "PT002")

        self.assertIsNotNone(alert)
        self.assertIn(alert.severity, [AlertSeverity.HIGH, AlertSeverity.CRITICAL])

    def test_assess_patient_normal(self):
        """Test patient assessment with normal vitals"""
        vitals = VitalSigns(
            respiratory_rate=16,
            oxygen_saturation=98,
            systolic_bp=120,
            heart_rate=75,
            consciousness_level='A',
            temperature_celsius=37.0
        )

        alert = self.ews.assess_patient(vitals, "PT003")

        # Normal vitals should not trigger alert
        self.assertIsNone(alert)


class TestClinicalDecisionSupportEngine(unittest.TestCase):
    """Test cases for Clinical Decision Support Engine"""

    def setUp(self):
        self.engine = ClinicalDecisionSupportEngine()

    def test_comprehensive_assessment_normal_patient(self):
        """Test comprehensive assessment for normal patient"""
        vitals = VitalSigns(
            temperature_celsius=37.0,
            heart_rate=75,
            respiratory_rate=16,
            systolic_bp=120,
            diastolic_bp=80,
            oxygen_saturation=98,
            consciousness_level='A'
        )
        labs = LabValues(
            wbc_count=7.5,
            lactate=1.2
        )

        assessment = self.engine.comprehensive_assessment(
            patient_id="PT001",
            vitals=vitals,
            labs=labs
        )

        self.assertEqual(assessment['patient_id'], "PT001")
        self.assertEqual(assessment['alert_count']['total'], 0)
        self.assertIsNotNone(assessment['scores'])
        self.assertIsNotNone(assessment['processing_time_ms'])

    def test_comprehensive_assessment_septic_patient(self):
        """Test comprehensive assessment for septic patient"""
        vitals = VitalSigns(
            temperature_celsius=38.8,
            heart_rate=125,
            respiratory_rate=28,
            systolic_bp=88,
            diastolic_bp=55,
            oxygen_saturation=90,
            consciousness_level='V'
        )
        labs = LabValues(
            wbc_count=18.5,
            lactate=4.5
        )

        assessment = self.engine.comprehensive_assessment(
            patient_id="PT002",
            vitals=vitals,
            labs=labs
        )

        # Should have multiple critical alerts
        self.assertGreater(assessment['alert_count']['total'], 0)
        self.assertGreater(assessment['alert_count']['critical'], 0)

        # Should have high scores
        self.assertGreater(assessment['scores']['news2'], 5)
        self.assertGreater(assessment['scores']['qsofa'], 1)

    def test_comprehensive_assessment_drug_interactions(self):
        """Test comprehensive assessment with drug interactions"""
        vitals = VitalSigns(
            temperature_celsius=37.0,
            heart_rate=75,
            respiratory_rate=16,
            systolic_bp=120,
            diastolic_bp=80,
            oxygen_saturation=98,
            consciousness_level='A'
        )

        medications = ["warfarin", "aspirin", "amiodarone"]

        assessment = self.engine.comprehensive_assessment(
            patient_id="PT003",
            vitals=vitals,
            medications=medications
        )

        # Should detect drug interactions
        self.assertGreater(assessment['alert_count']['total'], 0)

        # Check that drug interaction alerts are present
        drug_alerts = [
            alert for alert in assessment['alerts']
            if alert['alert_type'] == 'DRUG_INTERACTION'
        ]
        self.assertGreater(len(drug_alerts), 0)

    def test_alert_severity_sorting(self):
        """Test that alerts are sorted by severity"""
        vitals = VitalSigns(
            temperature_celsius=38.8,
            heart_rate=125,
            respiratory_rate=28,
            systolic_bp=88,
            diastolic_bp=55,
            oxygen_saturation=90,
            consciousness_level='V'
        )
        labs = LabValues(
            wbc_count=18.5,
            lactate=4.5
        )

        assessment = self.engine.comprehensive_assessment(
            patient_id="PT004",
            vitals=vitals,
            labs=labs,
            medications=["warfarin", "aspirin"]
        )

        # Verify alerts are sorted by severity
        alerts = assessment['alerts']
        if len(alerts) > 1:
            severity_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
            for i in range(len(alerts) - 1):
                current_severity = alerts[i]['severity']
                next_severity = alerts[i + 1]['severity']
                self.assertLessEqual(
                    severity_order.index(current_severity),
                    severity_order.index(next_severity)
                )

    def test_audit_logging(self):
        """Test HIPAA-compliant audit logging"""
        vitals = VitalSigns(
            temperature_celsius=37.0,
            heart_rate=75,
            respiratory_rate=16,
            systolic_bp=120,
            diastolic_bp=80,
            oxygen_saturation=98,
            consciousness_level='A'
        )

        initial_audit_count = len(self.engine.audit_log)

        assessment = self.engine.comprehensive_assessment(
            patient_id="PT005",
            vitals=vitals
        )

        # Verify audit log entry was created
        self.assertEqual(len(self.engine.audit_log), initial_audit_count + 1)

        # Verify audit log content
        latest_audit = self.engine.audit_log[-1]
        self.assertEqual(latest_audit['patient_id'], "PT005")
        self.assertEqual(latest_audit['action'], "CLINICAL_ASSESSMENT")
        self.assertIn('timestamp', latest_audit)

    def test_get_audit_trail_by_patient(self):
        """Test retrieving audit trail for specific patient"""
        vitals = VitalSigns(
            temperature_celsius=37.0,
            heart_rate=75,
            respiratory_rate=16,
            systolic_bp=120,
            diastolic_bp=80,
            oxygen_saturation=98,
            consciousness_level='A'
        )

        # Create assessments for different patients
        self.engine.comprehensive_assessment(patient_id="PT006", vitals=vitals)
        self.engine.comprehensive_assessment(patient_id="PT007", vitals=vitals)
        self.engine.comprehensive_assessment(patient_id="PT006", vitals=vitals)

        # Get audit trail for PT006
        pt006_audit = self.engine.get_audit_trail("PT006")

        self.assertEqual(len(pt006_audit), 2)
        for entry in pt006_audit:
            self.assertEqual(entry['patient_id'], "PT006")

    def test_export_assessment_report(self):
        """Test assessment report export"""
        vitals = VitalSigns(
            temperature_celsius=38.5,
            heart_rate=110,
            respiratory_rate=24,
            systolic_bp=95,
            diastolic_bp=60,
            oxygen_saturation=92,
            consciousness_level='A'
        )
        labs = LabValues(
            wbc_count=14.0,
            lactate=2.8
        )

        assessment = self.engine.comprehensive_assessment(
            patient_id="PT008",
            vitals=vitals,
            labs=labs
        )

        report = self.engine.export_assessment_report(assessment)

        # Verify report contains key sections
        self.assertIn("CLINICAL DECISION SUPPORT", report)
        self.assertIn("Patient ID: PT008", report)
        self.assertIn("VITAL SIGNS", report)
        self.assertIn("EARLY WARNING SCORES", report)
        self.assertIn("NEWS2", report)
        self.assertIn("Processing Time", report)


class TestConvenienceFunction(unittest.TestCase):
    """Test cases for convenience assessment function"""

    def test_assess_patient_function(self):
        """Test convenience assess_patient function"""
        assessment = assess_patient(
            patient_id="PT001",
            temperature_c=38.5,
            heart_rate=110,
            respiratory_rate=24,
            systolic_bp=95,
            diastolic_bp=60,
            oxygen_sat=91,
            consciousness="A",
            lactate=3.2,
            medications=["warfarin", "aspirin"]
        )

        self.assertIsNotNone(assessment)
        self.assertEqual(assessment['patient_id'], "PT001")
        self.assertIn('alerts', assessment)
        self.assertIn('scores', assessment)

    def test_assess_patient_minimal_data(self):
        """Test convenience function with minimal data"""
        assessment = assess_patient(
            patient_id="PT002",
            heart_rate=75,
            respiratory_rate=16
        )

        self.assertIsNotNone(assessment)
        self.assertEqual(assessment['patient_id'], "PT002")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""

    def test_missing_vital_signs(self):
        """Test handling of missing vital signs"""
        vitals = VitalSigns()  # All None
        sepsis_system = SepsisWarningSystem()

        score, criteria = sepsis_system.calculate_qsofa(vitals)
        self.assertEqual(score, 0)
        self.assertEqual(len(criteria), 0)

    def test_missing_lab_values(self):
        """Test handling of missing lab values"""
        vitals = VitalSigns()
        labs = LabValues()  # All None
        sepsis_system = SepsisWarningSystem()

        score, criteria = sepsis_system.calculate_sirs(vitals, labs)
        self.assertEqual(score, 0)

    def test_partial_vital_signs(self):
        """Test with partial vital signs data"""
        vitals = VitalSigns(
            heart_rate=95,
            # Other vitals missing
        )
        ews = EarlyWarningScores()

        score, components = ews.calculate_news2(vitals)
        self.assertGreaterEqual(score, 0)

    def test_extreme_values(self):
        """Test with extreme vital sign values"""
        vitals = VitalSigns(
            temperature_celsius=42.0,  # Extreme hyperthermia
            heart_rate=200,             # Extreme tachycardia
            respiratory_rate=40,        # Extreme tachypnea
            systolic_bp=50,             # Extreme hypotension
            oxygen_saturation=70        # Severe hypoxemia
        )
        ews = EarlyWarningScores()

        score, components = ews.calculate_news2(vitals)
        self.assertGreater(score, 10)  # Should have very high score

    def test_timestamp_auto_generation(self):
        """Test that timestamps are automatically generated"""
        vitals = VitalSigns(heart_rate=75)
        self.assertIsNotNone(vitals.timestamp)

        labs = LabValues(wbc_count=7.5)
        self.assertIsNotNone(labs.timestamp)


class TestProductionReadiness(unittest.TestCase):
    """Test production readiness features"""

    def test_performance_acceptable(self):
        """Test that assessment completes in acceptable time"""
        import time

        engine = ClinicalDecisionSupportEngine()
        vitals = VitalSigns(
            temperature_celsius=38.5,
            heart_rate=110,
            respiratory_rate=24,
            systolic_bp=95,
            diastolic_bp=60,
            oxygen_saturation=92,
            consciousness_level='A'
        )
        labs = LabValues(wbc_count=14.0, lactate=2.8)
        medications = ["warfarin", "aspirin", "amiodarone"]

        start = time.time()
        assessment = engine.comprehensive_assessment(
            patient_id="PT001",
            vitals=vitals,
            labs=labs,
            medications=medications
        )
        duration_ms = (time.time() - start) * 1000

        # Assessment should complete in under 100ms
        self.assertLess(duration_ms, 100)
        self.assertLess(assessment['processing_time_ms'], 100)

    def test_concurrent_assessments(self):
        """Test that engine can handle concurrent assessments"""
        engine = ClinicalDecisionSupportEngine()
        vitals = VitalSigns(
            temperature_celsius=37.0,
            heart_rate=75,
            respiratory_rate=16,
            systolic_bp=120,
            diastolic_bp=80,
            oxygen_saturation=98,
            consciousness_level='A'
        )

        # Simulate concurrent assessments
        for i in range(10):
            assessment = engine.comprehensive_assessment(
                patient_id=f"PT{i:03d}",
                vitals=vitals
            )
            self.assertEqual(assessment['patient_id'], f"PT{i:03d}")

        # Verify all assessments logged
        self.assertEqual(len(engine.audit_log), 10)

    def test_data_integrity(self):
        """Test that patient data integrity is maintained"""
        engine = ClinicalDecisionSupportEngine()
        vitals = VitalSigns(
            temperature_celsius=37.5,
            heart_rate=80
        )

        assessment = engine.comprehensive_assessment(
            patient_id="PT001",
            vitals=vitals
        )

        # Verify original vitals data is preserved
        self.assertEqual(assessment['vital_signs']['temperature_celsius'], 37.5)
        self.assertEqual(assessment['vital_signs']['heart_rate'], 80)


def run_test_suite():
    """Run complete test suite with detailed output"""
    print("\n" + "=" * 80)
    print("PHASE 12: CLINICAL DECISION SUPPORT - COMPREHENSIVE TEST SUITE")
    print("=" * 80 + "\n")

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSepsisWarningSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestDrugInteractionChecker))
    suite.addTests(loader.loadTestsFromTestCase(TestEarlyWarningScores))
    suite.addTests(loader.loadTestsFromTestCase(TestClinicalDecisionSupportEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunction))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestProductionReadiness))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("=" * 80)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)
