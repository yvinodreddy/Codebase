#!/usr/bin/env python3
"""Sample: Adverse Event Reporting"""
import sys, os
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from trial_lifecycle_core import ClinicalTrialLifecycleSystem, TrialPhase, AESeverity, AECausality

system = ClinicalTrialLifecycleSystem()
trial = system.create_trial("NCT12345678", "Test", TrialPhase.PHASE_II, "Sponsor", "PI", "v1.0", 10)
participant = system.enroll_participant(trial.trial_id, "SITE001", "SCR001", {"age": 55})

ae = system.report_adverse_event(
    trial.trial_id, participant.participant_id, "SITE001",
    "Headache", "Mild headache", AESeverity.GRADE_1,
    AECausality.POSSIBLE, datetime.now()
)

print(f"✅ Adverse event reported")
print(f"   Severity: {ae.severity.value}")
print(f"   Serious: {'Yes' if ae.serious else 'No'}")
