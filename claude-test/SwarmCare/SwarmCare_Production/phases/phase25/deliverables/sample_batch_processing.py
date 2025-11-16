#!/usr/bin/env python3
"""
Sample: Batch Processing
Demonstrates efficient batch processing of multiple patient explanations
"""

import sys
import os
import time

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from patient_facing_xai_core import (
    PatientFacingXAIPipeline,
    create_patient_profile,
    create_medical_concept,
    ExplanationType
)


def main():
    print("=" * 80)
    print("SAMPLE: BATCH PROCESSING")
    print("=" * 80)
    print()

    pipeline = PatientFacingXAIPipeline()

    # Create batch of patients and concepts
    patients_concepts = [
        (
            create_patient_profile("P001", 45, "High School"),
            create_medical_concept(
                ExplanationType.DIAGNOSIS,
                "Hypertension",
                {"condition": "Hypertension", "simple_description": "high blood pressure"}
            )
        ),
        (
            create_patient_profile("P002", 55, "Middle School"),
            create_medical_concept(
                ExplanationType.MEDICATION,
                "Metformin",
                {"medication": "Metformin", "purpose": "lower blood sugar"}
            )
        ),
        (
            create_patient_profile("P003", 35, "Bachelor's Degree"),
            create_medical_concept(
                ExplanationType.TEST_RESULT,
                "HbA1c",
                {"test": "HbA1c", "result": "7.2%"}
            )
        ),
        (
            create_patient_profile("P004", 65, "High School"),
            create_medical_concept(
                ExplanationType.DIAGNOSIS,
                "Diabetes Mellitus",
                {"condition": "Diabetes", "simple_description": "high blood sugar"}
            )
        ),
        (
            create_patient_profile("P005", 50, "Master's Degree"),
            create_medical_concept(
                ExplanationType.MEDICATION,
                "Lisinopril",
                {"medication": "Lisinopril", "purpose": "lower blood pressure"}
            )
        )
    ]

    print(f"Processing {len(patients_concepts)} patients...")
    print()

    # Batch process
    start_time = time.time()
    results = pipeline.batch_generate_explanations(patients_concepts)
    duration = time.time() - start_time

    # Display results
    print("-" * 80)
    for i, result in enumerate(results, 1):
        print(f"Patient {i}:")
        print(f"  Literacy: {result['explanation']['literacy_level']}")
        print(f"  Type: {result['explanation']['concept_type']}")
        print(f"  Validated: {'✅' if result['validation']['overall_passed'] else '❌'}")
        print(f"  Portal Ready: {'✅' if result['portal_ready'] else '❌'}")
    print("-" * 80)

    print()
    print("Performance:")
    print(f"  Total time: {duration*1000:.1f}ms")
    print(f"  Avg per patient: {duration*1000/len(results):.1f}ms")
    print()

    stats = pipeline.get_statistics()
    print("Statistics:")
    print(f"  Total explanations: {stats['total_explanations']}")
    print(f"  Validation pass rate: {stats['validation_pass_rate']:.1f}%")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
