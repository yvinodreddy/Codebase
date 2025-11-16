#!/usr/bin/env python3
"""Sample: Trial Creation"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from trial_lifecycle_core import ClinicalTrialLifecycleSystem, TrialPhase

system = ClinicalTrialLifecycleSystem()

trial = system.create_trial(
    trial_number="NCT12345678",
    title="Hypertension Treatment Study",
    phase=TrialPhase.PHASE_III,
    sponsor="Pharma Corp",
    pi="Dr. Jane Smith",
    protocol_version="v1.0",
    target_enrollment=100
)

print(f"✅ Trial created: {trial.trial_number}")
print(f"   Phase: {trial.phase.value}")
print(f"   Target enrollment: {trial.target_enrollment}")
