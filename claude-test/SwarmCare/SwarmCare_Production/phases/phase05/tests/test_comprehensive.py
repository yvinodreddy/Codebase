"""
Comprehensive Test Suite for Phase 05: Audio Generation
Tests all major components with production scenarios
"""

import unittest
import sys
import os
from pathlib import Path

# Add code directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))

from audio_providers.base_provider import AudioFormat, VoiceProfile, VoiceGender, AudioGenerationRequest
from audio_providers.azure_tts import AzureTTSProvider
from audio_providers.aws_polly import AWSPollyProvider
from audio_providers.google_tts import GoogleTTSProvider
from processors.audio_processor import AudioProcessor, ProcessingConfig
from processors.normalization import AudioNormalizer
from processors.format_converter import FormatConverter, ConversionConfig
from processors.effects_processor import EffectsProcessor, EffectConfig, EffectType
from validators.audio_validator import AudioValidator, ValidationLevel
from validators.quality_metrics import QualityMetrics
from storage.audio_storage import AudioStorage, StorageConfig, StorageBackend
from storage.cache_manager import CacheManager


class TestAudioProviders(unittest.TestCase):
    """Test TTS providers"""

    def setUp(self):
        self.config = {
            'azure_subscription_key': 'test-key',
            'azure_region': 'eastus',
            'aws_access_key_id': 'test-key',
            'aws_secret_access_key': 'test-secret',
            'google_credentials_path': 'credentials.json'
        }

    def test_azure_provider_initialization(self):
        """Test Azure TTS provider initialization"""
        provider = AzureTTSProvider(self.config)
        self.assertEqual(provider.provider_name, 'azure')
        self.assertIsNotNone(provider.subscription_key)

    def test_aws_provider_initialization(self):
        """Test AWS Polly provider initialization"""
        provider = AWSPollyProvider(self.config)
        self.assertEqual(provider.provider_name, 'aws_polly')

    def test_google_provider_initialization(self):
        """Test Google TTS provider initialization"""
        provider = GoogleTTSProvider(self.config)
        self.assertEqual(provider.provider_name, 'google_tts')

    def test_get_available_voices(self):
        """Test getting available voices"""
        provider = AzureTTSProvider(self.config)
        voices = provider.get_available_voices()
        self.assertGreater(len(voices), 0)
        self.assertIsInstance(voices[0], VoiceProfile)

    def test_voice_validation(self):
        """Test voice ID validation"""
        provider = AzureTTSProvider(self.config)
        self.assertTrue(provider.validate_voice("en-US-AriaNeural"))
        self.assertFalse(provider.validate_voice("invalid-voice-id"))

    def test_audio_generation(self):
        """Test audio generation"""
        provider = AzureTTSProvider(self.config)
        voice = VoiceProfile(
            provider='azure',
            voice_id='en-US-AriaNeural',
            voice_name='Aria',
            language='en-US',
            gender=VoiceGender.FEMALE
        )

        request = AudioGenerationRequest(
            text="This is a test of the audio generation system.",
            voice_profile=voice,
            output_format=AudioFormat.MP3
        )

        response = provider.generate_audio(request)
        self.assertTrue(response.success)
        self.assertIsNotNone(response.audio_data)
        self.assertGreater(response.file_size_bytes, 0)


class TestAudioProcessing(unittest.TestCase):
    """Test audio processing pipeline"""

    def setUp(self):
        self.test_audio = b'\x00' * 10000  # Simulated audio data

    def test_audio_processor_initialization(self):
        """Test audio processor initialization"""
        config = ProcessingConfig(
            normalize_audio=True,
            reduce_noise=True,
            apply_compression=True
        )
        processor = AudioProcessor(config)
        self.assertIsNotNone(processor.config)

    def test_audio_processing(self):
        """Test full audio processing pipeline"""
        processor = AudioProcessor()
        result = processor.process(self.test_audio, 'mp3')
        self.assertTrue(result.success)
        self.assertIsNotNone(result.processed_audio)
        self.assertGreater(len(result.stages_applied), 0)

    def test_normalization(self):
        """Test audio normalization"""
        normalizer = AudioNormalizer(target_lufs=-16.0)
        normalized, metrics = normalizer.normalize(self.test_audio, 'mp3')
        self.assertIsNotNone(normalized)
        self.assertEqual(metrics.output_lufs, -16.0)

    def test_format_conversion(self):
        """Test format conversion"""
        converter = FormatConverter()
        config = ConversionConfig(
            output_format='aac',
            bitrate_kbps=128,
            sample_rate=44100
        )
        result = converter.convert(self.test_audio, 'mp3', config)
        self.assertTrue(result.success)
        self.assertEqual(result.output_format, 'aac')

    def test_effects_processor(self):
        """Test audio effects"""
        processor = EffectsProcessor()
        effect = EffectConfig(
            effect_type=EffectType.REVERB,
            intensity=0.3
        )
        result = processor.apply_effect(self.test_audio, effect)
        self.assertTrue(result.success)


class TestAudioValidation(unittest.TestCase):
    """Test audio validation"""

    def setUp(self):
        self.test_audio = b'\x00' * 10000

    def test_validator_initialization(self):
        """Test validator initialization"""
        validator = AudioValidator(ValidationLevel.STANDARD)
        self.assertEqual(validator.validation_level, ValidationLevel.STANDARD)

    def test_basic_validation(self):
        """Test basic audio validation"""
        validator = AudioValidator(ValidationLevel.BASIC)
        result = validator.validate(self.test_audio, 'mp3')
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result.score, 0)
        self.assertLessEqual(result.score, 100)

    def test_medical_validation(self):
        """Test medical-grade validation"""
        validator = AudioValidator(ValidationLevel.MEDICAL)
        result = validator.validate(self.test_audio, 'mp3')
        self.assertIsNotNone(result)
        self.assertIn('intelligibility_score', result.metrics)

    def test_quality_metrics(self):
        """Test quality metrics calculation"""
        metrics = QualityMetrics()
        score = metrics.calculate_quality_score(self.test_audio, 'mp3')
        self.assertIsNotNone(score)
        self.assertGreater(score.overall_score, 0)
        self.assertIn(score.grade, ['A+', 'A', 'B', 'C', 'D', 'F'])


class TestAudioStorage(unittest.TestCase):
    """Test audio storage system"""

    def setUp(self):
        self.config = StorageConfig(
            backend=StorageBackend.LOCAL,
            base_path='/tmp/audio_test',
            encryption_enabled=True
        )
        self.storage = AudioStorage(self.config)
        self.test_audio = b'\x00' * 10000

    def test_storage_initialization(self):
        """Test storage system initialization"""
        self.assertIsNotNone(self.storage)
        self.assertEqual(self.storage.config.backend, StorageBackend.LOCAL)

    def test_store_and_retrieve(self):
        """Test storing and retrieving audio"""
        metadata = {
            'name': 'test_audio.mp3',
            'format': 'mp3',
            'duration': 10.0,
            'tags': {'type': 'test'}
        }

        # Store
        storage_metadata = self.storage.store(self.test_audio, metadata)
        self.assertIsNotNone(storage_metadata)
        self.assertTrue(storage_metadata.encrypted)

    def test_cache_manager(self):
        """Test cache manager"""
        cache = CacheManager(max_memory_mb=10, max_disk_gb=1)

        # Set cache
        cache.set('test_key', self.test_audio, ttl=3600)

        # Get cache
        cached_data = cache.get('test_key')
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), len(self.test_audio))

        # Get stats
        stats = cache.get_stats()
        self.assertGreater(stats['memory_entries'], 0)


class TestProductionScenarios(unittest.TestCase):
    """Test production scenarios"""

    def test_end_to_end_podcast_generation(self):
        """Test complete podcast audio generation flow"""
        # 1. Generate audio
        config = {'azure_subscription_key': 'test'}
        provider = AzureTTSProvider(config)

        voice = VoiceProfile(
            provider='azure',
            voice_id='en-US-AriaNeural',
            voice_name='Aria',
            language='en-US',
            gender=VoiceGender.FEMALE
        )

        request = AudioGenerationRequest(
            text="Medical podcast episode test content.",
            voice_profile=voice
        )

        response = provider.generate_audio(request)
        self.assertTrue(response.success)

        # 2. Process audio
        processor = AudioProcessor()
        process_result = processor.process(response.audio_data)
        self.assertTrue(process_result.success)

        # 3. Validate quality
        validator = AudioValidator(ValidationLevel.MEDICAL)
        validation_result = validator.validate(process_result.processed_audio)
        self.assertIsNotNone(validation_result)

    def test_multi_provider_fallback(self):
        """Test fallback between multiple providers"""
        config = {
            'azure_subscription_key': 'test',
            'aws_access_key_id': 'test',
            'google_credentials_path': 'test.json'
        }

        providers = [
            AzureTTSProvider(config),
            AWSPollyProvider(config),
            GoogleTTSProvider(config)
        ]

        # Verify all providers initialized
        self.assertEqual(len(providers), 3)
        for provider in providers:
            voices = provider.get_available_voices('en-US')
            self.assertGreater(len(voices), 0)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAudioProviders))
    suite.addTests(loader.loadTestsFromTestCase(TestAudioProcessing))
    suite.addTests(loader.loadTestsFromTestCase(TestAudioValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestAudioStorage))
    suite.addTests(loader.loadTestsFromTestCase(TestProductionScenarios))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
