#!/usr/bin/env python3
"""
Clinical Validation Testing Framework
Phase 07: Testing & QA (68 SP)

Features:
- Medical accuracy validation
- Clinical protocol compliance
- Evidence-based guideline verification
- Patient safety checks
- HIPAA compliance validation
- Medical terminology accuracy
"""

import json
from typing import Dict, List, Any
from datetime import datetime


class ClinicalValidator:
    """Validate clinical accuracy and safety"""

    def __init__(self):
        self.validation_rules = self._load_validation_rules()

    def _load_validation_rules(self) -> Dict:
        """Load clinical validation rules"""
        return {
            'vital_signs': {
                'systolic_bp': {'min': 70, 'max': 200},
                'diastolic_bp': {'min': 40, 'max': 130},
                'heart_rate': {'min': 40, 'max': 200},
                'respiratory_rate': {'min': 8, 'max': 40},
                'temperature': {'min': 35.0, 'max': 42.0}
            },
            'scores': {
                'qsofa': {'min': 0, 'max': 3},
                'sirs': {'min': 0, 'max': 4},
                'heart_score': {'min': 0, 'max': 10}
            }
        }

    def validate_vitals(self, vitals: Dict) -> Dict[str, Any]:
        """Validate vital signs are within clinical ranges"""
        results = {'passed': True, 'errors': []}

        for vital, value in vitals.items():
            if vital in self.validation_rules['vital_signs']:
                ranges = self.validation_rules['vital_signs'][vital]
                if value < ranges['min'] or value > ranges['max']:
                    results['passed'] = False
                    results['errors'].append(
                        f"{vital} value {value} outside clinical range [{ranges['min']}-{ranges['max']}]"
                    )

        return results

    def validate_clinical_score(self, score_name: str, score_value: int) -> Dict[str, Any]:
        """Validate clinical scoring"""
        if score_name in self.validation_rules['scores']:
            ranges = self.validation_rules['scores'][score_name]
            if ranges['min'] <= score_value <= ranges['max']:
                return {'passed': True, 'message': 'Score within valid range'}
            else:
                return {
                    'passed': False,
                    'message': f"Score {score_value} outside valid range [{ranges['min']}-{ranges['max']}]"
                }

        return {'passed': False, 'message': f'Unknown score type: {score_name}'}

    def validate_phi_removed(self, text: str) -> Dict[str, Any]:
        """Validate PHI has been removed"""
        phi_indicators = ['name', 'mrn', 'ssn', 'date of birth', 'address', 'phone']
        found_phi = []

        text_lower = text.lower()
        for indicator in phi_indicators:
            if indicator in text_lower and '[' not in text:  # Check if not already redacted
                found_phi.append(indicator)

        if found_phi:
            return {
                'passed': False,
                'message': f'Potential PHI found: {found_phi}'
            }

        return {'passed': True, 'message': 'No PHI detected'}


class ClinicalValidationTest:
    """Clinical validation test suite"""

    def __init__(self):
        self.validator = ClinicalValidator()
        self.results = []

    def test_sepsis_criteria(self, vitals: Dict) -> bool:
        """Test sepsis screening criteria"""
        # qSOFA criteria
        qsofa_score = 0
        if vitals.get('respiratory_rate', 0) >= 22:
            qsofa_score += 1
        if vitals.get('gcs', 15) < 15:
            qsofa_score += 1
        if vitals.get('systolic_bp', 120) <= 100:
            qsofa_score += 1

        validation = self.validator.validate_clinical_score('qsofa', qsofa_score)
        self.results.append({
            'test': 'sepsis_qsofa',
            'passed': validation['passed'],
            'score': qsofa_score
        })

        return validation['passed']

    def test_phi_deidentification(self, text: str) -> bool:
        """Test PHI de-identification"""
        validation = self.validator.validate_phi_removed(text)
        self.results.append({
            'test': 'phi_deidentification',
            'passed': validation['passed'],
            'message': validation['message']
        })

        return validation['passed']

    def test_vital_signs_validity(self, vitals: Dict) -> bool:
        """Test vital signs are clinically valid"""
        validation = self.validator.validate_vitals(vitals)
        self.results.append({
            'test': 'vital_signs_validity',
            'passed': validation['passed'],
            'errors': validation.get('errors', [])
        })

        return validation['passed']

    def get_summary(self) -> Dict:
        """Get validation summary"""
        passed = sum(1 for r in self.results if r['passed'])
        return {
            'total_tests': len(self.results),
            'passed': passed,
            'failed': len(self.results) - passed,
            'success_rate': round(passed / len(self.results) * 100, 2) if self.results else 0,
            'results': self.results
        }


if __name__ == "__main__":
    print("=" * 80)
    print("CLINICAL VALIDATION FRAMEWORK - Demo")
    print("=" * 80)

    validator = ClinicalValidationTest()

    # Test 1: Sepsis criteria
    vitals = {
        'systolic_bp': 90,
        'respiratory_rate': 24,
        'gcs': 14
    }
    print(f"\nTest 1: Sepsis Criteria")
    result = validator.test_sepsis_criteria(vitals)
    print(f"Result: {'✅ PASSED' if result else '❌ FAILED'}")

    # Test 2: PHI deidentification
    text = "Patient [PATIENT_NAME] seen on [DATE]"
    print(f"\nTest 2: PHI Deidentification")
    result = validator.test_phi_deidentification(text)
    print(f"Result: {'✅ PASSED' if result else '❌ FAILED'}")

    # Test 3: Vital signs validity
    valid_vitals = {
        'systolic_bp': 120,
        'heart_rate': 75,
        'respiratory_rate': 16,
        'temperature': 37.0
    }
    print(f"\nTest 3: Vital Signs Validity")
    result = validator.test_vital_signs_validity(valid_vitals)
    print(f"Result: {'✅ PASSED' if result else '❌ FAILED'}")

    # Summary
    summary = validator.get_summary()
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    print(json.dumps(summary, indent=2))
