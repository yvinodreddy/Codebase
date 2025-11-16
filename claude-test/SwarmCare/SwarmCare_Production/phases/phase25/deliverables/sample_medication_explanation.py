#!/usr/bin/env python3
"""
Sample: Medication Explanation Generation
Demonstrates medication instructions adapted to health literacy level
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
    print("SAMPLE: MEDICATION EXPLANATION GENERATION")
    print("=" * 80)
    print()

    pipeline = PatientFacingXAIPipeline()

    # Example: Metformin explanation
    patient = create_patient_profile(
        patient_id="P003",
        age=60,
        education_level="High School"
    )

    concept = create_medical_concept(
        concept_type=ExplanationType.MEDICATION,
        technical_term="Metformin",
        context={
            "medication": "Metformin",
            "purpose": "lower your blood sugar levels",
            "dosage": "500mg",
            "frequency": "twice daily with meals"
        }
    )

    result = pipeline.generate_patient_explanation(
        patient, concept, validate=True, deliver_to_portal=True
    )

    print("Patient ID:", patient.patient_id)
    print("Medication:", concept.technical_term)
    print()
    print("Explanation:")
    print(result['explanation']['primary_text'])
    print()
    print("Action Steps:")
    for i, step in enumerate(result['explanation']['action_steps'], 1):
        print(f"  {i}. {step}")
    print()
    print("Validation:", "✅ PASSED" if result['validation']['overall_passed'] else "❌ FAILED")
    print("=" * 80)


if __name__ == "__main__":
    main()
