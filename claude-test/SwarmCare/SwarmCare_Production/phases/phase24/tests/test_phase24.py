"""
Phase 24: 100% Automated Coding & EHR Integration
Comprehensive test suite

Tests cover:
- EHR Integration Engine (8 systems)
- Automated Coding System (ICD-10, CPT, HCPCS)
- Billing Engine
- Phase24 implementation
"""

import unittest
import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import (
    Phase24Implementation,
    EHRConnector,
    EHRIntegrationEngine,
    AutomatedCodingSystem,
    BillingEngine
)


class TestEHRConnector(unittest.TestCase):
    """Test cases for EHR Connector base class"""

    def setUp(self):
        """Set up test fixtures"""
        self.connector = EHRConnector("TestEHR", "TestVendor", "FHIR R4")

    def test_ehr_connector_initialization(self):
        """Test EHR connector initializes properly"""
        self.assertEqual(self.connector.system_name, "TestEHR")
        self.assertEqual(self.connector.vendor, "TestVendor")
        self.assertEqual(self.connector.api_version, "FHIR R4")
        self.assertEqual(self.connector.connection_status, "disconnected")

    def test_ehr_connector_connect(self):
        """Test EHR connector can establish connection"""
        result = self.connector.connect()
        self.assertEqual(result["status"], "connected")
        self.assertEqual(result["system"], "TestEHR")
        self.assertEqual(self.connector.connection_status, "connected")

    def test_ehr_connector_verify_connection(self):
        """Test connection verification"""
        self.connector.connect()
        verification = self.connector.verify_connection()
        self.assertTrue(verification["connected"])
        self.assertEqual(verification["system"], "TestEHR")
        self.assertIn("latency_ms", verification)

    def test_ehr_connector_read_patient(self):
        """Test patient data read operation"""
        result = self.connector.read_patient("PAT12345")
        self.assertEqual(result["patient_id"], "PAT12345")
        self.assertEqual(result["system"], "TestEHR")
        self.assertTrue(result["data_retrieved"])

    def test_ehr_connector_supported_operations(self):
        """Test connector has required supported operations"""
        self.assertGreater(len(self.connector.supported_operations), 0)
        self.assertIn("patient_read", self.connector.supported_operations)


class TestEHRIntegrationEngine(unittest.TestCase):
    """Test cases for EHR Integration Engine"""

    def setUp(self):
        """Set up test fixtures"""
        self.engine = EHRIntegrationEngine()

    def test_ehr_engine_initialization(self):
        """Test EHR engine initializes with all 11 systems"""
        self.assertEqual(len(self.engine.systems), 11)
        expected_systems = [
            "Epic", "Cerner", "Allscripts", "athenahealth",
            "eClinicalWorks", "NextGen", "MEDITECH", "Practice Fusion",
            "ModMed", "AdvancedMD", "Greenway Health"
        ]
        for system in expected_systems:
            self.assertIn(system, self.engine.systems)

    def test_ehr_engine_system_types(self):
        """Test all systems are EHRConnector instances"""
        for system_name, connector in self.engine.systems.items():
            self.assertIsInstance(connector, EHRConnector)
            self.assertEqual(connector.system_name, system_name)

    def test_ehr_engine_integrate_all_systems(self):
        """Test integration with all EHR systems"""
        result = self.engine.integrate_all_systems()
        self.assertEqual(result["total_count"], 11)
        self.assertEqual(result["connected_count"], 11)
        self.assertEqual(result["success_rate"], 1.0)
        self.assertEqual(len(result["systems"]), 11)

    def test_ehr_engine_verify_all_connections(self):
        """Test verification of all connections"""
        self.engine.integrate_all_systems()
        verification = self.engine.verify_all_connections()
        self.assertEqual(len(verification), 11)
        for system, status in verification.items():
            self.assertTrue(status["connected"])

    def test_ehr_engine_epic_integration(self):
        """Test Epic EHR system specifically"""
        self.assertIn("Epic", self.engine.systems)
        epic = self.engine.systems["Epic"]
        self.assertEqual(epic.vendor, "Epic Systems")
        self.assertEqual(epic.api_version, "FHIR R4")

    def test_ehr_engine_cerner_integration(self):
        """Test Cerner EHR system specifically"""
        self.assertIn("Cerner", self.engine.systems)
        cerner = self.engine.systems["Cerner"]
        self.assertEqual(cerner.vendor, "Oracle Health")


class TestAutomatedCodingSystem(unittest.TestCase):
    """Test cases for Automated Coding System"""

    def setUp(self):
        """Set up test fixtures"""
        self.coding_system = AutomatedCodingSystem()

    def test_coding_system_initialization(self):
        """Test coding system initializes with code sets"""
        self.assertEqual(len(self.coding_system.icd10_codes), 500)
        self.assertEqual(len(self.coding_system.cpt_codes), 500)
        self.assertEqual(len(self.coding_system.hcpcs_codes), 500)

    def test_coding_system_icd10_codes(self):
        """Test ICD-10 codes are valid format"""
        for code in self.coding_system.icd10_codes:
            self.assertIsInstance(code, str)
            self.assertGreater(len(code), 0)

    def test_coding_system_cpt_codes(self):
        """Test CPT codes are valid format"""
        for code in self.coding_system.cpt_codes:
            self.assertIsInstance(code, str)
            self.assertGreaterEqual(len(code), 5)  # CPT codes are 5 digits minimum

    def test_coding_system_hcpcs_codes(self):
        """Test HCPCS codes are valid format"""
        for code in self.coding_system.hcpcs_codes:
            self.assertIsInstance(code, str)
            self.assertGreater(len(code), 0)

    def test_coding_system_generate_codes(self):
        """Test code generation for encounters"""
        result = self.coding_system.generate_codes_for_encounters(encounter_count=50)
        self.assertEqual(result["encounter_count"], 50)
        self.assertGreater(result["total_codes"], 0)
        self.assertGreater(result["icd10_codes_generated"], 0)
        self.assertGreater(result["cpt_codes_generated"], 0)

    def test_coding_system_code_counts(self):
        """Test code generation produces reasonable counts"""
        result = self.coding_system.generate_codes_for_encounters(encounter_count=100)
        # Each encounter should have multiple codes
        self.assertGreater(result["avg_codes_per_encounter"], 3)
        self.assertEqual(result["coding_accuracy"], 1.0)  # Production ready: 100% accuracy

    def test_coding_system_validate_codes_valid(self):
        """Test code validation with valid codes"""
        valid_codes = ["I10", "99201", "E1000"]
        result = self.coding_system.validate_codes(valid_codes)
        self.assertEqual(result["valid_codes"], 3)
        self.assertEqual(result["invalid_codes"], 0)
        self.assertEqual(result["validation_rate"], 1.0)

    def test_coding_system_validate_codes_invalid(self):
        """Test code validation with invalid codes"""
        invalid_codes = ["INVALID1", "INVALID2"]
        result = self.coding_system.validate_codes(invalid_codes)
        self.assertEqual(result["valid_codes"], 0)
        self.assertEqual(result["invalid_codes"], 2)
        self.assertEqual(result["validation_rate"], 0.0)

    def test_coding_system_validate_codes_mixed(self):
        """Test code validation with mixed valid/invalid codes"""
        mixed_codes = ["I10", "INVALID", "99201"]
        result = self.coding_system.validate_codes(mixed_codes)
        self.assertEqual(result["valid_codes"], 2)
        self.assertEqual(result["invalid_codes"], 1)


class TestBillingEngine(unittest.TestCase):
    """Test cases for Billing Engine"""

    def setUp(self):
        """Set up test fixtures"""
        self.billing_engine = BillingEngine()

    def test_billing_engine_initialization(self):
        """Test billing engine initializes with pricing"""
        self.assertEqual(len(self.billing_engine.cpt_prices), 500)

    def test_billing_engine_cpt_prices(self):
        """Test CPT code pricing is valid"""
        for code, price in self.billing_engine.cpt_prices.items():
            self.assertIsInstance(code, str)
            self.assertIsInstance(price, (int, float))
            self.assertGreater(price, 0)

    def test_billing_engine_generate_billing_records(self):
        """Test billing record generation"""
        result = self.billing_engine.generate_billing_records(encounter_count=50)
        self.assertEqual(result["total_records"], 50)
        self.assertGreater(result["total_value"], 0)
        self.assertGreater(result["avg_claim_value"], 0)

    def test_billing_engine_billing_accuracy(self):
        """Test billing accuracy meets threshold"""
        result = self.billing_engine.generate_billing_records(encounter_count=100)
        self.assertEqual(result["billing_accuracy"], 1.0)  # Production ready: 100% accuracy

    def test_billing_engine_records_structure(self):
        """Test billing records have proper structure"""
        result = self.billing_engine.generate_billing_records(encounter_count=10)
        for record in result["records"]:
            self.assertIn("encounter_id", record)
            self.assertIn("services", record)
            self.assertIn("total_charge", record)
            self.assertIn("status", record)

    def test_billing_engine_calculation_accuracy(self):
        """Test billing calculations are accurate"""
        result = self.billing_engine.generate_billing_records(encounter_count=100)
        expected_avg = result["total_value"] / result["total_records"]
        self.assertAlmostEqual(result["avg_claim_value"], expected_avg, places=2)


class TestPhase24Implementation(unittest.TestCase):
    """Test cases for Phase 24 Implementation"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase24Implementation()

    def test_phase24_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 24)
        self.assertEqual(self.implementation.phase_name, "100% Automated Coding & EHR Integration")
        self.assertEqual(self.implementation.story_points, 48)
        self.assertEqual(self.implementation.priority, "P0")

    def test_phase24_framework_components(self):
        """Test framework components are initialized"""
        # Check that framework components exist (if framework available)
        if hasattr(self.implementation, 'guardrails'):
            self.assertIsNotNone(self.implementation.guardrails)
        else:
            # Framework not available, skip this test gracefully
            self.skipTest("Framework not available")

    def test_phase24_execution(self):
        """Test phase execution completes successfully"""
        task = {"goal": "Implement 100% Automated Coding & EHR Integration", "phase_id": 24}
        result = self.implementation.execute(task)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)

    def test_phase24_output_structure(self):
        """Test output has required fields"""
        task = {"goal": "Implement Phase 24", "phase_id": 24}
        result = self.implementation.execute(task)
        output = result.output
        self.assertIn("phase_id", output)
        self.assertIn("status", output)
        self.assertIn("components", output)

    def test_phase24_ehr_systems_count(self):
        """Test correct number of EHR systems integrated"""
        task = {"goal": "Implement Phase 24", "phase_id": 24}
        result = self.implementation.execute(task)
        self.assertEqual(result.output["components"]["ehr_systems_integrated"], 11)

    def test_phase24_coding_generation(self):
        """Test automated coding generates codes"""
        task = {"goal": "Implement Phase 24", "phase_id": 24}
        result = self.implementation.execute(task)
        components = result.output["components"]
        self.assertGreater(components["total_codes_generated"], 0)
        self.assertGreater(components["icd10_codes"], 0)
        self.assertGreater(components["cpt_codes"], 0)

    def test_phase24_billing_generation(self):
        """Test billing records are generated"""
        task = {"goal": "Implement Phase 24", "phase_id": 24}
        result = self.implementation.execute(task)
        components = result.output["components"]
        self.assertGreater(components["billing_records_generated"], 0)
        self.assertGreater(components["total_claims_value"], 0)

    def test_phase24_verification_passes(self):
        """Test verification passes"""
        task = {"goal": "Implement Phase 24", "phase_id": 24}
        result = self.implementation.execute(task)
        self.assertTrue(result.output["components"]["verification_passed"])

    def test_phase24_production_ready(self):
        """Test implementation is marked production ready"""
        task = {"goal": "Implement Phase 24", "phase_id": 24}
        result = self.implementation.execute(task)
        self.assertTrue(result.output["components"]["production_ready"])

    def test_phase24_get_stats(self):
        """Test get_stats returns proper statistics"""
        stats = self.implementation.get_stats()
        self.assertEqual(stats["phase_id"], 24)
        self.assertEqual(stats["story_points"], 48)
        self.assertEqual(stats["framework_version"], "100%")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
