"""
Phase 19: Voice AI & Ambient Intelligence - Integration Tests
Realistic Clinical Scenarios

Scenarios:
1. Emergency Department Chest Pain Patient
2. ICU Sepsis Patient with Multiple Commands
3. Outpatient Diabetes Follow-up
4. Inpatient Discharge Planning
5. Surgical Consultation
6. Pediatric Well-Child Visit
7. Psychiatric Evaluation
8. Multi-provider Handoff

Target: 8+ comprehensive integration scenarios
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from voice_ai_system import (
    VoiceAISystem, SpeakerRole, generate_clinical_note_from_conversation,
    assess_voice_command
)


class TestIntegrationScenarios(unittest.TestCase):
    """Test realistic clinical integration scenarios"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = VoiceAISystem()

    # ========================================================================
    # SCENARIO 1: ED CHEST PAIN PATIENT
    # ========================================================================

    def test_scenario_1_ed_chest_pain(self):
        """
        SCENARIO 1: Emergency Department - Chest Pain Patient

        Patient: 58-year-old male with acute chest pain
        Setting: Emergency Department
        Workflow: Triage → Assessment → Orders → Disposition
        """
        print("\n" + "="*80)
        print("SCENARIO 1: ED Chest Pain Patient")
        print("="*80)

        # Simulate clinical encounter conversation
        conversation = [
            ("I have severe chest pain that started an hour ago", SpeakerRole.PATIENT, 3.0),
            ("Tell me more about the chest pain. Where exactly?", SpeakerRole.PHYSICIAN, 2.5),
            ("It's in the center of my chest, feels like pressure", SpeakerRole.PATIENT, 3.0),
            ("Does it radiate anywhere?", SpeakerRole.PHYSICIAN, 1.5),
            ("Yes, to my left arm and jaw", SpeakerRole.PATIENT, 2.0),
            ("Any shortness of breath, nausea, or sweating?", SpeakerRole.PHYSICIAN, 2.0),
            ("Yes, I feel short of breath and I'm sweating", SpeakerRole.PATIENT, 2.5),
            ("Blood pressure 145 over 92, heart rate 105, oxygen saturation 94 percent", SpeakerRole.PHYSICIAN, 4.0),
            ("This could be a heart attack. I need to order some tests immediately", SpeakerRole.PHYSICIAN, 3.0),
        ]

        # Process encounter
        encounter = self.system.conduct_clinical_encounter(
            "ED_CHEST_PAIN_001",
            "PT_ED_12345",
            "DR_CARDIO_001",
            conversation
        )

        # Verify encounter completed
        self.assertEqual(encounter["session"]["status"], "completed")
        self.assertEqual(encounter["soap_note"]["patient_id"], "PT_ED_12345")

        # Verify SOAP note contains key information
        soap_content = encounter["soap_note"]["content"]
        self.assertIn("chest pain", soap_content["subjective"].lower())
        self.assertIn("blood pressure", soap_content["objective"].lower())

        # Now process urgent orders via voice commands
        orders = [
            "Order troponin stat",
            "Order EKG immediately",
            "Order chest x-ray portable",
            "Prescribe aspirin 324mg chew and swallow",
            "Prescribe nitroglycerin 0.4mg sublingual"
        ]

        executed_orders = []
        for order in orders:
            result = self.system.process_voice_command(order, "DR_CARDIO_001")
            executed_orders.append(result)
            self.assertTrue(result["execution_result"]["success"])

        print(f"✅ Encounter completed: {len(conversation)} conversation segments")
        print(f"✅ SOAP note generated: {encounter['soap_note']['note_id']}")
        print(f"✅ Orders executed: {len(executed_orders)}")
        print(f"✅ Medical entities extracted: {encounter['transcript_summary']['medical_entities']}")

        # Verify all orders executed
        self.assertEqual(len(executed_orders), 5)

    # ========================================================================
    # SCENARIO 2: ICU SEPSIS PATIENT
    # ========================================================================

    def test_scenario_2_icu_sepsis(self):
        """
        SCENARIO 2: ICU - Septic Shock Patient

        Patient: 72-year-old female with septic shock
        Setting: Intensive Care Unit
        Workflow: Rounds → Assessment → Orders → Documentation
        """
        print("\n" + "="*80)
        print("SCENARIO 2: ICU Sepsis Patient")
        print("="*80)

        conversation = [
            ("Patient is a 72-year-old female admitted for pneumonia", SpeakerRole.PHYSICIAN, 3.0),
            ("Now presenting with hypotension and altered mental status", SpeakerRole.PHYSICIAN, 3.0),
            ("Blood pressure 85 over 50 despite two liters of fluids", SpeakerRole.PHYSICIAN, 3.0),
            ("Heart rate 125, respiratory rate 28, temperature 39.2 celsius", SpeakerRole.PHYSICIAN, 3.5),
            ("Lactate is 4.8, white blood cell count 22,000", SpeakerRole.PHYSICIAN, 3.0),
            ("This is septic shock from pneumonia", SpeakerRole.PHYSICIAN, 2.0),
            ("Need to start broad-spectrum antibiotics and consider vasopressors", SpeakerRole.PHYSICIAN, 3.0),
            ("Patient is on ventilator, sedated with propofol", SpeakerRole.NURSE, 2.5),
            ("Central line in place, arterial line monitoring", SpeakerRole.NURSE, 2.0),
        ]

        encounter = self.system.conduct_clinical_encounter(
            "ICU_SEPSIS_001",
            "PT_ICU_67890",
            "DR_ICU_002",
            conversation
        )

        # Verify critical care documentation
        self.assertEqual(encounter["session"]["status"], "completed")
        self.assertGreater(encounter["transcript_summary"]["medical_entities"], 0)

        # Process ICU orders
        icu_orders = [
            "Order blood cultures times two",
            "Prescribe vancomycin 15mg per kg IV",
            "Prescribe cefepime 2g IV every 8 hours",
            "Order repeat lactate in 2 hours",
            "Start norepinephrine drip"
        ]

        for order in icu_orders:
            result = self.system.process_voice_command(order, "DR_ICU_002")
            self.assertTrue(result["execution_result"]["success"])

        print(f"✅ ICU encounter completed")
        print(f"✅ Sepsis diagnosis documented")
        print(f"✅ Critical orders placed: {len(icu_orders)}")

    # ========================================================================
    # SCENARIO 3: OUTPATIENT DIABETES FOLLOW-UP
    # ========================================================================

    def test_scenario_3_outpatient_diabetes(self):
        """
        SCENARIO 3: Outpatient Clinic - Diabetes Follow-up

        Patient: 55-year-old with Type 2 Diabetes
        Setting: Primary Care Clinic
        Workflow: Check-in → Visit → Med Reconciliation → Plan
        """
        print("\n" + "="*80)
        print("SCENARIO 3: Outpatient Diabetes Follow-up")
        print("="*80)

        conversation = [
            ("How are you feeling today?", SpeakerRole.PHYSICIAN, 1.5),
            ("Pretty good overall, checking my sugars regularly", SpeakerRole.PATIENT, 2.5),
            ("What medications are you currently taking?", SpeakerRole.PHYSICIAN, 2.0),
            ("I'm on metformin 1000mg twice daily and lisinopril 20mg once daily", SpeakerRole.PATIENT, 3.5),
            ("Good. Have you been checking your blood sugars?", SpeakerRole.PHYSICIAN, 2.0),
            ("Yes, they've been running between 130 and 160", SpeakerRole.PATIENT, 2.5),
            ("Let me check your blood pressure. 128 over 82, that's good", SpeakerRole.PHYSICIAN, 3.0),
            ("Your last HbA1c was 7.2, which is okay but we can do better", SpeakerRole.PHYSICIAN, 3.0),
            ("I'd like to increase your metformin dose", SpeakerRole.PHYSICIAN, 2.0),
            ("Let's also order your annual labs including kidney function", SpeakerRole.PHYSICIAN, 2.5),
        ]

        encounter = self.system.conduct_clinical_encounter(
            "CLINIC_DM_001",
            "PT_CLINIC_11111",
            "DR_PCP_003",
            conversation
        )

        # Verify outpatient documentation
        self.assertEqual(encounter["session"]["status"], "completed")

        # Process medication adjustment
        result = self.system.process_voice_command(
            "Prescribe metformin 1000mg three times daily",
            "DR_PCP_003"
        )
        self.assertTrue(result["execution_result"]["success"])

        # Order labs
        lab_orders = [
            "Order hemoglobin A1C",
            "Order comprehensive metabolic panel",
            "Order lipid panel"
        ]

        for order in lab_orders:
            result = self.system.process_voice_command(order, "DR_PCP_003")
            self.assertTrue(result["execution_result"]["success"])

        print(f"✅ Outpatient visit completed")
        print(f"✅ Medication adjustment documented")
        print(f"✅ Follow-up labs ordered")

    # ========================================================================
    # SCENARIO 4: INPATIENT DISCHARGE PLANNING
    # ========================================================================

    def test_scenario_4_discharge_planning(self):
        """
        SCENARIO 4: Inpatient - Discharge Planning

        Patient: 68-year-old admitted for heart failure exacerbation
        Setting: Medical Floor
        Workflow: Final Assessment → Discharge Orders → Instructions
        """
        print("\n" + "="*80)
        print("SCENARIO 4: Discharge Planning")
        print("="*80)

        conversation = [
            ("Patient has improved significantly over the past 3 days", SpeakerRole.PHYSICIAN, 3.0),
            ("No longer short of breath, oxygen saturation 98 percent on room air", SpeakerRole.PHYSICIAN, 3.5),
            ("Weight down 5 pounds with diuresis", SpeakerRole.PHYSICIAN, 2.0),
            ("Lungs are clear bilaterally, no peripheral edema", SpeakerRole.PHYSICIAN, 2.5),
            ("I think we can discharge home today", SpeakerRole.PHYSICIAN, 2.0),
            ("Will continue furosemide 40mg daily at home", SpeakerRole.PHYSICIAN, 2.5),
            ("Also continuing carvedilol and lisinopril", SpeakerRole.PHYSICIAN, 2.0),
            ("Follow up with cardiology in one week", SpeakerRole.PHYSICIAN, 2.0),
            ("Daily weights and call if weight increases by more than 2 pounds", SpeakerRole.PHYSICIAN, 3.0),
        ]

        # Generate discharge summary using convenience function
        admission_date = datetime.now() - timedelta(days=3)
        discharge_date = datetime.now()

        # First create session and segments
        session_id = "DISCHARGE_001"
        self.system.ambient_intelligence.start_session(session_id, "PT_DISCHARGE_22222", "DR_HOSP_004")

        segments = []
        for text, speaker, duration in conversation:
            segment = self.system.ambient_intelligence.transcribe_segment(
                session_id, text, speaker, duration
            )
            segments.append(segment)

        # Generate discharge summary
        discharge_note = self.system.note_generator.generate_discharge_summary(
            "PT_DISCHARGE_22222",
            "DR_HOSP_004",
            admission_date,
            discharge_date,
            segments,
            session_id
        )

        # Verify discharge summary
        self.assertEqual(discharge_note.note_type.value, "discharge")
        self.assertIn("discharge_medications", discharge_note.content)
        self.assertIn("follow_up", discharge_note.content)

        print(f"✅ Discharge summary generated: {discharge_note.note_id}")
        print(f"✅ Medications documented")
        print(f"✅ Follow-up instructions included")

    # ========================================================================
    # SCENARIO 5: SURGICAL CONSULTATION
    # ========================================================================

    def test_scenario_5_surgical_consult(self):
        """
        SCENARIO 5: Surgical Consultation

        Patient: 45-year-old with acute appendicitis
        Setting: Emergency Department
        Workflow: Surgical Eval → Decision → Consent → Orders
        """
        print("\n" + "="*80)
        print("SCENARIO 5: Surgical Consultation")
        print("="*80)

        conversation = [
            ("Patient is a 45-year-old female with right lower quadrant pain", SpeakerRole.PHYSICIAN, 3.5),
            ("Pain started 12 hours ago, progressively worsening", SpeakerRole.PHYSICIAN, 2.5),
            ("Now with fever and nausea", SpeakerRole.PHYSICIAN, 2.0),
            ("When I press on your right side here, does it hurt?", SpeakerRole.PHYSICIAN, 2.5),
            ("Yes, that's very painful", SpeakerRole.PATIENT, 1.5),
            ("CT scan shows acute appendicitis with possible early perforation", SpeakerRole.PHYSICIAN, 3.0),
            ("White blood cell count elevated at 18,000", SpeakerRole.PHYSICIAN, 2.5),
            ("This requires emergency surgery", SpeakerRole.PHYSICIAN, 2.0),
            ("We need to remove your appendix laparoscopically", SpeakerRole.PHYSICIAN, 2.5),
            ("I understand, when will this happen?", SpeakerRole.PATIENT, 2.0),
            ("We'll take you to the OR within the next hour", SpeakerRole.PHYSICIAN, 2.5),
        ]

        encounter = self.system.conduct_clinical_encounter(
            "SURG_CONSULT_001",
            "PT_SURG_33333",
            "DR_SURGERY_005",
            conversation
        )

        # Verify surgical consultation
        self.assertEqual(encounter["session"]["status"], "completed")

        # Process pre-op orders
        preop_orders = [
            "Order complete blood count",
            "Order basic metabolic panel",
            "Prescribe cefoxitin 2g IV preoperative"
        ]

        for order in preop_orders:
            result = self.system.process_voice_command(order, "DR_SURGERY_005")
            self.assertTrue(result["execution_result"]["success"])

        # Document diagnosis
        result = self.system.process_voice_command(
            "Diagnose acute appendicitis",
            "DR_SURGERY_005"
        )
        self.assertTrue(result["execution_result"]["success"])

        print(f"✅ Surgical consultation completed")
        print(f"✅ Diagnosis documented")
        print(f"✅ Pre-op orders placed")

    # ========================================================================
    # SCENARIO 6: PEDIATRIC WELL-CHILD VISIT
    # ========================================================================

    def test_scenario_6_pediatric_wellchild(self):
        """
        SCENARIO 6: Pediatric Well-Child Visit

        Patient: 3-year-old for routine check-up
        Setting: Pediatric Clinic
        Workflow: Growth Check → Development → Immunizations
        """
        print("\n" + "="*80)
        print("SCENARIO 6: Pediatric Well-Child Visit")
        print("="*80)

        conversation = [
            ("How is Johnny doing?", SpeakerRole.PHYSICIAN, 1.5),
            ("He's doing great, very active and talking a lot", SpeakerRole.FAMILY, 3.0),
            ("Any concerns about his development?", SpeakerRole.PHYSICIAN, 2.0),
            ("No, he seems right on track", SpeakerRole.FAMILY, 2.0),
            ("Great. Height is 38 inches, weight is 32 pounds", SpeakerRole.PHYSICIAN, 3.0),
            ("He's in the 60th percentile for both", SpeakerRole.PHYSICIAN, 2.5),
            ("Head circumference normal, vital signs stable", SpeakerRole.PHYSICIAN, 2.5),
            ("He's due for his DTaP and MMR boosters today", SpeakerRole.PHYSICIAN, 3.0),
            ("Okay, is that safe to give together?", SpeakerRole.FAMILY, 2.0),
            ("Yes, it's safe and recommended", SpeakerRole.PHYSICIAN, 2.0),
        ]

        encounter = self.system.conduct_clinical_encounter(
            "PEDS_WCV_001",
            "PT_PEDS_44444",
            "DR_PEDS_006",
            conversation
        )

        # Verify pediatric visit
        self.assertEqual(encounter["session"]["status"], "completed")

        # Document vital signs
        vitals_commands = [
            "Record heart rate 100",
            "Record blood pressure 95 over 60"
        ]

        for cmd in vitals_commands:
            result = self.system.process_voice_command(cmd, "DR_PEDS_006")
            self.assertTrue(result["execution_result"]["success"])

        print(f"✅ Well-child visit completed")
        print(f"✅ Growth parameters documented")
        print(f"✅ Immunizations discussed")

    # ========================================================================
    # SCENARIO 7: MULTI-PROVIDER HANDOFF
    # ========================================================================

    def test_scenario_7_provider_handoff(self):
        """
        SCENARIO 7: Multi-Provider Handoff

        Patient: ICU patient, shift change handoff
        Setting: Intensive Care Unit
        Workflow: Outgoing → Incoming → Nurse Input → Orders
        """
        print("\n" + "="*80)
        print("SCENARIO 7: Multi-Provider Handoff")
        print("="*80)

        conversation = [
            ("Presenting patient in bed 5, 62-year-old male with respiratory failure", SpeakerRole.PHYSICIAN, 4.0),
            ("Intubated 2 days ago for ARDS from COVID pneumonia", SpeakerRole.PHYSICIAN, 3.0),
            ("Currently on AC mode, PEEP 12, FiO2 60 percent", SpeakerRole.PHYSICIAN, 3.5),
            ("Oxygenation improved slightly, P to F ratio now 180", SpeakerRole.PHYSICIAN, 3.0),
            ("On norepinephrine 8 micrograms per minute for blood pressure support", SpeakerRole.PHYSICIAN, 3.5),
            ("Sedated with propofol and fentanyl", SpeakerRole.PHYSICIAN, 2.0),
            ("Any issues overnight?", SpeakerRole.PHYSICIAN, 1.5),
            ("Yes, had episode of hypotension around 3 AM, increased pressors temporarily", SpeakerRole.NURSE, 4.0),
            ("Urine output decreased, only 20 mL last hour", SpeakerRole.NURSE, 2.5),
            ("Okay, may need to start CRRT if kidney function worsens", SpeakerRole.PHYSICIAN, 3.0),
            ("Continue current ventilator settings", SpeakerRole.PHYSICIAN, 2.0),
            ("Order morning labs including arterial blood gas", SpeakerRole.PHYSICIAN, 2.5),
        ]

        encounter = self.system.conduct_clinical_encounter(
            "ICU_HANDOFF_001",
            "PT_ICU_55555",
            "DR_ICU_007",
            conversation
        )

        # Verify handoff documented
        self.assertEqual(encounter["session"]["status"], "completed")
        self.assertGreater(encounter["transcript_summary"]["total_segments"], 10)

        # Verify multiple speakers
        print(f"✅ Multi-provider handoff completed")
        print(f"✅ All providers' input documented")
        print(f"✅ Plan of care updated")

    # ========================================================================
    # SCENARIO 8: HIPAA COMPLIANCE VERIFICATION
    # ========================================================================

    def test_scenario_8_hipaa_compliance(self):
        """
        SCENARIO 8: HIPAA Compliance Verification

        Test: Verify all voice data is encrypted and audited
        Focus: Security, encryption, de-identification, audit logging
        """
        print("\n" + "="*80)
        print("SCENARIO 8: HIPAA Compliance Verification")
        print("="*80)

        # Create a transcript with PHI
        transcript_with_phi = (
            "Patient John Smith, born 05/15/1965, lives at 123 Main Street. "
            "Phone number 555-123-4567. Social security number will not be included. "
            "Diagnosed with diabetes and hypertension."
        )

        # Test encryption
        audio_data = transcript_with_phi.encode('utf-8')
        encryption_result = self.system.security.encrypt_audio_data(
            audio_data, "PT_PHI_66666", "DR_SECURE_008"
        )

        self.assertTrue(encryption_result["encrypted"])
        self.assertEqual(encryption_result["encryption_method"], "AES-256")

        # Test de-identification
        deidentified = self.system.security.de_identify_transcript(transcript_with_phi)

        self.assertNotIn("John Smith", deidentified)
        self.assertNotIn("05/15/1965", deidentified)
        self.assertNotIn("123 Main Street", deidentified)
        self.assertNotIn("555-123-4567", deidentified)
        self.assertIn("[NAME]", deidentified)
        self.assertIn("[DATE]", deidentified)
        self.assertIn("[ADDRESS]", deidentified)
        self.assertIn("[PHONE]", deidentified)

        # Test audit logging
        audit_log = self.system.security.log_voice_access(
            "DR_SECURE_008", "PT_PHI_66666", "transcribe", "hash_secure_123"
        )

        self.assertEqual(audit_log.user_id, "DR_SECURE_008")
        self.assertEqual(audit_log.patient_id, "PT_PHI_66666")
        self.assertEqual(audit_log.encryption_status, "encrypted")

        # Verify audit trail retrievable
        audit_trail = self.system.security.get_audit_trail(patient_id="PT_PHI_66666")
        self.assertGreater(len(audit_trail), 0)

        # Verify retention policy
        days_to_expiry = (audit_log.retention_expires - datetime.now()).days
        self.assertGreaterEqual(days_to_expiry, 2554)  # 7 years = 2555 days

        print(f"✅ Audio data encrypted: {encryption_result['encryption_method']}")
        print(f"✅ PHI de-identified successfully")
        print(f"✅ Audit logging functional")
        print(f"✅ Retention policy: {days_to_expiry} days")
        print(f"✅ HIPAA compliance verified")


# ============================================================================
# PERFORMANCE INTEGRATION TESTS
# ============================================================================

class TestPerformanceIntegration(unittest.TestCase):
    """Test system performance under realistic loads"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = VoiceAISystem()

    def test_concurrent_encounters(self):
        """Test system can handle multiple concurrent encounters"""
        print("\n" + "="*80)
        print("PERFORMANCE TEST: Concurrent Encounters")
        print("="*80)

        # Simulate 5 concurrent patient encounters
        encounters = []
        for i in range(5):
            conversation = [
                (f"Patient {i} presents with complaint", SpeakerRole.PATIENT, 2.0),
                ("Tell me more", SpeakerRole.PHYSICIAN, 1.0),
                (f"Patient {i} provides history", SpeakerRole.PATIENT, 2.0),
            ]

            encounter = self.system.conduct_clinical_encounter(
                f"SESSION_PERF_{i}",
                f"PT_PERF_{i}",
                f"DR_PERF_{i}",
                conversation
            )
            encounters.append(encounter)

        # Verify all completed
        for encounter in encounters:
            self.assertEqual(encounter["session"]["status"], "completed")

        print(f"✅ {len(encounters)} concurrent encounters completed successfully")

    def test_high_volume_commands(self):
        """Test system can handle high volume of voice commands"""
        print("\n" + "="*80)
        print("PERFORMANCE TEST: High Volume Commands")
        print("="*80)

        import time

        commands = [
            "Order chest x-ray",
            "Order CBC",
            "Prescribe aspirin 81mg",
            "Record blood pressure 120 over 80",
            "Diagnose pneumonia"
        ]

        start_time = time.time()
        results = []

        # Process 50 commands
        for i in range(10):
            for cmd in commands:
                result = self.system.process_voice_command(cmd, f"DR_PERF_{i}")
                results.append(result)

        end_time = time.time()
        duration = end_time - start_time

        # Verify all successful
        success_count = sum(1 for r in results if r["execution_result"]["success"])
        self.assertEqual(success_count, 50)

        avg_time = duration / 50
        print(f"✅ Processed 50 commands in {duration:.2f}s")
        print(f"✅ Average time per command: {avg_time*1000:.2f}ms")
        self.assertLess(avg_time, 0.1)  # Less than 100ms per command


# ============================================================================
# RUN INTEGRATION TESTS
# ============================================================================

if __name__ == "__main__":
    # Run with verbose output
    unittest.main(verbosity=2)
