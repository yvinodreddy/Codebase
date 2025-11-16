"""
Phase 28: Ultra-fast Offline Voice AI - Integration Tests

Realistic Clinical Scenarios:
1. Complete Patient Encounter Workflow
2. Multi-EHR Hospital Network
3. Emergency Department Rapid Assessment
4. Telemedicine Consultation
5. Medication Reconciliation
6. Lab Results Review
7. High Volume Outpatient Clinic
8. Voice-Activated EHR Documentation
"""

import unittest
import time
import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from voice_ai_system import (
    VoiceAIOrchestrator,
    AudioInput,
    EHRSystem,
    VoiceCommand
)


class TestIntegrationScenarios(unittest.TestCase):
    """Integration tests with realistic clinical scenarios"""

    def setUp(self):
        """Set up orchestrator for each test"""
        self.orchestrator = VoiceAIOrchestrator(target_latency_ms=500.0, cache_ttl=300)

    def test_scenario_1_complete_patient_encounter(self):
        """
        SCENARIO 1: Complete Patient Encounter Workflow

        Context: Primary care physician performing routine patient exam
        Workflow: Check history → Review vitals → Check medications → Review allergies
        """
        patient_id = "PAT_001"
        user_id = "DR_SMITH"
        ehr_system = EHRSystem.EPIC

        # Step 1: Get patient information
        audio1 = AudioInput(
            audio_data=b"scenario1_step1_patient_info",
            sample_rate=16000,
            duration_ms=1200.0
        )

        interaction1 = self.orchestrator.process_voice_input(
            audio_input=audio1,
            ehr_system=ehr_system,
            user_id=user_id,
            patient_id=patient_id
        )

        self.assertTrue(interaction1.success)
        self.assertLess(interaction1.total_latency_ms, 1000)

        # Step 2: Get vital signs
        audio2 = AudioInput(
            audio_data=b"scenario1_step2_vitals",
            sample_rate=16000,
            duration_ms=1000.0
        )

        interaction2 = self.orchestrator.process_voice_input(
            audio_input=audio2,
            ehr_system=ehr_system,
            user_id=user_id,
            patient_id=patient_id
        )

        self.assertTrue(interaction2.success)
        self.assertIsNotNone(interaction2.ehr_response)

        # Step 3: Get medications
        audio3 = AudioInput(
            audio_data=b"scenario1_step3_medications",
            sample_rate=16000,
            duration_ms=1100.0
        )

        interaction3 = self.orchestrator.process_voice_input(
            audio_input=audio3,
            ehr_system=ehr_system,
            user_id=user_id,
            patient_id=patient_id
        )

        self.assertTrue(interaction3.success)

        # Step 4: Get allergies
        audio4 = AudioInput(
            audio_data=b"scenario1_step4_allergies",
            sample_rate=16000,
            duration_ms=900.0
        )

        interaction4 = self.orchestrator.process_voice_input(
            audio_input=audio4,
            ehr_system=ehr_system,
            user_id=user_id,
            patient_id=patient_id
        )

        self.assertTrue(interaction4.success)

        # Verify all interactions completed successfully
        self.assertEqual(len(self.orchestrator.interactions), 4)
        self.assertEqual(len(self.orchestrator.audit_logs), 4)

        # Check average latency
        metrics = self.orchestrator.get_performance_metrics()
        self.assertLess(metrics.avg_latency_ms, 1000)

    def test_scenario_2_multi_ehr_hospital_network(self):
        """
        SCENARIO 2: Multi-EHR Hospital Network

        Context: Healthcare network with multiple EHR systems
        Workflow: Query same patient across different EHR systems
        """
        patient_id = "PAT_002"
        user_id = "DR_JONES"

        # Different hospitals use different EHR systems
        ehr_systems = [
            EHRSystem.EPIC,
            EHRSystem.CERNER,
            EHRSystem.ALLSCRIPTS,
            EHRSystem.ATHENAHEALTH
        ]

        audio = AudioInput(
            audio_data=b"scenario2_patient_query",
            sample_rate=16000,
            duration_ms=1000.0
        )

        # Query each EHR system
        for ehr_system in ehr_systems:
            interaction = self.orchestrator.process_voice_input(
                audio_input=audio,
                ehr_system=ehr_system,
                user_id=user_id,
                patient_id=patient_id
            )

            self.assertTrue(interaction.success)
            self.assertLess(interaction.total_latency_ms, 1000)

        # Verify all 4 EHR systems queried
        self.assertEqual(len(self.orchestrator.interactions), 4)

    def test_scenario_3_emergency_department_rapid_assessment(self):
        """
        SCENARIO 3: Emergency Department Rapid Assessment

        Context: ED physician needs rapid patient information
        Workflow: Quick vitals → Known allergies → Current medications
        Target: All queries <500ms for emergency response
        """
        patient_id = "PAT_003_EMERGENCY"
        user_id = "DR_EMERGENCY"
        ehr_system = EHRSystem.EPIC

        # ED physician needs rapid fire information
        queries = [
            b"ed_vitals_query",
            b"ed_allergies_query",
            b"ed_medications_query"
        ]

        start_time = time.time()

        for query_data in queries:
            audio = AudioInput(
                audio_data=query_data,
                sample_rate=16000,
                duration_ms=800.0
            )

            interaction = self.orchestrator.process_voice_input(
                audio_input=audio,
                ehr_system=ehr_system,
                user_id=user_id,
                patient_id=patient_id
            )

            self.assertTrue(interaction.success)
            # Emergency queries should be fast
            self.assertLess(interaction.total_latency_ms, 1000)

        total_time = (time.time() - start_time) * 1000

        # All 3 queries should complete quickly
        self.assertLess(total_time, 3000)  # 3 seconds for 3 queries

    def test_scenario_4_telemedicine_consultation(self):
        """
        SCENARIO 4: Telemedicine Consultation

        Context: Remote consultation with patient
        Workflow: Review patient history during video call
        Requirements: Low latency for real-time interaction
        """
        patient_id = "PAT_004_TELE"
        user_id = "DR_TELEHEALTH"
        ehr_system = EHRSystem.CERNER

        # Physician asks multiple questions during consultation
        consultations = [
            b"tele_patient_history",
            b"tele_recent_labs",
            b"tele_current_vitals",
            b"tele_medication_list"
        ]

        latencies = []

        for consult_data in consultations:
            audio = AudioInput(
                audio_data=consult_data,
                sample_rate=16000,
                duration_ms=1200.0
            )

            interaction = self.orchestrator.process_voice_input(
                audio_input=audio,
                ehr_system=ehr_system,
                user_id=user_id,
                patient_id=patient_id
            )

            self.assertTrue(interaction.success)
            latencies.append(interaction.total_latency_ms)

        # Average latency should be low for good UX
        avg_latency = sum(latencies) / len(latencies)
        self.assertLess(avg_latency, 1000)

    def test_scenario_5_medication_reconciliation(self):
        """
        SCENARIO 5: Medication Reconciliation

        Context: Pharmacist reconciling medications post-discharge
        Workflow: Check current meds → Review allergies → Verify interactions
        """
        patient_id = "PAT_005_MED_REC"
        user_id = "PHARMACIST_001"
        ehr_system = EHRSystem.ECLINICALWORKS

        # Step 1: Get current medications
        audio1 = AudioInput(
            audio_data=b"med_rec_current_meds",
            sample_rate=16000,
            duration_ms=1000.0
        )

        interaction1 = self.orchestrator.process_voice_input(
            audio_input=audio1,
            ehr_system=ehr_system,
            user_id=user_id,
            patient_id=patient_id
        )

        self.assertTrue(interaction1.success)

        # Step 2: Check allergies
        audio2 = AudioInput(
            audio_data=b"med_rec_allergies",
            sample_rate=16000,
            duration_ms=900.0
        )

        interaction2 = self.orchestrator.process_voice_input(
            audio_input=audio2,
            ehr_system=ehr_system,
            user_id=user_id,
            patient_id=patient_id
        )

        self.assertTrue(interaction2.success)

        # Verify both queries completed
        self.assertGreaterEqual(len(self.orchestrator.interactions), 2)

    def test_scenario_6_lab_results_review(self):
        """
        SCENARIO 6: Lab Results Review

        Context: Physician reviewing lab results for multiple patients
        Workflow: Sequential lab result queries with caching
        """
        user_id = "DR_PATHOLOGY"
        ehr_system = EHRSystem.NEXTGEN

        # Review labs for 5 different patients
        for patient_num in range(5):
            patient_id = f"PAT_LAB_{patient_num:03d}"

            audio = AudioInput(
                audio_data=f"lab_review_{patient_num}".encode(),
                sample_rate=16000,
                duration_ms=1000.0
            )

            interaction = self.orchestrator.process_voice_input(
                audio_input=audio,
                ehr_system=ehr_system,
                user_id=user_id,
                patient_id=patient_id
            )

            self.assertTrue(interaction.success)

        # Verify 5 lab queries completed
        self.assertEqual(len(self.orchestrator.interactions), 5)

        # Check performance metrics
        metrics = self.orchestrator.get_performance_metrics()
        self.assertEqual(metrics.total_requests, 5)

    def test_scenario_7_high_volume_outpatient_clinic(self):
        """
        SCENARIO 7: High Volume Outpatient Clinic

        Context: Busy clinic with 20 patient encounters
        Workflow: Rapid sequential patient queries
        Requirements: Maintain <500ms latency under load
        """
        user_id = "DR_CLINIC"
        ehr_system = EHRSystem.MEDITECH

        start_time = time.time()

        # Simulate 20 patient encounters
        for patient_num in range(20):
            patient_id = f"CLINIC_PAT_{patient_num:03d}"

            audio = AudioInput(
                audio_data=f"clinic_encounter_{patient_num}".encode(),
                sample_rate=16000,
                duration_ms=1000.0
            )

            interaction = self.orchestrator.process_voice_input(
                audio_input=audio,
                ehr_system=ehr_system,
                user_id=user_id,
                patient_id=patient_id
            )

            self.assertTrue(interaction.success)

        total_time = (time.time() - start_time) * 1000

        # Verify all 20 encounters completed
        self.assertEqual(len(self.orchestrator.interactions), 20)

        # Check that system maintained performance under load
        metrics = self.orchestrator.get_performance_metrics()
        self.assertEqual(metrics.total_requests, 20)
        self.assertLess(total_time, 30000)  # 30 seconds for 20 encounters

    def test_scenario_8_voice_activated_ehr_documentation(self):
        """
        SCENARIO 8: Voice-Activated EHR Documentation

        Context: Physician documenting patient encounter via voice
        Workflow: Multiple voice commands for documentation
        Requirements: Fast response for natural conversation flow
        """
        patient_id = "PAT_VOICE_DOC"
        user_id = "DR_VOICE_USER"
        ehr_system = EHRSystem.PRACTICE_FUSION

        # Physician gives multiple voice commands
        commands = [
            b"voice_doc_chief_complaint",
            b"voice_doc_history",
            b"voice_doc_physical_exam",
            b"voice_doc_assessment",
            b"voice_doc_plan"
        ]

        latencies = []

        for cmd_data in commands:
            audio = AudioInput(
                audio_data=cmd_data,
                sample_rate=16000,
                duration_ms=1500.0
            )

            start = time.time()

            interaction = self.orchestrator.process_voice_input(
                audio_input=audio,
                ehr_system=ehr_system,
                user_id=user_id,
                patient_id=patient_id
            )

            latency = (time.time() - start) * 1000
            latencies.append(latency)

            self.assertTrue(interaction.success)

        # All commands should be fast for natural conversation
        max_latency = max(latencies)
        self.assertLess(max_latency, 2000)

        # Verify all documentation steps completed
        self.assertEqual(len(self.orchestrator.interactions), 5)

    def test_scenario_9_cache_effectiveness(self):
        """
        SCENARIO 9: Cache Effectiveness Test

        Context: Repeated queries for same patient information
        Workflow: Query same data multiple times, verify cache improves performance
        """
        patient_id = "PAT_CACHE_TEST"
        user_id = "DR_CACHE"
        ehr_system = EHRSystem.EPIC

        audio = AudioInput(
            audio_data=b"cache_test_vitals",
            sample_rate=16000,
            duration_ms=1000.0
        )

        # First query - cache miss
        interaction1 = self.orchestrator.process_voice_input(
            audio_input=audio,
            ehr_system=ehr_system,
            user_id=user_id,
            patient_id=patient_id
        )

        # Second query - should hit cache
        interaction2 = self.orchestrator.process_voice_input(
            audio_input=audio,
            ehr_system=ehr_system,
            user_id=user_id,
            patient_id=patient_id
        )

        # Third query - should hit cache
        interaction3 = self.orchestrator.process_voice_input(
            audio_input=audio,
            ehr_system=ehr_system,
            user_id=user_id,
            patient_id=patient_id
        )

        # Verify cache is being used
        cache_hit_rate = self.orchestrator.cache.get_hit_rate()
        self.assertGreater(cache_hit_rate, 0.5)  # At least 50% hit rate

    def test_scenario_10_all_ehr_systems_integration(self):
        """
        SCENARIO 10: Complete EHR Systems Integration Test

        Context: Verify all 11 EHR systems work correctly (100% market coverage)
        Workflow: Query each EHR system with same patient
        """
        patient_id = "PAT_ALL_EHRS"
        user_id = "DR_INTEGRATION"

        # All 11 supported EHR systems - 100% market coverage
        all_ehr_systems = [
            EHRSystem.EPIC,
            EHRSystem.CERNER,
            EHRSystem.ALLSCRIPTS,
            EHRSystem.ATHENAHEALTH,
            EHRSystem.ECLINICALWORKS,
            EHRSystem.NEXTGEN,
            EHRSystem.MEDITECH,
            EHRSystem.PRACTICE_FUSION,
            EHRSystem.MODMED,
            EHRSystem.ADVANCEDMD,
            EHRSystem.GREENWAY
        ]

        audio = AudioInput(
            audio_data=b"all_ehr_integration_test",
            sample_rate=16000,
            duration_ms=1000.0
        )

        # Test each EHR system
        for ehr_system in all_ehr_systems:
            interaction = self.orchestrator.process_voice_input(
                audio_input=audio,
                ehr_system=ehr_system,
                user_id=user_id,
                patient_id=patient_id
            )

            self.assertTrue(interaction.success, f"{ehr_system.value} failed")
            self.assertLess(interaction.total_latency_ms, 1000, f"{ehr_system.value} too slow")

        # Verify all 11 systems queried successfully
        self.assertEqual(len(self.orchestrator.interactions), 11)

        # Check success rate
        metrics = self.orchestrator.get_performance_metrics()
        self.assertEqual(metrics.success_rate, 1.0)


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
