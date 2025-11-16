"""
Integration Tests for Phase 12: Clinical Decision Support System
Realistic clinical scenarios testing end-to-end workflows

Scenarios:
1. Septic Patient in Emergency Department
2. Post-Operative Patient with Early Warning Signs
3. Complex Polypharmacy Patient
4. ICU Patient with Multiple Organ Dysfunction
5. Pediatric Patient (adapted scoring)
"""

import unittest
import sys
import os
from datetime import datetime

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from clinical_decision_support import (
    ClinicalDecisionSupportEngine,
    VitalSigns,
    LabValues,
    AlertSeverity,
    AlertType,
    assess_patient
)


class TestEmergencyDepartmentScenarios(unittest.TestCase):
    """Test realistic ED scenarios"""

    def setUp(self):
        self.engine = ClinicalDecisionSupportEngine()

    def test_scenario_1_septic_patient_ed(self):
        """
        SCENARIO: 68-year-old male presents to ED with 3 days of fever and confusion
        - History: Diabetes, hypertension
        - Vital signs: Fever 39.2°C, HR 125, RR 28, BP 88/55, SpO2 91%, confused
        - Labs: WBC 22, Lactate 4.8
        - Expected: Critical septic shock alert
        """
        print("\n📋 SCENARIO 1: Septic Patient in ED")
        print("-" * 60)

        vitals = VitalSigns(
            temperature_celsius=39.2,
            heart_rate=125,
            respiratory_rate=28,
            systolic_bp=88,
            diastolic_bp=55,
            oxygen_saturation=91,
            consciousness_level='V'  # Confused, responds to voice
        )

        labs = LabValues(
            wbc_count=22.0,
            lactate=4.8,
            creatinine=2.3  # Acute kidney injury
        )

        assessment = self.engine.comprehensive_assessment(
            patient_id="ED_PT_001",
            vitals=vitals,
            labs=labs,
            age_years=68
        )

        # Verify critical alerts generated
        self.assertGreater(assessment['alert_count']['critical'], 0)
        self.assertGreater(assessment['alert_count']['total'], 0)

        # Verify sepsis detection
        sepsis_alerts = [
            a for a in assessment['alerts']
            if a['alert_type'] == 'SEPSIS'
        ]
        self.assertGreater(len(sepsis_alerts), 0)

        # Verify high risk scores
        self.assertGreaterEqual(assessment['scores']['qsofa'], 2)
        self.assertGreaterEqual(assessment['scores']['news2'], 7)

        # Print results
        print(f"✓ Alerts Generated: {assessment['alert_count']['total']}")
        print(f"✓ Critical Alerts: {assessment['alert_count']['critical']}")
        print(f"✓ qSOFA Score: {assessment['scores']['qsofa']}/3")
        print(f"✓ NEWS2 Score: {assessment['scores']['news2']}")
        print(f"✓ Processing Time: {assessment['processing_time_ms']:.2f}ms")

        for i, alert in enumerate(assessment['alerts'][:3], 1):
            print(f"\n  Alert {i}: {alert['title']}")
            print(f"  Severity: {alert['severity']}")
            print(f"  Recommendation: {alert['recommendation'][:80]}...")

        self.assertTrue(True, "ED Sepsis scenario passed")

    def test_scenario_2_urosepsis_elderly(self):
        """
        SCENARIO: 82-year-old female with suspected urosepsis
        - History: UTI symptoms, nursing home resident
        - Vital signs: Temp 38.0°C, HR 98, RR 24, BP 105/65, SpO2 94%, Alert
        - Labs: WBC 16, Lactate 2.4
        - Medications: Warfarin, furosemide, metoprolol
        - Expected: Possible sepsis warning
        """
        print("\n📋 SCENARIO 2: Elderly Patient with Urosepsis")
        print("-" * 60)

        vitals = VitalSigns(
            temperature_celsius=38.0,
            heart_rate=98,
            respiratory_rate=24,
            systolic_bp=105,
            diastolic_bp=65,
            oxygen_saturation=94,
            consciousness_level='A'
        )

        labs = LabValues(
            wbc_count=16.0,
            lactate=2.4
        )

        medications = ["warfarin", "furosemide", "metoprolol"]

        assessment = self.engine.comprehensive_assessment(
            patient_id="ED_PT_002",
            vitals=vitals,
            labs=labs,
            medications=medications,
            age_years=82
        )

        # Should have at least early warning or sepsis alert
        self.assertGreater(assessment['alert_count']['total'], 0)

        # NEWS2 should be elevated
        self.assertGreaterEqual(assessment['scores']['news2'], 4)

        print(f"✓ Total Alerts: {assessment['alert_count']['total']}")
        print(f"✓ NEWS2 Score: {assessment['scores']['news2']}")
        print(f"✓ SIRS Score: {assessment['scores']['sirs']}/4")

        self.assertTrue(True, "Elderly urosepsis scenario passed")


class TestPostOperativeScenarios(unittest.TestCase):
    """Test post-operative patient scenarios"""

    def setUp(self):
        self.engine = ClinicalDecisionSupportEngine()

    def test_scenario_3_post_op_deterioration(self):
        """
        SCENARIO: Post-op day 2 s/p abdominal surgery showing deterioration
        - Vital signs: Temp 37.8°C, HR 115, RR 26, BP 98/62, SpO2 92%, Alert
        - Labs: WBC 14, Lactate 2.8
        - Expected: High early warning score, possible sepsis
        """
        print("\n📋 SCENARIO 3: Post-Operative Deterioration")
        print("-" * 60)

        vitals = VitalSigns(
            temperature_celsius=37.8,
            heart_rate=115,
            respiratory_rate=26,
            systolic_bp=98,
            diastolic_bp=62,
            oxygen_saturation=92,
            consciousness_level='A'
        )

        labs = LabValues(
            wbc_count=14.0,
            lactate=2.8
        )

        assessment = self.engine.comprehensive_assessment(
            patient_id="POSTOP_PT_001",
            vitals=vitals,
            labs=labs,
            age_years=55
        )

        # Should trigger early warning or sepsis alert
        self.assertGreater(assessment['alert_count']['total'], 0)
        self.assertGreaterEqual(assessment['scores']['news2'], 5)

        print(f"✓ Alerts: {assessment['alert_count']['total']}")
        print(f"✓ NEWS2: {assessment['scores']['news2']}")
        print(f"✓ qSOFA: {assessment['scores']['qsofa']}/3")

        self.assertTrue(True, "Post-op deterioration scenario passed")


class TestPolypharmacyScenarios(unittest.TestCase):
    """Test complex medication scenarios"""

    def setUp(self):
        self.engine = ClinicalDecisionSupportEngine()

    def test_scenario_4_complex_polypharmacy(self):
        """
        SCENARIO: 75-year-old with multiple conditions and medications
        - Diagnoses: AFib, CHF, Diabetes, CKD
        - Medications: Warfarin, Digoxin, Amiodarone, Metformin, Furosemide
        - Expected: Multiple drug interaction alerts
        """
        print("\n📋 SCENARIO 4: Complex Polypharmacy Patient")
        print("-" * 60)

        vitals = VitalSigns(
            temperature_celsius=37.2,
            heart_rate=88,
            respiratory_rate=18,
            systolic_bp=128,
            diastolic_bp=78,
            oxygen_saturation=96,
            consciousness_level='A'
        )

        medications = [
            "warfarin",
            "digoxin",
            "amiodarone",
            "metformin",
            "furosemide"
        ]

        assessment = self.engine.comprehensive_assessment(
            patient_id="POLY_PT_001",
            vitals=vitals,
            medications=medications,
            age_years=75
        )

        # Should detect warfarin + amiodarone interaction
        drug_alerts = [
            a for a in assessment['alerts']
            if a['alert_type'] == 'DRUG_INTERACTION'
        ]
        self.assertGreater(len(drug_alerts), 0)

        print(f"✓ Drug Interaction Alerts: {len(drug_alerts)}")
        for alert in drug_alerts:
            print(f"  - {alert['title']}: {alert['severity']}")

        self.assertTrue(True, "Polypharmacy scenario passed")

    def test_scenario_5_dangerous_combination(self):
        """
        SCENARIO: Patient with dangerous drug combination
        - Medications: SSRI (sertraline) + Tramadol
        - Expected: Serotonin syndrome warning
        """
        print("\n📋 SCENARIO 5: Dangerous Drug Combination")
        print("-" * 60)

        vitals = VitalSigns(
            temperature_celsius=37.5,
            heart_rate=82,
            respiratory_rate=16,
            systolic_bp=135,
            diastolic_bp=85,
            oxygen_saturation=98,
            consciousness_level='A'
        )

        medications = ["ssri", "tramadol"]

        assessment = self.engine.comprehensive_assessment(
            patient_id="DRUG_PT_001",
            vitals=vitals,
            medications=medications
        )

        drug_alerts = [
            a for a in assessment['alerts']
            if a['alert_type'] == 'DRUG_INTERACTION'
        ]
        self.assertGreater(len(drug_alerts), 0)

        # Should be high severity
        high_severity_alerts = [
            a for a in drug_alerts
            if a['severity'] in ['HIGH', 'CRITICAL']
        ]
        self.assertGreater(len(high_severity_alerts), 0)

        print(f"✓ High Severity Alerts: {len(high_severity_alerts)}")

        self.assertTrue(True, "Dangerous combination scenario passed")


class TestICUScenarios(unittest.TestCase):
    """Test intensive care unit scenarios"""

    def setUp(self):
        self.engine = ClinicalDecisionSupportEngine()

    def test_scenario_6_icu_mods(self):
        """
        SCENARIO: ICU patient with multiple organ dysfunction
        - Diagnoses: Septic shock, ARDS, AKI
        - Vital signs: Very abnormal
        - Labs: Severely deranged
        - Expected: Multiple critical alerts
        """
        print("\n📋 SCENARIO 6: ICU Patient with MODS")
        print("-" * 60)

        vitals = VitalSigns(
            temperature_celsius=38.5,
            heart_rate=135,
            respiratory_rate=32,
            systolic_bp=78,
            diastolic_bp=45,
            oxygen_saturation=88,
            consciousness_level='P'  # Responds to pain only
        )

        labs = LabValues(
            wbc_count=24.5,
            lactate=6.2,
            creatinine=3.8,
            platelet_count=85.0,
            bilirubin=3.5
        )

        assessment = self.engine.comprehensive_assessment(
            patient_id="ICU_PT_001",
            vitals=vitals,
            labs=labs,
            age_years=62
        )

        # Should have multiple critical alerts
        self.assertGreater(assessment['alert_count']['critical'], 1)
        self.assertGreaterEqual(assessment['scores']['news2'], 10)
        self.assertEqual(assessment['scores']['qsofa'], 3)

        print(f"✓ Critical Alerts: {assessment['alert_count']['critical']}")
        print(f"✓ Total Alerts: {assessment['alert_count']['total']}")
        print(f"✓ NEWS2: {assessment['scores']['news2']}")
        print(f"✓ qSOFA: {assessment['scores']['qsofa']}/3")
        print(f"✓ SIRS: {assessment['scores']['sirs']}/4")

        self.assertTrue(True, "ICU MODS scenario passed")


class TestNormalPatientScenarios(unittest.TestCase):
    """Test that normal patients don't generate false alarms"""

    def setUp(self):
        self.engine = ClinicalDecisionSupportEngine()

    def test_scenario_7_healthy_patient(self):
        """
        SCENARIO: Healthy patient for routine check
        - Vital signs: All normal
        - Labs: Normal
        - Expected: No alerts
        """
        print("\n📋 SCENARIO 7: Healthy Patient - No False Alarms")
        print("-" * 60)

        vitals = VitalSigns(
            temperature_celsius=37.0,
            heart_rate=72,
            respiratory_rate=14,
            systolic_bp=118,
            diastolic_bp=76,
            oxygen_saturation=99,
            consciousness_level='A'
        )

        labs = LabValues(
            wbc_count=7.2,
            lactate=1.0,
            creatinine=0.9
        )

        assessment = self.engine.comprehensive_assessment(
            patient_id="HEALTHY_PT_001",
            vitals=vitals,
            labs=labs,
            age_years=45
        )

        # Should have no alerts
        self.assertEqual(assessment['alert_count']['total'], 0)
        self.assertLess(assessment['scores']['news2'], 3)

        print(f"✓ No false alarms: {assessment['alert_count']['total']} alerts")
        print(f"✓ NEWS2: {assessment['scores']['news2']} (Low risk)")

        self.assertTrue(True, "Healthy patient scenario passed")

    def test_scenario_8_stable_chronic_conditions(self):
        """
        SCENARIO: Stable patient with controlled chronic conditions
        - Diagnoses: Controlled HTN, well-managed diabetes
        - Vital signs: Slightly elevated but stable
        - Medications: Common, no dangerous interactions
        - Expected: Minimal or no alerts
        """
        print("\n📋 SCENARIO 8: Stable Chronic Conditions")
        print("-" * 60)

        vitals = VitalSigns(
            temperature_celsius=37.1,
            heart_rate=78,
            respiratory_rate=16,
            systolic_bp=142,  # Slightly elevated but controlled
            diastolic_bp=86,
            oxygen_saturation=97,
            consciousness_level='A'
        )

        medications = ["metformin", "lisinopril", "atorvastatin"]

        assessment = self.engine.comprehensive_assessment(
            patient_id="STABLE_PT_001",
            vitals=vitals,
            medications=medications,
            age_years=62
        )

        # Should have no critical alerts
        self.assertEqual(assessment['alert_count']['critical'], 0)

        print(f"✓ No critical alerts for stable patient")
        print(f"✓ NEWS2: {assessment['scores']['news2']}")

        self.assertTrue(True, "Stable chronic patient scenario passed")


class TestPerformanceScenarios(unittest.TestCase):
    """Test system performance under load"""

    def test_scenario_9_rapid_sequential_assessments(self):
        """
        SCENARIO: Process 100 patient assessments rapidly
        - Expected: All complete successfully, average <100ms each
        """
        print("\n📋 SCENARIO 9: Rapid Sequential Assessment Performance")
        print("-" * 60)

        engine = ClinicalDecisionSupportEngine()
        processing_times = []

        for i in range(100):
            vitals = VitalSigns(
                temperature_celsius=37.0 + (i % 3),
                heart_rate=70 + (i % 30),
                respiratory_rate=14 + (i % 8),
                systolic_bp=110 + (i % 40),
                diastolic_bp=70 + (i % 20),
                oxygen_saturation=96 + (i % 4),
                consciousness_level='A'
            )

            assessment = engine.comprehensive_assessment(
                patient_id=f"PERF_PT_{i:03d}",
                vitals=vitals
            )

            processing_times.append(assessment['processing_time_ms'])

        avg_time = sum(processing_times) / len(processing_times)
        max_time = max(processing_times)

        print(f"✓ Assessments Completed: 100")
        print(f"✓ Average Processing Time: {avg_time:.2f}ms")
        print(f"✓ Max Processing Time: {max_time:.2f}ms")
        print(f"✓ Audit Log Entries: {len(engine.audit_log)}")

        # Performance assertions
        self.assertLess(avg_time, 100, "Average processing time should be <100ms")
        self.assertEqual(len(engine.audit_log), 100, "All assessments should be logged")

        self.assertTrue(True, "Performance scenario passed")


def run_integration_tests():
    """Run complete integration test suite"""
    print("\n" + "=" * 80)
    print("PHASE 12: CLINICAL DECISION SUPPORT - INTEGRATION TEST SUITE")
    print("Realistic Clinical Scenarios")
    print("=" * 80)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEmergencyDepartmentScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestPostOperativeScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestPolypharmacyScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestICUScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestNormalPatientScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceScenarios))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 80)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 80)
    print(f"Scenarios Tested: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("=" * 80)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
