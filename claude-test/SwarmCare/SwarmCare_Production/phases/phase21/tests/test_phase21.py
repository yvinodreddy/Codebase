"""
Phase 21: Closed-Loop Clinical Automation
Comprehensive Test Suite

Tests for:
- Order validation and management
- Smart alerts and clinical decision support
- Workflow automation and task management
- HIPAA compliance
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import (
    Phase21Implementation,
    OrderValidator,
    AlertEngine,
    WorkflowEngine,
    ClinicalOrder,
    SmartAlert,
    WorkflowTask,
    ClinicalWorkflow,
    OrderType,
    OrderPriority,
    OrderStatus,
    AlertType,
    AlertSeverity,
    WorkflowType,
    TaskStatus
)


# ================================================================================
# ORDER VALIDATOR TESTS
# ================================================================================

class TestOrderValidator(unittest.TestCase):
    """Test cases for OrderValidator"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = OrderValidator()

    def test_anonymize_patient_id(self):
        """Test patient ID anonymization for HIPAA compliance"""
        patient_id = "PATIENT_12345"
        anonymized = self.validator.anonymize_patient_id(patient_id)

        # Check hash is created
        self.assertIsNotNone(anonymized)
        self.assertEqual(len(anonymized), 16)

        # Check original ID is not in hash
        self.assertNotIn(patient_id, anonymized)

        # Check consistency (same input = same output)
        anonymized2 = self.validator.anonymize_patient_id(patient_id)
        self.assertEqual(anonymized, anonymized2)

    def test_validate_medication_order_valid(self):
        """Test validation of valid medication order"""
        order = ClinicalOrder(
            order_id="ORD001",
            patient_id="PT001",
            order_type=OrderType.MEDICATION,
            priority=OrderPriority.ROUTINE,
            description="Aspirin 81mg PO daily",
            ordered_by="Dr. Smith",
            ordered_at=datetime.now(),
            details={
                "drug_name": "aspirin",
                "dose": "81 mg",
                "route": "PO",
                "frequency": "daily"
            }
        )

        is_valid, errors = self.validator.validate_order(order)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_validate_medication_order_missing_fields(self):
        """Test validation fails when required fields missing"""
        order = ClinicalOrder(
            order_id="ORD001",
            patient_id="PT001",
            order_type=OrderType.MEDICATION,
            priority=OrderPriority.ROUTINE,
            description="Aspirin",
            ordered_by="Dr. Smith",
            ordered_at=datetime.now(),
            details={"drug_name": "aspirin"}  # Missing dose, route, frequency
        )

        is_valid, errors = self.validator.validate_order(order)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)

    def test_validate_lab_order_valid(self):
        """Test validation of valid lab order"""
        order = ClinicalOrder(
            order_id="ORD002",
            patient_id="PT001",
            order_type=OrderType.LAB,
            priority=OrderPriority.STAT,
            description="Complete Blood Count",
            ordered_by="Dr. Smith",
            ordered_at=datetime.now(),
            details={
                "test_name": "CBC",
                "specimen_type": "blood",
                "stat_reason": "Suspected anemia"
            }
        )

        is_valid, errors = self.validator.validate_order(order)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_validate_lab_order_invalid_specimen(self):
        """Test validation fails with invalid specimen type"""
        order = ClinicalOrder(
            order_id="ORD002",
            patient_id="PT001",
            order_type=OrderType.LAB,
            priority=OrderPriority.ROUTINE,
            description="CBC",
            ordered_by="Dr. Smith",
            ordered_at=datetime.now(),
            details={
                "test_name": "CBC",
                "specimen_type": "invalid_type"
            }
        )

        is_valid, errors = self.validator.validate_order(order)
        self.assertFalse(is_valid)
        self.assertTrue(any("specimen type" in e.lower() for e in errors))

    def test_validate_stat_order_requires_reason(self):
        """Test STAT orders require a reason"""
        order = ClinicalOrder(
            order_id="ORD003",
            patient_id="PT001",
            order_type=OrderType.LAB,
            priority=OrderPriority.STAT,
            description="Troponin",
            ordered_by="Dr. Smith",
            ordered_at=datetime.now(),
            details={
                "test_name": "Troponin",
                "specimen_type": "blood"
                # Missing stat_reason
            }
        )

        is_valid, errors = self.validator.validate_order(order)
        self.assertFalse(is_valid)
        self.assertTrue(any("STAT" in e for e in errors))

    def test_validate_timed_order_requires_schedule(self):
        """Test timed orders require scheduled time"""
        order = ClinicalOrder(
            order_id="ORD004",
            patient_id="PT001",
            order_type=OrderType.MEDICATION,
            priority=OrderPriority.TIMED,
            description="Medication",
            ordered_by="Dr. Smith",
            ordered_at=datetime.now(),
            scheduled_time=None,  # Missing scheduled time
            details={
                "drug_name": "test",
                "dose": "10 mg",
                "route": "PO",
                "frequency": "once"
            }
        )

        is_valid, errors = self.validator.validate_order(order)
        self.assertFalse(is_valid)
        self.assertTrue(any("scheduled time" in e.lower() for e in errors))

    def test_validate_imaging_order_valid(self):
        """Test validation of valid imaging order"""
        order = ClinicalOrder(
            order_id="ORD005",
            patient_id="PT001",
            order_type=OrderType.IMAGING,
            priority=OrderPriority.ROUTINE,
            description="Chest X-Ray",
            ordered_by="Dr. Smith",
            ordered_at=datetime.now(),
            details={
                "study_type": "xray",
                "body_part": "chest"
            }
        )

        is_valid, errors = self.validator.validate_order(order)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)


# ================================================================================
# ALERT ENGINE TESTS
# ================================================================================

class TestAlertEngine(unittest.TestCase):
    """Test cases for AlertEngine"""

    def setUp(self):
        """Set up test fixtures"""
        self.engine = AlertEngine()

    def test_create_alert(self):
        """Test basic alert creation"""
        alert = self.engine.create_alert(
            patient_id="PT001",
            alert_type=AlertType.CRITICAL_VALUE,
            severity=AlertSeverity.HIGH,
            message="Test alert",
            triggered_by="TestSystem"
        )

        self.assertIsNotNone(alert)
        self.assertEqual(alert.patient_id, "PT001")
        self.assertEqual(alert.alert_type, AlertType.CRITICAL_VALUE)
        self.assertEqual(alert.severity, AlertSeverity.HIGH)
        self.assertFalse(alert.acknowledged)

    def test_check_critical_value_high(self):
        """Test critical value alert for high potassium"""
        alert = self.engine.check_critical_value(
            patient_id="PT001",
            test_name="potassium",
            value=6.5
        )

        self.assertIsNotNone(alert)
        self.assertEqual(alert.alert_type, AlertType.CRITICAL_VALUE)
        self.assertEqual(alert.severity, AlertSeverity.HIGH)
        self.assertIn("6.5", alert.message)

    def test_check_critical_value_low(self):
        """Test critical value alert for low potassium"""
        alert = self.engine.check_critical_value(
            patient_id="PT001",
            test_name="potassium",
            value=2.0
        )

        self.assertIsNotNone(alert)
        self.assertEqual(alert.alert_type, AlertType.CRITICAL_VALUE)
        self.assertEqual(alert.severity, AlertSeverity.HIGH)
        self.assertIn("2.0", alert.message)

    def test_check_critical_value_normal(self):
        """Test no alert for normal potassium"""
        alert = self.engine.check_critical_value(
            patient_id="PT001",
            test_name="potassium",
            value=4.0
        )

        self.assertIsNone(alert)

    def test_check_drug_interaction(self):
        """Test drug interaction detection"""
        alerts = self.engine.check_drug_interaction(
            patient_id="PT001",
            new_medication="warfarin",
            current_medications=["aspirin", "lisinopril"]
        )

        self.assertGreater(len(alerts), 0)
        self.assertEqual(alerts[0].alert_type, AlertType.DRUG_INTERACTION)
        self.assertEqual(alerts[0].severity, AlertSeverity.HIGH)

    def test_check_drug_interaction_no_interaction(self):
        """Test no alert when no drug interactions"""
        alerts = self.engine.check_drug_interaction(
            patient_id="PT001",
            new_medication="acetaminophen",
            current_medications=["lisinopril", "metformin"]
        )

        self.assertEqual(len(alerts), 0)

    def test_duplicate_alert_suppression(self):
        """Test that duplicate alerts are suppressed"""
        # Create first alert
        alert1 = self.engine.create_alert(
            patient_id="PT001",
            alert_type=AlertType.CRITICAL_VALUE,
            severity=AlertSeverity.HIGH,
            message="Duplicate test",
            triggered_by="Test"
        )

        initial_count = len(self.engine.active_alerts)

        # Try to create duplicate
        alert2 = self.engine.create_alert(
            patient_id="PT001",
            alert_type=AlertType.CRITICAL_VALUE,
            severity=AlertSeverity.HIGH,
            message="Duplicate test",
            triggered_by="Test"
        )

        # Count should not increase
        self.assertEqual(len(self.engine.active_alerts), initial_count)

    def test_acknowledge_alert(self):
        """Test alert acknowledgment"""
        alert = self.engine.create_alert(
            patient_id="PT001",
            alert_type=AlertType.CLINICAL_DECISION,
            severity=AlertSeverity.MEDIUM,
            message="Test",
            triggered_by="Test"
        )

        # Acknowledge the alert
        success = self.engine.acknowledge_alert(alert.alert_id, "Dr. Smith")

        self.assertTrue(success)
        self.assertTrue(alert.acknowledged)
        self.assertEqual(alert.acknowledged_by, "Dr. Smith")
        self.assertIsNotNone(alert.acknowledged_at)

    def test_get_active_alerts(self):
        """Test getting active (unacknowledged) alerts"""
        # Create two alerts
        alert1 = self.engine.create_alert(
            patient_id="PT001",
            alert_type=AlertType.CRITICAL_VALUE,
            severity=AlertSeverity.HIGH,
            message="Alert 1",
            triggered_by="Test"
        )

        alert2 = self.engine.create_alert(
            patient_id="PT001",
            alert_type=AlertType.ABNORMAL_RESULT,
            severity=AlertSeverity.MEDIUM,
            message="Alert 2",
            triggered_by="Test"
        )

        # Acknowledge one
        self.engine.acknowledge_alert(alert1.alert_id, "Dr. Smith")

        # Get active alerts
        active = self.engine.get_active_alerts()

        # Should only have one active
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].alert_id, alert2.alert_id)

    def test_get_active_alerts_by_severity(self):
        """Test filtering alerts by severity"""
        # Create alerts with different severities
        self.engine.create_alert(
            patient_id="PT001",
            alert_type=AlertType.CRITICAL_VALUE,
            severity=AlertSeverity.HIGH,
            message="High severity",
            triggered_by="Test"
        )

        self.engine.create_alert(
            patient_id="PT001",
            alert_type=AlertType.ABNORMAL_RESULT,
            severity=AlertSeverity.MEDIUM,
            message="Medium severity",
            triggered_by="Test"
        )

        # Get only high severity
        high_alerts = self.engine.get_active_alerts(severity=AlertSeverity.HIGH)

        self.assertGreater(len(high_alerts), 0)
        self.assertTrue(all(a.severity == AlertSeverity.HIGH for a in high_alerts))


# ================================================================================
# WORKFLOW ENGINE TESTS
# ================================================================================

class TestWorkflowEngine(unittest.TestCase):
    """Test cases for WorkflowEngine"""

    def setUp(self):
        """Set up test fixtures"""
        self.engine = WorkflowEngine()

    def test_start_workflow(self):
        """Test starting a workflow"""
        workflow = self.engine.start_workflow(
            patient_id="PT001",
            workflow_type=WorkflowType.ADMISSION,
            started_by="Nurse Smith"
        )

        self.assertIsNotNone(workflow)
        self.assertEqual(workflow.patient_id, "PT001")
        self.assertEqual(workflow.workflow_type, WorkflowType.ADMISSION)
        self.assertEqual(workflow.status, "active")
        self.assertGreater(len(workflow.tasks), 0)

    def test_workflow_tasks_created_from_template(self):
        """Test that workflow tasks are created from template"""
        workflow = self.engine.start_workflow(
            patient_id="PT001",
            workflow_type=WorkflowType.SEPSIS_PROTOCOL,
            started_by="Dr. Jones"
        )

        # Sepsis protocol should have 5 tasks
        self.assertEqual(len(workflow.tasks), 5)

        # Check first task
        first_task = workflow.tasks[0]
        self.assertEqual(first_task.workflow_id, workflow.workflow_id)
        self.assertEqual(first_task.patient_id, "PT001")
        self.assertEqual(first_task.status, TaskStatus.PENDING)

    def test_assign_task(self):
        """Test assigning a task to a user"""
        workflow = self.engine.start_workflow(
            patient_id="PT001",
            workflow_type=WorkflowType.ADMISSION,
            started_by="Admin"
        )

        task = workflow.tasks[0]
        success = self.engine.assign_task(task.task_id, "Nurse Johnson")

        self.assertTrue(success)
        self.assertEqual(task.assigned_to, "Nurse Johnson")
        self.assertEqual(task.status, TaskStatus.ASSIGNED)

    def test_start_task(self):
        """Test marking task as in progress"""
        workflow = self.engine.start_workflow(
            patient_id="PT001",
            workflow_type=WorkflowType.DISCHARGE,
            started_by="Admin"
        )

        task = workflow.tasks[0]
        success = self.engine.start_task(task.task_id)

        self.assertTrue(success)
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)

    def test_complete_task(self):
        """Test completing a task"""
        workflow = self.engine.start_workflow(
            patient_id="PT001",
            workflow_type=WorkflowType.ADMISSION,
            started_by="Admin"
        )

        task = workflow.tasks[0]
        success = self.engine.complete_task(task.task_id)

        self.assertTrue(success)
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(task.completed_at)

    def test_workflow_completion(self):
        """Test that workflow completes when all tasks done"""
        workflow = self.engine.start_workflow(
            patient_id="PT001",
            workflow_type=WorkflowType.ADMISSION,
            started_by="Admin"
        )

        # Complete all tasks
        for task in workflow.tasks:
            self.engine.complete_task(task.task_id)

        # Workflow should be completed
        self.assertEqual(workflow.status, "completed")
        self.assertIsNotNone(workflow.completed_at)

    def test_get_workflow(self):
        """Test retrieving workflow by ID"""
        workflow = self.engine.start_workflow(
            patient_id="PT001",
            workflow_type=WorkflowType.SEPSIS_PROTOCOL,
            started_by="Dr. Lee"
        )

        retrieved = self.engine.get_workflow(workflow.workflow_id)

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.workflow_id, workflow.workflow_id)

    def test_get_patient_workflows(self):
        """Test getting all workflows for a patient"""
        # Create multiple workflows for same patient
        wf1 = self.engine.start_workflow(
            patient_id="PT001",
            workflow_type=WorkflowType.ADMISSION,
            started_by="Admin"
        )

        wf2 = self.engine.start_workflow(
            patient_id="PT001",
            workflow_type=WorkflowType.SEPSIS_PROTOCOL,
            started_by="Dr. Smith"
        )

        # Create workflow for different patient
        wf3 = self.engine.start_workflow(
            patient_id="PT002",
            workflow_type=WorkflowType.DISCHARGE,
            started_by="Admin"
        )

        workflows = self.engine.get_patient_workflows("PT001")

        self.assertEqual(len(workflows), 2)
        self.assertTrue(all(wf.patient_id == "PT001" for wf in workflows))


# ================================================================================
# PHASE 21 IMPLEMENTATION TESTS
# ================================================================================

class TestPhase21Implementation(unittest.TestCase):
    """Test cases for Phase21Implementation"""

    def setUp(self):
        """Set up test fixtures"""
        self.impl = Phase21Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.impl.phase_id, 21)
        self.assertEqual(self.impl.phase_name, "Closed-Loop Clinical Automation")
        self.assertEqual(self.impl.story_points, 38)
        self.assertEqual(self.impl.priority, "P0")
        self.assertIsNotNone(self.impl.order_validator)
        self.assertIsNotNone(self.impl.alert_engine)
        self.assertIsNotNone(self.impl.workflow_engine)

    def test_create_order_valid(self):
        """Test creating a valid order"""
        order, errors, alerts = self.impl.create_order(
            patient_id="PT001",
            order_type=OrderType.LAB,
            priority=OrderPriority.STAT,
            description="CBC",
            ordered_by="Dr. Smith",
            details={
                "test_name": "CBC",
                "specimen_type": "blood",
                "stat_reason": "Anemia workup"
            }
        )

        self.assertIsNotNone(order)
        self.assertEqual(len(errors), 0)
        self.assertEqual(order.status, OrderStatus.VALIDATED)

    def test_create_order_invalid(self):
        """Test creating an invalid order"""
        order, errors, alerts = self.impl.create_order(
            patient_id="PT001",
            order_type=OrderType.MEDICATION,
            priority=OrderPriority.ROUTINE,
            description="Incomplete medication order",
            ordered_by="Dr. Smith",
            details={"drug_name": "test"}  # Missing required fields
        )

        self.assertIsNone(order)
        self.assertGreater(len(errors), 0)

    def test_activate_order(self):
        """Test activating a validated order"""
        order, _, _ = self.impl.create_order(
            patient_id="PT001",
            order_type=OrderType.LAB,
            priority=OrderPriority.ROUTINE,
            description="Metabolic Panel",
            ordered_by="Dr. Brown",
            details={
                "test_name": "BMP",
                "specimen_type": "blood"
            }
        )

        success = self.impl.activate_order(order.order_id)

        self.assertTrue(success)
        self.assertEqual(order.status, OrderStatus.ACTIVE)

    def test_complete_order(self):
        """Test completing an order"""
        order, _, _ = self.impl.create_order(
            patient_id="PT001",
            order_type=OrderType.LAB,
            priority=OrderPriority.ROUTINE,
            description="Lipid Panel",
            ordered_by="Dr. Lee",
            details={
                "test_name": "Lipids",
                "specimen_type": "blood"
            }
        )

        success = self.impl.complete_order(order.order_id)

        self.assertTrue(success)
        self.assertEqual(order.status, OrderStatus.COMPLETED)
        self.assertIsNotNone(order.completed_at)

    def test_cancel_order(self):
        """Test cancelling an order"""
        order, _, _ = self.impl.create_order(
            patient_id="PT001",
            order_type=OrderType.LAB,
            priority=OrderPriority.ROUTINE,
            description="Test order",
            ordered_by="Dr. Smith",
            details={
                "test_name": "Test",
                "specimen_type": "blood"
            }
        )

        success = self.impl.cancel_order(order.order_id, "Patient declined")

        self.assertTrue(success)
        self.assertEqual(order.status, OrderStatus.CANCELLED)
        self.assertIsNotNone(order.cancelled_at)
        self.assertGreater(len(order.notes), 0)

    def test_duplicate_order_alert(self):
        """Test that duplicate orders generate alerts"""
        # Create first order
        order1, _, _ = self.impl.create_order(
            patient_id="PT001",
            order_type=OrderType.LAB,
            priority=OrderPriority.ROUTINE,
            description="CBC",
            ordered_by="Dr. Smith",
            details={
                "test_name": "CBC",
                "specimen_type": "blood"
            }
        )

        self.impl.activate_order(order1.order_id)

        # Create duplicate order
        order2, _, alerts = self.impl.create_order(
            patient_id="PT001",
            order_type=OrderType.LAB,
            priority=OrderPriority.ROUTINE,
            description="CBC",
            ordered_by="Dr. Jones",
            details={
                "test_name": "CBC",
                "specimen_type": "blood"
            }
        )

        # Should have duplicate alert
        self.assertGreater(len(alerts), 0)
        self.assertTrue(any(a.alert_type == AlertType.DUPLICATE_ORDER for a in alerts))

    def test_drug_interaction_alert(self):
        """Test that drug interactions generate alerts"""
        # Create first medication
        order1, _, _ = self.impl.create_order(
            patient_id="PT001",
            order_type=OrderType.MEDICATION,
            priority=OrderPriority.ROUTINE,
            description="Aspirin",
            ordered_by="Dr. Smith",
            details={
                "drug_name": "aspirin",
                "dose": "81 mg",
                "route": "PO",
                "frequency": "daily"
            }
        )

        self.impl.activate_order(order1.order_id)

        # Create interacting medication
        order2, _, alerts = self.impl.create_order(
            patient_id="PT001",
            order_type=OrderType.MEDICATION,
            priority=OrderPriority.ROUTINE,
            description="Warfarin",
            ordered_by="Dr. Smith",
            details={
                "drug_name": "warfarin",
                "dose": "5 mg",
                "route": "PO",
                "frequency": "daily"
            }
        )

        # Should have interaction alert
        self.assertGreater(len(alerts), 0)
        self.assertTrue(any(a.alert_type == AlertType.DRUG_INTERACTION for a in alerts))

    def test_get_active_orders(self):
        """Test getting active orders"""
        # Create and activate orders
        order1, _, _ = self.impl.create_order(
            patient_id="PT001",
            order_type=OrderType.LAB,
            priority=OrderPriority.ROUTINE,
            description="Test 1",
            ordered_by="Dr. Smith",
            details={"test_name": "Test1", "specimen_type": "blood"}
        )

        order2, _, _ = self.impl.create_order(
            patient_id="PT002",
            order_type=OrderType.LAB,
            priority=OrderPriority.ROUTINE,
            description="Test 2",
            ordered_by="Dr. Smith",
            details={"test_name": "Test2", "specimen_type": "blood"}
        )

        self.impl.activate_order(order1.order_id)
        self.impl.activate_order(order2.order_id)

        # Get all active orders
        active = self.impl.get_active_orders()
        self.assertGreaterEqual(len(active), 2)

        # Get active orders for specific patient
        pt001_orders = self.impl.get_active_orders(patient_id="PT001")
        self.assertTrue(all(o.patient_id == "PT001" for o in pt001_orders))

    def test_get_stats(self):
        """Test getting execution statistics"""
        stats = self.impl.get_stats()

        self.assertIn("phase_id", stats)
        self.assertIn("phase_name", stats)
        self.assertIn("story_points", stats)
        self.assertIn("total_orders", stats)
        self.assertIn("active_orders", stats)
        self.assertIn("total_alerts", stats)
        self.assertIn("active_workflows", stats)


# ================================================================================
# INTEGRATION TESTS
# ================================================================================

class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""

    def setUp(self):
        """Set up test fixtures"""
        self.impl = Phase21Implementation()

    def test_end_to_end_sepsis_workflow(self):
        """Test complete sepsis protocol workflow"""
        patient_id = "PT_SEPSIS_001"

        # Start sepsis protocol
        sepsis_workflow = self.impl.workflow_engine.start_workflow(
            patient_id=patient_id,
            workflow_type=WorkflowType.SEPSIS_PROTOCOL,
            started_by="Dr. Emergency"
        )

        self.assertEqual(len(sepsis_workflow.tasks), 5)

        # Create STAT blood culture order
        bc_order, errors, alerts = self.impl.create_order(
            patient_id=patient_id,
            order_type=OrderType.LAB,
            priority=OrderPriority.STAT,
            description="Blood Cultures x2",
            ordered_by="Dr. Emergency",
            details={
                "test_name": "Blood Cultures",
                "specimen_type": "blood",
                "stat_reason": "Sepsis protocol"
            }
        )

        self.assertIsNotNone(bc_order)
        self.impl.activate_order(bc_order.order_id)

        # Create STAT antibiotic order
        abx_order, errors, alerts = self.impl.create_order(
            patient_id=patient_id,
            order_type=OrderType.MEDICATION,
            priority=OrderPriority.STAT,
            description="Ceftriaxone 2g IV",
            ordered_by="Dr. Emergency",
            details={
                "drug_name": "ceftriaxone",
                "dose": "2 g",
                "route": "IV",
                "frequency": "once",
                "stat_reason": "Sepsis protocol"
            }
        )

        self.assertIsNotNone(abx_order)
        self.impl.activate_order(abx_order.order_id)

        # Complete first workflow task
        first_task = sepsis_workflow.tasks[0]
        self.impl.workflow_engine.assign_task(first_task.task_id, "Nurse Critical")
        self.impl.workflow_engine.start_task(first_task.task_id)
        self.impl.workflow_engine.complete_task(first_task.task_id)

        # Verify state
        self.assertEqual(first_task.status, TaskStatus.COMPLETED)
        self.assertEqual(len(self.impl.orders), 2)
        self.assertEqual(len(self.impl.get_active_orders(patient_id=patient_id)), 2)

    def test_end_to_end_admission_with_alerts(self):
        """Test admission workflow with alert generation"""
        patient_id = "PT_ADMIT_001"

        # Start admission workflow
        admission_workflow = self.impl.workflow_engine.start_workflow(
            patient_id=patient_id,
            workflow_type=WorkflowType.ADMISSION,
            started_by="Nurse Admitting"
        )

        self.assertGreater(len(admission_workflow.tasks), 0)

        # Add medications with potential interaction
        med1, _, _ = self.impl.create_order(
            patient_id=patient_id,
            order_type=OrderType.MEDICATION,
            priority=OrderPriority.ROUTINE,
            description="Aspirin 81mg daily",
            ordered_by="Dr. Attending",
            details={
                "drug_name": "aspirin",
                "dose": "81 mg",
                "route": "PO",
                "frequency": "daily"
            }
        )

        self.impl.activate_order(med1.order_id)

        # Add interacting medication
        med2, _, alerts = self.impl.create_order(
            patient_id=patient_id,
            order_type=OrderType.MEDICATION,
            priority=OrderPriority.ROUTINE,
            description="Warfarin 5mg daily",
            ordered_by="Dr. Attending",
            details={
                "drug_name": "warfarin",
                "dose": "5 mg",
                "route": "PO",
                "frequency": "daily"
            }
        )

        # Should have drug interaction alert
        self.assertGreater(len(alerts), 0)

        # Check critical lab value
        critical_alert = self.impl.alert_engine.check_critical_value(
            patient_id=patient_id,
            test_name="potassium",
            value=6.8
        )

        self.assertIsNotNone(critical_alert)
        self.assertEqual(critical_alert.severity, AlertSeverity.HIGH)

        # Verify all active alerts
        all_alerts = self.impl.alert_engine.get_active_alerts(patient_id=patient_id)
        self.assertGreater(len(all_alerts), 0)


# ================================================================================
# TEST RUNNER
# ================================================================================

def run_tests():
    """Run all tests and print results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestOrderValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestAlertEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestWorkflowEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestPhase21Implementation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"Success Rate: {success_rate:.2f}%")
    print("=" * 80)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
