#!/usr/bin/env python3
"""
Phase 17: Population Health Management
Production Validation Script

Comprehensive validation checks for production readiness
"""

import sys
import os
import time
import json
from datetime import datetime

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase17Implementation
from population_health_core import (
    PopulationHealthPipeline, RiskStratificationEngine, CareGapsEngine,
    QualityMeasuresEngine, create_sample_patient
)


class Phase17Validator:
    """Production validation for Phase 17"""

    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.checks_total = 0

    def run_check(self, check_name: str, check_func):
        """Run a validation check"""
        self.checks_total += 1
        try:
            result = check_func()
            if result:
                print(f"  ✅ {check_name}")
                self.checks_passed += 1
                return True
            else:
                print(f"  ❌ {check_name} - FAILED")
                self.checks_failed += 1
                return False
        except Exception as e:
            print(f"  ❌ {check_name} - ERROR: {e}")
            self.checks_failed += 1
            return False

    def validate_all(self):
        """Run all validation checks"""
        print("\n" + "="*80)
        print("PHASE 17: POPULATION HEALTH MANAGEMENT - PRODUCTION VALIDATION")
        print("="*80 + "\n")

        # Section 1: Implementation Validation
        print("="*80)
        print("SECTION 1: IMPLEMENTATION VALIDATION")
        print("="*80)

        self.run_check(
            "Implementation class exists",
            lambda: Phase17Implementation() is not None
        )

        impl = Phase17Implementation()

        self.run_check(
            "Phase ID is correct (17)",
            lambda: impl.phase_id == 17
        )

        self.run_check(
            "Phase name is correct",
            lambda: impl.phase_name == "Population Health Management"
        )

        self.run_check(
            "Story points is correct (43)",
            lambda: impl.story_points == 43
        )

        self.run_check(
            "Priority is correct (P1)",
            lambda: impl.priority == "P1"
        )

        self.run_check(
            "Framework version is 100%",
            lambda: impl.framework_version == "100%"
        )

        # Section 2: Population Health Core
        print("\n" + "="*80)
        print("SECTION 2: POPULATION HEALTH CORE VALIDATION")
        print("="*80)

        self.run_check(
            "PopulationHealthPipeline initializes",
            lambda: PopulationHealthPipeline(use_guardrails=False) is not None
        )

        self.run_check(
            "RiskStratificationEngine initializes",
            lambda: RiskStratificationEngine() is not None
        )

        self.run_check(
            "CareGapsEngine initializes",
            lambda: CareGapsEngine() is not None
        )

        self.run_check(
            "QualityMeasuresEngine initializes",
            lambda: QualityMeasuresEngine() is not None
        )

        # Section 3: Risk Stratification
        print("\n" + "="*80)
        print("SECTION 3: RISK STRATIFICATION VALIDATION")
        print("="*80)

        engine = RiskStratificationEngine()
        patient_data = create_sample_patient()

        def check_risk_calculation():
            risk_score = engine.calculate_hcc_risk(
                patient_data['patient_id'],
                patient_data['demographics'],
                patient_data['diagnoses'],
                patient_data['encounters']
            )
            return (0 <= risk_score.risk_score <= 100 and
                    risk_score.projected_annual_cost > 0)

        self.run_check("Risk score calculation works", check_risk_calculation)

        self.run_check(
            "HCC weights are defined",
            lambda: len(engine.HCC_WEIGHTS) > 0
        )

        self.run_check(
            "ICD-10 to HCC mapping exists",
            lambda: len(engine.ICD10_TO_HCC) > 0
        )

        # Section 4: Care Gaps
        print("\n" + "="*80)
        print("SECTION 4: CARE GAPS VALIDATION")
        print("="*80)

        gaps_engine = CareGapsEngine()

        def check_gaps_identification():
            gaps = gaps_engine.identify_gaps(
                patient_data['patient_id'],
                patient_data['demographics'],
                patient_data['diagnoses'],
                patient_data['medications'],
                patient_data['encounters'],
                patient_data['lab_results']
            )
            return len(gaps) > 0

        self.run_check("Care gaps are identified", check_gaps_identification)

        # Section 5: Quality Measures
        print("\n" + "="*80)
        print("SECTION 5: QUALITY MEASURES VALIDATION")
        print("="*80)

        quality_engine = QualityMeasuresEngine()

        def check_hedis_measures():
            population = [patient_data for _ in range(5)]
            measures = quality_engine.calculate_hedis_measures(population)
            return len(measures) > 0

        self.run_check("HEDIS measures calculate", check_hedis_measures)

        # Section 6: Pipeline Integration
        print("\n" + "="*80)
        print("SECTION 6: PIPELINE INTEGRATION VALIDATION")
        print("="*80)

        pipeline = PopulationHealthPipeline(use_guardrails=False)

        def check_patient_analysis():
            analysis = pipeline.analyze_patient(
                patient_data['patient_id'],
                patient_data['demographics'],
                patient_data['diagnoses'],
                patient_data['medications'],
                patient_data['encounters'],
                patient_data['lab_results']
            )
            return (analysis['hipaa_compliant'] and
                    analysis['phi_removed'] and
                    len(analysis['care_gaps']) > 0)

        self.run_check("Patient analysis works", check_patient_analysis)

        def check_population_analysis():
            population = [create_sample_patient() for _ in range(5)]
            for i, p in enumerate(population):
                p['patient_id'] = f"PATIENT-{i+1:03d}"
                p['demographics'].patient_id = f"PATIENT-{i+1:03d}"
            analysis = pipeline.analyze_population(population)
            return analysis['population_size'] == 5

        self.run_check("Population analysis works", check_population_analysis)

        # Section 7: HIPAA Compliance
        print("\n" + "="*80)
        print("SECTION 7: HIPAA COMPLIANCE VALIDATION")
        print("="*80)

        def check_phi_protection():
            analysis = pipeline.analyze_patient(
                patient_data['patient_id'],
                patient_data['demographics'],
                patient_data['diagnoses'],
                patient_data['medications'],
                patient_data['encounters'],
                patient_data['lab_results']
            )
            return (analysis['hipaa_compliant'] and
                    analysis['phi_removed'] and
                    'patient_id_hash' in analysis)

        self.run_check("PHI protection is enabled", check_phi_protection)

        self.run_check(
            "Patient ID hashing works",
            lambda: len(patient_data['demographics'].patient_id_hash) == 16
        )

        # Section 8: Performance
        print("\n" + "="*80)
        print("SECTION 8: PERFORMANCE VALIDATION")
        print("="*80)

        def check_patient_analysis_performance():
            start = time.time()
            pipeline.analyze_patient(
                patient_data['patient_id'],
                patient_data['demographics'],
                patient_data['diagnoses'],
                patient_data['medications'],
                patient_data['encounters'],
                patient_data['lab_results']
            )
            duration_ms = (time.time() - start) * 1000
            print(f"      Patient analysis: {duration_ms:.2f}ms")
            return duration_ms < 500  # Target < 500ms

        self.run_check(
            "Patient analysis performance < 500ms",
            check_patient_analysis_performance
        )

        def check_risk_calculation_performance():
            start = time.time()
            engine.calculate_hcc_risk(
                patient_data['patient_id'],
                patient_data['demographics'],
                patient_data['diagnoses'],
                patient_data['encounters']
            )
            duration_ms = (time.time() - start) * 1000
            print(f"      Risk calculation: {duration_ms:.2f}ms")
            return duration_ms < 100  # Target < 100ms

        self.run_check(
            "Risk calculation performance < 100ms",
            check_risk_calculation_performance
        )

        # Section 9: Agent Framework Integration
        print("\n" + "="*80)
        print("SECTION 9: AGENT FRAMEWORK INTEGRATION")
        print("="*80)

        self.run_check(
            "Framework available flag exists",
            lambda: hasattr(impl, 'framework_available')
        )

        def check_execution():
            task = {"goal": "Test execution", "phase_id": 17}
            result = impl.execute(task)
            return result.success

        self.run_check("Implementation execution works", check_execution)

        # Section 10: Production Readiness
        print("\n" + "="*80)
        print("SECTION 10: PRODUCTION READINESS")
        print("="*80)

        def check_capabilities():
            task = {"goal": "Test", "phase_id": 17}
            context = {"task": task, "phase_id": 17}
            output = impl.take_action(task, context)
            caps = output["components"]["capabilities"]
            return (
                "risk_stratification" in caps and
                "care_gaps_identification" in caps and
                "quality_measures" in caps and
                "interventions" in caps and
                "cohort_management" in caps
            )

        self.run_check("All capabilities are present", check_capabilities)

        def check_compliance_features():
            task = {"goal": "Test", "phase_id": 17}
            context = {"task": task, "phase_id": 17}
            output = impl.take_action(task, context)
            comp = output["components"]["compliance"]
            return (comp["hipaa_compliant"] and
                    "phi_protection" in comp and
                    "audit_logging" in comp)

        self.run_check("Compliance features are configured", check_compliance_features)

        # Final Summary
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        print(f"Total Checks:  {self.checks_total}")
        print(f"Passed:        {self.checks_passed} ✅")
        print(f"Failed:        {self.checks_failed} ❌")
        print(f"Success Rate:  {(self.checks_passed/self.checks_total*100):.1f}%")
        print("="*80)

        if self.checks_failed == 0:
            print("\n🎉 ALL VALIDATION CHECKS PASSED - PRODUCTION READY! 🎉\n")
            return True
        else:
            print(f"\n⚠️  {self.checks_failed} VALIDATION CHECKS FAILED ⚠️\n")
            return False


if __name__ == "__main__":
    validator = Phase17Validator()
    success = validator.validate_all()
    sys.exit(0 if success else 1)
