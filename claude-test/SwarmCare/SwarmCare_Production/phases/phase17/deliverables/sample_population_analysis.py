#!/usr/bin/env python3
"""
Phase 17: Sample Population Analysis Demonstration
Shows how to analyze a population cohort
"""

import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from population_health_core import create_sample_patient, PopulationHealthPipeline

def main():
    print("\n" + "="*80)
    print("PHASE 17: POPULATION ANALYSIS DEMONSTRATION")
    print("="*80 + "\n")

    # Initialize pipeline
    pipeline = PopulationHealthPipeline(use_guardrails=False)

    # Create sample population
    print("📊 Creating sample population (10 patients)...")
    population_data = []
    for i in range(10):
        patient = create_sample_patient()
        patient['patient_id'] = f"PATIENT-{i+1:03d}"
        patient['demographics'].patient_id = f"PATIENT-{i+1:03d}"
        population_data.append(patient)

    print(f"✅ Created {len(population_data)} patients\n")

    # Analyze population
    print("🔍 Analyzing population...")
    analysis = pipeline.analyze_population(population_data)

    # Display results
    print("\n" + "="*80)
    print("POPULATION METRICS")
    print("="*80)
    metrics = analysis['metrics']
    print(f"\nTotal Patients:              {metrics['total_patients']}")
    print(f"Average Risk Score:          {metrics['average_risk_score']:.1f}")
    print(f"Total Care Gaps:             {metrics['total_care_gaps']}")
    print(f"High Priority Interventions: {metrics['high_priority_interventions']}")
    print(f"Total Projected Cost:        ${metrics['total_projected_cost']:,.2f}")

    print("\n" + "-"*80)
    print("RISK DISTRIBUTION")
    print("-"*80)
    for tier, count in metrics['risk_distribution'].items():
        pct = (count / metrics['total_patients']) * 100
        print(f"{tier:20s} {count:3d} ({pct:5.1f}%)")

    print("\n" + "-"*80)
    print("QUALITY MEASURES")
    print("-"*80)
    for measure in analysis['quality_measures']:
        print(f"\n{measure['measure_name']}")
        print(f"  Performance: {measure['performance_rate']:.1f}%")
        print(f"  Benchmark:   {measure['benchmark_rate']:.1f}%")
        print(f"  Gap:         {measure['gap_to_benchmark']:.1f}%")

    print("\n" + "-"*80)
    print("COHORTS")
    print("-"*80)
    for cohort_name, patient_list in analysis['cohorts'].items():
        print(f"{cohort_name:30s} {len(patient_list):3d} patients")

    print("\n✅ Population analysis complete!\n")

if __name__ == "__main__":
    main()
