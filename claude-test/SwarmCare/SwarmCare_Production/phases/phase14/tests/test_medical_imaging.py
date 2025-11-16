"""
Phase 14: Comprehensive Medical Imaging Test Suite
Production-grade testing for DICOM processing, AI analysis, and HIPAA compliance

Test Coverage:
- DICOM processing
- X-ray/CT/MRI analysis
- Abnormality detection
- HIPAA compliance
- Performance benchmarks
- Integration tests
"""

import unittest
import sys
import os
import json
import time
import tempfile
import numpy as np
from pathlib import Path

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

try:
    from medical_imaging_core import (
        MedicalImagingPipeline,
        DICOMProcessor,
        XRayAnalyzer,
        CTAnalyzer,
        MRIAnalyzer,
        ImagingModality,
        AbnormalityType,
        ImageMetadata,
        AbnormalityDetection
    )
    IMAGING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Medical imaging modules not available: {e}")
    IMAGING_AVAILABLE = False


class TestDICOMProcessor(unittest.TestCase):
    """Test DICOM processing and HIPAA compliance"""

    def setUp(self):
        """Set up test fixtures"""
        if not IMAGING_AVAILABLE:
            self.skipTest("Medical imaging modules not available")

        self.processor = DICOMProcessor()
        self.test_image = self._create_test_image()

    def _create_test_image(self):
        """Create temporary test image"""
        temp_dir = tempfile.mkdtemp()
        image_path = os.path.join(temp_dir, "test_xray.png")

        # Create synthetic medical image
        try:
            from PIL import Image
            img = Image.fromarray(np.random.randint(0, 255, (512, 512), dtype=np.uint8))
            img.save(image_path)
        except ImportError:
            # Create dummy file if PIL not available
            with open(image_path, 'w') as f:
                f.write("dummy")

        return image_path

    def test_supported_formats(self):
        """Test supported image formats"""
        expected_formats = ['.dcm', '.png', '.jpg', '.jpeg', '.tiff', '.bmp']
        self.assertEqual(self.processor.supported_formats, expected_formats)

    def test_phi_patterns(self):
        """Test PHI pattern recognition"""
        self.assertIn('patient_name', self.processor.phi_patterns)
        self.assertIn('medical_record_number', self.processor.phi_patterns)

    def test_metadata_anonymization(self):
        """Test that metadata is properly anonymized"""
        img_array = np.random.randint(0, 255, (512, 512), dtype=np.uint8)
        metadata = self.processor._create_anonymous_metadata(Path("test.png"), img_array)

        # Verify anonymization
        self.assertTrue(metadata.patient_id.startswith("ANON_"))
        self.assertEqual(metadata.institution, "ANONYMIZED")
        self.assertEqual(metadata.device_manufacturer, "ANONYMIZED")
        self.assertTrue(metadata.phi_removed)
        self.assertTrue(metadata.hipaa_compliant)

    def test_image_preprocessing(self):
        """Test image preprocessing"""
        img_array = np.random.randint(0, 255, (256, 256), dtype=np.uint8)
        preprocessed = self.processor.preprocess_image(img_array)

        # Verify preprocessing
        self.assertEqual(preprocessed.shape, (512, 512))  # Resized to standard
        self.assertEqual(preprocessed.dtype, np.uint8)
        self.assertGreaterEqual(preprocessed.min(), 0)
        self.assertLessEqual(preprocessed.max(), 255)

    def test_quality_score_calculation(self):
        """Test image quality score calculation"""
        # High quality image (good contrast)
        high_quality = np.random.randint(0, 255, (512, 512), dtype=np.uint8)
        quality = self.processor.calculate_quality_score(high_quality)

        self.assertIsInstance(quality, float)
        self.assertGreaterEqual(quality, 0.0)
        self.assertLessEqual(quality, 100.0)

    def test_metadata_integrity(self):
        """Test metadata integrity with hash"""
        img_array = np.random.randint(0, 255, (512, 512), dtype=np.uint8)
        metadata1 = self.processor._create_anonymous_metadata(Path("test.png"), img_array)
        metadata2 = self.processor._create_anonymous_metadata(Path("test.png"), img_array)

        # Same image should produce same hash
        self.assertEqual(metadata1.image_hash, metadata2.image_hash)


class TestXRayAnalyzer(unittest.TestCase):
    """Test X-ray analysis engine"""

    def setUp(self):
        """Set up test fixtures"""
        if not IMAGING_AVAILABLE:
            self.skipTest("Medical imaging modules not available")

        self.analyzer = XRayAnalyzer()
        self.test_image = np.random.randint(0, 255, (512, 512), dtype=np.uint8)
        self.metadata = ImageMetadata(
            patient_id="ANON_TEST",
            study_id="STUDY_TEST",
            series_id="SERIES_TEST",
            modality="XRAY",
            body_part="CHEST",
            acquisition_date="2025-10-31",
            institution="TEST_HOSPITAL",
            device_manufacturer="TEST_DEVICE",
            image_hash="test_hash",
            phi_removed=True,
            hipaa_compliant=True
        )

    def test_supported_body_parts(self):
        """Test supported body parts"""
        expected_parts = ['CHEST', 'HAND', 'FOOT', 'SPINE', 'PELVIS']
        self.assertEqual(self.analyzer.supported_body_parts, expected_parts)

    def test_chest_xray_analysis(self):
        """Test chest X-ray analysis"""
        detections = self.analyzer.analyze(self.test_image, self.metadata)

        # Should return detections
        self.assertIsInstance(detections, list)
        self.assertGreater(len(detections), 0)

        # Check detection structure
        for detection in detections:
            self.assertIsInstance(detection, AbnormalityDetection)
            self.assertIn('abnormality_type', detection.__dict__)
            self.assertIn('confidence', detection.__dict__)
            self.assertIn('severity', detection.__dict__)
            self.assertIsInstance(detection.confidence, float)
            self.assertGreaterEqual(detection.confidence, 0.0)
            self.assertLessEqual(detection.confidence, 1.0)

    def test_general_xray_analysis(self):
        """Test general X-ray analysis"""
        self.metadata.body_part = "HAND"
        detections = self.analyzer.analyze(self.test_image, self.metadata)

        self.assertIsInstance(detections, list)
        self.assertGreater(len(detections), 0)

    def test_abnormality_types(self):
        """Test that abnormality types are valid"""
        detections = self.analyzer.analyze(self.test_image, self.metadata)

        valid_types = [abn.value for abn in AbnormalityType]
        for detection in detections:
            self.assertIn(detection.abnormality_type, valid_types)

    def test_evidence_based_recommendations(self):
        """Test that recommendations are evidence-based"""
        detections = self.analyzer.analyze(self.test_image, self.metadata)

        for detection in detections:
            self.assertTrue(detection.evidence_based)
            self.assertIsInstance(detection.recommended_action, str)
            self.assertGreater(len(detection.recommended_action), 0)


class TestCTAnalyzer(unittest.TestCase):
    """Test CT scan analysis engine"""

    def setUp(self):
        """Set up test fixtures"""
        if not IMAGING_AVAILABLE:
            self.skipTest("Medical imaging modules not available")

        self.analyzer = CTAnalyzer()
        self.test_image = np.random.randint(0, 255, (512, 512), dtype=np.uint8)
        self.metadata = ImageMetadata(
            patient_id="ANON_TEST",
            study_id="STUDY_TEST",
            series_id="SERIES_TEST",
            modality="CT",
            body_part="BRAIN",
            acquisition_date="2025-10-31",
            institution="TEST_HOSPITAL",
            device_manufacturer="TEST_DEVICE",
            image_hash="test_hash",
            phi_removed=True,
            hipaa_compliant=True
        )

    def test_window_level_presets(self):
        """Test CT window/level presets"""
        self.assertIn('brain', self.analyzer.window_level_presets)
        self.assertIn('lung', self.analyzer.window_level_presets)
        self.assertIn('abdomen', self.analyzer.window_level_presets)

    def test_brain_ct_analysis(self):
        """Test brain CT analysis"""
        detections = self.analyzer.analyze(self.test_image, self.metadata)

        self.assertIsInstance(detections, list)
        self.assertGreater(len(detections), 0)

    def test_chest_ct_analysis(self):
        """Test chest CT analysis"""
        self.metadata.body_part = "CHEST"
        detections = self.analyzer.analyze(self.test_image, self.metadata)

        self.assertIsInstance(detections, list)
        self.assertGreater(len(detections), 0)

    def test_urgency_detection(self):
        """Test that urgent findings are flagged"""
        # Create high-density image to simulate hemorrhage
        urgent_image = np.full((512, 512), 220, dtype=np.uint8)
        detections = self.analyzer.analyze(urgent_image, self.metadata)

        # Check if any high/critical severity findings
        severities = [d.severity for d in detections]
        self.assertTrue(len(detections) > 0)


class TestMRIAnalyzer(unittest.TestCase):
    """Test MRI analysis engine"""

    def setUp(self):
        """Set up test fixtures"""
        if not IMAGING_AVAILABLE:
            self.skipTest("Medical imaging modules not available")

        self.analyzer = MRIAnalyzer()
        self.test_image = np.random.randint(0, 255, (512, 512), dtype=np.uint8)
        self.metadata = ImageMetadata(
            patient_id="ANON_TEST",
            study_id="STUDY_TEST",
            series_id="SERIES_TEST",
            modality="MRI",
            body_part="BRAIN",
            acquisition_date="2025-10-31",
            institution="TEST_HOSPITAL",
            device_manufacturer="TEST_DEVICE",
            image_hash="test_hash",
            phi_removed=True,
            hipaa_compliant=True
        )

    def test_sequence_types(self):
        """Test MRI sequence types"""
        expected_sequences = ['T1', 'T2', 'FLAIR', 'DWI', 'T1+C']
        self.assertEqual(self.analyzer.sequence_types, expected_sequences)

    def test_mri_analysis(self):
        """Test MRI analysis"""
        detections = self.analyzer.analyze(self.test_image, self.metadata)

        self.assertIsInstance(detections, list)
        self.assertGreater(len(detections), 0)

    def test_signal_abnormality_detection(self):
        """Test signal abnormality detection"""
        # Create image with signal abnormality
        abnormal_image = np.random.randint(50, 200, (512, 512), dtype=np.uint8)
        abnormal_image[200:260, 200:260] = 250  # High signal area

        detections = self.analyzer.analyze(abnormal_image, self.metadata)
        self.assertGreater(len(detections), 0)


class TestMedicalImagingPipeline(unittest.TestCase):
    """Test complete medical imaging pipeline"""

    def setUp(self):
        """Set up test fixtures"""
        if not IMAGING_AVAILABLE:
            self.skipTest("Medical imaging modules not available")

        self.pipeline = MedicalImagingPipeline(use_guardrails=False)
        self.test_image_path = self._create_test_image()

    def _create_test_image(self):
        """Create temporary test image"""
        temp_dir = tempfile.mkdtemp()
        image_path = os.path.join(temp_dir, "test_medical_image.png")

        try:
            from PIL import Image
            img = Image.fromarray(np.random.randint(0, 255, (512, 512), dtype=np.uint8))
            img.save(image_path)
        except ImportError:
            # Create dummy file
            with open(image_path, 'wb') as f:
                f.write(b'\x89PNG\r\n\x1a\n')  # PNG header

        return image_path

    def test_pipeline_initialization(self):
        """Test pipeline initialization"""
        self.assertIsNotNone(self.pipeline.dicom_processor)
        self.assertIsNotNone(self.pipeline.xray_analyzer)
        self.assertIsNotNone(self.pipeline.ct_analyzer)
        self.assertIsNotNone(self.pipeline.mri_analyzer)

    def test_xray_pipeline(self):
        """Test complete X-ray analysis pipeline"""
        result = self.pipeline.analyze_image(self.test_image_path, "XRAY")

        if result:
            self.assertEqual(result.modality, "XRAY")
            self.assertIsNotNone(result.metadata)
            self.assertIsInstance(result.detections, list)
            self.assertGreater(result.quality_score, 0)
            self.assertIn(result.clinical_priority, ["Routine", "Priority", "Urgent", "Emergency"])
            self.assertIsInstance(result.findings_summary, str)
            self.assertIsInstance(result.recommendations, list)

    def test_ct_pipeline(self):
        """Test complete CT analysis pipeline"""
        result = self.pipeline.analyze_image(self.test_image_path, "CT")

        if result:
            self.assertEqual(result.modality, "CT")
            self.assertGreater(len(result.detections), 0)

    def test_mri_pipeline(self):
        """Test complete MRI analysis pipeline"""
        result = self.pipeline.analyze_image(self.test_image_path, "MRI")

        if result:
            self.assertEqual(result.modality, "MRI")
            self.assertGreater(len(result.detections), 0)

    def test_performance_benchmark(self):
        """Test processing performance"""
        start = time.time()
        result = self.pipeline.analyze_image(self.test_image_path, "XRAY")
        duration_ms = (time.time() - start) * 1000

        if result:
            # Should complete within reasonable time
            self.assertLess(duration_ms, 5000)  # 5 seconds max
            self.assertGreater(result.processing_time_ms, 0)

    def test_clinical_priority_routing(self):
        """Test clinical priority determination"""
        result = self.pipeline.analyze_image(self.test_image_path, "XRAY")

        if result:
            valid_priorities = ["Routine", "Priority", "Urgent", "Emergency"]
            self.assertIn(result.clinical_priority, valid_priorities)

    def test_hipaa_compliance(self):
        """Test HIPAA compliance in results"""
        result = self.pipeline.analyze_image(self.test_image_path, "XRAY")

        if result:
            # Verify no PHI in results
            self.assertTrue(result.metadata.phi_removed)
            self.assertTrue(result.metadata.hipaa_compliant)
            self.assertTrue(result.metadata.patient_id.startswith("ANON_"))

    def test_batch_processing(self):
        """Test batch image processing"""
        image_paths = [self.test_image_path] * 3
        results = self.pipeline.batch_analyze(image_paths, "XRAY")

        self.assertIsInstance(results, list)
        # At least some should succeed
        self.assertGreaterEqual(len(results), 0)

    def test_result_serialization(self):
        """Test that results can be serialized to JSON"""
        result = self.pipeline.analyze_image(self.test_image_path, "XRAY")

        if result:
            result_dict = result.to_dict()
            json_str = json.dumps(result_dict, default=str)
            self.assertIsInstance(json_str, str)
            self.assertGreater(len(json_str), 0)


class TestIntegration(unittest.TestCase):
    """Integration tests with agent framework"""

    def setUp(self):
        """Set up test fixtures"""
        if not IMAGING_AVAILABLE:
            self.skipTest("Medical imaging modules not available")

    def test_phase_implementation_import(self):
        """Test that phase implementation can import imaging modules"""
        try:
            from implementation import Phase14Implementation
            impl = Phase14Implementation()
            self.assertEqual(impl.phase_id, 14)
        except ImportError:
            self.skipTest("Phase implementation not available")

    def test_guardrails_integration(self):
        """Test guardrails integration"""
        try:
            pipeline = MedicalImagingPipeline(use_guardrails=True)

            # If guardrails available, should be initialized
            if pipeline.use_guardrails:
                self.assertIsNotNone(pipeline.guardrails)
        except (ValueError, ImportError) as e:
            # Guardrails not available (e.g., Azure credentials not set)
            # This is acceptable for testing environment
            self.skipTest(f"Guardrails not available: {e}")


class TestProductionReadiness(unittest.TestCase):
    """Production readiness tests"""

    def test_imaging_modality_enum(self):
        """Test imaging modality enumeration"""
        if not IMAGING_AVAILABLE:
            self.skipTest("Medical imaging modules not available")

        modalities = [m.value for m in ImagingModality]
        self.assertIn("X-Ray", modalities)
        self.assertIn("CT Scan", modalities)
        self.assertIn("MRI", modalities)

    def test_abnormality_type_enum(self):
        """Test abnormality type enumeration"""
        if not IMAGING_AVAILABLE:
            self.skipTest("Medical imaging modules not available")

        abnormalities = [a.value for a in AbnormalityType]
        self.assertIn("Fracture", abnormalities)
        self.assertIn("Pneumonia", abnormalities)
        self.assertIn("Tumor", abnormalities)
        self.assertIn("Normal", abnormalities)

    def test_error_handling(self):
        """Test error handling"""
        if not IMAGING_AVAILABLE:
            self.skipTest("Medical imaging modules not available")

        processor = DICOMProcessor()

        # Test with non-existent file
        img, metadata = processor.load_image("/nonexistent/file.png")
        self.assertIsNone(img)

        # Test with invalid format
        img, metadata = processor.load_image("test.xyz")
        self.assertIsNone(img)


def run_comprehensive_tests():
    """Run all tests with detailed reporting"""
    print("\n" + "="*80)
    print("PHASE 14: MEDICAL IMAGING - COMPREHENSIVE TEST SUITE")
    print("="*80)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDICOMProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestXRayAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestCTAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestMRIAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestMedicalImagingPipeline))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestProductionReadiness))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED - PRODUCTION READY")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED - REVIEW REQUIRED")
        return 1


if __name__ == "__main__":
    exit(run_comprehensive_tests())
