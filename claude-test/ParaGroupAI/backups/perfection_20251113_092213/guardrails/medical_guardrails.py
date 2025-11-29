"""
Medical-Specific Guardrails
HIPAA compliance, PHI detection, medical terminology validation, and fact-checking
"""

import os
import re
import logging
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result from validation check"""
    passed: bool
    layer: str
    message: str
    severity: Optional[int] = None
    details: Optional[Dict] = None
    timestamp: str = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class PHIDetector:
    """
    Protected Health Information (PHI) Detector
    Identifies and flags potential PHI in medical content
    """

    # PHI patterns (18 HIPAA identifiers)
    PATTERNS = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b(?:\+?1[-.]?)?(?:\(\d{3}\)|\d{3})[-.]?\d{3}[-.]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "medical_record": r'\b(?:MRN|MR#|Medical Record|Patient ID)[\s:]+[A-Z0-9]{6,}\b',
        "date_of_birth": r'\b(?:DOB|Date of Birth)[\s:]+\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        "account_number": r'\b(?:Account|Acct)[\s#:]+\d{6,}\b',
        "ip_address": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        "url": r'https?://[^\s]+',
        "name_patterns": r'\b(?:Dr\.|Doctor|Patient|Mr\.|Mrs\.|Ms\.)\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b',
        "address": r'\b\d+\s+[A-Z][a-z]+\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b',
        "zip_code": r'\b\d{5}(?:-\d{4})?\b',
    }

    # Sensitive medical terms that may indicate PHI context
    SENSITIVE_CONTEXTS = [
        "patient name", "patient's name", "named", "called",
        "address", "phone number", "email address",
        "social security", "SSN", "date of birth", "DOB",
        "medical record number", "MRN", "account number",
        "diagnosed on", "admitted on", "discharged on"
    ]

    def detect_phi(self, text: str) -> ValidationResult:
        """
        Detect potential PHI in text.

        Args:
            text: Text to analyze

        Returns:
            ValidationResult indicating if PHI was detected
        """
        detected_phi = []
        content_lower = text.lower()

        # Check patterns
        for phi_type, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detected_phi.append({
                    "type": phi_type,
                    "count": len(matches),
                    "samples": matches[:3]  # First 3 samples only
                })

        # Check sensitive contexts
        found_contexts = []
        for context in self.SENSITIVE_CONTEXTS:
            if context.lower() in content_lower:
                found_contexts.append(context)

        if detected_phi or found_contexts:
            return ValidationResult(
                passed=False,
                layer="phi_detection",
                message=f"Potential PHI detected: {len(detected_phi)} pattern types, {len(found_contexts)} sensitive contexts",
                severity=len(detected_phi) + len(found_contexts),
                details={
                    "detected_phi": detected_phi,
                    "sensitive_contexts": found_contexts
                }
            )

        return ValidationResult(
            passed=True,
            layer="phi_detection",
            message="No PHI detected"
        )


class HIPAAComplianceValidator:
    """
    HIPAA Compliance Validator
    Ensures content meets HIPAA de-identification standards
    """

    REQUIRED_DISCLAIMERS = [
        "educational purposes",
        "not medical advice",
        "consult healthcare provider",
        "anonymized",
        "de-identified"
    ]

    PROHIBITED_TERMS = [
        "actual patient name",
        "real patient",
        "identified patient",
        "not anonymized",
        "contains PHI"
    ]

    def validate_compliance(self, text: str, content_type: str = "medical_education") -> ValidationResult:
        """
        Validate HIPAA compliance.

        Args:
            text: Text to validate
            content_type: Type of content (medical_education, clinical_case, etc.)

        Returns:
            ValidationResult indicating compliance status
        """
        issues = []
        content_lower = text.lower()

        # Check for prohibited terms
        found_prohibited = []
        for term in self.PROHIBITED_TERMS:
            if term in content_lower:
                found_prohibited.append(term)

        if found_prohibited:
            issues.append(f"Contains prohibited terms: {found_prohibited}")

        # Check for required disclaimers (at least one should be present)
        has_disclaimer = any(
            disclaimer in content_lower
            for disclaimer in self.REQUIRED_DISCLAIMERS
        )

        if not has_disclaimer and content_type == "medical_education":
            issues.append("Missing required medical disclaimer")

        # Check for proper anonymization indicators
        anonymization_keywords = ["anonymized", "de-identified", "fictional", "hypothetical"]
        has_anonymization_indicator = any(
            keyword in content_lower
            for keyword in anonymization_keywords
        )

        if not has_anonymization_indicator and content_type in ["clinical_case", "patient_story"]:
            issues.append("Missing anonymization indicator for patient data")

        if issues:
            return ValidationResult(
                passed=False,
                layer="hipaa_compliance",
                message=f"HIPAA compliance issues: {'; '.join(issues)}",
                severity=len(issues),
                details={"issues": issues}
            )

        return ValidationResult(
            passed=True,
            layer="hipaa_compliance",
            message="HIPAA compliance validated"
        )


class MedicalTerminologyValidator:
    """
    Medical Terminology Validator
    Validates correct use of medical terms and coding systems
    """

    # Common medical terminology prefixes/suffixes
    MEDICAL_PREFIXES = [
        "cardio", "neuro", "hepat", "gastr", "pneum", "derm",
        "hemo", "osteo", "arthr", "myel", "cephal", "cardi"
    ]

    MEDICAL_SUFFIXES = [
        "ology", "itis", "osis", "ectomy", "otomy", "plasty",
        "scopy", "pathy", "penia", "trophy", "algia"
    ]

    # Coding system patterns
    CODING_PATTERNS = {
        "SNOMED": r'\b\d{6,18}\b',  # SNOMED CT codes
        "LOINC": r'\b\d{4,5}-\d{1}\b',  # LOINC codes
        "ICD-10": r'\b[A-Z]\d{2}(?:\.\d{1,4})?\b',  # ICD-10 codes
        "CPT": r'\b\d{5}\b',  # CPT codes
        "RxNorm": r'\bRxNorm:\s*\d+\b'  # RxNorm codes
    }

    def validate_terminology(self, text: str) -> ValidationResult:
        """
        Validate medical terminology usage.

        Args:
            text: Text to validate

        Returns:
            ValidationResult indicating terminology validation status
        """
        issues = []
        findings = {
            "medical_terms_count": 0,
            "coding_systems_used": []
        }

        # Check for medical terminology
        content_lower = text.lower()
        medical_term_count = 0

        for prefix in self.MEDICAL_PREFIXES:
            if prefix in content_lower:
                medical_term_count += content_lower.count(prefix)

        for suffix in self.MEDICAL_SUFFIXES:
            if suffix in content_lower:
                medical_term_count += content_lower.count(suffix)

        findings["medical_terms_count"] = medical_term_count

        # Check for coding systems
        for coding_system, pattern in self.CODING_PATTERNS.items():
            if re.search(pattern, text):
                findings["coding_systems_used"].append(coding_system)

        # Validate minimum medical terminology for medical content
        min_expected_terms = 5
        if medical_term_count < min_expected_terms:
            issues.append(f"Low medical terminology usage (found {medical_term_count}, expected at least {min_expected_terms})")

        if issues:
            return ValidationResult(
                passed=False,
                layer="medical_terminology",
                message=f"Terminology validation issues: {'; '.join(issues)}",
                severity=len(issues),
                details={"issues": issues, "findings": findings}
            )

        return ValidationResult(
            passed=True,
            layer="medical_terminology",
            message="Medical terminology validated",
            details={"findings": findings}
        )


class MedicalFactChecker:
    """
    Medical Fact Checker
    Validates medical facts and clinical accuracy
    """

    # Known incorrect or outdated medical claims
    KNOWN_INCORRECT_CLAIMS = [
        "vaccines cause autism",
        "antibiotics cure viral infections",
        "cancer is contagious",
        "diabetes is only from eating sugar",
        "you only use 10% of your brain"
    ]

    # Required evidence levels for claims
    EVIDENCE_KEYWORDS = [
        "according to", "research shows", "studies indicate",
        "evidence-based", "clinical trials", "peer-reviewed",
        "FDA approved", "recommended by", "guidelines suggest"
    ]

    # Medical measurement ranges (simplified - in production, use comprehensive database)
    NORMAL_RANGES = {
        "blood pressure systolic": (90, 140),
        "blood pressure diastolic": (60, 90),
        "heart rate": (60, 100),
        "temperature fahrenheit": (97.0, 99.5),
        "temperature celsius": (36.1, 37.5),
        "glucose fasting": (70, 100),
        "hemoglobin a1c": (4.0, 5.6)
    }

    def check_medical_facts(self, text: str) -> ValidationResult:
        """
        Check medical facts and clinical accuracy.

        Args:
            text: Text to check

        Returns:
            ValidationResult indicating fact-check status
        """
        issues = []
        warnings = []
        content_lower = text.lower()

        # Check for known incorrect claims
        found_incorrect = []
        for claim in self.KNOWN_INCORRECT_CLAIMS:
            if claim.lower() in content_lower:
                found_incorrect.append(claim)

        if found_incorrect:
            issues.append(f"Contains known incorrect medical claims: {found_incorrect}")

        # Check for evidence-based language
        has_evidence_based = any(
            keyword in content_lower
            for keyword in self.EVIDENCE_KEYWORDS
        )

        if not has_evidence_based:
            warnings.append("No evidence-based language detected - consider adding references")

        # Check for unrealistic vital sign ranges (simplified validation)
        for vital, (min_val, max_val) in self.NORMAL_RANGES.items():
            # Look for pattern like "blood pressure 200/120"
            pattern = rf"{vital}[:\s]+(\d+(?:\.\d+)?)"
            matches = re.findall(pattern, content_lower)
            for match in matches:
                try:
                    value = float(match)
                    if value < min_val * 0.5 or value > max_val * 2:
                        warnings.append(f"Unusual {vital} value detected: {value}")
                except ValueError:
                    pass

        # Critical issues fail validation
        if issues:
            return ValidationResult(
                passed=False,
                layer="medical_fact_checking",
                message=f"Medical fact-check failed: {'; '.join(issues)}",
                severity=len(issues),
                details={"issues": issues, "warnings": warnings}
            )

        # Warnings don't fail validation but are noted
        if warnings:
            return ValidationResult(
                passed=True,
                layer="medical_fact_checking",
                message=f"Medical fact-check passed with warnings",
                severity=0,
                details={"warnings": warnings}
            )

        return ValidationResult(
            passed=True,
            layer="medical_fact_checking",
            message="Medical fact-check passed"
        )
