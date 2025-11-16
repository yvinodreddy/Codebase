#!/usr/bin/env python3
"""
Comprehensive Test Suite for Clinical Trial Lifecycle System
Tests all components: Trial Management, eConsent, AE Reporting, EDC
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from trial_lifecycle_core import (
    # Systems
    TrialManagementSystem,
    ElectronicConsentSystem,
    AdverseEventReportingSystem,
    ElectronicDataCaptureSystem,
    ClinicalTrialLifecycleSystem,
    # Enums
    TrialPhase, TrialStatus, ParticipantStatus,
    ConsentStatus, AESeverity, AECausality,
    DataPointStatus, QueryStatus,
    # Helper functions
    create_trial, create_participant
)


# ============================================================================
# TRIAL MANAGEMENT TESTS
# ============================================================================

class TestTrialManagementSystem(unittest.TestCase):
    """Test trial management functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = TrialManagementSystem()

    def test_create_trial(self):
        """Test trial creation"""
        trial = self.system.create_trial(
            trial_number="NCT12345678",
            title="Test Trial for Hypertension",
            phase=TrialPhase.PHASE_II,
            sponsor="Test Pharma Inc",
            pi="Dr. John Smith",
            protocol_version="v1.0",
            target_enrollment=100
        )

        self.assertEqual(trial.trial_number, "NCT12345678")
        self.assertEqual(trial.phase, TrialPhase.PHASE_II)
        self.assertEqual(trial.status, TrialStatus.PLANNING)
        self.assertEqual(trial.target_enrollment, 100)
        self.assertIsNotNone(trial.trial_hash)

    def test_enroll_participant(self):
        """Test participant enrollment"""
        trial = self.system.create_trial(
            "NCT12345678", "Test Trial", TrialPhase.PHASE_II,
            "Sponsor", "PI", "v1.0", 100
        )

        participant = self.system.enroll_participant(
            trial_id=trial.trial_id,
            site_id="SITE001",
            screening_number="SCR001",
            demographics={"age": 45, "gender": "M"}
        )

        self.assertEqual(participant.trial_id, trial.trial_id)
        self.assertEqual(participant.site_id, "SITE001")
        self.assertEqual(participant.status, ParticipantStatus.SCREENING)
        self.assertIsNotNone(participant.participant_hash)

    def test_randomize_participant(self):
        """Test participant randomization"""
        trial = self.system.create_trial(
            "NCT12345678", "Test Trial", TrialPhase.PHASE_II,
            "Sponsor", "PI", "v1.0", 100
        )

        participant = self.system.enroll_participant(
            trial.trial_id, "SITE001", "SCR001",
            {"age": 45, "gender": "M"}
        )

        randomization_number = self.system.randomize_participant(participant.participant_id)

        self.assertIsNotNone(randomization_number)
        self.assertTrue(randomization_number.startswith("R"))
        self.assertEqual(participant.status, ParticipantStatus.ENROLLED)
        self.assertIsNotNone(participant.enrollment_date)

    def test_enrollment_stats(self):
        """Test enrollment statistics"""
        trial = self.system.create_trial(
            "NCT12345678", "Test Trial", TrialPhase.PHASE_II,
            "Sponsor", "PI", "v1.0", 100
        )

        # Enroll 3 participants
        for i in range(3):
            participant = self.system.enroll_participant(
                trial.trial_id, "SITE001", f"SCR00{i+1}",
                {"age": 45, "gender": "M"}
            )
            if i < 2:  # Randomize 2 out of 3
                self.system.randomize_participant(participant.participant_id)

        stats = self.system.get_trial_enrollment_stats(trial.trial_id)

        self.assertEqual(stats["total_participants"], 3)
        self.assertEqual(stats["enrolled"], 2)
        self.assertEqual(stats["enrollment_percentage"], 3.0)  # 3/100 * 100

    def test_audit_log_creation(self):
        """Test audit log is created for actions"""
        trial = self.system.create_trial(
            "NCT12345678", "Test Trial", TrialPhase.PHASE_II,
            "Sponsor", "PI", "v1.0", 100
        )

        # Check audit log
        self.assertGreater(len(self.system.audit_log), 0)
        log_entry = self.system.audit_log[0]
        self.assertEqual(log_entry.action, "CREATE")
        self.assertEqual(log_entry.entity_type, "Trial")
        self.assertIsNotNone(log_entry.log_hash)


# ============================================================================
# ELECTRONIC CONSENT TESTS
# ============================================================================

class TestElectronicConsentSystem(unittest.TestCase):
    """Test electronic consent functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = ElectronicConsentSystem()

    def test_create_consent_form(self):
        """Test consent form creation"""
        consent = self.system.create_consent_form(
            trial_id="trial123",
            participant_id="participant456",
            version="v1.0",
            form_content="This is a test consent form...",
            language="en"
        )

        self.assertEqual(consent.trial_id, "trial123")
        self.assertEqual(consent.participant_id, "participant456")
        self.assertEqual(consent.version, "v1.0")
        self.assertEqual(consent.status, ConsentStatus.PENDING)
        self.assertIsNotNone(consent.consent_hash)

    def test_comprehension_assessment(self):
        """Test comprehension assessment"""
        consent = self.system.create_consent_form(
            "trial123", "participant456", "v1.0",
            "Consent form content", "en"
        )

        # Provide good answers
        answers = {
            "purpose": "To test a new treatment for hypertension",
            "voluntary": "Yes, I can leave at any time",
            "risks": "Possible side effects include headache and dizziness",
            "benefits": "May help lower my blood pressure",
            "confidentiality": "My information will be kept private and secure"
        }

        assessment = self.system.assess_comprehension(consent.consent_id, answers)

        self.assertTrue(assessment["overall_passed"])
        self.assertEqual(assessment["total_questions"], 5)
        self.assertGreaterEqual(assessment["pass_rate"], 0.8)

    def test_comprehension_assessment_fail(self):
        """Test comprehension assessment failure"""
        consent = self.system.create_consent_form(
            "trial123", "participant456", "v1.0",
            "Consent form content", "en"
        )

        # Provide poor answers
        answers = {
            "purpose": "No",  # Too short
            "voluntary": "No",  # Wrong answer
            "risks": "No",
            "benefits": "No",
            "confidentiality": "No"
        }

        assessment = self.system.assess_comprehension(consent.consent_id, answers)

        self.assertFalse(assessment["overall_passed"])
        self.assertLess(assessment["pass_rate"], 0.8)

    def test_sign_consent(self):
        """Test consent signing"""
        consent = self.system.create_consent_form(
            "trial123", "participant456", "v1.0",
            "Consent form content", "en"
        )

        # First assess comprehension
        answers = {
            "purpose": "To test a new treatment for hypertension",
            "voluntary": "Yes, I can leave at any time",
            "risks": "Possible side effects",
            "benefits": "May help lower blood pressure",
            "confidentiality": "Information kept private"
        }
        self.system.assess_comprehension(consent.consent_id, answers)

        # Sign consent
        success = self.system.sign_consent(
            consent.consent_id,
            signature_data="John Doe signature data",
            witness_signature="Witness signature"
        )

        self.assertTrue(success)
        self.assertEqual(consent.status, ConsentStatus.SIGNED)
        self.assertIsNotNone(consent.signed_at)
        self.assertIsNotNone(consent.signature_data)

    def test_sign_consent_without_comprehension_fails(self):
        """Test signing without comprehension fails"""
        consent = self.system.create_consent_form(
            "trial123", "participant456", "v1.0",
            "Consent form content", "en"
        )

        # Try to sign without comprehension
        with self.assertRaises(ValueError):
            self.system.sign_consent(consent.consent_id, "signature")

    def test_withdraw_consent(self):
        """Test consent withdrawal"""
        consent = self.system.create_consent_form(
            "trial123", "participant456", "v1.0",
            "Consent form content", "en"
        )

        # Sign consent first with proper comprehension answers
        answers = {
            "purpose": "To test a new treatment for hypertension and evaluate safety",
            "voluntary": "Yes, I can leave the study at any time without penalty",
            "risks": "Possible side effects include headache dizziness and nausea",
            "benefits": "May help lower my blood pressure and improve my health",
            "confidentiality": "My information will be kept private and confidential per HIPAA"
        }
        self.system.assess_comprehension(consent.consent_id, answers)
        self.system.sign_consent(consent.consent_id, "signature")

        # Withdraw consent
        success = self.system.withdraw_consent(
            consent.consent_id,
            reason="Personal reasons"
        )

        self.assertTrue(success)
        self.assertEqual(consent.status, ConsentStatus.WITHDRAWN)
        self.assertIsNotNone(consent.withdrawal_date)
        self.assertEqual(consent.withdrawal_reason, "Personal reasons")

    def test_consent_history(self):
        """Test consent history retrieval"""
        # Create multiple consents for same participant
        for i in range(3):
            self.system.create_consent_form(
                "trial123", "participant456", f"v{i+1}.0",
                "Consent form content", "en"
            )

        history = self.system.get_consent_history("participant456")

        self.assertEqual(len(history), 3)
        # Should be sorted by creation date (descending)
        self.assertEqual(history[0]["version"], "v3.0")


# ============================================================================
# ADVERSE EVENT REPORTING TESTS
# ============================================================================

class TestAdverseEventReportingSystem(unittest.TestCase):
    """Test adverse event reporting functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = AdverseEventReportingSystem()

    def test_report_adverse_event(self):
        """Test AE reporting"""
        ae = self.system.report_adverse_event(
            trial_id="trial123",
            participant_id="participant456",
            site_id="SITE001",
            event_term="Headache",
            event_description="Patient reported mild headache",
            severity=AESeverity.GRADE_1,
            causality=AECausality.POSSIBLE,
            onset_date=datetime.now()
        )

        self.assertEqual(ae.event_term, "Headache")
        self.assertEqual(ae.severity, AESeverity.GRADE_1)
        self.assertFalse(ae.serious)  # Grade 1 is not SAE
        self.assertIsNotNone(ae.ae_hash)

    def test_report_serious_adverse_event(self):
        """Test SAE reporting with auto-flagging"""
        ae = self.system.report_adverse_event(
            trial_id="trial123",
            participant_id="participant456",
            site_id="SITE001",
            event_term="Myocardial Infarction",
            event_description="Life-threatening heart attack",
            severity=AESeverity.GRADE_4,
            causality=AECausality.PROBABLE,
            onset_date=datetime.now()
        )

        self.assertEqual(ae.severity, AESeverity.GRADE_4)
        self.assertTrue(ae.serious)  # Grade 4 is SAE
        self.assertTrue(ae.reported_to_irb)
        self.assertTrue(ae.reported_to_sponsor)

    def test_report_death_triggers_fda_reporting(self):
        """Test Grade 5 (death) triggers FDA reporting"""
        ae = self.system.report_adverse_event(
            trial_id="trial123",
            participant_id="participant456",
            site_id="SITE001",
            event_term="Death",
            event_description="Patient died",
            severity=AESeverity.GRADE_5,
            causality=AECausality.DEFINITE,
            onset_date=datetime.now()
        )

        self.assertEqual(ae.severity, AESeverity.GRADE_5)
        self.assertTrue(ae.serious)
        self.assertTrue(ae.reported_to_fda)  # Death requires FDA reporting

    def test_update_ae_outcome(self):
        """Test updating AE outcome"""
        ae = self.system.report_adverse_event(
            "trial123", "participant456", "SITE001",
            "Nausea", "Mild nausea", AESeverity.GRADE_1,
            AECausality.POSSIBLE, datetime.now()
        )

        updated_ae = self.system.update_ae_outcome(
            ae.ae_id,
            outcome="Resolved",
            resolution_date=datetime.now(),
            action_taken="No action required"
        )

        self.assertEqual(updated_ae.outcome, "Resolved")
        self.assertIsNotNone(updated_ae.resolution_date)
        self.assertEqual(updated_ae.action_taken, "No action required")

    def test_causality_assessment(self):
        """Test causality assessment (Naranjo algorithm)"""
        ae = self.system.report_adverse_event(
            "trial123", "participant456", "SITE001",
            "Rash", "Skin rash", AESeverity.GRADE_2,
            AECausality.POSSIBLE, datetime.now()
        )

        # Provide factors for causality assessment
        factors = {
            "temporal_relationship": True,
            "known_reaction": True,
            "improved_on_discontinuation": True,
            "reappeared_on_rechallenge": False,
            "alternative_causes": False
        }

        causality = self.system.assess_causality(ae.ae_id, factors)

        self.assertIn(causality, [
            AECausality.UNLIKELY, AECausality.POSSIBLE,
            AECausality.PROBABLE, AECausality.DEFINITE
        ])
        # With these factors, score should be 6, resulting in PROBABLE
        self.assertEqual(causality, AECausality.PROBABLE)

    def test_safety_summary(self):
        """Test safety summary generation"""
        # Report multiple AEs
        for i in range(5):
            severity = AESeverity.GRADE_1 if i < 3 else AESeverity.GRADE_3
            self.system.report_adverse_event(
                "trial123", "participant456", "SITE001",
                f"Event {i}", f"Description {i}",
                severity, AECausality.POSSIBLE, datetime.now()
            )

        summary = self.system.get_safety_summary("trial123")

        self.assertEqual(summary["total_aes"], 5)
        self.assertEqual(summary["severity_breakdown"]["Grade 1"], 3)
        self.assertEqual(summary["severity_breakdown"]["Grade 3"], 2)
        self.assertEqual(summary["serious_aes"], 2)  # Grade 3+ are SAEs


# ============================================================================
# ELECTRONIC DATA CAPTURE TESTS
# ============================================================================

class TestElectronicDataCaptureSystem(unittest.TestCase):
    """Test EDC functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = ElectronicDataCaptureSystem()

    def test_enter_data(self):
        """Test CRF data entry"""
        data = self.system.enter_data(
            trial_id="trial123",
            participant_id="participant456",
            visit_id="V1",
            form_name="Demographics",
            field_name="age",
            field_value=45,
            entered_by="user1"
        )

        self.assertEqual(data.field_name, "age")
        self.assertEqual(data.field_value, 45)
        self.assertEqual(data.status, DataPointStatus.ENTERED)
        self.assertIsNotNone(data.data_hash)

    def test_data_validation(self):
        """Test automatic data validation"""
        # Enter valid age
        data_valid = self.system.enter_data(
            "trial123", "participant456", "V1",
            "Demographics", "age", 45, "user1"
        )
        self.assertEqual(data_valid.status, DataPointStatus.ENTERED)
        self.assertIsNone(data_valid.query_id)

        # Enter invalid age (out of range)
        data_invalid = self.system.enter_data(
            "trial123", "participant456", "V1",
            "Demographics", "age", 150, "user1"  # > 120
        )
        self.assertEqual(data_invalid.status, DataPointStatus.QUERY_OPEN)
        self.assertIsNotNone(data_invalid.query_id)  # Auto-query created

    def test_verify_data(self):
        """Test data verification (SDV)"""
        data = self.system.enter_data(
            "trial123", "participant456", "V1",
            "Demographics", "age", 45, "user1"
        )

        verified_data = self.system.verify_data(data.crf_id, "verifier1")

        self.assertEqual(verified_data.status, DataPointStatus.VERIFIED)
        self.assertEqual(verified_data.verified_by, "verifier1")
        self.assertIsNotNone(verified_data.verified_at)

    def test_lock_data(self):
        """Test data locking"""
        data = self.system.enter_data(
            "trial123", "participant456", "V1",
            "Demographics", "age", 45, "user1"
        )

        # Must verify before locking
        self.system.verify_data(data.crf_id, "verifier1")

        locked_data = self.system.lock_data(data.crf_id, "dm_user")

        self.assertTrue(locked_data.locked)
        self.assertEqual(locked_data.status, DataPointStatus.LOCKED)

    def test_cannot_lock_unverified_data(self):
        """Test cannot lock unverified data"""
        data = self.system.enter_data(
            "trial123", "participant456", "V1",
            "Demographics", "age", 45, "user1"
        )

        with self.assertRaises(ValueError):
            self.system.lock_data(data.crf_id, "dm_user")

    def test_create_query(self):
        """Test data query creation"""
        data = self.system.enter_data(
            "trial123", "participant456", "V1",
            "Demographics", "age", 45, "user1"
        )

        query = self.system.create_query(
            trial_id="trial123",
            participant_id="participant456",
            crf_id=data.crf_id,
            field_name="age",
            query_text="Please verify this age value",
            opened_by="dm_user"
        )

        self.assertEqual(query.query_text, "Please verify this age value")
        self.assertEqual(query.status, QueryStatus.OPEN)
        self.assertIsNotNone(query.query_hash)

    def test_respond_to_query(self):
        """Test query response"""
        data = self.system.enter_data(
            "trial123", "participant456", "V1",
            "Demographics", "age", 45, "user1"
        )

        query = self.system.create_query(
            "trial123", "participant456", data.crf_id,
            "age", "Please verify", "dm_user"
        )

        responded_query = self.system.respond_to_query(
            query.query_id,
            response_text="Age verified from source documents",
            responded_by="site_user"
        )

        self.assertEqual(responded_query.status, QueryStatus.ANSWERED)
        self.assertIsNotNone(responded_query.response_text)
        self.assertIsNotNone(responded_query.responded_at)

    def test_close_query(self):
        """Test query closure"""
        data = self.system.enter_data(
            "trial123", "participant456", "V1",
            "Demographics", "age", 45, "user1"
        )

        query = self.system.create_query(
            "trial123", "participant456", data.crf_id,
            "age", "Please verify", "dm_user"
        )

        self.system.respond_to_query(
            query.query_id, "Verified", "site_user"
        )

        closed_query = self.system.close_query(query.query_id, "dm_user")

        self.assertEqual(closed_query.status, QueryStatus.CLOSED)
        self.assertIsNotNone(closed_query.closed_at)

    def test_export_data_cdisc(self):
        """Test CDISC SDTM export"""
        # Enter multiple data points
        for i in range(3):
            self.system.enter_data(
                "trial123", "participant456", "V1",
                "Demographics", f"field_{i}", f"value_{i}", "user1"
            )

        export = self.system.export_data_cdisc("trial123")

        self.assertEqual(export["trial_id"], "trial123")
        self.assertEqual(export["format"], "CDISC SDTM")
        self.assertEqual(export["total_records"], 3)
        self.assertIn("domains", export)

    def test_data_quality_metrics(self):
        """Test data quality metrics"""
        # Enter and verify some data
        for i in range(5):
            data = self.system.enter_data(
                "trial123", "participant456", "V1",
                "Demographics", f"field_{i}", f"value_{i}", "user1"
            )
            if i < 3:  # Verify 3 out of 5
                self.system.verify_data(data.crf_id, "verifier1")

        metrics = self.system.get_data_quality_metrics("trial123")

        self.assertEqual(metrics["total_data_points"], 5)
        self.assertEqual(metrics["verified"], 3)
        self.assertEqual(metrics["verification_rate"], 0.6)


# ============================================================================
# INTEGRATED SYSTEM TESTS
# ============================================================================

class TestClinicalTrialLifecycleSystem(unittest.TestCase):
    """Test integrated clinical trial lifecycle system"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = ClinicalTrialLifecycleSystem()

    def test_integrated_trial_creation(self):
        """Test integrated trial creation"""
        trial = self.system.create_trial(
            trial_number="NCT12345678",
            title="Integrated Test Trial",
            phase=TrialPhase.PHASE_III,
            sponsor="Test Pharma",
            pi="Dr. Smith",
            protocol_version="v1.0",
            target_enrollment=50
        )

        self.assertEqual(self.system.stats["trials_created"], 1)
        self.assertIsNotNone(trial.trial_id)

    def test_integrated_participant_enrollment(self):
        """Test integrated participant enrollment with auto-consent"""
        trial = self.system.create_trial(
            "NCT12345678", "Test Trial", TrialPhase.PHASE_III,
            "Sponsor", "PI", "v1.0", 50
        )

        participant = self.system.enroll_participant(
            trial_id=trial.trial_id,
            site_id="SITE001",
            screening_number="SCR001",
            demographics={"age": 45, "gender": "M", "language": "en"}
        )

        self.assertEqual(self.system.stats["participants_enrolled"], 1)
        # Check that consent was auto-created
        consents = [c for c in self.system.econsent.consent_forms.values()
                   if c.participant_id == participant.participant_id]
        self.assertEqual(len(consents), 1)

    def test_integrated_consent_process(self):
        """Test integrated consent processing"""
        trial = self.system.create_trial(
            "NCT12345678", "Test Trial", TrialPhase.PHASE_III,
            "Sponsor", "PI", "v1.0", 50
        )

        participant = self.system.enroll_participant(
            trial.trial_id, "SITE001", "SCR001",
            {"age": 45, "gender": "M", "language": "en"}
        )

        # Process consent
        result = self.system.process_consent(
            participant_id=participant.participant_id,
            signature_data="John Doe signature",
            comprehension_answers={
                "purpose": "To test new treatment",
                "voluntary": "Yes, I can leave anytime",
                "risks": "Possible side effects",
                "benefits": "May improve condition",
                "confidentiality": "Information kept private"
            }
        )

        self.assertTrue(result["success"])
        self.assertEqual(self.system.stats["consents_signed"], 1)
        self.assertEqual(participant.status, ParticipantStatus.CONSENTED)

    def test_integrated_ae_reporting(self):
        """Test integrated AE reporting"""
        trial = self.system.create_trial(
            "NCT12345678", "Test Trial", TrialPhase.PHASE_III,
            "Sponsor", "PI", "v1.0", 50
        )

        participant = self.system.enroll_participant(
            trial.trial_id, "SITE001", "SCR001",
            {"age": 45, "gender": "M"}
        )

        ae = self.system.report_adverse_event(
            trial_id=trial.trial_id,
            participant_id=participant.participant_id,
            site_id="SITE001",
            event_term="Headache",
            event_description="Mild headache",
            severity=AESeverity.GRADE_1,
            causality=AECausality.POSSIBLE,
            onset_date=datetime.now()
        )

        self.assertEqual(self.system.stats["aes_reported"], 1)
        self.assertIn(ae.ae_id, participant.adverse_events)

    def test_integrated_visit_data_entry(self):
        """Test integrated visit data entry"""
        trial = self.system.create_trial(
            "NCT12345678", "Test Trial", TrialPhase.PHASE_III,
            "Sponsor", "PI", "v1.0", 50
        )

        participant = self.system.enroll_participant(
            trial.trial_id, "SITE001", "SCR001",
            {"age": 45, "gender": "M"}
        )

        form_data = {
            "Vitals": {
                "weight": 75.5,
                "height": 175,
                "blood_pressure_systolic": 120,
                "blood_pressure_diastolic": 80,
                "heart_rate": 72
            }
        }

        crf_entries = self.system.enter_visit_data(
            trial_id=trial.trial_id,
            participant_id=participant.participant_id,
            visit_id="V1",
            form_data=form_data,
            entered_by="user1"
        )

        self.assertEqual(len(crf_entries), 5)
        self.assertEqual(self.system.stats["data_points_entered"], 5)
        self.assertIn("V1", participant.visits_completed)

    def test_trial_dashboard(self):
        """Test comprehensive trial dashboard"""
        trial = self.system.create_trial(
            "NCT12345678", "Test Trial", TrialPhase.PHASE_III,
            "Sponsor", "PI", "v1.0", 10
        )

        # Enroll and consent participants
        for i in range(5):
            participant = self.system.enroll_participant(
                trial.trial_id, "SITE001", f"SCR00{i+1}",
                {"age": 45, "gender": "M"}
            )

            # Process consent with proper comprehension answers
            self.system.process_consent(
                participant.participant_id,
                f"Signature {i}",
                {
                    "purpose": "To test a new treatment for the medical condition",
                    "voluntary": "Yes, I understand participation is completely voluntary",
                    "risks": "Possible side effects include headache nausea and fatigue",
                    "benefits": "Potential benefits include improved health outcomes",
                    "confidentiality": "My personal information will be kept private and secure"
                }
            )

            # Enter visit data
            self.system.enter_visit_data(
                trial.trial_id, participant.participant_id, "V1",
                {"Vitals": {"weight": 75}}, "user1"
            )

        dashboard = self.system.generate_trial_dashboard(trial.trial_id)

        self.assertEqual(dashboard["enrollment"]["total_participants"], 5)
        self.assertEqual(dashboard["consents"]["signed"], 5)
        self.assertIn("overall_health", dashboard)
        self.assertIsNotNone(dashboard["data_quality"])

    def test_system_statistics(self):
        """Test system statistics"""
        stats = self.system.get_statistics()

        self.assertIn("trials_created", stats)
        self.assertIn("participants_enrolled", stats)
        self.assertIn("consents_signed", stats)
        self.assertIn("aes_reported", stats)
        self.assertIn("data_points_entered", stats)
        self.assertIn("total_audit_entries", stats)


if __name__ == "__main__":
    unittest.main()
