"""
Phase 23: FDA Clearance & PACS Integration
Comprehensive Test Suite

Tests all Phase 23 frameworks:
- FDA 510(k) clearance
- DICOM handler
- PACS integration
- Radiology workflow
- Main implementation
"""

import unittest
import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase23Implementation
from fda_clearance import (
    FDA510kFramework, PredicateDevice, SubjectDevice,
    DeviceClass, SubmissionType, RiskLevel
)
from dicom_handler import (
    DICOMHandler, Modality, Patient, Study, Series,
    QueryRetrieveLevel
)
from pacs_integration import (
    PACSIntegration, PACSConnectionStatus, Priority, ArchiveTier
)
from radiology_workflow import (
    RadiologyWorkflow, ExamPriority, ExamStatus,
    ReportStatus, QAResult
)


class TestFDA510kFramework(unittest.TestCase):
    """Test FDA 510(k) clearance framework"""

    def setUp(self):
        self.framework = FDA510kFramework()

    def test_framework_initialization(self):
        """Test framework initializes correctly"""
        self.assertIsNotNone(self.framework)
        self.assertEqual(self.framework.version, "1.0.0")
        stats = self.framework.get_stats()
        self.assertIn('framework_name', stats)
        self.assertIn('total_submissions', stats)

    def test_register_predicate_device(self):
        """Test registering predicate device"""
        predicate = PredicateDevice(
            device_id="TEST-PRED-001",
            manufacturer="Test Manufacturer",
            device_name="Test Device",
            k_number="K123456",
            clearance_date="2023-01-01",
            device_class=DeviceClass.CLASS_II,
            intended_use="Test use",
            indications_for_use="Test indications",
            technological_characteristics=["AI", "Cloud"]
        )

        device_id = self.framework.register_predicate_device(predicate)
        self.assertEqual(device_id, "TEST-PRED-001")
        self.assertIn(device_id, self.framework.predicate_database)

    def test_device_comparison(self):
        """Test substantial equivalence comparison"""
        predicate = PredicateDevice(
            device_id="PRED-001",
            manufacturer="Test Co",
            device_name="Device A",
            k_number="K123456",
            clearance_date="2023-01-01",
            device_class=DeviceClass.CLASS_II,
            intended_use="Medical diagnosis",
            indications_for_use="For diagnosis",
            technological_characteristics=["AI", "DICOM"],
            performance_data={"accuracy": 0.95}
        )

        subject = SubjectDevice(
            device_id="SUBJ-001",
            manufacturer="Test Co",
            device_name="Device B",
            model_number="V2.0",
            device_class=DeviceClass.CLASS_II,
            intended_use="Medical diagnosis",
            indications_for_use="For diagnosis",
            technological_characteristics=["AI", "DICOM"],
            performance_data={"accuracy": 0.96}
        )

        comparison = self.framework.compare_devices(subject, predicate)
        self.assertIsNotNone(comparison)
        self.assertTrue(comparison.intended_use_same)
        self.assertIsInstance(comparison.is_substantially_equivalent, bool)

    def test_risk_analysis(self):
        """Test ISO 14971 risk analysis"""
        subject = SubjectDevice(
            device_id="SUBJ-001",
            manufacturer="Test Co",
            device_name="Test Device",
            model_number="V1.0",
            device_class=DeviceClass.CLASS_II,
            intended_use="Test",
            indications_for_use="Test",
            technological_characteristics=["AI"]
        )

        hazards = [{
            "hazard": "Algorithm error",
            "situation": "Incorrect output",
            "harm": "Wrong diagnosis",
            "severity": RiskLevel.HIGH,
            "probability": RiskLevel.LOW,
            "controls": ["Validation", "Testing"],
            "verification": ["Clinical trials"]
        }]

        risks = self.framework.perform_risk_analysis(subject, hazards)
        self.assertEqual(len(risks), 1)
        self.assertEqual(risks[0].hazard, "Algorithm error")

    def test_submission_creation(self):
        """Test 510(k) submission creation"""
        predicate = PredicateDevice(
            device_id="PRED-001", manufacturer="Test", device_name="Device A",
            k_number="K123", clearance_date="2023-01-01",
            device_class=DeviceClass.CLASS_II, intended_use="Test",
            indications_for_use="Test", technological_characteristics=["AI"]
        )

        subject = SubjectDevice(
            device_id="SUBJ-001", manufacturer="Test", device_name="Device B",
            model_number="V2", device_class=DeviceClass.CLASS_II,
            intended_use="Test", indications_for_use="Test",
            technological_characteristics=["AI"]
        )

        submission_id = self.framework.create_submission(
            subject_device=subject,
            predicate_devices=[predicate]
        )

        self.assertIsNotNone(submission_id)
        self.assertIn(submission_id, self.framework.submissions)


class TestDICOMHandler(unittest.TestCase):
    """Test DICOM standard implementation"""

    def setUp(self):
        self.handler = DICOMHandler()

    def test_handler_initialization(self):
        """Test DICOM handler initialization"""
        self.assertIsNotNone(self.handler)
        self.assertEqual(self.handler.version, "1.0.0")
        stats = self.handler.get_stats()
        self.assertIn('framework_name', stats)

    def test_patient_creation(self):
        """Test creating patient record"""
        patient = self.handler.create_patient(
            patient_id="P001",
            patient_name="DOE^JOHN",
            date_of_birth="19800101",
            sex="M"
        )

        self.assertEqual(patient.patient_id, "P001")
        self.assertEqual(patient.patient_name, "DOE^JOHN")
        self.assertIn("P001", self.handler.patients)

    def test_study_creation(self):
        """Test creating DICOM study"""
        self.handler.create_patient(patient_id="P001", patient_name="DOE^JOHN")

        study = self.handler.create_study(
            patient_id="P001",
            study_date="20251031",
            study_description="Test Study"
        )

        self.assertIsNotNone(study.study_instance_uid)
        self.assertEqual(study.patient_id, "P001")

    def test_series_creation(self):
        """Test creating DICOM series"""
        self.handler.create_patient(patient_id="P001", patient_name="DOE^JOHN")
        study = self.handler.create_study(
            patient_id="P001",
            study_date="20251031"
        )

        series = self.handler.create_series(
            study_uid=study.study_instance_uid,
            modality=Modality.CT,
            series_number=1
        )

        self.assertIsNotNone(series.series_instance_uid)
        self.assertEqual(series.modality, Modality.CT)

    def test_instance_creation(self):
        """Test creating DICOM instance"""
        self.handler.create_patient(patient_id="P001", patient_name="DOE^JOHN")
        study = self.handler.create_study(patient_id="P001", study_date="20251031")
        series = self.handler.create_series(
            study_uid=study.study_instance_uid,
            modality=Modality.CT,
            series_number=1
        )

        instance = self.handler.create_instance(
            series_uid=series.series_instance_uid,
            instance_number=1,
            sop_class_uid="1.2.840.10008.5.1.4.1.1.2"
        )

        self.assertIsNotNone(instance.sop_instance_uid)
        self.assertEqual(instance.instance_number, 1)

    def test_c_find_patients(self):
        """Test DICOM C-FIND for patients"""
        self.handler.create_patient(patient_id="P001", patient_name="DOE^JOHN")

        query = self.handler.c_find(
            QueryRetrieveLevel.PATIENT,
            PatientID="*"
        )

        self.assertGreater(len(query.results), 0)

    def test_worklist_creation(self):
        """Test modality worklist entry creation"""
        entry = self.handler.create_worklist_entry(
            patient_id="P001",
            patient_name="DOE^JOHN",
            accession_number="ACC001",
            modality=Modality.CT,
            scheduled_date="20251031",
            scheduled_time="14:00:00",
            ae_title="CT_SCANNER"
        )

        self.assertIsNotNone(entry.entry_id)
        self.assertEqual(entry.modality, Modality.CT)


class TestPACSIntegration(unittest.TestCase):
    """Test PACS integration system"""

    def setUp(self):
        self.pacs = PACSIntegration()

    def test_pacs_initialization(self):
        """Test PACS integration initialization"""
        self.assertIsNotNone(self.pacs)
        self.assertEqual(self.pacs.version, "1.0.0")

    def test_register_pacs_node(self):
        """Test registering PACS node"""
        node_id = self.pacs.register_pacs_node(
            ae_title="TEST_PACS",
            hostname="pacs.test.local",
            port=11112
        )

        self.assertIsNotNone(node_id)
        self.assertIn(node_id, self.pacs.pacs_nodes)

    def test_connect_to_node(self):
        """Test connecting to PACS node"""
        node_id = self.pacs.register_pacs_node(
            ae_title="TEST_PACS",
            hostname="pacs.test.local",
            port=11112
        )

        result = self.pacs.connect_to_node(node_id)
        self.assertTrue(result)

        node = self.pacs.pacs_nodes[node_id]
        self.assertEqual(node.connection_status, PACSConnectionStatus.CONNECTED)

    def test_store_image(self):
        """Test storing image to PACS"""
        node_id = self.pacs.register_pacs_node(
            ae_title="TEST_PACS",
            hostname="pacs.test.local",
            port=11112
        )
        self.pacs.connect_to_node(node_id)

        transaction_id = self.pacs.store_image(
            destination_node_id=node_id,
            study_uid="1.2.3",
            series_uid="1.2.3.4",
            sop_uid="1.2.3.4.5",
            modality="CT",
            image_data=b"test_data"
        )

        self.assertIsNotNone(transaction_id)

    def test_archive_study(self):
        """Test archiving study"""
        archive_id = self.pacs.archive_study(
            study_uid="1.2.3",
            patient_id="P001",
            modality="CT",
            number_of_images=100,
            size_bytes=500 * 1024 * 1024
        )

        self.assertIsNotNone(archive_id)
        self.assertIn(archive_id, self.pacs.archive_entries)

    def test_routing_rule(self):
        """Test creating routing rule"""
        node_id = self.pacs.register_pacs_node(
            ae_title="ARCHIVE",
            hostname="archive.local",
            port=11113
        )

        rule_id = self.pacs.create_routing_rule(
            rule_name="Route CT",
            destination_node_ids=[node_id],
            modality="CT"
        )

        self.assertIsNotNone(rule_id)
        self.assertEqual(len(self.pacs.routing_rules), 1)


class TestRadiologyWorkflow(unittest.TestCase):
    """Test radiology workflow management"""

    def setUp(self):
        self.workflow = RadiologyWorkflow()

    def test_workflow_initialization(self):
        """Test workflow initialization"""
        self.assertIsNotNone(self.workflow)
        self.assertEqual(self.workflow.version, "1.0.0")

    def test_schedule_exam(self):
        """Test scheduling radiology exam"""
        exam_id = self.workflow.schedule_exam(
            patient_id="P001",
            patient_name="DOE^JOHN",
            exam_type="CT Chest",
            modality="CT",
            body_part="CHEST",
            scheduled_date="20251031",
            scheduled_time="14:00:00",
            ordering_physician="Dr. Smith",
            clinical_indication="Test indication"
        )

        self.assertIsNotNone(exam_id)
        self.assertIn(exam_id, self.workflow.exams)

    def test_check_in_patient(self):
        """Test patient check-in"""
        exam_id = self.workflow.schedule_exam(
            patient_id="P001", patient_name="DOE^JOHN",
            exam_type="CT Chest", modality="CT", body_part="CHEST",
            scheduled_date="20251031", scheduled_time="14:00:00",
            ordering_physician="Dr. Smith", clinical_indication="Test"
        )

        result = self.workflow.check_in_patient(exam_id)
        self.assertTrue(result)

        exam = self.workflow.exams[exam_id]
        self.assertEqual(exam.status, ExamStatus.CHECKED_IN)

    def test_complete_exam(self):
        """Test completing exam"""
        exam_id = self.workflow.schedule_exam(
            patient_id="P001", patient_name="DOE^JOHN",
            exam_type="CT Chest", modality="CT", body_part="CHEST",
            scheduled_date="20251031", scheduled_time="14:00:00",
            ordering_physician="Dr. Smith", clinical_indication="Test"
        )

        self.workflow.check_in_patient(exam_id)
        self.workflow.start_exam(exam_id, "Tech-A", "CT-1")
        result = self.workflow.complete_exam(exam_id, "1.2.3", 100)

        self.assertTrue(result)
        exam = self.workflow.exams[exam_id]
        # After completion, exam is automatically added to reading worklist
        self.assertEqual(exam.status, ExamStatus.READY_FOR_READING)

    def test_create_report(self):
        """Test creating radiology report"""
        exam_id = self.workflow.schedule_exam(
            patient_id="P001", patient_name="DOE^JOHN",
            exam_type="CT Chest", modality="CT", body_part="CHEST",
            scheduled_date="20251031", scheduled_time="14:00:00",
            ordering_physician="Dr. Smith", clinical_indication="Test"
        )

        self.workflow.check_in_patient(exam_id)
        self.workflow.start_exam(exam_id, "Tech-A", "CT-1")
        self.workflow.complete_exam(exam_id, "1.2.3", 100)

        exam = self.workflow.exams[exam_id]
        report_id = self.workflow.create_report(
            accession_number=exam.accession_number,
            radiologist_name="Dr. Jones",
            radiologist_id="RAD001",
            findings="Normal findings",
            impression="No abnormalities"
        )

        self.assertIsNotNone(report_id)
        self.assertIn(report_id, self.workflow.reports)

    def test_sign_report(self):
        """Test signing report"""
        exam_id = self.workflow.schedule_exam(
            patient_id="P001", patient_name="DOE^JOHN",
            exam_type="CT Chest", modality="CT", body_part="CHEST",
            scheduled_date="20251031", scheduled_time="14:00:00",
            ordering_physician="Dr. Smith", clinical_indication="Test"
        )

        self.workflow.complete_exam(exam_id, "1.2.3", 100)
        exam = self.workflow.exams[exam_id]

        report_id = self.workflow.create_report(
            accession_number=exam.accession_number,
            radiologist_name="Dr. Jones",
            radiologist_id="RAD001",
            findings="Normal",
            impression="No abnormalities"
        )

        result = self.workflow.sign_report(report_id, ReportStatus.FINAL)
        self.assertTrue(result)

        report = self.workflow.reports[report_id]
        self.assertEqual(report.report_status, ReportStatus.FINAL)

    def test_quality_assurance(self):
        """Test QA assessment"""
        exam_id = self.workflow.schedule_exam(
            patient_id="P001", patient_name="DOE^JOHN",
            exam_type="CT Chest", modality="CT", body_part="CHEST",
            scheduled_date="20251031", scheduled_time="14:00:00",
            ordering_physician="Dr. Smith", clinical_indication="Test"
        )

        qa_id = self.workflow.perform_qa(
            exam_id=exam_id,
            qa_type="random_sample",
            reviewer_name="QA-Supervisor"
        )

        self.assertIsNotNone(qa_id)
        self.assertIn(qa_id, self.workflow.qa_assessments)

    def test_reading_worklist(self):
        """Test reading worklist"""
        exam_id = self.workflow.schedule_exam(
            patient_id="P001", patient_name="DOE^JOHN",
            exam_type="CT Chest", modality="CT", body_part="CHEST",
            scheduled_date="20251031", scheduled_time="14:00:00",
            ordering_physician="Dr. Smith", clinical_indication="Test"
        )

        self.workflow.complete_exam(exam_id, "1.2.3", 100)

        worklist = self.workflow.get_reading_worklist()
        self.assertGreater(len(worklist), 0)


class TestPhase23Implementation(unittest.TestCase):
    """Test Phase 23 main implementation"""

    def setUp(self):
        self.implementation = Phase23Implementation()

    def test_initialization(self):
        """Test Phase 23 initialization"""
        self.assertEqual(self.implementation.phase_id, 23)
        self.assertEqual(self.implementation.phase_name, "FDA Clearance & PACS Integration")
        self.assertEqual(self.implementation.story_points, 52)
        self.assertEqual(self.implementation.priority, "P0")

    def test_all_frameworks_initialized(self):
        """Test all frameworks are initialized"""
        self.assertIsNotNone(self.implementation.fda_framework)
        self.assertIsNotNone(self.implementation.dicom_handler)
        self.assertIsNotNone(self.implementation.pacs_integration)
        self.assertIsNotNone(self.implementation.radiology_workflow)

    def test_fda_clearance_implementation(self):
        """Test FDA clearance implementation method"""
        result = self.implementation.implement_fda_clearance()

        self.assertIsNotNone(result)
        self.assertIn('framework', result)
        self.assertIn('k_number', result)
        self.assertIn('substantially_equivalent', result)

    def test_dicom_implementation(self):
        """Test DICOM implementation method"""
        result = self.implementation.implement_dicom()

        self.assertIsNotNone(result)
        self.assertIn('framework', result)
        self.assertIn('study_uid', result)
        self.assertIn('instances_created', result)

    def test_pacs_implementation(self):
        """Test PACS implementation method"""
        # First create a study to get UID
        dicom_result = self.implementation.implement_dicom()
        study_uid = dicom_result['study_uid']

        result = self.implementation.implement_pacs(study_uid)

        self.assertIsNotNone(result)
        self.assertIn('framework', result)
        self.assertIn('connected_nodes', result)

    def test_radiology_workflow_implementation(self):
        """Test radiology workflow implementation method"""
        dicom_result = self.implementation.implement_dicom()
        study_uid = dicom_result['study_uid']

        result = self.implementation.implement_radiology_workflow(study_uid)

        self.assertIsNotNone(result)
        self.assertIn('framework', result)
        self.assertIn('exams_completed', result)

    def test_full_execution(self):
        """Test full Phase 23 execution"""
        task = {"goal": "Implement FDA Clearance & PACS Integration", "phase_id": 23}
        result = self.implementation.execute(task)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        self.assertEqual(result.output['phase_id'], 23)
        self.assertEqual(result.output['status'], 'COMPLETED')

    def test_execution_creates_all_components(self):
        """Test execution creates all framework components"""
        task = {"goal": "Implement Phase 23", "phase_id": 23}
        result = self.implementation.execute(task)

        self.assertTrue(result.success)
        components = result.output['components']

        self.assertIn('fda_clearance', components)
        self.assertIn('dicom', components)
        self.assertIn('pacs', components)
        self.assertIn('radiology_workflow', components)

    def test_statistics_retrieval(self):
        """Test getting implementation statistics"""
        stats = self.implementation.get_stats()

        self.assertIsNotNone(stats)
        self.assertEqual(stats['phase_id'], 23)
        self.assertIn('frameworks', stats)


class TestIntegration(unittest.TestCase):
    """Integration tests for Phase 23"""

    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        impl = Phase23Implementation()

        task = {"goal": "Complete FDA Clearance & PACS Integration", "phase_id": 23}
        result = impl.execute(task)

        # Verify success
        self.assertTrue(result.success)

        # Verify all components executed
        output = result.output
        self.assertIn('fda_clearance', output['components'])
        self.assertIn('dicom', output['components'])
        self.assertIn('pacs', output['components'])
        self.assertIn('radiology_workflow', output['components'])

        # Verify summary metrics
        summary = output['summary']
        self.assertIn('fda_submission', summary)
        self.assertIn('dicom_images', summary)
        self.assertIn('pacs_nodes', summary)
        self.assertIn('exams_completed', summary)

    def test_multi_framework_coordination(self):
        """Test coordination between multiple frameworks"""
        impl = Phase23Implementation()

        # Create DICOM study
        dicom_result = impl.implement_dicom()
        study_uid = dicom_result['study_uid']

        # Use study in PACS
        pacs_result = impl.implement_pacs(study_uid)
        self.assertGreater(pacs_result['connected_nodes'], 0)

        # Use study in workflow
        workflow_result = impl.implement_radiology_workflow(study_uid)
        self.assertGreater(workflow_result['exams_completed'], 0)


def main():
    """Run test suite"""
    print("=" * 80)
    print("PHASE 23 COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print()

    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("=" * 80)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
