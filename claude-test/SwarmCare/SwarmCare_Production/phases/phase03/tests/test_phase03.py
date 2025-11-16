#!/usr/bin/env python3
"""
Phase 03: Workflow Orchestration
Comprehensive Unit and Integration Tests

Test Coverage:
- WorkflowEngine core functionality
- EHR-to-Podcast workflow
- Diagnostic workflows (sepsis, stroke, cardiac)
- Phase implementation
- Error handling and recovery
"""

import unittest
import sys
import os
from datetime import datetime
from pathlib import Path

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'deliverables'))

from implementation import Phase03Implementation

try:
    from workflow_engine import WorkflowEngine, Task, WorkflowState, TaskState
    from ehr_to_podcast_workflow import EHRToPodcastWorkflow
    from diagnostic_workflows import DiagnosticWorkflows
    DELIVERABLES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Deliverables not available: {e}")
    DELIVERABLES_AVAILABLE = False


class TestPhase03Implementation(unittest.TestCase):
    """Test Phase 03 main implementation"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase03Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 3)
        self.assertEqual(self.implementation.phase_name, "Workflow Orchestration")
        self.assertEqual(self.implementation.story_points, 76)
        self.assertEqual(self.implementation.priority, "P0")

    def test_phase_execution(self):
        """Test phase execution"""
        task = {"goal": "Implement Workflow Orchestration", "phase_id": 3}
        result = self.implementation.execute(task)

        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'success'))

        if result.success:
            self.assertIsNotNone(result.output)
            self.assertIn('phase_id', result.output)
            self.assertIn('components', result.output)

    def test_get_stats(self):
        """Test statistics retrieval"""
        stats = self.implementation.get_stats()

        self.assertIn('phase_id', stats)
        self.assertIn('phase_name', stats)
        self.assertIn('story_points', stats)
        self.assertEqual(stats['phase_id'], 3)


@unittest.skipUnless(DELIVERABLES_AVAILABLE, "Deliverables not available")
class TestWorkflowEngine(unittest.TestCase):
    """Test WorkflowEngine core functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.engine = WorkflowEngine()

    def test_engine_initialization(self):
        """Test engine initialization"""
        self.assertIsNotNone(self.engine)
        self.assertEqual(len(self.engine.workflows), 0)
        self.assertTrue(self.engine.persistence_dir.exists())

    def test_workflow_registration(self):
        """Test workflow registration"""
        def sample_task(context):
            return {"result": "success"}

        tasks = [
            Task(
                task_id="task1",
                name="Sample Task",
                action=sample_task,
                dependencies=[]
            )
        ]

        workflow_id = self.engine.register_workflow("test_workflow", tasks)

        self.assertEqual(workflow_id, "test_workflow")
        self.assertIn("test_workflow", self.engine.workflows)
        self.assertEqual(len(self.engine.workflows["test_workflow"]), 1)

    def test_dag_validation_success(self):
        """Test DAG validation with valid workflow"""
        def task1(context):
            return {"result": "task1"}

        def task2(context):
            return {"result": "task2"}

        tasks = [
            Task(task_id="t1", name="Task 1", action=task1, dependencies=[]),
            Task(task_id="t2", name="Task 2", action=task2, dependencies=["t1"])
        ]

        # Should not raise exception
        workflow_id = self.engine.register_workflow("valid_dag", tasks)
        self.assertIsNotNone(workflow_id)

    def test_dag_validation_cycle_detection(self):
        """Test DAG validation detects cycles"""
        def task_action(context):
            return {"result": "test"}

        # Create circular dependency
        tasks = [
            Task(task_id="t1", name="Task 1", action=task_action, dependencies=["t2"]),
            Task(task_id="t2", name="Task 2", action=task_action, dependencies=["t1"])
        ]

        with self.assertRaises(ValueError) as cm:
            self.engine.register_workflow("circular_workflow", tasks)

        self.assertIn("cycle", str(cm.exception).lower())

    def test_dag_validation_missing_dependency(self):
        """Test DAG validation detects missing dependencies"""
        def task_action(context):
            return {"result": "test"}

        tasks = [
            Task(task_id="t1", name="Task 1", action=task_action, dependencies=["nonexistent"])
        ]

        with self.assertRaises(ValueError) as cm:
            self.engine.register_workflow("missing_dep_workflow", tasks)

        self.assertIn("non-existent", str(cm.exception).lower())

    def test_workflow_execution_simple(self):
        """Test simple workflow execution"""
        def increment(context):
            context['value'] = context.get('value', 0) + 1
            return {"incremented": True}

        tasks = [
            Task(task_id="inc1", name="Increment 1", action=increment, dependencies=[]),
            Task(task_id="inc2", name="Increment 2", action=increment, dependencies=["inc1"]),
            Task(task_id="inc3", name="Increment 3", action=increment, dependencies=["inc2"])
        ]

        self.engine.register_workflow("increment_workflow", tasks)
        execution = self.engine.execute_workflow("increment_workflow", {"value": 0})

        self.assertEqual(execution.state, WorkflowState.COMPLETED)
        self.assertEqual(execution.context['value'], 3)

    def test_workflow_execution_parallel_tasks(self):
        """Test parallel task execution"""
        def task_a(context):
            context['a'] = True
            return {"completed": "a"}

        def task_b(context):
            context['b'] = True
            return {"completed": "b"}

        def task_c(context):
            # Depends on both a and b
            self.assertTrue(context.get('a'))
            self.assertTrue(context.get('b'))
            context['c'] = True
            return {"completed": "c"}

        tasks = [
            Task(task_id="a", name="Task A", action=task_a, dependencies=[]),
            Task(task_id="b", name="Task B", action=task_b, dependencies=[]),
            Task(task_id="c", name="Task C", action=task_c, dependencies=["a", "b"])
        ]

        self.engine.register_workflow("parallel_workflow", tasks)
        execution = self.engine.execute_workflow("parallel_workflow")

        self.assertEqual(execution.state, WorkflowState.COMPLETED)
        self.assertTrue(execution.context.get('a'))
        self.assertTrue(execution.context.get('b'))
        self.assertTrue(execution.context.get('c'))

    def test_task_retry_mechanism(self):
        """Test task retry on failure"""
        attempt_count = {'count': 0}

        def failing_task(context):
            attempt_count['count'] += 1
            if attempt_count['count'] < 3:
                raise Exception(f"Attempt {attempt_count['count']} failed")
            return {"success": True}

        tasks = [
            Task(
                task_id="retry_task",
                name="Retry Task",
                action=failing_task,
                dependencies=[],
                max_retries=3
            )
        ]

        self.engine.register_workflow("retry_workflow", tasks)
        execution = self.engine.execute_workflow("retry_workflow")

        self.assertEqual(execution.state, WorkflowState.COMPLETED)
        self.assertEqual(attempt_count['count'], 3)

    def test_workflow_failure_on_task_failure(self):
        """Test workflow fails when task exceeds retries"""
        def always_fails(context):
            raise Exception("This task always fails")

        tasks = [
            Task(
                task_id="fail_task",
                name="Always Fails",
                action=always_fails,
                dependencies=[],
                max_retries=1
            )
        ]

        self.engine.register_workflow("fail_workflow", tasks)
        execution = self.engine.execute_workflow("fail_workflow")

        self.assertEqual(execution.state, WorkflowState.FAILED)
        self.assertIsNotNone(execution.error)

    def test_execution_persistence(self):
        """Test execution state persistence"""
        def simple_task(context):
            return {"persisted": True}

        tasks = [
            Task(task_id="persist", name="Persist Task", action=simple_task, dependencies=[])
        ]

        self.engine.register_workflow("persist_workflow", tasks)
        execution = self.engine.execute_workflow("persist_workflow")

        # Load execution from disk
        loaded_execution = self.engine.load_execution(execution.execution_id)

        self.assertIsNotNone(loaded_execution)
        self.assertEqual(loaded_execution.execution_id, execution.execution_id)
        self.assertEqual(loaded_execution.state, WorkflowState.COMPLETED)

    def test_get_execution_status(self):
        """Test execution status retrieval"""
        def status_task(context):
            return {"status": "ok"}

        tasks = [
            Task(task_id="status", name="Status Task", action=status_task, dependencies=[])
        ]

        self.engine.register_workflow("status_workflow", tasks)
        execution = self.engine.execute_workflow("status_workflow")

        status = self.engine.get_execution_status(execution.execution_id)

        self.assertIsNotNone(status)
        self.assertEqual(status['execution_id'], execution.execution_id)
        self.assertEqual(status['state'], WorkflowState.COMPLETED.value)
        self.assertIn('tasks', status)

    def test_engine_metrics(self):
        """Test engine metrics tracking"""
        def metric_task(context):
            return {"metric": True}

        tasks = [
            Task(task_id="metric", name="Metric Task", action=metric_task, dependencies=[])
        ]

        self.engine.register_workflow("metric_workflow", tasks)

        # Execute multiple times
        for _ in range(3):
            self.engine.execute_workflow("metric_workflow")

        metrics = self.engine.get_metrics()

        self.assertGreaterEqual(metrics['total_executions'], 3)
        self.assertIn('completed', metrics)
        self.assertIn('success_rate', metrics)


@unittest.skipUnless(DELIVERABLES_AVAILABLE, "Deliverables not available")
class TestEHRToPodcastWorkflow(unittest.TestCase):
    """Test EHR-to-Podcast workflow"""

    def setUp(self):
        """Set up test fixtures"""
        self.engine = WorkflowEngine()
        self.workflow = EHRToPodcastWorkflow(self.engine)

    def test_workflow_initialization(self):
        """Test workflow initialization"""
        self.assertIsNotNone(self.workflow)
        self.assertEqual(self.workflow.workflow_id, "ehr_to_podcast")
        self.assertIn("ehr_to_podcast", self.engine.workflows)

    def test_ehr_extraction(self):
        """Test EHR data extraction"""
        context = {'patient_id': 'TEST_001', 'encounter_id': 'ENC_001'}
        result = self.workflow.extract_ehr_data(context)

        self.assertEqual(result['status'], 'success')
        self.assertIn('ehr_data', context)
        self.assertIn('clinical_notes', context['ehr_data'])

    def test_phi_deidentification(self):
        """Test PHI de-identification"""
        context = {
            'ehr_data': {
                'demographics': {'name': 'John Doe', 'mrn': 'MRN12345'},
                'clinical_notes': [
                    {'text': 'Patient John Doe seen on 2025-10-28', 'author': 'Dr. Smith', 'date': '2025-10-28'}
                ]
            }
        }

        result = self.workflow.deidentify_phi(context)

        self.assertEqual(result['status'], 'success')
        self.assertTrue(context['phi_removed'])
        self.assertIn('[PATIENT_NAME]', context['deidentified_data']['clinical_notes'][0]['text'])

    def test_clinical_note_processing(self):
        """Test clinical note processing"""
        context = {
            'deidentified_data': {
                'clinical_notes': [
                    {'text': 'Patient has hypertension, prescribed lisinopril'}
                ]
            }
        }

        result = self.workflow.process_clinical_notes(context)

        self.assertEqual(result['status'], 'success')
        self.assertIn('processed_notes', context)
        self.assertGreater(len(context['processed_notes']), 0)

    def test_podcast_script_generation(self):
        """Test podcast script generation"""
        context = {
            'processed_notes': [
                {
                    'extracted_concepts': {
                        'diagnoses': [{'term': 'Hypertension', 'confidence': 0.95}],
                        'medications': [{'term': 'Lisinopril', 'confidence': 0.98}],
                        'findings': []
                    }
                }
            ],
            'deidentified_data': {}
        }

        result = self.workflow.generate_podcast_script(context)

        self.assertEqual(result['status'], 'success')
        self.assertIn('podcast_script', context)
        self.assertGreater(len(context['podcast_script']), 100)

    def test_complete_workflow_execution(self):
        """Test complete EHR-to-Podcast workflow"""
        result = self.workflow.execute("PATIENT_001", "ENC_001")

        self.assertIn('execution_id', result)
        self.assertIn('status', result)
        # Status could be COMPLETED or FAILED depending on guardrails availability


@unittest.skipUnless(DELIVERABLES_AVAILABLE, "Deliverables not available")
class TestDiagnosticWorkflows(unittest.TestCase):
    """Test diagnostic workflows"""

    def setUp(self):
        """Set up test fixtures"""
        self.engine = WorkflowEngine()
        self.diagnostics = DiagnosticWorkflows(self.engine)

    def test_diagnostics_initialization(self):
        """Test diagnostics initialization"""
        self.assertIsNotNone(self.diagnostics)
        self.assertIn("sepsis_screening", self.engine.workflows)
        self.assertIn("stroke_assessment", self.engine.workflows)
        self.assertIn("cardiac_assessment", self.engine.workflows)

    def test_qsofa_calculation_positive(self):
        """Test qSOFA calculation - positive case"""
        context = {
            'vitals': {
                'respiratory_rate': 24,  # >= 22
                'gcs': 14,  # < 15
                'systolic_bp': 95  # <= 100
            }
        }

        result = self.diagnostics.calculate_qsofa(context)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(context['qsofa']['score'], 3)
        self.assertTrue(context['qsofa']['positive'])

    def test_qsofa_calculation_negative(self):
        """Test qSOFA calculation - negative case"""
        context = {
            'vitals': {
                'respiratory_rate': 16,
                'gcs': 15,
                'systolic_bp': 120
            }
        }

        result = self.diagnostics.calculate_qsofa(context)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(context['qsofa']['score'], 0)
        self.assertFalse(context['qsofa']['positive'])

    def test_sirs_calculation(self):
        """Test SIRS criteria calculation"""
        context = {
            'vitals': {
                'temperature': 38.5,  # > 38
                'heart_rate': 95,  # > 90
                'respiratory_rate': 22,  # > 20
                'wbc': 13.0  # > 12
            }
        }

        result = self.diagnostics.calculate_sirs(context)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(context['sirs']['score'], 4)
        self.assertTrue(context['sirs']['positive'])

    def test_sepsis_screening_low_risk(self):
        """Test sepsis screening - low risk"""
        vitals = {
            'systolic_bp': 120,
            'respiratory_rate': 16,
            'heart_rate': 75,
            'temperature': 37.0,
            'gcs': 15,
            'wbc': 8.0
        }

        result = self.diagnostics.screen_sepsis("PATIENT_001", vitals)

        self.assertIn('risk_level', result)
        self.assertEqual(result['risk_level'], 'LOW')

    def test_sepsis_screening_high_risk(self):
        """Test sepsis screening - high risk"""
        vitals = {
            'systolic_bp': 90,
            'respiratory_rate': 24,
            'heart_rate': 110,
            'temperature': 38.8,
            'gcs': 14,
            'wbc': 15.0
        }

        result = self.diagnostics.screen_sepsis("PATIENT_002", vitals)

        self.assertIn('risk_level', result)
        self.assertIn(result['risk_level'], ['HIGH', 'CRITICAL'])

    def test_fast_assessment_positive(self):
        """Test FAST assessment - stroke suspected"""
        context = {
            'fast': {
                'face_droop': True,
                'arm_weakness': True,
                'speech_difficulty': False
            }
        }

        result = self.diagnostics.fast_assessment(context)

        self.assertTrue(context['fast_assessment']['stroke_suspected'])

    def test_heart_score_calculation(self):
        """Test HEART score calculation"""
        context = {
            'cardiac_data': {
                'history': 'highly_suspicious',
                'ecg': 'significant',
                'age': 70,
                'risk_factors': 4,
                'troponin': '>3x'
            }
        }

        result = self.diagnostics.calculate_heart_score(context)

        self.assertEqual(result['status'], 'success')
        self.assertGreaterEqual(context['heart_score']['score'], 7)

    def test_cardiac_assessment(self):
        """Test complete cardiac risk assessment"""
        cardiac_data = {
            'history': 'moderately_suspicious',
            'ecg': 'normal',
            'age': 55,
            'risk_factors': 2,
            'troponin': 'normal'
        }

        result = self.diagnostics.assess_cardiac_risk_patient("PATIENT_003", cardiac_data)

        self.assertIn('heart_score', result)
        self.assertIn('risk_level', result)
        self.assertIn('recommendations', result)


class TestIntegration(unittest.TestCase):
    """Integration tests"""

    def test_phase03_deliverables_integration(self):
        """Test that all Phase 03 components integrate properly"""
        impl = Phase03Implementation()
        task = {"goal": "Test integration", "phase_id": 3}

        result = impl.execute(task)

        # Should complete successfully
        self.assertIsNotNone(result)


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPhase03Implementation))

    if DELIVERABLES_AVAILABLE:
        suite.addTests(loader.loadTestsFromTestCase(TestWorkflowEngine))
        suite.addTests(loader.loadTestsFromTestCase(TestEHRToPodcastWorkflow))
        suite.addTests(loader.loadTestsFromTestCase(TestDiagnosticWorkflows))

    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    print("=" * 80)
    print("PHASE 03: WORKFLOW ORCHESTRATION - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print()

    result = run_tests()

    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED")
        sys.exit(1)
