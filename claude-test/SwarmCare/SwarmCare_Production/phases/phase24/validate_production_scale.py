#!/usr/bin/env python3
"""
Phase 24 Production Scale Validation Script

Validates that all systems are operating at production scale with 500 codes per category
and 500 billing records.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, 'code')
from implementation import (
    Phase24Implementation,
    AutomatedCodingSystem,
    BillingEngine,
    EHRIntegrationEngine
)


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def validate_code_system():
    """Validate coding system has 500 codes per category"""
    print_header("VALIDATING CODE SYSTEM")

    coding_system = AutomatedCodingSystem()

    validations = {
        "ICD-10 Codes": (len(coding_system.icd10_codes), 500),
        "CPT Codes": (len(coding_system.cpt_codes), 500),
        "HCPCS Codes": (len(coding_system.hcpcs_codes), 500)
    }

    all_passed = True
    for name, (actual, expected) in validations.items():
        status = "✅ PASS" if actual == expected else "❌ FAIL"
        print(f"{status} | {name}: {actual}/{expected}")
        if actual != expected:
            all_passed = False

    return all_passed, coding_system


def validate_billing_system():
    """Validate billing system has 500 pricing codes"""
    print_header("VALIDATING BILLING SYSTEM")

    billing_engine = BillingEngine()

    actual = len(billing_engine.cpt_prices)
    expected = 500
    status = "✅ PASS" if actual == expected else "❌ FAIL"
    print(f"{status} | CPT Pricing Codes: {actual}/{expected}")

    return actual == expected, billing_engine


def validate_encounter_generation():
    """Validate encounter generation at scale"""
    print_header("VALIDATING ENCOUNTER GENERATION")

    coding_system = AutomatedCodingSystem()
    billing_engine = BillingEngine()

    # Generate codes for 500 encounters
    coding_data = coding_system.generate_codes_for_encounters(encounter_count=500)

    # Generate billing for 500 encounters
    billing_data = billing_engine.generate_billing_records(encounter_count=500)

    validations = {
        "Encounters (Coding)": (coding_data["encounter_count"], 500),
        "Encounters (Billing)": (billing_data["total_records"], 500),
        "Total Codes Generated": (coding_data["total_codes"], ">2000"),
        "Coding Accuracy": (coding_data["coding_accuracy"], 1.0),
        "Billing Accuracy": (billing_data["billing_accuracy"], 1.0)
    }

    all_passed = True
    for name, values in validations.items():
        if isinstance(values[1], str) and values[1].startswith(">"):
            threshold = int(values[1][1:])
            passed = values[0] > threshold
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} | {name}: {values[0]} (>{threshold})")
        else:
            passed = values[0] == values[1]
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} | {name}: {values[0]}/{values[1]}")

        if not passed:
            all_passed = False

    print(f"\n📊 Generated Code Breakdown:")
    print(f"   ICD-10: {coding_data['icd10_codes_generated']} codes")
    print(f"   CPT: {coding_data['cpt_codes_generated']} codes")
    print(f"   HCPCS: {coding_data['hcpcs_codes_generated']} codes")
    print(f"\n💰 Billing Summary:")
    print(f"   Total Records: {billing_data['total_records']}")
    print(f"   Total Value: ${billing_data['total_value']:,.2f}")
    print(f"   Average Claim: ${billing_data['avg_claim_value']:,.2f}")

    return all_passed


def validate_ehr_integration():
    """Validate EHR integration"""
    print_header("VALIDATING EHR INTEGRATION")

    ehr_engine = EHRIntegrationEngine()
    integration_result = ehr_engine.integrate_all_systems()

    validations = {
        "EHR Systems": (integration_result["total_count"], 11),
        "Connected Systems": (integration_result["connected_count"], 11),
        "Success Rate": (integration_result["success_rate"], 1.0)
    }

    all_passed = True
    for name, (actual, expected) in validations.items():
        status = "✅ PASS" if actual == expected else "❌ FAIL"
        print(f"{status} | {name}: {actual}/{expected}")
        if actual != expected:
            all_passed = False

    print(f"\n🏥 Integrated EHR Systems:")
    for i, system in enumerate(integration_result["systems"], 1):
        print(f"   {i:2d}. {system}")

    return all_passed


def validate_data_exports():
    """Validate data exports exist"""
    print_header("VALIDATING DATA EXPORTS")

    required_files = [
        "deliverables/icd10_codes_data.json",
        "deliverables/cpt_codes_data.json",
        "deliverables/hcpcs_codes_data.json",
        "deliverables/billing_records_data.json"
    ]

    all_passed = True
    for file_path in required_files:
        exists = Path(file_path).exists()
        status = "✅ PASS" if exists else "❌ FAIL"
        print(f"{status} | {Path(file_path).name}")

        if exists:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if "total_codes" in data:
                    print(f"        Total Codes: {data['total_codes']}")
                elif "total_records" in data:
                    print(f"        Total Records: {data['total_records']}")
                    print(f"        Total Value: ${data['total_value']:,.2f}")
        else:
            all_passed = False

    return all_passed


def validate_end_to_end():
    """Validate end-to-end Phase 24 implementation"""
    print_header("VALIDATING END-TO-END IMPLEMENTATION")

    impl = Phase24Implementation()
    task = {"goal": "Validate Phase 24 at production scale", "phase_id": 24}
    result = impl.execute(task)

    if result.success:
        components = result.output["components"]

        validations = {
            "Phase Execution": (result.success, True),
            "Production Ready": (components["production_ready"], True),
            "Verification Passed": (components["verification_passed"], True),
            "Total Codes >= 2000": (components["total_codes_generated"] >= 2000, True),
            "Billing Records": (components["billing_records_generated"], 500),
            "EHR Systems": (components["ehr_systems_integrated"], 11)
        }

        all_passed = True
        for name, (actual, expected) in validations.items():
            status = "✅ PASS" if actual == expected else "❌ FAIL"
            print(f"{status} | {name}: {actual}")
            if actual != expected:
                all_passed = False

        print(f"\n📈 Production Metrics:")
        print(f"   Total Codes Generated: {components['total_codes_generated']:,}")
        print(f"   ICD-10 Codes: {components['icd10_codes']:,}")
        print(f"   CPT Codes: {components['cpt_codes']:,}")
        print(f"   HCPCS Codes: {components['hcpcs_codes']:,}")
        print(f"   Billing Records: {components['billing_records_generated']:,}")
        print(f"   Total Claims Value: ${components['total_claims_value']:,.2f}")
        print(f"   Coding Accuracy: {components['coding_accuracy']*100}%")
        print(f"   Billing Accuracy: {components['billing_accuracy']*100}%")
        print(f"   Avg Processing Time: {components['avg_processing_time_ms']}ms")

        return all_passed
    else:
        print("❌ FAIL | Phase execution failed")
        return False


def main():
    """Run all validations"""
    print_header("PHASE 24 PRODUCTION SCALE VALIDATION")
    print("Validating 500 codes per category and 500 billing records\n")

    results = {
        "Code System": validate_code_system()[0],
        "Billing System": validate_billing_system()[0],
        "Encounter Generation": validate_encounter_generation(),
        "EHR Integration": validate_ehr_integration(),
        "Data Exports": validate_data_exports(),
        "End-to-End": validate_end_to_end()
    }

    print_header("VALIDATION SUMMARY")

    all_passed = all(results.values())

    for category, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} | {category}")

    print(f"\n{'='*80}")
    if all_passed:
        print("  ✅ ALL VALIDATIONS PASSED - PRODUCTION READY")
    else:
        print("  ❌ SOME VALIDATIONS FAILED - NOT PRODUCTION READY")
    print(f"{'='*80}\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
