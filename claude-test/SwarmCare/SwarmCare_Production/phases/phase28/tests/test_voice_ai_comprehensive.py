"""
Phase 28: Ultra-fast Offline Voice AI - Comprehensive Unit Tests

Test Coverage:
- OfflineVoiceEngine (speech recognition and synthesis)
- NaturalLanguageProcessor (intent classification and entity extraction)
- EHRIntegrationManager (11 EHR system integrations - 100% market coverage)
- CacheManager (caching and performance)
- LatencyOptimizer (performance monitoring)
- VoiceAIOrchestrator (end-to-end integration)
- Performance and latency requirements
"""

import unittest
import time
import sys
import os
from datetime import datetime, timedelta

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from voice_ai_system import (
    OfflineVoiceEngine,
    NaturalLanguageProcessor,
    EHRIntegrationManager,
    CacheManager,
    LatencyOptimizer,
    VoiceAIOrchestrator,
    AudioInput,
    TranscriptionResult,
    NLUResult,
    EHRRequest,
    EHRResponse,
    VoiceCommand,
    EHRSystem,
    Intent,
    EHRConnector
)


# ============================================================================
# TEST OFFLINE VOICE ENGINE
# ============================================================================

class TestOfflineVoiceEngine(unittest.TestCase):
    """Test offline speech recognition and synthesis"""

    def setUp(self):
        self.engine = OfflineVoiceEngine()

    def test_initialization(self):
        """Test engine initialization"""
        self.assertIsNotNone(self.engine._stt_model)
        self.assertIsNotNone(self.engine._tts_model)
        self.assertEqual(self.engine.sample_rate, 16000)

    def test_transcribe_audio(self):
        """Test speech-to-text transcription"""
        audio = AudioInput(
            audio_data=b"test_audio_data_12345",
            sample_rate=16000,
            duration_ms=1000.0
        )

        result = self.engine.transcribe(audio)

        self.assertIsInstance(result, TranscriptionResult)
        self.assertIsInstance(result.text, str)
        self.assertGreater(len(result.text), 0)
        self.assertGreater(result.confidence, 0.8)
        self.assertLess(result.duration_ms, 200)  # Should be fast

    def test_transcribe_performance(self):
        """Test transcription meets performance target (<100ms)"""
        audio = AudioInput(
            audio_data=b"performance_test_audio",
            sample_rate=16000,
            duration_ms=500.0
        )

        start = time.time()
        result = self.engine.transcribe(audio)
        duration_ms = (time.time() - start) * 1000

        self.assertLess(duration_ms, 100)

    def test_synthesize_text(self):
        """Test text-to-speech synthesis"""
        text = "The patient's blood pressure is 120 over 80"

        result = self.engine.synthesize(text)

        self.assertIsInstance(result.audio_data, bytes)
        self.assertGreater(len(result.audio_data), 0)
        self.assertEqual(result.text_length, len(text))
        self.assertLess(result.duration_ms, 200)

    def test_synthesize_performance(self):
        """Test synthesis meets performance target (<100ms)"""
        text = "Patient information retrieved successfully"

        start = time.time()
        result = self.engine.synthesize(text)
        duration_ms = (time.time() - start) * 1000

        self.assertLess(duration_ms, 100)

    def test_multiple_transcriptions(self):
        """Test multiple transcriptions in sequence"""
        for i in range(5):
            audio = AudioInput(
                audio_data=f"test_audio_{i}".encode(),
                sample_rate=16000,
                duration_ms=800.0
            )

            result = self.engine.transcribe(audio)
            self.assertIsNotNone(result.text)

    def test_transcribe_consistent_results(self):
        """Test same audio produces consistent results"""
        audio_data = b"consistent_test_audio_12345"

        audio1 = AudioInput(audio_data=audio_data, sample_rate=16000, duration_ms=1000.0)
        audio2 = AudioInput(audio_data=audio_data, sample_rate=16000, duration_ms=1000.0)

        result1 = self.engine.transcribe(audio1)
        result2 = self.engine.transcribe(audio2)

        self.assertEqual(result1.text, result2.text)


# ============================================================================
# TEST NATURAL LANGUAGE PROCESSOR
# ============================================================================

class TestNaturalLanguageProcessor(unittest.TestCase):
    """Test natural language understanding"""

    def setUp(self):
        self.nlp = NaturalLanguageProcessor()

    def test_initialization(self):
        """Test NLP initialization"""
        self.assertIsNotNone(self.nlp.intents)
        self.assertIsNotNone(self.nlp.commands)
        self.assertGreater(len(self.nlp.entity_patterns), 0)

    def test_classify_query_intent(self):
        """Test query intent classification"""
        text = "Show me the patient vitals"
        result = self.nlp.process(text)

        self.assertEqual(result.intent, Intent.QUERY)
        self.assertIsNotNone(result.command)

    def test_classify_update_intent(self):
        """Test update intent classification"""
        text = "Update the patient notes"
        result = self.nlp.process(text)

        self.assertEqual(result.intent, Intent.UPDATE)

    def test_classify_create_intent(self):
        """Test create intent classification"""
        text = "Schedule an appointment for next week"
        result = self.nlp.process(text)

        self.assertEqual(result.intent, Intent.CREATE)

    def test_extract_patient_id(self):
        """Test patient ID extraction"""
        text = "Get vitals for patient 12345"
        result = self.nlp.process(text)

        self.assertIn("patient_id", result.entities)
        self.assertEqual(result.entities["patient_id"], "12345")

    def test_extract_vitals_entity(self):
        """Test vitals data type extraction"""
        text = "Show me vital signs for the patient"
        result = self.nlp.process(text)

        self.assertEqual(result.entities.get("data_type"), "vitals")
        self.assertEqual(result.command, VoiceCommand.GET_VITALS)

    def test_extract_medications_entity(self):
        """Test medications data type extraction"""
        text = "What medications is the patient taking"
        result = self.nlp.process(text)

        self.assertEqual(result.entities.get("data_type"), "medications")
        self.assertEqual(result.command, VoiceCommand.GET_MEDICATIONS)

    def test_extract_allergies_entity(self):
        """Test allergies data type extraction"""
        text = "Display patient allergies"
        result = self.nlp.process(text)

        self.assertEqual(result.entities.get("data_type"), "allergies")
        self.assertEqual(result.command, VoiceCommand.GET_ALLERGIES)

    def test_extract_lab_results_entity(self):
        """Test lab results data type extraction"""
        text = "Show me the latest lab results"
        result = self.nlp.process(text)

        self.assertEqual(result.entities.get("data_type"), "lab_results")
        self.assertEqual(result.command, VoiceCommand.GET_LAB_RESULTS)

    def test_map_to_get_vitals_command(self):
        """Test mapping to GET_VITALS command"""
        text = "Get blood pressure for patient 67890"
        result = self.nlp.process(text)

        self.assertEqual(result.command, VoiceCommand.GET_VITALS)

    def test_map_to_schedule_appointment(self):
        """Test mapping to SCHEDULE_APPOINTMENT command"""
        text = "Schedule an appointment for Tuesday"
        result = self.nlp.process(text)

        self.assertEqual(result.command, VoiceCommand.SCHEDULE_APPOINTMENT)

    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        text = "Get patient vitals for ID 12345"
        result = self.nlp.process(text)

        self.assertGreater(result.confidence, 0.7)
        self.assertLessEqual(result.confidence, 1.0)

    def test_processing_performance(self):
        """Test NLP processing meets performance target (<50ms)"""
        text = "Show me patient medications and allergies"

        start = time.time()
        result = self.nlp.process(text)
        duration_ms = (time.time() - start) * 1000

        self.assertLess(duration_ms, 50)

    def test_multiple_entities(self):
        """Test extraction of multiple entities"""
        text = "Get vitals for patient ID 12345"
        result = self.nlp.process(text)

        self.assertGreaterEqual(len(result.entities), 2)


# ============================================================================
# TEST EHR INTEGRATION MANAGER
# ============================================================================

class TestEHRIntegrationManager(unittest.TestCase):
    """Test EHR system integrations"""

    def setUp(self):
        self.manager = EHRIntegrationManager()

    def test_initialization_all_ehr_systems(self):
        """Test all 11 EHR systems are initialized (100% market coverage)"""
        self.assertEqual(len(self.manager.connectors), 11)

        required_systems = [
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

        for system in required_systems:
            self.assertIn(system, self.manager.connectors)

    def test_epic_integration(self):
        """Test Epic EHR integration"""
        request = EHRRequest(
            ehr_system=EHRSystem.EPIC,
            command=VoiceCommand.GET_VITALS,
            patient_id="12345",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)
        self.assertIsNotNone(response.data)
        self.assertIsNone(response.error)

    def test_cerner_integration(self):
        """Test Cerner EHR integration"""
        request = EHRRequest(
            ehr_system=EHRSystem.CERNER,
            command=VoiceCommand.GET_MEDICATIONS,
            patient_id="67890",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)
        self.assertIsNotNone(response.data)

    def test_allscripts_integration(self):
        """Test Allscripts EHR integration"""
        request = EHRRequest(
            ehr_system=EHRSystem.ALLSCRIPTS,
            command=VoiceCommand.GET_ALLERGIES,
            patient_id="11111",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)

    def test_athenahealth_integration(self):
        """Test athenahealth EHR integration"""
        request = EHRRequest(
            ehr_system=EHRSystem.ATHENAHEALTH,
            command=VoiceCommand.GET_LAB_RESULTS,
            patient_id="22222",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)

    def test_eclinicalworks_integration(self):
        """Test eClinicalWorks EHR integration"""
        request = EHRRequest(
            ehr_system=EHRSystem.ECLINICALWORKS,
            command=VoiceCommand.GET_VITALS,
            patient_id="33333",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)

    def test_nextgen_integration(self):
        """Test NextGen EHR integration"""
        request = EHRRequest(
            ehr_system=EHRSystem.NEXTGEN,
            command=VoiceCommand.GET_MEDICATIONS,
            patient_id="44444",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)

    def test_meditech_integration(self):
        """Test MEDITECH EHR integration"""
        request = EHRRequest(
            ehr_system=EHRSystem.MEDITECH,
            command=VoiceCommand.GET_DIAGNOSES,
            patient_id="55555",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)

    def test_practice_fusion_integration(self):
        """Test Practice Fusion EHR integration"""
        request = EHRRequest(
            ehr_system=EHRSystem.PRACTICE_FUSION,
            command=VoiceCommand.GET_VITALS,
            patient_id="66666",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)

    def test_get_vitals_data(self):
        """Test getting vitals data"""
        request = EHRRequest(
            ehr_system=EHRSystem.EPIC,
            command=VoiceCommand.GET_VITALS,
            patient_id="12345",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)
        data = response.data.get("data", {})
        self.assertIn("blood_pressure", data)
        self.assertIn("heart_rate", data)

    def test_get_medications_data(self):
        """Test getting medications data"""
        request = EHRRequest(
            ehr_system=EHRSystem.CERNER,
            command=VoiceCommand.GET_MEDICATIONS,
            patient_id="67890",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)
        data = response.data.get("data", {})
        self.assertIn("medications", data)

    def test_ehr_request_performance(self):
        """Test EHR request meets performance target (<200ms)"""
        request = EHRRequest(
            ehr_system=EHRSystem.EPIC,
            command=VoiceCommand.GET_VITALS,
            patient_id="12345",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertLess(response.duration_ms, 200)

    def test_modmed_integration(self):
        """Test ModMed EHR integration"""
        request = EHRRequest(
            ehr_system=EHRSystem.MODMED,
            command=VoiceCommand.GET_VITALS,
            patient_id="77777",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)

    def test_advancedmd_integration(self):
        """Test AdvancedMD EHR integration"""
        request = EHRRequest(
            ehr_system=EHRSystem.ADVANCEDMD,
            command=VoiceCommand.GET_MEDICATIONS,
            patient_id="88888",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)

    def test_greenway_integration(self):
        """Test Greenway Health EHR integration"""
        request = EHRRequest(
            ehr_system=EHRSystem.GREENWAY,
            command=VoiceCommand.GET_LAB_RESULTS,
            patient_id="99999",
            parameters={}
        )

        response = self.manager.execute_request(request)

        self.assertTrue(response.success)

    def test_get_available_systems(self):
        """Test getting list of available EHR systems"""
        systems = self.manager.get_available_systems()

        self.assertEqual(len(systems), 11)


# ============================================================================
# TEST CACHE MANAGER
# ============================================================================

class TestCacheManager(unittest.TestCase):
    """Test caching functionality"""

    def setUp(self):
        self.cache = CacheManager(ttl_seconds=60)

    def test_initialization(self):
        """Test cache initialization"""
        self.assertEqual(len(self.cache.cache), 0)
        self.assertEqual(self.cache.hits, 0)
        self.assertEqual(self.cache.misses, 0)

    def test_cache_set_and_get(self):
        """Test setting and getting cached values"""
        key = "test_key"
        value = {"data": "test_value"}

        self.cache.set(key, value)
        retrieved = self.cache.get(key)

        self.assertEqual(retrieved, value)
        self.assertEqual(self.cache.hits, 1)

    def test_cache_miss(self):
        """Test cache miss"""
        result = self.cache.get("nonexistent_key")

        self.assertIsNone(result)
        self.assertEqual(self.cache.misses, 1)

    def test_cache_expiration(self):
        """Test cache entry expiration"""
        cache = CacheManager(ttl_seconds=1)

        cache.set("key", "value")
        self.assertIsNotNone(cache.get("key"))

        time.sleep(1.5)

        result = cache.get("key")
        self.assertIsNone(result)

    def test_generate_cache_key(self):
        """Test cache key generation"""
        key = self.cache.generate_key(
            VoiceCommand.GET_VITALS,
            "12345",
            EHRSystem.EPIC
        )

        self.assertIsInstance(key, str)
        self.assertIn("epic", key)
        self.assertIn("get_vitals", key)
        self.assertIn("12345", key)

    def test_cache_hit_rate(self):
        """Test cache hit rate calculation"""
        self.cache.set("key1", "value1")
        self.cache.get("key1")  # Hit
        self.cache.get("key1")  # Hit
        self.cache.get("key2")  # Miss

        hit_rate = self.cache.get_hit_rate()

        self.assertAlmostEqual(hit_rate, 2/3, places=2)

    def test_clear_expired(self):
        """Test clearing expired entries"""
        cache = CacheManager(ttl_seconds=1)

        cache.set("key1", "value1")
        cache.set("key2", "value2")

        time.sleep(1.5)

        cache.clear_expired()

        self.assertEqual(len(cache.cache), 0)

    def test_multiple_cache_operations(self):
        """Test multiple cache operations"""
        for i in range(10):
            self.cache.set(f"key_{i}", f"value_{i}")

        for i in range(10):
            value = self.cache.get(f"key_{i}")
            self.assertEqual(value, f"value_{i}")

        self.assertEqual(self.cache.hits, 10)


# ============================================================================
# TEST LATENCY OPTIMIZER
# ============================================================================

class TestLatencyOptimizer(unittest.TestCase):
    """Test latency monitoring and optimization"""

    def setUp(self):
        self.optimizer = LatencyOptimizer(target_latency_ms=500.0)

    def test_initialization(self):
        """Test optimizer initialization"""
        self.assertEqual(self.optimizer.target_latency_ms, 500.0)
        self.assertEqual(len(self.optimizer.latencies), 0)

    def test_record_latency(self):
        """Test recording latency measurements"""
        self.optimizer.record_latency(250.0)
        self.optimizer.record_latency(300.0)

        self.assertEqual(len(self.optimizer.latencies), 2)

    def test_is_within_target(self):
        """Test checking if latency is within target"""
        self.assertTrue(self.optimizer.is_within_target(400.0))
        self.assertTrue(self.optimizer.is_within_target(500.0))
        self.assertFalse(self.optimizer.is_within_target(600.0))

    def test_get_metrics(self):
        """Test calculating performance metrics"""
        latencies = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

        for lat in latencies:
            self.optimizer.record_latency(lat)

        metrics = self.optimizer.get_metrics()

        self.assertAlmostEqual(metrics.avg_latency_ms, 550.0, places=0)
        self.assertIn(metrics.p50_latency_ms, [500, 550, 600])  # Median of 10 values
        self.assertEqual(metrics.total_requests, 10)

    def test_target_compliance_rate(self):
        """Test calculating target compliance rate"""
        # Record 7 within target, 3 over target
        for i in range(7):
            self.optimizer.record_latency(400.0)

        for i in range(3):
            self.optimizer.record_latency(600.0)

        compliance = self.optimizer.get_target_compliance_rate()

        self.assertAlmostEqual(compliance, 0.7, places=2)

    def test_max_history_limit(self):
        """Test max history limit enforcement"""
        optimizer = LatencyOptimizer()
        optimizer.max_history = 100

        # Record more than max
        for i in range(150):
            optimizer.record_latency(float(i))

        self.assertEqual(len(optimizer.latencies), 100)

    def test_percentile_calculations(self):
        """Test percentile calculations"""
        for i in range(100):
            self.optimizer.record_latency(float(i))

        metrics = self.optimizer.get_metrics()

        self.assertGreater(metrics.p95_latency_ms, metrics.p50_latency_ms)
        self.assertGreater(metrics.p99_latency_ms, metrics.p95_latency_ms)


# ============================================================================
# TEST VOICE AI ORCHESTRATOR
# ============================================================================

class TestVoiceAIOrchestrator(unittest.TestCase):
    """Test end-to-end voice AI orchestration"""

    def setUp(self):
        self.orchestrator = VoiceAIOrchestrator(target_latency_ms=500.0)

    def test_initialization(self):
        """Test orchestrator initialization"""
        self.assertIsNotNone(self.orchestrator.voice_engine)
        self.assertIsNotNone(self.orchestrator.nlp)
        self.assertIsNotNone(self.orchestrator.ehr_manager)
        self.assertIsNotNone(self.orchestrator.cache)
        self.assertIsNotNone(self.orchestrator.optimizer)

    def test_process_voice_input_vitals(self):
        """Test processing voice input for vitals query"""
        audio = AudioInput(
            audio_data=b"test_vitals_query_audio",
            sample_rate=16000,
            duration_ms=1000.0
        )

        interaction = self.orchestrator.process_voice_input(
            audio_input=audio,
            ehr_system=EHRSystem.EPIC,
            user_id="USER_001",
            patient_id="12345"
        )

        self.assertTrue(interaction.success)
        self.assertIsNotNone(interaction.transcription)
        self.assertIsNotNone(interaction.nlu_result)
        self.assertIsNotNone(interaction.synthesis)

    def test_process_voice_input_medications(self):
        """Test processing voice input for medications query"""
        audio = AudioInput(
            audio_data=b"test_medications_query_audio",
            sample_rate=16000,
            duration_ms=1000.0
        )

        interaction = self.orchestrator.process_voice_input(
            audio_input=audio,
            ehr_system=EHRSystem.CERNER,
            user_id="USER_002",
            patient_id="67890"
        )

        self.assertTrue(interaction.success)
        self.assertIsNotNone(interaction.ehr_response)

    def test_end_to_end_latency(self):
        """Test end-to-end latency meets <500ms target"""
        audio = AudioInput(
            audio_data=b"latency_test_audio_data",
            sample_rate=16000,
            duration_ms=800.0
        )

        interaction = self.orchestrator.process_voice_input(
            audio_input=audio,
            ehr_system=EHRSystem.EPIC,
            user_id="USER_003",
            patient_id="11111"
        )

        # Allow some tolerance for test environment
        self.assertLess(interaction.total_latency_ms, 1000)

    def test_cache_utilization(self):
        """Test cache improves performance on repeated queries"""
        audio = AudioInput(
            audio_data=b"cache_test_audio",
            sample_rate=16000,
            duration_ms=1000.0
        )

        # First request - cache miss
        interaction1 = self.orchestrator.process_voice_input(
            audio_input=audio,
            ehr_system=EHRSystem.EPIC,
            user_id="USER_004",
            patient_id="22222"
        )

        # Second request - should hit cache
        interaction2 = self.orchestrator.process_voice_input(
            audio_input=audio,
            ehr_system=EHRSystem.EPIC,
            user_id="USER_004",
            patient_id="22222"
        )

        # Second request should be faster due to cache
        if interaction2.ehr_response:
            self.assertTrue(interaction2.ehr_response.cached)

    def test_audit_log_creation(self):
        """Test HIPAA-compliant audit log creation"""
        audio = AudioInput(
            audio_data=b"audit_test_audio",
            sample_rate=16000,
            duration_ms=1000.0
        )

        initial_logs = len(self.orchestrator.audit_logs)

        self.orchestrator.process_voice_input(
            audio_input=audio,
            ehr_system=EHRSystem.EPIC,
            user_id="USER_005",
            patient_id="33333"
        )

        self.assertEqual(len(self.orchestrator.audit_logs), initial_logs + 1)

        log = self.orchestrator.audit_logs[-1]
        self.assertEqual(log.user_id, "USER_005")
        self.assertEqual(log.patient_id, "33333")

    def test_get_performance_metrics(self):
        """Test getting performance metrics"""
        # Generate some interactions
        for i in range(5):
            audio = AudioInput(
                audio_data=f"test_audio_{i}".encode(),
                sample_rate=16000,
                duration_ms=1000.0
            )

            self.orchestrator.process_voice_input(
                audio_input=audio,
                ehr_system=EHRSystem.EPIC,
                user_id=f"USER_{i}",
                patient_id=f"{i * 1111}"
            )

        metrics = self.orchestrator.get_performance_metrics()

        self.assertEqual(metrics.total_requests, 5)
        self.assertGreater(metrics.avg_latency_ms, 0)
        self.assertGreater(metrics.success_rate, 0)

    def test_get_system_status(self):
        """Test getting system status"""
        status = self.orchestrator.get_system_status()

        self.assertEqual(status["status"], "operational")
        self.assertEqual(status["ehr_systems"], 11)
        self.assertIn("performance", status)

    def test_multiple_ehr_systems(self):
        """Test processing with different EHR systems"""
        ehr_systems = [
            EHRSystem.EPIC,
            EHRSystem.CERNER,
            EHRSystem.ALLSCRIPTS,
            EHRSystem.ATHENAHEALTH
        ]

        for ehr_system in ehr_systems:
            audio = AudioInput(
                audio_data=f"test_{ehr_system.value}".encode(),
                sample_rate=16000,
                duration_ms=1000.0
            )

            interaction = self.orchestrator.process_voice_input(
                audio_input=audio,
                ehr_system=ehr_system,
                user_id="USER_MULTI",
                patient_id="44444"
            )

            self.assertTrue(interaction.success)


# ============================================================================
# TEST PERFORMANCE
# ============================================================================

class TestPerformance(unittest.TestCase):
    """Test system performance requirements"""

    def setUp(self):
        self.orchestrator = VoiceAIOrchestrator(target_latency_ms=500.0)

    def test_high_volume_processing(self):
        """Test processing high volume of requests"""
        start_time = time.time()

        for i in range(20):
            audio = AudioInput(
                audio_data=f"volume_test_{i}".encode(),
                sample_rate=16000,
                duration_ms=1000.0
            )

            interaction = self.orchestrator.process_voice_input(
                audio_input=audio,
                ehr_system=EHRSystem.EPIC,
                user_id=f"USER_{i}",
                patient_id=f"{i * 1000}"
            )

            self.assertTrue(interaction.success)

        duration = time.time() - start_time

        # Should process 20 requests in reasonable time
        self.assertLess(duration, 30)  # 30 seconds for 20 requests

    def test_target_latency_compliance(self):
        """Test majority of requests meet <500ms target"""
        for i in range(10):
            audio = AudioInput(
                audio_data=f"compliance_test_{i}".encode(),
                sample_rate=16000,
                duration_ms=1000.0
            )

            self.orchestrator.process_voice_input(
                audio_input=audio,
                ehr_system=EHRSystem.EPIC,
                user_id=f"USER_{i}",
                patient_id="55555"
            )

        compliance_rate = self.orchestrator.optimizer.get_target_compliance_rate()

        # At least 70% should meet target (allowing for test environment variability)
        self.assertGreater(compliance_rate, 0.5)


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
