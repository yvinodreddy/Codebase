#!/usr/bin/env python3
"""
Phase 06: HIPAA Compliance - Comprehensive Test Suite

Tests all HIPAA compliance components with 100% coverage target.
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from hipaa_compliance_system import (
    EncryptionSystem, MFASystem, JWTManager, RBACSystem,
    TamperProofAuditLog, SessionManager, PHIMasking,
    HIPAAComplianceSystem, AuditLogEntry
)
from datetime import datetime
import secrets


class TestHIPAACompliance:
    """Comprehensive HIPAA compliance test suite"""

    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0

    def test_encryption_system(self):
        """Test encryption/decryption"""
        print("\n  Testing Encryption System...")
        encryption = EncryptionSystem()

        plaintext = "Sensitive PHI Data"
        encrypted = encryption.encrypt(plaintext)

        assert "ciphertext" in encrypted
        assert "nonce" in encrypted
        assert encrypted["algorithm"] == "AES-256-GCM"

        decrypted = encryption.decrypt(encrypted["ciphertext"], encrypted["nonce"])
        assert decrypted == plaintext

        print("    ✅ Encryption/Decryption works")
        self.tests_passed += 1

    def test_mfa_system(self):
        """Test MFA setup and verification"""
        print("\n  Testing MFA System...")
        mfa = MFASystem()

        setup = mfa.setup_totp("test_user")
        assert "secret" in setup
        assert "backup_codes" in setup
        assert len(setup["backup_codes"]) == 8

        print("    ✅ MFA setup works")
        self.tests_passed += 1

    def test_jwt_manager(self):
        """Test JWT token creation and verification"""
        print("\n  Testing JWT Manager...")
        jwt_mgr = JWTManager()

        token = jwt_mgr.create_access_token("user_123", ["doctor"], True)
        assert token is not None

        payload = jwt_mgr.verify_token(token)
        assert payload["sub"] == "user_123"
        assert payload["mfa_verified"] is True

        print("    ✅ JWT tokens work")
        self.tests_passed += 1

    def test_rbac_system(self):
        """Test RBAC permissions"""
        print("\n  Testing RBAC System...")
        rbac = RBACSystem()

        # Admin has all permissions
        assert rbac.check_permission(["admin"], "read:all_phi")
        assert rbac.check_permission(["admin"], "delete:phi")

        # Doctor has limited permissions
        assert rbac.check_permission(["doctor"], "read:assigned_phi")
        assert not rbac.check_permission(["doctor"], "delete:phi")

        # Patient has minimal permissions
        assert rbac.check_permission(["patient"], "read:own_phi")
        assert not rbac.check_permission(["patient"], "read:all_phi")

        print("    ✅ RBAC permissions work")
        self.tests_passed += 1

    def test_audit_logging(self):
        """Test tamper-proof audit logging"""
        print("\n  Testing Audit Logging...")
        audit_log = TamperProofAuditLog()

        log_entry1 = AuditLogEntry(
            timestamp=datetime.utcnow().isoformat(),
            event_id=secrets.token_urlsafe(16),
            event_type="PHI_ACCESS",
            user_id="user_123",
            user_role="doctor",
            patient_id="patient_456",
            action="READ",
            resource="/api/patients/456",
            ip_address="192.168.1.1",
            session_id="sess_abc",
            mfa_verified=True,
            result="SUCCESS",
            phi_accessed=True,
            data_categories=["demographics"],
            metadata={}
        )

        hash1 = audit_log.append_log(log_entry1)
        assert hash1 is not None
        assert len(audit_log.log_chain) == 1

        # Add second entry
        log_entry2 = AuditLogEntry(
            timestamp=datetime.utcnow().isoformat(),
            event_id=secrets.token_urlsafe(16),
            event_type="PHI_ACCESS",
            user_id="user_123",
            user_role="doctor",
            patient_id="patient_789",
            action="WRITE",
            resource="/api/patients/789",
            ip_address="192.168.1.1",
            session_id="sess_abc",
            mfa_verified=True,
            result="SUCCESS",
            phi_accessed=True,
            data_categories=["vitals"],
            metadata={}
        )

        hash2 = audit_log.append_log(log_entry2)
        assert len(audit_log.log_chain) == 2

        # Verify chain integrity
        assert audit_log.verify_chain() is True

        print("    ✅ Audit logging works")
        self.tests_passed += 1

    def test_session_management(self):
        """Test session management"""
        print("\n  Testing Session Management...")
        session_mgr = SessionManager()

        session_id = session_mgr.create_session("user_123", {"role": "doctor"})
        assert session_id.startswith("sess_")

        session = session_mgr.validate_session(session_id)
        assert session["user_id"] == "user_123"

        print("    ✅ Session management works")
        self.tests_passed += 1

    def test_phi_masking(self):
        """Test PHI masking"""
        print("\n  Testing PHI Masking...")
        masking = PHIMasking()

        ssn_masked = masking.mask_ssn("123-45-6789")
        assert ssn_masked == "***-**-6789"

        phone_masked = masking.mask_phone("(555) 123-4567")
        assert "***" in phone_masked

        email_masked = masking.mask_email("john.doe@example.com")
        assert email_masked[0] == 'j'
        assert '*' in email_masked

        print("    ✅ PHI masking works")
        self.tests_passed += 1

    def test_integrated_system(self):
        """Test complete integrated system"""
        print("\n  Testing Integrated System...")
        hipaa = HIPAAComplianceSystem()

        # Test encryption
        phi = "Patient: John Doe, SSN: 123-45-6789"
        encrypted = hipaa.encrypt_phi(phi)
        decrypted = hipaa.decrypt_phi(encrypted)
        assert decrypted == phi

        # Test audit log integrity
        assert hipaa.verify_audit_log_integrity() is True

        print("    ✅ Integrated system works")
        self.tests_passed += 1

    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*80)
        print("HIPAA COMPLIANCE - COMPREHENSIVE TEST SUITE")
        print("="*80)

        tests = [
            ("Encryption System", self.test_encryption_system),
            ("MFA System", self.test_mfa_system),
            ("JWT Manager", self.test_jwt_manager),
            ("RBAC System", self.test_rbac_system),
            ("Audit Logging", self.test_audit_logging),
            ("Session Management", self.test_session_management),
            ("PHI Masking", self.test_phi_masking),
            ("Integrated System", self.test_integrated_system)
        ]

        for test_name, test_func in tests:
            self.tests_run += 1
            try:
                test_func()
            except Exception as e:
                print(f"    ❌ {test_name} FAILED: {e}")
                self.tests_failed += 1

        # Summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Total Tests:     {self.tests_run}")
        print(f"✅ Passed:       {self.tests_passed}")
        print(f"❌ Failed:       {self.tests_failed}")
        print(f"Success Rate:    {(self.tests_passed/self.tests_run)*100:.1f}%")
        print("="*80 + "\n")

        if self.tests_failed == 0:
            print("✅✅✅ ALL TESTS PASSED - 100% SUCCESS ✅✅✅\n")
            return 0
        else:
            print("❌ SOME TESTS FAILED\n")
            return 1


if __name__ == "__main__":
    tester = TestHIPAACompliance()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)
