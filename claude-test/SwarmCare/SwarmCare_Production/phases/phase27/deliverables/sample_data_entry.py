#!/usr/bin/env python3
"""Sample: Data Entry"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from trial_lifecycle_core import ClinicalTrialLifecycleSystem, TrialPhase

system = ClinicalTrialLifecycleSystem()
trial = system.create_trial("NCT12345678", "Test", TrialPhase.PHASE_II, "Sponsor", "PI", "v1.0", 10)
participant = system.enroll_participant(trial.trial_id, "SITE001", "SCR001", {"age": 55})

crf_entries = system.enter_visit_data(
    trial.trial_id, participant.participant_id, "V1",
    {
        "Vitals": {
            "weight": 75.5,
            "height": 175,
            "blood_pressure_systolic": 120,
            "blood_pressure_diastolic": 80
        }
    },
    "site_coordinator"
)

print(f"✅ Visit data entered")
print(f"   Data points: {len(crf_entries)}")
print(f"   Visit: V1")
