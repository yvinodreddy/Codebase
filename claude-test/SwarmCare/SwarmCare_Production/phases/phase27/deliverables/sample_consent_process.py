#!/usr/bin/env python3
"""Sample: Consent Processing"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from trial_lifecycle_core import ClinicalTrialLifecycleSystem, TrialPhase

system = ClinicalTrialLifecycleSystem()
trial = system.create_trial("NCT12345678", "Test", TrialPhase.PHASE_II, "Sponsor", "PI", "v1.0", 10)
participant = system.enroll_participant(trial.trial_id, "SITE001", "SCR001", {"age": 55})

result = system.process_consent(
    participant.participant_id, "Signature Data",
    {
        "purpose": "To evaluate new treatment for condition",
        "voluntary": "Yes, participation is voluntary",
        "risks": "Possible side effects include headache",
        "benefits": "May improve health outcomes",
        "confidentiality": "Information kept private"
    }
)

if result["success"]:
    print("✅ Consent signed successfully")
    print(f"   Comprehension: {result['comprehension']['pass_rate']*100:.0f}% pass rate")
