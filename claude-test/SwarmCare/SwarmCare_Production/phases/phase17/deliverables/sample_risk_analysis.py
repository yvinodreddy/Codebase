#!/usr/bin/env python3
"""
Phase 17: Sample Risk Analysis Demonstration
Shows how to use the risk stratification engine
"""

import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from population_health_core import create_sample_patient, PopulationHealthPipeline

def main():
    print("\n" + "="*80)
    print("PHASE 17: RISK STRATIFICATION DEMONSTRATION")
    print("="*80 + "\n")

    # Initialize pipeline
    pipeline = PopulationHealthPipeline(use_guardrails=False)
    
    # Create sample patient
    patient_data = create_sample_patient()

    # Analyze patient
    analysis = pipeline.analyze_patient(
        patient_data['patient_id'],
        patient_data['demographics'],
        patient_data['diagnoses'],
        patient_data['medications'],
        patient_data['encounters'],
        patient_data['lab_results']
    )

    # Display risk assessment
    risk = analysis['risk_assessment']
    print("📊 RISK ASSESSMENT")
    print("-" * 80)
    print(f"Patient ID:              {patient_data['patient_id']}")
    print(f"Age:                     {patient_data['demographics'].age}")
    print(f"Gender:                  {patient_data['demographics'].gender}")
    print(f"\nRisk Score:              {risk['risk_score']:.1f}/100")
    print(f"Risk Tier:               {risk['risk_tier']}")
    print(f"Risk Model:              {risk['risk_model']}")
    print(f"Projected Annual Cost:   ${risk['projected_annual_cost']:,.2f}")
    print(f"Confidence:              {risk['confidence_score']*100:.0f}%")

    print(f"\n Contributing Factors:")
    for factor in risk['contributing_factors']:
        print(f"  • {factor}")

    print("\n✅ Risk analysis complete!\n")

if __name__ == "__main__":
    main()
