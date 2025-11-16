#!/usr/bin/env python3
"""
Phase 19: Voice AI & Ambient Intelligence - Verification Script
Automated verification of all system components

Usage:
    python3 verify_phase19.py
    python3 verify_phase19.py --quick
    python3 verify_phase19.py --full
"""

import sys
import os
import json
import time
from datetime import datetime

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

try:
    from voice_ai_system import (
        VoiceAISystem, VoiceCommandProcessor, AmbientClinicalIntelligence,
        ClinicalNoteGenerator, VoiceDataSecurity, SpeakerRole
    )
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f"❌ Import Error: {e}")
    IMPORT_SUCCESS = False


class Phase19Verifier:
    """Comprehensive verification for Phase 19"""

    def __init__(self, quick_mode=False):
        self.quick_mode = quick_mode
        self.results = []
        self.start_time = time.time()

    def run_all_checks(self):
        """Run all verification checks"""
        print("="*80)
        print("PHASE 19: VOICE AI & AMBIENT INTELLIGENCE - VERIFICATION")
        print("="*80)
        print(f"Mode: {'Quick' if self.quick_mode else 'Full'}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        print()

        checks = [
            ("Module Import", self.check_module_import),
            ("Voice Command Processor", self.check_voice_processor),
            ("Ambient Intelligence", self.check_ambient_intelligence),
            ("Clinical Note Generator", self.check_note_generator),
            ("Voice Data Security", self.check_security),
            ("Integrated System", self.check_integrated_system),
        ]

        if not self.quick_mode:
            checks.extend([
                ("Performance Test", self.check_performance),
                ("HIPAA Compliance", self.check_hipaa_compliance),
            ])

        for check_name, check_func in checks:
            self._run_check(check_name, check_func)

        self._print_summary()
        return self._get_success_rate() == 100.0

    def _run_check(self, name, func):
        """Run a single check"""
        print(f"Running: {name}...", end=" ")
        sys.stdout.flush()

        start = time.time()
        try:
            result = func()
            duration = (time.time() - start) * 1000  # ms

            self.results.append({
                "name": name,
                "passed": result,
                "duration_ms": duration
            })

            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{status} ({duration:.2f}ms)")

        except Exception as e:
            duration = (time.time() - start) * 1000
            self.results.append({
                "name": name,
                "passed": False,
                "duration_ms": duration,
                "error": str(e)
            })
            print(f"❌ FAILED ({duration:.2f}ms) - {e}")

    def check_module_import(self):
        """Check if all modules import correctly"""
        return IMPORT_SUCCESS

    def check_voice_processor(self):
        """Check VoiceCommandProcessor functionality"""
        processor = VoiceCommandProcessor()

        # Test medication order
        cmd1 = processor.process_command("Prescribe amoxicillin 500mg three times daily")
        if cmd1.command_type.value != "medication":
            return False

        # Test clinical order
        cmd2 = processor.process_command("Order chest x-ray stat")
        if cmd2.command_type.value != "clinical_order":
            return False

        # Test vital signs
        cmd3 = processor.process_command("Record blood pressure 120 over 80")
        if cmd3.command_type.value != "vital_signs":
            return False

        # Test execution
        result = processor.execute_command(cmd1)
        if not result["success"]:
            return False

        return True

    def check_ambient_intelligence(self):
        """Check AmbientClinicalIntelligence functionality"""
        ambient = AmbientClinicalIntelligence()

        # Start session
        session = ambient.start_session("TEST_SESSION", "PT_TEST", "DR_TEST")
        if session["status"] != "active":
            return False

        # Transcribe segments
        seg1 = ambient.transcribe_segment(
            "TEST_SESSION",
            "I have chest pain and shortness of breath",
            SpeakerRole.PATIENT,
            3.0
        )
        if seg1.speaker != SpeakerRole.PATIENT:
            return False

        # Check medical entity extraction
        if len(seg1.medical_entities) == 0:
            return False

        # Get transcript
        transcript = ambient.get_session_transcript("TEST_SESSION")
        if transcript["total_segments"] != 1:
            return False

        # End session
        summary = ambient.end_session("TEST_SESSION")
        if summary["status"] != "completed":
            return False

        return True

    def check_note_generator(self):
        """Check ClinicalNoteGenerator functionality"""
        from voice_ai_system import TranscriptionSegment

        generator = ClinicalNoteGenerator()

        # Create sample segments
        segments = [
            TranscriptionSegment(
                segment_id="SEG_001",
                timestamp=datetime.now(),
                speaker=SpeakerRole.PATIENT,
                text="I have chest pain",
                confidence=0.95,
                duration_seconds=2.0,
                medical_entities=[]
            ),
            TranscriptionSegment(
                segment_id="SEG_002",
                timestamp=datetime.now(),
                speaker=SpeakerRole.PHYSICIAN,
                text="Assessment is angina, plan to order EKG",
                confidence=0.95,
                duration_seconds=3.0,
                medical_entities=[]
            )
        ]

        # Generate SOAP note
        note = generator.generate_soap_note(
            "PT_TEST", "DR_TEST", segments, "SESSION_TEST"
        )

        if note.note_type.value != "soap":
            return False

        if "subjective" not in note.content:
            return False

        # Test note retrieval
        retrieved = generator.get_note(note.note_id)
        if retrieved is None:
            return False

        return True

    def check_security(self):
        """Check VoiceDataSecurity functionality"""
        security = VoiceDataSecurity()

        # Test encryption
        audio_data = b"test audio data"
        enc_result = security.encrypt_audio_data(audio_data, "PT_TEST", "DR_TEST")
        if not enc_result["encrypted"]:
            return False

        # Test audit logging
        log = security.log_voice_access("DR_TEST", "PT_TEST", "transcribe", "hash123")
        if log.user_id != "DR_TEST":
            return False

        # Test audit trail retrieval
        trail = security.get_audit_trail(patient_id="PT_TEST")
        if len(trail) == 0:
            return False

        # Test de-identification
        text = "Patient John Smith, born 05/15/1965"
        deidentified = security.de_identify_transcript(text)
        if "John Smith" in deidentified:
            return False
        if "[NAME]" not in deidentified:
            return False

        return True

    def check_integrated_system(self):
        """Check integrated VoiceAISystem"""
        system = VoiceAISystem()

        # Test voice command processing
        result = system.process_voice_command("Order chest x-ray", "DR_TEST")
        if not result["execution_result"]["success"]:
            return False

        # Test clinical encounter
        conversation = [
            ("I have chest pain", SpeakerRole.PATIENT, 2.0),
            ("Blood pressure 120 over 80", SpeakerRole.PHYSICIAN, 2.0),
            ("Plan to order EKG", SpeakerRole.PHYSICIAN, 2.0)
        ]

        encounter = system.conduct_clinical_encounter(
            "SESSION_TEST", "PT_TEST", "DR_TEST", conversation
        )

        if encounter["session"]["status"] != "completed":
            return False

        if encounter["soap_note"]["note_type"] != "soap":
            return False

        # Test stats
        stats = system.get_system_stats()
        if "commands_processed" not in stats:
            return False

        return True

    def check_performance(self):
        """Check system performance"""
        system = VoiceAISystem()

        # Test command processing speed
        start = time.time()
        for _ in range(10):
            system.process_voice_command("Order chest x-ray", "DR_TEST")
        duration = time.time() - start

        avg_time = duration / 10
        if avg_time > 0.1:  # Should be under 100ms per command
            print(f"\n   Warning: Slow performance ({avg_time*1000:.2f}ms per command)")
            return False

        return True

    def check_hipaa_compliance(self):
        """Check HIPAA compliance features"""
        security = VoiceDataSecurity()

        # Test encryption
        enc = security.encrypt_audio_data(b"test", "PT_TEST", "DR_TEST")
        if enc["encryption_method"] != "AES-256":
            return False

        # Test audit logging
        log = security.log_voice_access("DR_TEST", "PT_TEST", "test", "hash")
        if log.encryption_status != "encrypted":
            return False

        # Test retention policy (7 years)
        days_to_expiry = (log.retention_expires - datetime.now()).days
        if days_to_expiry < 2554:  # 7 years = 2555 days
            return False

        return True

    def _print_summary(self):
        """Print verification summary"""
        print()
        print("="*80)
        print("VERIFICATION SUMMARY")
        print("="*80)

        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        failed = total - passed
        success_rate = (passed / total * 100) if total > 0 else 0

        print(f"Total Checks: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print()

        if failed > 0:
            print("Failed Checks:")
            for result in self.results:
                if not result["passed"]:
                    error = result.get("error", "Unknown error")
                    print(f"  ❌ {result['name']}: {error}")
            print()

        total_duration = (time.time() - self.start_time) * 1000
        print(f"Total Duration: {total_duration:.2f}ms")
        print()

        if failed == 0:
            print("✅ ALL VERIFICATIONS PASSED - SYSTEM READY")
        else:
            print("❌ VERIFICATION FAILED - FIX ERRORS ABOVE")

        print("="*80)

    def _get_success_rate(self):
        """Get success rate percentage"""
        if not self.results:
            return 0.0
        passed = sum(1 for r in self.results if r["passed"])
        return (passed / len(self.results)) * 100

    def save_results(self, filename="verification_report.json"):
        """Save results to JSON file"""
        report = {
            "verification_time": datetime.now().isoformat(),
            "total_checks": len(self.results),
            "passed": sum(1 for r in self.results if r["passed"]),
            "failed": sum(1 for r in self.results if not r["passed"]),
            "success_rate": self._get_success_rate(),
            "total_duration_ms": (time.time() - self.start_time) * 1000,
            "checks": self.results,
            "status": "PASSED" if self._get_success_rate() == 100.0 else "FAILED"
        }

        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\nResults saved to: {filepath}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Verify Phase 19: Voice AI & Ambient Intelligence")
    parser.add_argument("--quick", action="store_true", help="Run quick verification (skip performance tests)")
    parser.add_argument("--full", action="store_true", help="Run full verification")
    parser.add_argument("--save", action="store_true", help="Save results to JSON")

    args = parser.parse_args()

    quick_mode = args.quick or not args.full

    verifier = Phase19Verifier(quick_mode=quick_mode)
    success = verifier.run_all_checks()

    if args.save:
        verifier.save_results()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
