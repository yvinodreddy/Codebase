#!/usr/bin/env python3
"""
Sample: Multi-Language Support
Demonstrates explanation generation in multiple languages
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
    print("SAMPLE: MULTI-LANGUAGE SUPPORT")
    print("=" * 80)
    print()

    pipeline = PatientFacingXAIPipeline()

    # English patient
    print("-" * 80)
    print("Example 1: English (en)")
    print("-" * 80)

    patient_en = create_patient_profile(
        patient_id="P001",
        age=50,
        education_level="High School",
        preferred_language="en"
    )

    concept_en = create_medical_concept(
        ExplanationType.DIAGNOSIS,
        "Hypertension",
        {
            "condition": "Hypertension",
            "simple_description": "high blood pressure",
            "why_important": "can damage your heart"
        }
    )

    result_en = pipeline.generate_patient_explanation(patient_en, concept_en)
    print(f"Language: {result_en['explanation']['language']}")
    print(f"Explanation: {result_en['explanation']['simplified_summary']}")
    print()

    # Spanish patient
    print("-" * 80)
    print("Example 2: Spanish (es)")
    print("-" * 80)

    patient_es = create_patient_profile(
        patient_id="P002",
        age=50,
        education_level="High School",
        preferred_language="es"
    )

    concept_es = create_medical_concept(
        ExplanationType.DIAGNOSIS,
        "Hipertensión",
        {
            "condition": "Hipertensión",
            "simple_description": "presión arterial alta",
            "why_important": "puede dañar su corazón"
        }
    )

    result_es = pipeline.generate_patient_explanation(patient_es, concept_es)
    print(f"Language: {result_es['explanation']['language']}")
    print(f"Explanation: {result_es['explanation']['simplified_summary']}")
    print()

    # Summary
    print("=" * 80)
    print("Supported Languages:")
    print("  • English (en)")
    print("  • Spanish (es)")
    print("  • Chinese (zh)")
    print("  • French (fr)")
    print("  • German (de)")
    print("  • Arabic (ar)")
    print("  • Portuguese (pt)")
    print("  • Russian (ru)")
    print("  • Japanese (ja)")
    print("  • Hindi (hi)")
    print()
    print("✅ Multi-language support demonstrated")
    print("=" * 80)


if __name__ == "__main__":
    main()
