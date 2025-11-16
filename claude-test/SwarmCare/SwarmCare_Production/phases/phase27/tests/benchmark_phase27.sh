#!/bin/bash
# Phase 27 Performance Benchmarks

echo "================================================================================"
echo "PHASE 27: CLINICAL TRIAL LIFECYCLE PERFORMANCE BENCHMARKS"
echo "================================================================================"
echo

PHASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PHASE_DIR/tests"

# Benchmark 1: Trial Creation
echo "[Benchmark 1: Trial Creation]"
echo "Target: < 10ms"
START=$(python3 -c 'import time; print(int(time.time() * 1000))')
python3 -c "
import sys, os
sys.path.insert(0, '../code')
from trial_lifecycle_core import TrialManagementSystem, TrialPhase
system = TrialManagementSystem()
trial = system.create_trial('NCT12345678', 'Test', TrialPhase.PHASE_II, 'Sponsor', 'PI', 'v1.0', 100)
" 2>/dev/null
END=$(python3 -c 'import time; print(int(time.time() * 1000))')
DURATION=$((END - START))
echo "Duration: ${DURATION}ms"
if [ $DURATION -lt 10 ]; then
    echo "✅ PASSED (within target)"
else
    echo "⚠️  EXCEEDED TARGET"
fi
echo

# Benchmark 2: Participant Enrollment
echo "[Benchmark 2: Participant Enrollment]"
echo "Target: < 20ms"
START=$(python3 -c 'import time; print(int(time.time() * 1000))')
python3 -c "
import sys, os
sys.path.insert(0, '../code')
from trial_lifecycle_core import ClinicalTrialLifecycleSystem, TrialPhase
system = ClinicalTrialLifecycleSystem()
trial = system.create_trial('NCT12345678', 'Test', TrialPhase.PHASE_II, 'Sponsor', 'PI', 'v1.0', 100)
participant = system.enroll_participant(trial.trial_id, 'SITE001', 'SCR001', {'age': 45})
" 2>/dev/null
END=$(python3 -c 'import time; print(int(time.time() * 1000))')
DURATION=$((END - START))
echo "Duration: ${DURATION}ms"
if [ $DURATION -lt 20 ]; then
    echo "✅ PASSED (within target)"
else
    echo "⚠️  EXCEEDED TARGET"
fi
echo

# Benchmark 3: Consent Processing
echo "[Benchmark 3: Consent Processing]"
echo "Target: < 50ms"
START=$(python3 -c 'import time; print(int(time.time() * 1000))')
python3 -c "
import sys, os
sys.path.insert(0, '../code')
from trial_lifecycle_core import ClinicalTrialLifecycleSystem, TrialPhase
system = ClinicalTrialLifecycleSystem()
trial = system.create_trial('NCT12345678', 'Test', TrialPhase.PHASE_II, 'Sponsor', 'PI', 'v1.0', 100)
participant = system.enroll_participant(trial.trial_id, 'SITE001', 'SCR001', {'age': 45})
result = system.process_consent(participant.participant_id, 'Signature', {
    'purpose': 'To test treatment for medical condition',
    'voluntary': 'Yes I understand participation is voluntary',
    'risks': 'Possible side effects include headache and nausea',
    'benefits': 'May improve health outcomes',
    'confidentiality': 'Information kept private per regulations'
})
" 2>/dev/null
END=$(python3 -c 'import time; print(int(time.time() * 1000))')
DURATION=$((END - START))
echo "Duration: ${DURATION}ms"
if [ $DURATION -lt 50 ]; then
    echo "✅ PASSED (within target)"
else
    echo "⚠️  EXCEEDED TARGET"
fi
echo

# Benchmark 4: Data Entry
echo "[Benchmark 4: EDC Data Entry]"
echo "Target: < 30ms"
START=$(python3 -c 'import time; print(int(time.time() * 1000))')
python3 -c "
import sys, os
sys.path.insert(0, '../code')
from trial_lifecycle_core import ElectronicDataCaptureSystem
system = ElectronicDataCaptureSystem()
data = system.enter_data('trial123', 'participant456', 'V1', 'Vitals', 'weight', 75, 'user1')
" 2>/dev/null
END=$(python3 -c 'import time; print(int(time.time() * 1000))')
DURATION=$((END - START))
echo "Duration: ${DURATION}ms"
if [ $DURATION -lt 30 ]; then
    echo "✅ PASSED (within target)"
else
    echo "⚠️  EXCEEDED TARGET"
fi
echo

# Benchmark 5: Dashboard Generation
echo "[Benchmark 5: Trial Dashboard Generation]"
echo "Target: < 100ms"
START=$(python3 -c 'import time; print(int(time.time() * 1000))')
python3 -c "
import sys, os
sys.path.insert(0, '../code')
from trial_lifecycle_core import ClinicalTrialLifecycleSystem, TrialPhase
system = ClinicalTrialLifecycleSystem()
trial = system.create_trial('NCT12345678', 'Test', TrialPhase.PHASE_II, 'Sponsor', 'PI', 'v1.0', 100)
for i in range(5):
    participant = system.enroll_participant(trial.trial_id, 'SITE001', f'SCR00{i}', {'age': 45})
dashboard = system.generate_trial_dashboard(trial.trial_id)
" 2>/dev/null
END=$(python3 -c 'import time; print(int(time.time() * 1000))')
DURATION=$((END - START))
echo "Duration: ${DURATION}ms"
if [ $DURATION -lt 100 ]; then
    echo "✅ PASSED (within target)"
else
    echo "⚠️  EXCEEDED TARGET"
fi
echo

# Benchmark 6: Batch Operations
echo "[Benchmark 6: Batch Operations (10 participants)]"
echo "Target: < 200ms"
START=$(python3 -c 'import time; print(int(time.time() * 1000))')
python3 -c "
import sys, os
sys.path.insert(0, '../code')
from trial_lifecycle_core import ClinicalTrialLifecycleSystem, TrialPhase
system = ClinicalTrialLifecycleSystem()
trial = system.create_trial('NCT12345678', 'Test', TrialPhase.PHASE_II, 'Sponsor', 'PI', 'v1.0', 100)
for i in range(10):
    participant = system.enroll_participant(trial.trial_id, 'SITE001', f'SCR{i:03d}', {'age': 45})
" 2>/dev/null
END=$(python3 -c 'import time; print(int(time.time() * 1000))')
DURATION=$((END - START))
echo "Duration: ${DURATION}ms"
if [ $DURATION -lt 200 ]; then
    echo "✅ PASSED (within target)"
else
    echo "⚠️  EXCEEDED TARGET"
fi
echo

echo "================================================================================"
echo "BENCHMARK SUMMARY: All benchmarks completed"
echo "================================================================================"
