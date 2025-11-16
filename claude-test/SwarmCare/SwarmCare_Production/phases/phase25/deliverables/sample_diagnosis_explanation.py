#!/usr/bin/env python3
"""
Sample: Diagnosis Explanation Generation
Demonstrates how to generate patient-facing explanations for medical diagnoses
"""

import sys
import os

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
    print("SAMPLE: DIAGNOSIS EXPLANATION GENERATION")
    print("=" * 80)
    print()

    # Initialize pipeline
    pipeline = PatientFacingXAIPipeline()
    print("✅ Pipeline initialized")
    print()

    # Example 1: Hypertension for patient with high school education
    print("-" * 80)
    print("Example 1: Hypertension (Intermediate Literacy Level)")
    print("-" * 80)

    patient1 = create_patient_profile(
        patient_id="P001",
        age=55,
        education_level="High School"
    )

    concept1 = create_medical_concept(
        concept_type=ExplanationType.DIAGNOSIS,
        technical_term="Hypertension",
        context={
            "condition": "Hypertension",
            "simple_description": "your blood pressure is too high",
            "why_important": "it can damage your heart and blood vessels over time"
        }
    )

    result1 = pipeline.generate_patient_explanation(
        patient1, concept1, validate=True, deliver_to_portal=True
    )

    print(f"Patient: {patient1.patient_id}")
    print(f"Literacy Level: {result1['explanation']['literacy_level']}")
    print(f"Validation: {'✅ PASSED' if result1['validation']['overall_passed'] else '❌ FAILED'}")
    print()
    print("Explanation:")
    print(result1['explanation']['primary_text'])
    print()
    if result1['explanation']['analogy']:
        print("Analogy:")
        print(result1['explanation']['analogy'])
        print()
    print(f"Key Points ({len(result1['explanation']['key_points'])}):")
    for i, point in enumerate(result1['explanation']['key_points'][:3], 1):
        print(f"  {i}. {point}")
    print()

    # Example 2: Diabetes for patient with college education
    print("-" * 80)
    print("Example 2: Diabetes (Advanced Literacy Level)")
    print("-" * 80)

    patient2 = create_patient_profile(
        patient_id="P002",
        age=45,
        education_level="Bachelor's Degree"
    )

    concept2 = create_medical_concept(
        concept_type=ExplanationType.DIAGNOSIS,
        technical_term="Diabetes Mellitus Type 2",
        context={
            "condition": "Type 2 Diabetes Mellitus",
            "mechanism": "insulin resistance and beta-cell dysfunction",
            "prognosis": "manageable with lifestyle changes and medication",
            "treatment_overview": "metformin therapy, diet modification, exercise"
        }
    )

    result2 = pipeline.generate_patient_explanation(
        patient2, concept2, validate=True, deliver_to_portal=True
    )

    print(f"Patient: {patient2.patient_id}")
    print(f"Literacy Level: {result2['explanation']['literacy_level']}")
    print(f"Validation: {'✅ PASSED' if result2['validation']['overall_passed'] else '❌ FAILED'}")
    print()
    print("Explanation:")
    print(result2['explanation']['primary_text'])
    print()
    print("Portal Ready:", "✅ YES" if result2['portal_ready'] else "❌ NO")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    stats = pipeline.get_statistics()
    print(f"Total Explanations: {stats['total_explanations']}")
    print(f"Validations Passed: {stats['validations_passed']}")
    print(f"Success Rate: {stats['validation_pass_rate']:.1f}%")
    print(f"Portal Deliveries: {stats['portal_deliveries']}")
    print()
    print("✅ Sample completed successfully")
    print("=" * 80)


if __name__ == "__main__":
    main()
