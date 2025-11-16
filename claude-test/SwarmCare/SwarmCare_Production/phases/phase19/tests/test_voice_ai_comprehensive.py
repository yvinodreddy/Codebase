"""
Phase 19: Voice AI & Ambient Intelligence - Comprehensive Unit Tests
Production-Ready Test Suite

Coverage:
- VoiceCommandProcessor (medication, orders, vitals, diagnosis)
- AmbientClinicalIntelligence (transcription, speaker diarization)
- ClinicalNoteGenerator (SOAP, H&P, discharge)
- VoiceDataSecurity (encryption, audit, de-identification)
- Integrated VoiceAISystem

Target: 40+ tests, 100% pass rate
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from voice_ai_system import (
    VoiceCommandProcessor, AmbientClinicalIntelligence, ClinicalNoteGenerator,
    VoiceDataSecurity, VoiceAISystem,
    VoiceCommandType, NoteType, SpeakerRole,
    VoiceCommand, TranscriptionSegment, ClinicalNote
)


# ============================================================================
# TEST VOICE COMMAND PROCESSOR
# ============================================================================

class TestVoiceCommandProcessor(unittest.TestCase):
    """Test VoiceCommandProcessor with medical commands"""

    def setUp(self):
        """Set up test fixtures"""
        self.processor = VoiceCommandProcessor()

    def test_initialization(self):
        """Test processor initializes correctly"""
        self.assertIsNotNone(self.processor)
        self.assertIsNotNone(self.processor.command_patterns)
        self.assertEqual(len(self.processor.command_history), 0)

    def test_medication_order_simple(self):
        """Test simple medication order: 'Prescribe amoxicillin 500mg three times daily'"""
        command = self.processor.process_command("Prescribe amoxicillin 500mg three times daily")

        self.assertEqual(command.command_type, VoiceCommandType.MEDICATION)
        self.assertEqual(command.extracted_data["medication"], "amoxicillin")
        self.assertEqual(command.extracted_data["dose"], "500mg")
        self.assertGreater(command.confidence, 0.8)

    def test_medication_order_case_insensitive(self):
        """Test case-insensitive medication parsing"""
        command = self.processor.process_command("PRESCRIBE METFORMIN 1000MG TWICE DAILY")

        self.assertEqual(command.command_type, VoiceCommandType.MEDICATION)
        self.assertEqual(command.extracted_data["medication"].lower(), "metformin")

    def test_medication_therapy_start(self):
        """Test therapy start command"""
        command = self.processor.process_command("Start insulin therapy")

        self.assertEqual(command.command_type, VoiceCommandType.MEDICATION)
        self.assertEqual(command.extracted_data["medication"], "insulin")

    def test_clinical_order_xray(self):
        """Test clinical order: chest x-ray"""
        command = self.processor.process_command("Order chest x-ray stat")

        self.assertEqual(command.command_type, VoiceCommandType.CLINICAL_ORDER)
        self.assertIn("chest x-ray", command.extracted_data["test_name"])
        self.assertGreater(command.confidence, 0.8)

    def test_clinical_order_ct_scan(self):
        """Test clinical order: CT scan"""
        command = self.processor.process_command("Order head ct scan")

        self.assertEqual(command.command_type, VoiceCommandType.CLINICAL_ORDER)
        self.assertIn("head ct", command.extracted_data["test_name"])

    def test_vital_signs_blood_pressure(self):
        """Test blood pressure documentation"""
        command = self.processor.process_command("Record blood pressure 120 over 80")

        self.assertEqual(command.command_type, VoiceCommandType.VITAL_SIGNS)
        self.assertEqual(command.extracted_data["systolic"], "120")
        self.assertEqual(command.extracted_data["diastolic"], "80")
        self.assertGreater(command.confidence, 0.9)

    def test_vital_signs_temperature_celsius(self):
        """Test temperature documentation in Celsius"""
        command = self.processor.process_command("Record temperature 38.5 celsius")

        self.assertEqual(command.command_type, VoiceCommandType.VITAL_SIGNS)
        self.assertEqual(command.extracted_data["value"], "38.5")
        self.assertEqual(command.extracted_data["unit"], "celsius")

    def test_vital_signs_heart_rate(self):
        """Test heart rate documentation"""
        command = self.processor.process_command("Document heart rate 95")

        self.assertEqual(command.command_type, VoiceCommandType.VITAL_SIGNS)
        self.assertEqual(command.extracted_data["value"], "95")

    def test_diagnosis_command(self):
        """Test diagnosis command"""
        command = self.processor.process_command("Diagnose pneumonia")

        self.assertEqual(command.command_type, VoiceCommandType.DIAGNOSIS)
        self.assertEqual(command.extracted_data["condition"], "pneumonia")

    def test_differential_diagnosis(self):
        """Test differential diagnosis (rule out)"""
        command = self.processor.process_command("Rule out pulmonary embolism")

        self.assertEqual(command.command_type, VoiceCommandType.DIAGNOSIS)
        self.assertEqual(command.extracted_data["differential"], "pulmonary embolism")

    def test_command_execution(self):
        """Test command execution"""
        command = self.processor.process_command("Order chest x-ray")
        result = self.processor.execute_command(command)

        self.assertTrue(result["success"])
        self.assertEqual(result["command_id"], command.command_id)
        self.assertTrue(command.executed)

    def test_command_history(self):
        """Test command history tracking"""
        initial_count = len(self.processor.command_history)

        self.processor.process_command("Order CBC")
        self.processor.process_command("Prescribe aspirin 81mg daily")

        self.assertEqual(len(self.processor.command_history), initial_count + 2)

        history = self.processor.get_command_history(limit=2)
        self.assertEqual(len(history), 2)

    def test_unknown_command_fallback(self):
        """Test unknown command defaults to documentation"""
        command = self.processor.process_command("This is random text")

        self.assertEqual(command.command_type, VoiceCommandType.DOCUMENTATION)
        self.assertLess(command.confidence, 0.6)


# ============================================================================
# TEST AMBIENT CLINICAL INTELLIGENCE
# ============================================================================

class TestAmbientClinicalIntelligence(unittest.TestCase):
    """Test ambient listening and transcription"""

    def setUp(self):
        """Set up test fixtures"""
        self.ambient = AmbientClinicalIntelligence()

    def test_initialization(self):
        """Test ambient intelligence initializes correctly"""
        self.assertIsNotNone(self.ambient)
        self.assertEqual(len(self.ambient.active_sessions), 0)

    def test_start_session(self):
        """Test starting ambient listening session"""
        result = self.ambient.start_session("SESSION_001", "PT_123", "DR_001")

        self.assertEqual(result["session_id"], "SESSION_001")
        self.assertEqual(result["status"], "active")
        self.assertIn("SESSION_001", self.ambient.active_sessions)

    def test_transcribe_patient_segment(self):
        """Test transcribing patient segment"""
        self.ambient.start_session("SESSION_001", "PT_123", "DR_001")

        segment = self.ambient.transcribe_segment(
            "SESSION_001",
            "I have chest pain and shortness of breath",
            SpeakerRole.PATIENT,
            3.0
        )

        self.assertEqual(segment.speaker, SpeakerRole.PATIENT)
        self.assertEqual(segment.text, "I have chest pain and shortness of breath")
        self.assertEqual(segment.duration_seconds, 3.0)
        self.assertGreater(segment.confidence, 0.9)

    def test_transcribe_physician_segment(self):
        """Test transcribing physician segment"""
        self.ambient.start_session("SESSION_001", "PT_123", "DR_001")

        segment = self.ambient.transcribe_segment(
            "SESSION_001",
            "Blood pressure is 140 over 90",
            SpeakerRole.PHYSICIAN,
            2.0
        )

        self.assertEqual(segment.speaker, SpeakerRole.PHYSICIAN)

    def test_medical_entity_extraction_symptoms(self):
        """Test medical entity extraction: symptoms"""
        self.ambient.start_session("SESSION_001", "PT_123", "DR_001")

        segment = self.ambient.transcribe_segment(
            "SESSION_001",
            "Patient reports chest pain and dyspnea",
            SpeakerRole.PHYSICIAN,
            2.0
        )

        entities = segment.medical_entities
        entity_texts = [e["text"] for e in entities]

        self.assertIn("chest pain", entity_texts)
        self.assertIn("dyspnea", entity_texts)

    def test_medical_entity_extraction_medications(self):
        """Test medical entity extraction: medications"""
        self.ambient.start_session("SESSION_001", "PT_123", "DR_001")

        segment = self.ambient.transcribe_segment(
            "SESSION_001",
            "Currently on metformin and insulin",
            SpeakerRole.PATIENT,
            2.0
        )

        entities = segment.medical_entities
        entity_types = [e["type"] for e in entities]

        self.assertIn("medication", entity_types)

    def test_medical_entity_extraction_diagnoses(self):
        """Test medical entity extraction: diagnoses"""
        self.ambient.start_session("SESSION_001", "PT_123", "DR_001")

        segment = self.ambient.transcribe_segment(
            "SESSION_001",
            "History of diabetes and hypertension",
            SpeakerRole.PHYSICIAN,
            2.0
        )

        entities = segment.medical_entities
        entity_types = [e["type"] for e in entities]

        self.assertIn("diagnosis", entity_types)

    def test_get_session_transcript(self):
        """Test retrieving full session transcript"""
        session_id = "SESSION_001"
        self.ambient.start_session(session_id, "PT_123", "DR_001")

        self.ambient.transcribe_segment(session_id, "First segment", SpeakerRole.PATIENT, 1.0)
        self.ambient.transcribe_segment(session_id, "Second segment", SpeakerRole.PHYSICIAN, 1.5)

        transcript = self.ambient.get_session_transcript(session_id)

        self.assertEqual(transcript["session_id"], session_id)
        self.assertEqual(transcript["total_segments"], 2)
        self.assertEqual(transcript["total_duration"], 2.5)

    def test_end_session(self):
        """Test ending ambient session"""
        session_id = "SESSION_001"
        self.ambient.start_session(session_id, "PT_123", "DR_001")
        self.ambient.transcribe_segment(session_id, "Test", SpeakerRole.PATIENT, 1.0)

        result = self.ambient.end_session(session_id)

        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["total_segments"], 1)

    def test_nonexistent_session(self):
        """Test accessing nonexistent session"""
        result = self.ambient.get_session_transcript("FAKE_SESSION")

        self.assertIn("error", result)


# ============================================================================
# TEST CLINICAL NOTE GENERATOR
# ============================================================================

class TestClinicalNoteGenerator(unittest.TestCase):
    """Test clinical note generation"""

    def setUp(self):
        """Set up test fixtures"""
        self.generator = ClinicalNoteGenerator()
        self.sample_segments = self._create_sample_segments()

    def _create_sample_segments(self):
        """Create sample transcript segments for testing"""
        segments = [
            TranscriptionSegment(
                segment_id="SEG_001",
                timestamp=datetime.now(),
                speaker=SpeakerRole.PATIENT,
                text="I have chest pain and shortness of breath",
                confidence=0.95,
                duration_seconds=3.0,
                medical_entities=[
                    {"text": "chest pain", "type": "symptom", "start": 7, "end": 17},
                    {"text": "shortness of breath", "type": "symptom", "start": 22, "end": 41}
                ]
            ),
            TranscriptionSegment(
                segment_id="SEG_002",
                timestamp=datetime.now(),
                speaker=SpeakerRole.PHYSICIAN,
                text="Blood pressure 140 over 90, heart rate 95",
                confidence=0.96,
                duration_seconds=2.5,
                medical_entities=[]
            ),
            TranscriptionSegment(
                segment_id="SEG_003",
                timestamp=datetime.now(),
                speaker=SpeakerRole.PHYSICIAN,
                text="Assessment: likely angina, rule out myocardial infarction",
                confidence=0.94,
                duration_seconds=4.0,
                medical_entities=[
                    {"text": "angina", "type": "diagnosis", "start": 23, "end": 29}
                ]
            ),
            TranscriptionSegment(
                segment_id="SEG_004",
                timestamp=datetime.now(),
                speaker=SpeakerRole.PHYSICIAN,
                text="Plan: order troponin, EKG, start aspirin",
                confidence=0.95,
                duration_seconds=3.0,
                medical_entities=[
                    {"text": "aspirin", "type": "medication", "start": 34, "end": 41}
                ]
            )
        ]
        return segments

    def test_initialization(self):
        """Test note generator initializes correctly"""
        self.assertIsNotNone(self.generator)
        self.assertIsNotNone(self.generator.note_templates)
        self.assertEqual(len(self.generator.generated_notes), 0)

    def test_soap_note_generation(self):
        """Test SOAP note generation"""
        note = self.generator.generate_soap_note(
            "PT_123", "DR_001", self.sample_segments, "SESSION_001"
        )

        self.assertEqual(note.note_type, NoteType.SOAP)
        self.assertEqual(note.patient_id, "PT_123")
        self.assertEqual(note.provider_id, "DR_001")
        self.assertIn("subjective", note.content)
        self.assertIn("objective", note.content)
        self.assertIn("assessment", note.content)
        self.assertIn("plan", note.content)

    def test_soap_note_subjective_extraction(self):
        """Test SOAP subjective section extraction"""
        note = self.generator.generate_soap_note(
            "PT_123", "DR_001", self.sample_segments, "SESSION_001"
        )

        subjective = note.content["subjective"]
        self.assertIn("chest pain", subjective.lower())
        self.assertIn("shortness of breath", subjective.lower())

    def test_soap_note_objective_extraction(self):
        """Test SOAP objective section extraction"""
        note = self.generator.generate_soap_note(
            "PT_123", "DR_001", self.sample_segments, "SESSION_001"
        )

        objective = note.content["objective"]
        self.assertIn("blood pressure", objective.lower())

    def test_soap_note_assessment_extraction(self):
        """Test SOAP assessment section extraction"""
        note = self.generator.generate_soap_note(
            "PT_123", "DR_001", self.sample_segments, "SESSION_001"
        )

        assessment = note.content["assessment"]
        self.assertIn("angina", assessment.lower())

    def test_soap_note_plan_extraction(self):
        """Test SOAP plan section extraction"""
        note = self.generator.generate_soap_note(
            "PT_123", "DR_001", self.sample_segments, "SESSION_001"
        )

        plan = note.content["plan"]
        self.assertIn("troponin", plan.lower())

    def test_history_physical_generation(self):
        """Test H&P note generation"""
        note = self.generator.generate_history_physical(
            "PT_123", "DR_001", self.sample_segments, "SESSION_001"
        )

        self.assertEqual(note.note_type, NoteType.HISTORY_PHYSICAL)
        self.assertIn("chief_complaint", note.content)
        self.assertIn("history_present_illness", note.content)
        self.assertIn("assessment", note.content)
        self.assertIn("plan", note.content)

    def test_discharge_summary_generation(self):
        """Test discharge summary generation"""
        admission = datetime.now() - timedelta(days=3)
        discharge = datetime.now()

        note = self.generator.generate_discharge_summary(
            "PT_123", "DR_001", admission, discharge,
            self.sample_segments, "SESSION_001"
        )

        self.assertEqual(note.note_type, NoteType.DISCHARGE)
        self.assertIn("admission_date", note.content)
        self.assertIn("discharge_date", note.content)
        self.assertIn("discharge_diagnosis", note.content)
        self.assertIn("discharge_medications", note.content)

    def test_medication_extraction(self):
        """Test medication extraction from segments"""
        medications = self.generator._extract_medications(self.sample_segments)

        self.assertIsInstance(medications, list)
        self.assertIn("aspirin", medications)

    def test_note_retrieval(self):
        """Test retrieving generated note by ID"""
        note = self.generator.generate_soap_note(
            "PT_123", "DR_001", self.sample_segments, "SESSION_001"
        )

        retrieved = self.generator.get_note(note.note_id)

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["note_id"], note.note_id)

    def test_note_not_found(self):
        """Test retrieving nonexistent note"""
        result = self.generator.get_note("FAKE_NOTE_ID")

        self.assertIsNone(result)


# ============================================================================
# TEST VOICE DATA SECURITY
# ============================================================================

class TestVoiceDataSecurity(unittest.TestCase):
    """Test HIPAA-compliant voice data handling"""

    def setUp(self):
        """Set up test fixtures"""
        self.security = VoiceDataSecurity(retention_days=2555)

    def test_initialization(self):
        """Test security system initializes correctly"""
        self.assertIsNotNone(self.security)
        self.assertEqual(self.security.retention_days, 2555)
        self.assertEqual(len(self.security.audit_logs), 0)

    def test_audio_encryption(self):
        """Test audio data encryption"""
        audio_data = b"sample audio data"
        result = self.security.encrypt_audio_data(audio_data, "PT_123", "DR_001")

        self.assertTrue(result["encrypted"])
        self.assertEqual(result["encryption_method"], "AES-256")
        self.assertIsNotNone(result["data_hash"])
        self.assertIsNotNone(result["audit_log_id"])

    def test_audit_log_creation(self):
        """Test audit log creation"""
        initial_count = len(self.security.audit_logs)

        self.security.log_voice_access("DR_001", "PT_123", "transcribe", "hash123")

        self.assertEqual(len(self.security.audit_logs), initial_count + 1)

    def test_audit_log_content(self):
        """Test audit log contains required information"""
        log = self.security.log_voice_access("DR_001", "PT_123", "transcribe", "hash123")

        self.assertEqual(log.user_id, "DR_001")
        self.assertEqual(log.patient_id, "PT_123")
        self.assertEqual(log.action, "transcribe")
        self.assertEqual(log.data_hash, "hash123")
        self.assertEqual(log.encryption_status, "encrypted")

    def test_audit_trail_retrieval_all(self):
        """Test retrieving all audit logs"""
        self.security.log_voice_access("DR_001", "PT_123", "transcribe", "hash1")
        self.security.log_voice_access("DR_002", "PT_456", "generate_note", "hash2")

        trail = self.security.get_audit_trail()

        self.assertGreaterEqual(len(trail), 2)

    def test_audit_trail_retrieval_by_patient(self):
        """Test retrieving audit logs for specific patient"""
        self.security.log_voice_access("DR_001", "PT_123", "transcribe", "hash1")
        self.security.log_voice_access("DR_002", "PT_456", "generate_note", "hash2")

        trail = self.security.get_audit_trail(patient_id="PT_123")

        self.assertGreater(len(trail), 0)
        for log in trail:
            self.assertEqual(log["patient_id"], "PT_123")

    def test_deidentification_names(self):
        """Test de-identification removes names"""
        transcript = "John Smith came to see Dr. Jane Doe today."
        deidentified = self.security.de_identify_transcript(transcript)

        self.assertNotIn("John Smith", deidentified)
        self.assertNotIn("Jane Doe", deidentified)
        self.assertIn("[NAME]", deidentified)

    def test_deidentification_dates(self):
        """Test de-identification removes dates"""
        transcript = "Patient seen on 10/31/2025"
        deidentified = self.security.de_identify_transcript(transcript)

        self.assertNotIn("10/31/2025", deidentified)
        self.assertIn("[DATE]", deidentified)

    def test_deidentification_phone(self):
        """Test de-identification removes phone numbers"""
        transcript = "Contact at 555-123-4567"
        deidentified = self.security.de_identify_transcript(transcript)

        self.assertNotIn("555-123-4567", deidentified)
        self.assertIn("[PHONE]", deidentified)

    def test_deidentification_address(self):
        """Test de-identification removes addresses"""
        transcript = "Patient lives at 123 Main Street"
        deidentified = self.security.de_identify_transcript(transcript)

        self.assertIn("[ADDRESS]", deidentified)

    def test_retention_expiry_calculation(self):
        """Test retention expiry is calculated correctly"""
        log = self.security.log_voice_access("DR_001", "PT_123", "test", "hash")

        days_until_expiry = (log.retention_expires - datetime.now()).days
        self.assertGreaterEqual(days_until_expiry, 2554)
        self.assertLessEqual(days_until_expiry, 2556)


# ============================================================================
# TEST INTEGRATED VOICE AI SYSTEM
# ============================================================================

class TestVoiceAISystem(unittest.TestCase):
    """Test integrated Voice AI system"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = VoiceAISystem()

    def test_initialization(self):
        """Test system initializes all components"""
        self.assertIsNotNone(self.system.voice_processor)
        self.assertIsNotNone(self.system.ambient_intelligence)
        self.assertIsNotNone(self.system.note_generator)
        self.assertIsNotNone(self.system.security)

    def test_process_voice_command_integration(self):
        """Test voice command processing through integrated system"""
        result = self.system.process_voice_command("Order chest x-ray", "DR_001")

        self.assertIn("command", result)
        self.assertIn("execution_result", result)
        self.assertTrue(result["execution_result"]["success"])

    def test_clinical_encounter_full_workflow(self):
        """Test complete clinical encounter workflow"""
        conversation = [
            ("I have chest pain", SpeakerRole.PATIENT, 2.0),
            ("When did it start?", SpeakerRole.PHYSICIAN, 1.0),
            ("This morning", SpeakerRole.PATIENT, 1.0),
            ("Blood pressure 140 over 90", SpeakerRole.PHYSICIAN, 2.0),
            ("Assess as angina", SpeakerRole.PHYSICIAN, 2.0),
            ("Plan to order EKG", SpeakerRole.PHYSICIAN, 2.0)
        ]

        result = self.system.conduct_clinical_encounter(
            "SESSION_TEST", "PT_123", "DR_001", conversation
        )

        self.assertIn("session", result)
        self.assertIn("soap_note", result)
        self.assertEqual(result["session"]["status"], "completed")
        self.assertEqual(result["soap_note"]["note_type"], "soap")

    def test_system_stats_tracking(self):
        """Test system statistics tracking"""
        initial_stats = self.system.get_system_stats()

        self.system.process_voice_command("Order CBC", "DR_001")

        updated_stats = self.system.get_system_stats()

        self.assertGreater(
            updated_stats["commands_processed"],
            initial_stats["commands_processed"]
        )

    def test_convenience_function_assess_voice_command(self):
        """Test convenience function for voice command assessment"""
        from voice_ai_system import assess_voice_command

        result = assess_voice_command("Prescribe aspirin 81mg daily")

        self.assertIn("command", result)
        self.assertEqual(result["command"]["command_type"], "medication")

    def test_convenience_function_generate_note(self):
        """Test convenience function for note generation"""
        from voice_ai_system import generate_clinical_note_from_conversation

        conversation = [
            ("I have a headache", "patient"),
            ("How long?", "physician"),
            ("Two days", "patient")
        ]

        result = generate_clinical_note_from_conversation("PT_123", "DR_001", conversation)

        self.assertIn("soap_note", result)
        self.assertEqual(result["soap_note"]["patient_id"], "PT_123")


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance(unittest.TestCase):
    """Test system performance"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = VoiceAISystem()

    def test_command_processing_speed(self):
        """Test command processing is fast"""
        import time

        start = time.time()
        for _ in range(100):
            self.system.process_voice_command("Order chest x-ray", "DR_001")
        duration = time.time() - start

        avg_per_command = duration / 100
        self.assertLess(avg_per_command, 0.1)  # Less than 100ms per command

    def test_note_generation_speed(self):
        """Test note generation is fast"""
        import time

        segments = [
            TranscriptionSegment(
                segment_id=f"SEG_{i}",
                timestamp=datetime.now(),
                speaker=SpeakerRole.PATIENT if i % 2 == 0 else SpeakerRole.PHYSICIAN,
                text="Test segment",
                confidence=0.95,
                duration_seconds=1.0,
                medical_entities=[]
            )
            for i in range(10)
        ]

        start = time.time()
        self.system.note_generator.generate_soap_note("PT_123", "DR_001", segments, "SESSION_TEST")
        duration = time.time() - start

        self.assertLess(duration, 0.5)  # Less than 500ms


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    # Run with verbose output
    unittest.main(verbosity=2)
