#!/bin/bash

################################################################################
# Phase 25: Performance Benchmarks
################################################################################
#
# Measures performance of key operations:
# 1. Health literacy assessment
# 2. Explanation generation
# 3. Validation
# 4. Portal delivery
# 5. End-to-end pipeline
# 6. Batch processing
#
# Performance Targets:
# - Literacy assessment: < 10ms
# - Explanation generation: < 100ms
# - Validation: < 50ms
# - Portal delivery: < 50ms
# - End-to-end: < 200ms
# - Batch (10 patients): < 1000ms
#
################################################################################

set -e

cd "$(dirname "$0")"

echo "================================================================================"
echo "PHASE 25: PERFORMANCE BENCHMARKS"
echo "================================================================================"
echo "Started: $(date)"
echo "================================================================================"
echo ""

PYTHON_CMD="python3"

# Create benchmark script
cat > /tmp/phase25_benchmark.py << 'EOF'
import sys
import os
import time
from statistics import mean, stdev

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))
sys.path.insert(0, '../code')

from patient_facing_xai_core import (
    PatientFacingXAIPipeline,
    HealthLiteracyAssessment,
    ExplanationGenerator,
    ExplanationValidator,
    PatientPortalIntegration,
    ExplanationType,
    create_patient_profile,
    create_medical_concept
)

def benchmark(name, func, iterations=10, target_ms=None):
    """Benchmark a function"""
    times = []
    for _ in range(iterations):
        start = time.time()
        func()
        duration = (time.time() - start) * 1000
        times.append(duration)

    avg = mean(times)
    std = stdev(times) if len(times) > 1 else 0

    status = "✅" if (target_ms is None or avg < target_ms) else "❌"
    target_str = f" (target: <{target_ms}ms)" if target_ms else ""

    print(f"{status} {name}:")
    print(f"   Average: {avg:.2f}ms{target_str}")
    print(f"   Std Dev: {std:.2f}ms")
    print(f"   Min/Max: {min(times):.2f}ms / {max(times):.2f}ms")
    print()

    return avg < target_ms if target_ms else True

# Setup
patient = create_patient_profile("BENCH001", 45, "High School")
concept = create_medical_concept(
    ExplanationType.DIAGNOSIS,
    "Hypertension",
    {
        "condition": "Hypertension",
        "simple_description": "high blood pressure",
        "why_important": "can damage your heart"
    }
)

print("=" * 80)
print("BENCHMARK 1: Health Literacy Assessment")
print("-" * 80)

assessor = HealthLiteracyAssessment()
b1 = benchmark(
    "Literacy assessment from demographics",
    lambda: assessor.assess_from_demographics("High School", 45),
    iterations=100,
    target_ms=10
)

print("=" * 80)
print("BENCHMARK 2: Explanation Generation")
print("-" * 80)

generator = ExplanationGenerator()
b2 = benchmark(
    "Generate patient explanation",
    lambda: generator.generate_explanation(concept, patient),
    iterations=50,
    target_ms=100
)

print("=" * 80)
print("BENCHMARK 3: Validation")
print("-" * 80)

validator = ExplanationValidator()
explanation = generator.generate_explanation(concept, patient)
b3 = benchmark(
    "Validate explanation",
    lambda: validator.validate_explanation(explanation),
    iterations=50,
    target_ms=50
)

print("=" * 80)
print("BENCHMARK 4: Portal Delivery")
print("-" * 80)

portal = PatientPortalIntegration()
b4 = benchmark(
    "Prepare for portal",
    lambda: portal.prepare_for_portal(explanation, patient),
    iterations=50,
    target_ms=50
)

print("=" * 80)
print("BENCHMARK 5: End-to-End Pipeline")
print("-" * 80)

pipeline = PatientFacingXAIPipeline()
b5 = benchmark(
    "Complete patient explanation pipeline",
    lambda: pipeline.generate_patient_explanation(patient, concept, validate=True, deliver_to_portal=True),
    iterations=20,
    target_ms=200
)

print("=" * 80)
print("BENCHMARK 6: Batch Processing")
print("-" * 80)

patients_concepts = [
    (
        create_patient_profile(f"BATCH{i:03d}", 40 + i, "High School"),
        create_medical_concept(ExplanationType.DIAGNOSIS, "Test", {"condition": "Test", "simple_description": "test"})
    )
    for i in range(10)
]

b6 = benchmark(
    "Batch process 10 patients",
    lambda: pipeline.batch_generate_explanations(patients_concepts),
    iterations=5,
    target_ms=1000
)

print("=" * 80)
print("BENCHMARK SUMMARY")
print("=" * 80)

results = [
    ("Health Literacy Assessment", b1),
    ("Explanation Generation", b2),
    ("Validation", b3),
    ("Portal Delivery", b4),
    ("End-to-End Pipeline", b5),
    ("Batch Processing (10 patients)", b6)
]

passed = sum(1 for _, result in results if result)
total = len(results)

print(f"Passed: {passed}/{total}")
print(f"Success Rate: {(passed/total*100):.1f}%")
print()

if passed == total:
    print("✅ ALL BENCHMARKS PASSED")
    sys.exit(0)
else:
    print("❌ SOME BENCHMARKS FAILED")
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    sys.exit(1)

EOF

# Run benchmarks
$PYTHON_CMD /tmp/phase25_benchmark.py
EXIT_CODE=$?

echo ""
echo "================================================================================"
echo "BENCHMARKS COMPLETED: $(date)"
echo "================================================================================"

exit $EXIT_CODE
