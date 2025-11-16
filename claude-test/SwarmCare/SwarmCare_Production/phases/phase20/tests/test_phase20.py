"""
Phase 20: Security Certifications (SOC 2, HITRUST)
Comprehensive Test Suite

Tests all security certification frameworks:
- SOC 2 Type II compliance
- HITRUST CSF certification
- Penetration testing
- Security audit system
"""

import unittest
import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase20Implementation
from soc2_framework import SOC2Framework, TrustServicesCriteria, ControlStatus
from hitrust_framework import HITRUSTFramework, HITRUSTCategory, ImplementationLevel, RiskLevel
from penetration_testing import PenetrationTestingFramework, TestType, Severity
from security_audit_system import SecurityAuditSystem, AuditFramework, AuditStatus


class TestSOC2Framework(unittest.TestCase):
    """Test SOC 2 Type II compliance framework"""

    def setUp(self):
        self.framework = SOC2Framework()

    def test_framework_initialization(self):
        """Test framework initializes with controls"""
        self.assertGreater(len(self.framework.controls), 0)
        stats = self.framework.get_stats()
        self.assertIn('total_controls', stats)
        self.assertIn('framework_version', stats)

    def test_control_categories(self):
        """Test all TSC categories are represented"""
        stats = self.framework.get_stats()
        categories = stats['controls_by_category']

        # Verify all 5 TSC categories exist
        self.assertIn('CC', categories)  # Security
        self.assertIn('A', categories)   # Availability
        self.assertIn('PI', categories)  # Processing Integrity
        self.assertIn('C', categories)   # Confidentiality
        self.assertIn('P', categories)   # Privacy

    def test_control_retrieval(self):
        """Test retrieving specific controls"""
        control = self.framework.get_control('CC6.7')
        self.assertIsNotNone(control)
        self.assertEqual(control.control_id, 'CC6.7')
        self.assertEqual(control.category, TrustServicesCriteria.SECURITY)

    def test_control_status_update(self):
        """Test updating control status"""
        self.framework.update_control_status(
            'CC6.7',
            ControlStatus.OPERATING_EFFECTIVELY,
            "Encryption tested and validated"
        )
        control = self.framework.get_control('CC6.7')
        self.assertEqual(control.status, ControlStatus.OPERATING_EFFECTIVELY)
        self.assertIsNotNone(control.last_tested)

    def test_compliance_assessment(self):
        """Test compliance assessment"""
        # Implement some controls
        self.framework.update_control_status('CC6.7', ControlStatus.OPERATING_EFFECTIVELY)
        self.framework.update_control_status('CC7.1', ControlStatus.OPERATING_EFFECTIVELY)

        report = self.framework.assess_compliance()

        self.assertIsNotNone(report)
        self.assertGreaterEqual(report.compliance_percentage, 0)
        self.assertLessEqual(report.compliance_percentage, 100)
        self.assertIn(report.overall_status, ['Ready for Audit', 'Needs Improvement', 'Not Ready'])

    def test_controls_by_category(self):
        """Test filtering controls by category"""
        security_controls = self.framework.get_controls_by_category(TrustServicesCriteria.SECURITY)
        self.assertGreater(len(security_controls), 0)
        self.assertTrue(all(c.category == TrustServicesCriteria.SECURITY for c in security_controls))


class TestHITRUSTFramework(unittest.TestCase):
    """Test HITRUST CSF certification framework"""

    def setUp(self):
        self.framework = HITRUSTFramework()

    def test_framework_initialization(self):
        """Test HITRUST framework initialization"""
        self.assertGreater(len(self.framework.controls), 0)
        stats = self.framework.get_stats()
        self.assertEqual(stats['framework_version'], 'CSF v11')

    def test_control_categories(self):
        """Test HITRUST control categories"""
        stats = self.framework.get_stats()
        categories = stats['controls_by_category']
        self.assertGreater(len(categories), 0)

    def test_control_maturity_update(self):
        """Test updating control maturity levels"""
        self.framework.update_control_maturity(
            '01.a',
            ImplementationLevel.LEVEL_5,
            'compliant'
        )
        control = self.framework.get_control('01.a')
        self.assertEqual(control.maturity_level, ImplementationLevel.LEVEL_5)
        self.assertEqual(control.compliance_status, 'compliant')

    def test_risk_assessment(self):
        """Test risk assessment functionality"""
        risk = self.framework.perform_risk_assessment(
            asset_name="Test Database",
            category=HITRUSTCategory.ACCESS_CONTROL,
            threat="Unauthorized access",
            vulnerability="Weak controls",
            likelihood=RiskLevel.HIGH,
            impact=RiskLevel.HIGH,
            controls=["11.f"]
        )

        self.assertIsNotNone(risk)
        self.assertEqual(risk.asset_name, "Test Database")
        self.assertIn(risk.inherent_risk, [RiskLevel.LOW, RiskLevel.MODERATE, RiskLevel.HIGH, RiskLevel.CRITICAL])
        self.assertIn(risk.risk_treatment, ['accept', 'mitigate', 'transfer', 'avoid'])

    def test_certification_readiness(self):
        """Test certification readiness assessment"""
        # Implement some controls
        self.framework.update_control_maturity('01.a', ImplementationLevel.LEVEL_5, 'compliant')
        self.framework.update_control_maturity('02.a', ImplementationLevel.LEVEL_4, 'compliant')

        readiness = self.framework.assess_certification_readiness()

        self.assertIsNotNone(readiness)
        self.assertGreaterEqual(readiness.readiness_percentage, 0)
        self.assertLessEqual(readiness.readiness_percentage, 100)
        self.assertIsInstance(readiness.ready_for_certification, bool)
        self.assertGreaterEqual(readiness.estimated_remediation_days, 0)


class TestPenetrationTesting(unittest.TestCase):
    """Test penetration testing framework"""

    def setUp(self):
        self.framework = PenetrationTestingFramework()

    def test_scope_creation(self):
        """Test creating penetration test scope"""
        scope = self.framework.create_scope(
            test_type=TestType.WEB_APPLICATION,
            targets=["https://test.example.com"],
            testing_window={"start": "2025-11-01T00:00:00", "end": "2025-11-05T23:59:59"}
        )

        self.assertIsNotNone(scope)
        self.assertEqual(scope.test_type, TestType.WEB_APPLICATION)
        self.assertEqual(len(scope.targets), 1)
        self.assertGreater(len(scope.rules_of_engagement), 0)
        self.assertGreater(len(scope.authorized_techniques), 0)

    def test_penetration_test_execution(self):
        """Test executing penetration test"""
        scope = self.framework.create_scope(
            test_type=TestType.WEB_APPLICATION,
            targets=["https://test.example.com"],
            testing_window={"start": "2025-11-01T00:00:00", "end": "2025-11-05T23:59:59"}
        )

        report = self.framework.perform_test(scope, tester="Test Team")

        self.assertIsNotNone(report)
        self.assertEqual(report.test_type, TestType.WEB_APPLICATION)
        self.assertGreaterEqual(report.total_vulnerabilities, 0)
        self.assertGreaterEqual(report.risk_score, 0)
        self.assertLessEqual(report.risk_score, 100)
        self.assertIn(report.overall_security_posture, ['excellent', 'good', 'fair', 'poor', 'critical'])

    def test_vulnerability_tracking(self):
        """Test vulnerability tracking"""
        scope = self.framework.create_scope(
            test_type=TestType.WEB_APPLICATION,
            targets=["https://test.example.com"],
            testing_window={"start": "2025-11-01T00:00:00", "end": "2025-11-05T23:59:59"}
        )

        report = self.framework.perform_test(scope, tester="Test Team")

        if report.total_vulnerabilities > 0:
            vuln = report.vulnerabilities[0]
            self.assertIsNotNone(vuln.vuln_id)
            self.assertIn(vuln.severity, [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFORMATIONAL])
            self.assertGreaterEqual(vuln.cvss_score, 0)
            self.assertLessEqual(vuln.cvss_score, 10)

    def test_framework_stats(self):
        """Test framework statistics"""
        stats = self.framework.get_stats()
        self.assertIn('framework_version', stats)
        self.assertIn('total_tests_performed', stats)


class TestSecurityAuditSystem(unittest.TestCase):
    """Test security audit and reporting system"""

    def setUp(self):
        self.audit_system = SecurityAuditSystem()

    def test_audit_execution(self):
        """Test conducting security audit"""
        controls = {
            "TEST-001": {
                "title": "Test Control",
                "description": "Test control description",
                "status": "operating_effectively",
                "evidence": ["Test evidence"],
                "risk_level": "high"
            }
        }

        report = self.audit_system.conduct_audit(
            framework=AuditFramework.SOC2_TYPE2,
            auditor="Test Auditor",
            scope="Test Scope",
            controls_to_test=controls
        )

        self.assertIsNotNone(report)
        self.assertEqual(report.framework, AuditFramework.SOC2_TYPE2)
        self.assertGreaterEqual(report.compliance_percentage, 0)
        self.assertLessEqual(report.compliance_percentage, 100)
        self.assertIn(report.certification_status, ['certified', 'conditionally_certified', 'not_certified'])

    def test_compliance_dashboard(self):
        """Test compliance dashboard generation"""
        # First conduct an audit to have data
        controls = {
            "TEST-001": {"title": "Test", "description": "Test", "status": "implemented", "risk_level": "medium"}
        }
        self.audit_system.conduct_audit(AuditFramework.SOC2_TYPE2, "Test Auditor", "Test", controls)

        dashboard = self.audit_system.generate_compliance_dashboard()

        self.assertIsNotNone(dashboard)
        self.assertGreaterEqual(dashboard.total_open_findings, 0)
        self.assertGreaterEqual(dashboard.remediation_velocity, 0)

    def test_remediation_tracking(self):
        """Test remediation item tracking"""
        controls = {
            "TEST-001": {
                "title": "Test Control",
                "description": "Test",
                "status": "not_implemented",
                "risk_level": "critical"
            }
        }

        report = self.audit_system.conduct_audit(
            AuditFramework.SOC2_TYPE2,
            "Test Auditor",
            "Test Scope",
            controls
        )

        # Verify remediation items created for failed controls
        self.assertGreater(len(self.audit_system.remediation_items), 0)

    def test_framework_stats(self):
        """Test audit system statistics"""
        stats = self.audit_system.get_stats()
        self.assertIn('system_version', stats)
        self.assertIn('total_audits_conducted', stats)


class TestPhase20Implementation(unittest.TestCase):
    """Test Phase 20 main implementation"""

    def setUp(self):
        self.implementation = Phase20Implementation()

    def test_initialization(self):
        """Test Phase 20 initialization"""
        self.assertEqual(self.implementation.phase_id, 20)
        self.assertEqual(self.implementation.phase_name, "Security Certifications (SOC 2, HITRUST)")
        self.assertEqual(self.implementation.story_points, 42)
        self.assertEqual(self.implementation.priority, "P0")

    def test_all_frameworks_initialized(self):
        """Test all security frameworks are initialized"""
        self.assertIsNotNone(self.implementation.soc2)
        self.assertIsNotNone(self.implementation.hitrust)
        self.assertIsNotNone(self.implementation.pentest)
        self.assertIsNotNone(self.implementation.audit_system)

    def test_soc2_implementation(self):
        """Test SOC 2 implementation method"""
        result = self.implementation.implement_soc2_compliance()

        self.assertIsNotNone(result)
        self.assertEqual(result['framework'], 'SOC 2 Type II')
        self.assertIn('total_controls', result)
        self.assertIn('compliance_percentage', result)

    def test_hitrust_implementation(self):
        """Test HITRUST implementation method"""
        result = self.implementation.implement_hitrust_certification()

        self.assertIsNotNone(result)
        self.assertEqual(result['framework'], 'HITRUST CSF')
        self.assertIn('readiness_percentage', result)
        self.assertIn('ready_for_certification', result)

    def test_penetration_testing_execution(self):
        """Test penetration testing execution"""
        result = self.implementation.conduct_penetration_testing()

        self.assertIsNotNone(result)
        self.assertIn('total_vulnerabilities', result)
        self.assertIn('security_posture', result)

    def test_security_audit_execution(self):
        """Test security audit execution"""
        result = self.implementation.perform_security_audits()

        self.assertIsNotNone(result)
        self.assertIn('compliance_percentage', result)
        self.assertIn('certification_status', result)

    def test_full_execution(self):
        """Test full Phase 20 execution"""
        task = {"goal": "Implement Security Certifications", "phase_id": 20}
        result = self.implementation.execute(task)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        self.assertEqual(result.output['phase_id'], 20)
        self.assertEqual(result.output['status'], 'COMPLETED')
        self.assertIn('components', result.output)
        self.assertIn('summary', result.output)

    def test_execution_creates_frameworks(self):
        """Test execution creates all framework components"""
        task = {"goal": "Implement Security Certifications", "phase_id": 20}
        result = self.implementation.execute(task)

        self.assertTrue(result.success)
        components = result.output['components']

        self.assertIn('soc2', components)
        self.assertIn('hitrust', components)
        self.assertIn('penetration_testing', components)
        self.assertIn('security_audit', components)

    def test_statistics_retrieval(self):
        """Test getting implementation statistics"""
        stats = self.implementation.get_stats()

        self.assertIsNotNone(stats)
        self.assertEqual(stats['phase_id'], 20)
        self.assertIn('frameworks', stats)
        self.assertIn('soc2', stats['frameworks'])
        self.assertIn('hitrust', stats['frameworks'])


class TestIntegration(unittest.TestCase):
    """Integration tests for Phase 20"""

    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # Initialize Phase 20
        impl = Phase20Implementation()

        # Execute full implementation
        task = {"goal": "Complete Security Certification", "phase_id": 20}
        result = impl.execute(task)

        # Verify success
        self.assertTrue(result.success)

        # Verify all components executed
        output = result.output
        self.assertIn('soc2', output['components'])
        self.assertIn('hitrust', output['components'])
        self.assertIn('penetration_testing', output['components'])
        self.assertIn('security_audit', output['components'])

        # Verify summary metrics
        summary = output['summary']
        self.assertIn('soc2_compliance', summary)
        self.assertIn('hitrust_readiness', summary)
        self.assertIn('vulnerabilities_found', summary)
        self.assertIn('security_posture', summary)

    def test_multi_framework_support(self):
        """Test support for multiple security frameworks"""
        impl = Phase20Implementation()

        # Verify all frameworks are operational
        soc2_stats = impl.soc2.get_stats()
        hitrust_stats = impl.hitrust.get_stats()
        pentest_stats = impl.pentest.get_stats()
        audit_stats = impl.audit_system.get_stats()

        self.assertGreater(soc2_stats['total_controls'], 0)
        self.assertGreater(hitrust_stats['total_controls'], 0)
        self.assertIn('framework_version', pentest_stats)
        self.assertIn('system_version', audit_stats)


def main():
    """Run test suite"""
    print("="*80)
    print("PHASE 20 COMPREHENSIVE TEST SUITE")
    print("="*80)
    print()

    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("="*80)
    print("TEST RESULTS")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*80)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
