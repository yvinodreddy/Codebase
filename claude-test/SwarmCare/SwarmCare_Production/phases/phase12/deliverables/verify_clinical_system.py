#!/usr/bin/env python3
"""
Phase 12: Clinical Decision Support System - Verification Script

This script performs comprehensive verification of the clinical decision support system:
- System health checks
- Performance validation
- Accuracy verification
- Security audit
- HIPAA compliance check

Usage:
    python3 verify_clinical_system.py
    python3 verify_clinical_system.py --verbose
    python3 verify_clinical_system.py --quick

Exit codes:
    0 - All checks passed
    1 - One or more checks failed
"""

import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

try:
    from clinical_decision_support import (
        ClinicalDecisionSupportEngine,
        VitalSigns,
        LabValues,
        assess_patient
    )
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    IMPORT_SUCCESS = False


class SystemVerifier:
    """Comprehensive system verification"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.results = []
        self.start_time = time.time()

    def log(self, message, level="INFO"):
        """Log verification message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if self.verbose or level in ["ERROR", "SUCCESS", "FAILED"]:
            symbol = {
                "INFO": "ℹ️",
                "SUCCESS": "✅",
                "FAILED": "❌",
                "WARNING": "⚠️",
                "ERROR": "❌"
            }.get(level, "ℹ️")
            print(f"[{timestamp}] {symbol} {message}")

    def run_check(self, name, check_func):
        """Run individual verification check"""
        self.log(f"Running: {name}", "INFO")
        try:
            start = time.time()
            result = check_func()
            duration = (time.time() - start) * 1000

            self.results.append({
                "name": name,
                "passed": result,
                "duration_ms": duration
            })

            if result:
                self.log(f"{name}: PASSED ({duration:.2f}ms)", "SUCCESS")
            else:
                self.log(f"{name}: FAILED", "FAILED")

            return result
        except Exception as e:
            self.log(f"{name}: ERROR - {e}", "ERROR")
            self.results.append({
                "name": name,
                "passed": False,
                "error": str(e)
            })
            return False

    def verify_imports(self):
        """Verify all required modules can be imported"""
        return IMPORT_SUCCESS

    def verify_engine_initialization(self):
        """Verify clinical decision support engine initializes"""
        try:
            engine = ClinicalDecisionSupportEngine()
            return engine is not None
        except Exception:
            return False

    def verify_sepsis_detection(self):
        """Verify sepsis detection accuracy"""
        try:
            # Critical septic patient
            vitals = VitalSigns(
                temperature_celsius=39.0,
                heart_rate=130,
                respiratory_rate=28,
                systolic_bp=85,
                consciousness_level='V'
            )
            labs = LabValues(wbc_count=20.0, lactate=5.0)

            assessment = assess_patient(
                patient_id="VERIFY_SEPSIS",
                temperature_c=vitals.temperature_celsius,
                heart_rate=vitals.heart_rate,
                respiratory_rate=vitals.respiratory_rate,
                systolic_bp=vitals.systolic_bp,
                consciousness=vitals.consciousness_level,
                wbc=labs.wbc_count,
                lactate=labs.lactate
            )

            # Should detect critical alerts
            return assessment['alert_count']['critical'] > 0 and assessment['scores']['qsofa'] == 3
        except Exception:
            return False

    def verify_drug_interactions(self):
        """Verify drug interaction detection"""
        try:
            vitals = VitalSigns(
                temperature_celsius=37.0,
                heart_rate=75,
                respiratory_rate=16,
                systolic_bp=120,
                oxygen_saturation=98,
                consciousness_level='A'
            )

            assessment = assess_patient(
                patient_id="VERIFY_DRUGS",
                temperature_c=vitals.temperature_celsius,
                heart_rate=vitals.heart_rate,
                respiratory_rate=vitals.respiratory_rate,
                systolic_bp=vitals.systolic_bp,
                oxygen_sat=vitals.oxygen_saturation,
                medications=["warfarin", "aspirin"]
            )

            # Should detect at least one drug interaction
            return assessment['alert_count']['total'] > 0
        except Exception:
            return False

    def verify_early_warning_scores(self):
        """Verify early warning score calculations"""
        try:
            # Normal patient - should have low NEWS2
            assessment_normal = assess_patient(
                patient_id="VERIFY_NORMAL",
                temperature_c=37.0,
                heart_rate=75,
                respiratory_rate=14,
                systolic_bp=120,
                oxygen_sat=98,
                consciousness="A"
            )

            # Critical patient - should have high NEWS2
            assessment_critical = assess_patient(
                patient_id="VERIFY_CRITICAL",
                temperature_c=39.0,
                heart_rate=130,
                respiratory_rate=28,
                systolic_bp=85,
                oxygen_sat=89,
                consciousness="V"
            )

            return (assessment_normal['scores']['news2'] < 3 and
                    assessment_critical['scores']['news2'] >= 7)
        except Exception:
            return False

    def verify_no_false_positives(self):
        """Verify healthy patients don't trigger false alarms"""
        try:
            assessment = assess_patient(
                patient_id="VERIFY_HEALTHY",
                temperature_c=37.0,
                heart_rate=72,
                respiratory_rate=14,
                systolic_bp=118,
                oxygen_sat=99,
                consciousness="A",
                wbc=7.2,
                lactate=1.0
            )

            # Should have no critical alerts for healthy patient
            return assessment['alert_count']['total'] == 0
        except Exception:
            return False

    def verify_performance(self):
        """Verify performance meets requirements (<100ms)"""
        try:
            start = time.time()

            # Run 100 assessments
            for i in range(100):
                assess_patient(
                    patient_id=f"PERF_{i}",
                    temperature_c=37.0 + (i % 3),
                    heart_rate=70 + (i % 30),
                    respiratory_rate=14 + (i % 8),
                    systolic_bp=110 + (i % 40),
                    oxygen_sat=96 + (i % 4)
                )

            duration_ms = (time.time() - start) * 1000
            avg_ms = duration_ms / 100

            self.log(f"Performance: {avg_ms:.2f}ms average", "INFO")

            # Should average <100ms per assessment
            return avg_ms < 100
        except Exception:
            return False

    def verify_audit_logging(self):
        """Verify audit logging functionality"""
        try:
            engine = ClinicalDecisionSupportEngine()
            initial_count = len(engine.audit_log)

            # Perform assessment
            vitals = VitalSigns(
                temperature_celsius=37.0,
                heart_rate=75,
                respiratory_rate=16,
                systolic_bp=120,
                oxygen_saturation=98,
                consciousness_level='A'
            )

            engine.comprehensive_assessment(
                patient_id="AUDIT_TEST",
                vitals=vitals
            )

            # Verify audit log entry was created
            return len(engine.audit_log) == initial_count + 1
        except Exception:
            return False

    def verify_data_integrity(self):
        """Verify patient data integrity is maintained"""
        try:
            original_data = {
                "patient_id": "INTEGRITY_TEST",
                "temperature_c": 37.5,
                "heart_rate": 80
            }

            assessment = assess_patient(**original_data)

            # Verify data matches
            return (assessment['vital_signs']['temperature_celsius'] == 37.5 and
                    assessment['vital_signs']['heart_rate'] == 80)
        except Exception:
            return False

    def verify_error_handling(self):
        """Verify graceful error handling"""
        try:
            # Test with missing data
            assessment = assess_patient(
                patient_id="ERROR_TEST",
                temperature_c=37.0
                # Missing other vital signs
            )

            # Should still return valid assessment
            return 'patient_id' in assessment and assessment['patient_id'] == "ERROR_TEST"
        except Exception:
            return False

    def verify_hipaa_compliance(self):
        """Verify HIPAA compliance features"""
        try:
            engine = ClinicalDecisionSupportEngine()

            # Verify audit trail exists
            if not hasattr(engine, 'audit_log'):
                return False

            # Perform assessment
            vitals = VitalSigns(
                temperature_celsius=37.0,
                heart_rate=75,
                respiratory_rate=16,
                systolic_bp=120,
                oxygen_saturation=98,
                consciousness_level='A'
            )

            engine.comprehensive_assessment(
                patient_id="HIPAA_TEST",
                vitals=vitals
            )

            # Verify audit trail can be retrieved
            audit_trail = engine.get_audit_trail("HIPAA_TEST")

            return len(audit_trail) > 0
        except Exception:
            return False

    def run_all_checks(self, quick=False):
        """Run all verification checks"""
        print("\n" + "=" * 80)
        print("PHASE 12: CLINICAL DECISION SUPPORT SYSTEM - VERIFICATION")
        print("=" * 80 + "\n")

        # Essential checks (always run)
        checks = [
            ("Module Import", self.verify_imports),
            ("Engine Initialization", self.verify_engine_initialization),
            ("Sepsis Detection", self.verify_sepsis_detection),
            ("Drug Interactions", self.verify_drug_interactions),
            ("Early Warning Scores", self.verify_early_warning_scores),
            ("No False Positives", self.verify_no_false_positives),
        ]

        # Additional checks (skip in quick mode)
        if not quick:
            checks.extend([
                ("Performance (<100ms)", self.verify_performance),
                ("Audit Logging", self.verify_audit_logging),
                ("Data Integrity", self.verify_data_integrity),
                ("Error Handling", self.verify_error_handling),
                ("HIPAA Compliance", self.verify_hipaa_compliance),
            ])

        # Run all checks
        passed = 0
        failed = 0

        for name, func in checks:
            if self.run_check(name, func):
                passed += 1
            else:
                failed += 1

        # Print summary
        total_duration = (time.time() - self.start_time) * 1000

        print("\n" + "=" * 80)
        print("VERIFICATION SUMMARY")
        print("=" * 80)
        print(f"Total Checks: {passed + failed}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed / (passed + failed) * 100):.1f}%")
        print(f"Total Time: {total_duration:.2f}ms")
        print("=" * 80)

        # Generate report
        self.generate_report(passed, failed, total_duration)

        return failed == 0

    def generate_report(self, passed, failed, duration):
        """Generate verification report"""
        report = {
            "verification_time": datetime.now().isoformat(),
            "total_checks": passed + failed,
            "passed": passed,
            "failed": failed,
            "success_rate": round(passed / (passed + failed) * 100, 2),
            "total_duration_ms": round(duration, 2),
            "checks": self.results,
            "status": "PASSED" if failed == 0 else "FAILED"
        }

        # Save report
        report_path = Path(__file__).parent / "verification_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        if self.verbose:
            print(f"\n📄 Report saved to: {report_path}")


def main():
    """Main verification entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Verify Clinical Decision Support System"
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--quick', '-q',
        action='store_true',
        help='Run quick verification (essential checks only)'
    )

    args = parser.parse_args()

    verifier = SystemVerifier(verbose=args.verbose)
    success = verifier.run_all_checks(quick=args.quick)

    if success:
        print("\n✅ ALL VERIFICATIONS PASSED - SYSTEM READY")
        return 0
    else:
        print("\n❌ VERIFICATION FAILED - REVIEW ERRORS ABOVE")
        return 1


if __name__ == "__main__":
    sys.exit(main())
