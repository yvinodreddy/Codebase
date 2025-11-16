"""
Multi-Layer Guardrail System
Comprehensive 7-layer guardrail system for medical AI applications
"""

import os
import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv

try:
    from .azure_content_safety import (
        AzureContentSafetyValidator,
        PromptShieldsValidator,
        GroundednessDetector,
        ValidationResult
    )
    from .medical_guardrails import (
        PHIDetector,
        HIPAAComplianceValidator,
        MedicalTerminologyValidator,
        MedicalFactChecker
    )
except ImportError:
    from azure_content_safety import (
        AzureContentSafetyValidator,
        PromptShieldsValidator,
        GroundednessDetector,
        ValidationResult
    )
    from medical_guardrails import (
        PHIDetector,
        HIPAAComplianceValidator,
        MedicalTerminologyValidator,
        MedicalFactChecker
    )

load_dotenv()

logger = logging.getLogger(__name__)


class MultiLayerGuardrailSystem:
    """
    Complete 7-layer guardrail system for SwarmCare medical AI application.

    Layers:
    1. Prompt Shields (jailbreak/injection prevention)
    2. Input Content Filtering (harmful content detection)
    3. PHI Detection (patient privacy protection)
    4. Medical Terminology Validation (clinical accuracy)
    5. Output Content Filtering (generated content safety)
    6. Groundedness Detection (factual accuracy)
    7. HIPAA Compliance & Medical Fact Checking (regulatory compliance)
    """

    def __init__(self):
        # ALWAYS ACTIVE: Security & Safety (critical for all content)
        self.prompt_shields = PromptShieldsValidator()
        self.content_safety = AzureContentSafetyValidator()
        self.groundedness = GroundednessDetector()

        # LAZY INITIALIZATION: Medical validators (only for medical content)
        self.phi_detector = None
        self.hipaa_validator = None
        self.terminology_validator = None
        self.fact_checker = None

        # Configuration
        self.content_threshold = int(os.getenv("GUARDRAIL_CONTENT_THRESHOLD", "2"))
        self.max_retries = int(os.getenv("GUARDRAIL_MAX_RETRIES", "5"))

        # Medical content detection
        self.medical_content_types = [
            "medical_education", "clinical_case", "medical_dialogue",
            "patient_story", "medical_knowledge", "compliance_report"
        ]

        logger.info("MultiLayerGuardrailSystem initialized (medical validators: lazy)")

        # Statistics
        self.medical_validators_initialized = False
        self.stats = {
            "total_requests": 0,
            "blocked_by_layer": {
                "layer_1_prompt_shields": 0,
                "layer_2_input_content": 0,
                "layer_3_phi_detection": 0,
                "layer_4_terminology": 0,
                "layer_5_output_content": 0,
                "layer_6_groundedness": 0,
                "layer_7_compliance": 0
            },
            "successful": 0,
            "warnings": 0
        }

    # ==========================================
    # HELPER: Initialize Medical Validators
    # ==========================================

    def _initialize_medical_validators(self):
        """Initialize medical validators on first use (lazy loading)"""
        if self.medical_validators_initialized:
            return

        logger.info("Initializing medical validators (first medical content detected)...")
        self.phi_detector = PHIDetector()
        self.hipaa_validator = HIPAAComplianceValidator()
        self.terminology_validator = MedicalTerminologyValidator()
        self.fact_checker = MedicalFactChecker()
        self.medical_validators_initialized = True
        logger.info("✓ Medical validators initialized")

    def _is_medical_content(self, content_type: str) -> bool:
        """Check if content type requires medical validation"""
        return content_type in self.medical_content_types

    # ==========================================
    # LAYER 1: Prompt Shields
    # ==========================================

    def layer1_prompt_shields(self, user_input: str, documents: Optional[List[str]] = None) -> ValidationResult:
        """
        Layer 1: Check for jailbreak attempts and prompt injection.
        """
        if not os.getenv("ENABLE_PROMPT_SHIELDS", "true").lower() == "true":
            return ValidationResult(
                passed=True,
                layer="layer_1_prompt_shields",
                message="Prompt shields disabled"
            )

        logger.info("Layer 1: Running Prompt Shields validation...")
        return self.prompt_shields.check_prompt_safety(user_input, documents)

    # ==========================================
    # LAYER 2: Input Content Filtering
    # ==========================================

    def layer2_input_content_filter(self, user_input: str) -> ValidationResult:
        """
        Layer 2: Check input for harmful content categories.
        """
        if not os.getenv("ENABLE_CONTENT_FILTERING", "true").lower() == "true":
            return ValidationResult(
                passed=True,
                layer="layer_2_input_content",
                message="Content filtering disabled"
            )

        logger.info("Layer 2: Running input content filtering...")
        return self.content_safety.analyze_text(user_input, self.content_threshold)

    # ==========================================
    # LAYER 3: PHI Detection
    # ==========================================

    def layer3_phi_detection(self, user_input: str, content_type: str = "general") -> ValidationResult:
        """
        Layer 3: Detect Protected Health Information (PHI).
        Only runs for medical content types.
        """
        # Skip for non-medical content
        if not self._is_medical_content(content_type):
            return ValidationResult(
                passed=True,
                layer="layer_3_phi_detection",
                message="PHI detection skipped (non-medical content)"
            )

        if not os.getenv("ENABLE_PHI_DETECTION", "true").lower() == "true":
            return ValidationResult(
                passed=True,
                layer="layer_3_phi_detection",
                message="PHI detection disabled"
            )

        # Initialize medical validators if needed
        self._initialize_medical_validators()

        logger.info("Layer 3: Running PHI detection...")
        return self.phi_detector.detect_phi(user_input)

    # ==========================================
    # LAYER 4: Medical Terminology Validation
    # ==========================================

    def layer4_terminology_validation(self, text: str, content_type: str = "general", enforce: bool = False) -> ValidationResult:
        """
        Layer 4: Validate medical terminology usage.
        Only runs for medical content types.

        Args:
            text: Text to validate
            content_type: Type of content being validated
            enforce: If True, fail on issues; if False, only warn
        """
        # Skip for non-medical content
        if not self._is_medical_content(content_type):
            return ValidationResult(
                passed=True,
                layer="layer_4_terminology",
                message="Terminology validation skipped (non-medical content)"
            )

        if not os.getenv("MEDICAL_TERMINOLOGY_VALIDATION", "true").lower() == "true":
            return ValidationResult(
                passed=True,
                layer="layer_4_terminology",
                message="Terminology validation disabled"
            )

        # Initialize medical validators if needed
        self._initialize_medical_validators()

        logger.info("Layer 4: Running medical terminology validation...")
        result = self.terminology_validator.validate_terminology(text)

        # Convert failures to warnings if not enforcing
        if not enforce and not result.passed:
            result.passed = True
            result.message = f"Warning: {result.message}"
            self.stats["warnings"] += 1

        return result

    # ==========================================
    # LAYER 5: Output Content Filtering
    # ==========================================

    def layer5_output_content_filter(self, output: str) -> ValidationResult:
        """
        Layer 5: Validate generated output for harmful content.
        """
        if not os.getenv("ENABLE_CONTENT_FILTERING", "true").lower() == "true":
            return ValidationResult(
                passed=True,
                layer="layer_5_output_content",
                message="Content filtering disabled"
            )

        logger.info("Layer 5: Running output content filtering...")
        return self.content_safety.analyze_text(output, self.content_threshold)

    # ==========================================
    # LAYER 6: Groundedness Detection
    # ==========================================

    def layer6_groundedness_check(
        self,
        output: str,
        source_documents: Optional[List[str]] = None,
        query: Optional[str] = None
    ) -> ValidationResult:
        """
        Layer 6: Check if output is grounded in source material.
        """
        if not os.getenv("ENABLE_GROUNDEDNESS_CHECK", "true").lower() == "true":
            return ValidationResult(
                passed=True,
                layer="layer_6_groundedness",
                message="Groundedness check disabled"
            )

        logger.info("Layer 6: Running groundedness detection...")
        return self.groundedness.detect_groundedness(
            output,
            source_documents or [],
            query,
            domain="Medical"
        )

    # ==========================================
    # LAYER 7: HIPAA Compliance & Fact Checking
    # ==========================================

    def layer7_compliance_and_facts(
        self,
        output: str,
        content_type: str = "general"
    ) -> ValidationResult:
        """
        Layer 7: Final HIPAA compliance and medical fact checking.
        Only runs for medical content types.
        """
        # Skip for non-medical content
        if not self._is_medical_content(content_type):
            return ValidationResult(
                passed=True,
                layer="layer_7_compliance_facts",
                message="Compliance and fact-check skipped (non-medical content)"
            )

        # Initialize medical validators if needed
        self._initialize_medical_validators()

        logger.info("Layer 7: Running compliance and fact checking...")

        # Run HIPAA compliance check
        hipaa_result = self.hipaa_validator.validate_compliance(output, content_type)
        if not hipaa_result.passed:
            return hipaa_result

        # Run medical fact checking
        fact_result = self.fact_checker.check_medical_facts(output)
        if not fact_result.passed:
            return fact_result

        # Combine results
        warnings = []
        if hipaa_result.details and "warnings" in hipaa_result.details:
            warnings.extend(hipaa_result.details["warnings"])
        if fact_result.details and "warnings" in fact_result.details:
            warnings.extend(fact_result.details["warnings"])

        if warnings:
            self.stats["warnings"] += len(warnings)

        return ValidationResult(
            passed=True,
            layer="layer_7_compliance_facts",
            message="Compliance and fact-check passed",
            details={"warnings": warnings} if warnings else None
        )

    # ==========================================
    # MAIN PROCESSING FUNCTION
    # ==========================================

    def process_with_guardrails(
        self,
        user_input: str,
        output: Optional[str] = None,
        source_documents: Optional[List[str]] = None,
        content_type: str = "medical_education",
        input_documents: Optional[List[str]] = None,
        query: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process input/output through all 7 layers of guardrails.

        Args:
            user_input: User's input text
            output: Generated output text (optional, for output validation)
            source_documents: Source documents for groundedness check
            content_type: Type of content (medical_education, clinical_case, etc.)
            input_documents: Documents in user input (for prompt shields)
            query: Original user query (for groundedness)

        Returns:
            dict with validation status, results, and logs
        """
        self.stats["total_requests"] += 1
        validation_log = []

        # === INPUT VALIDATION LAYERS ===

        # LAYER 1: Prompt Shields
        result = self.layer1_prompt_shields(user_input, input_documents)
        validation_log.append(result)
        if not result.passed:
            self.stats["blocked_by_layer"]["layer_1_prompt_shields"] += 1
            return self._create_response(False, None, validation_log, "layer_1")

        # LAYER 2: Input Content Filtering
        result = self.layer2_input_content_filter(user_input)
        validation_log.append(result)
        if not result.passed:
            self.stats["blocked_by_layer"]["layer_2_input_content"] += 1
            return self._create_response(False, None, validation_log, "layer_2")

        # LAYER 3: PHI Detection
        result = self.layer3_phi_detection(user_input, content_type)
        validation_log.append(result)
        if not result.passed:
            self.stats["blocked_by_layer"]["layer_3_phi_detection"] += 1
            return self._create_response(False, None, validation_log, "layer_3")

        # If no output provided, return success for input validation
        if output is None:
            self.stats["successful"] += 1
            return self._create_response(True, None, validation_log, None)

        # === OUTPUT VALIDATION LAYERS ===

        # LAYER 4: Medical Terminology Validation
        result = self.layer4_terminology_validation(output, content_type, enforce=False)
        validation_log.append(result)
        if not result.passed:
            self.stats["blocked_by_layer"]["layer_4_terminology"] += 1
            return self._create_response(False, None, validation_log, "layer_4")

        # LAYER 5: Output Content Filtering
        result = self.layer5_output_content_filter(output)
        validation_log.append(result)
        if not result.passed:
            self.stats["blocked_by_layer"]["layer_5_output_content"] += 1
            return self._create_response(False, None, validation_log, "layer_5")

        # LAYER 6: Groundedness Check
        result = self.layer6_groundedness_check(output, source_documents, query)
        validation_log.append(result)
        if not result.passed:
            self.stats["blocked_by_layer"]["layer_6_groundedness"] += 1
            return self._create_response(False, None, validation_log, "layer_6")

        # LAYER 7: HIPAA Compliance & Medical Fact Checking
        result = self.layer7_compliance_and_facts(output, content_type)
        validation_log.append(result)
        if not result.passed:
            self.stats["blocked_by_layer"]["layer_7_compliance"] += 1
            return self._create_response(False, None, validation_log, "layer_7")

        # ALL LAYERS PASSED!
        self.stats["successful"] += 1
        return self._create_response(True, output, validation_log, None)

    def _create_response(
        self,
        success: bool,
        output: Optional[str],
        validation_log: List[ValidationResult],
        blocked_at: Optional[str]
    ) -> Dict[str, Any]:
        """Create standardized response."""
        return {
            "success": success,
            "output": output,
            "blocked_at": blocked_at,
            "validation_log": [
                {
                    "layer": v.layer,
                    "passed": v.passed,
                    "message": v.message,
                    "severity": v.severity,
                    "timestamp": v.timestamp,
                    "details": v.details
                }
                for v in validation_log
            ],
            "warnings": sum(
                1 for v in validation_log
                if v.details and "warnings" in v.details
            ),
            "timestamp": datetime.now().isoformat()
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics."""
        success_rate = (
            self.stats["successful"] / self.stats["total_requests"] * 100
            if self.stats["total_requests"] > 0 else 0
        )

        return {
            **self.stats,
            "success_rate": round(success_rate, 2)
        }

    def reset_statistics(self):
        """Reset statistics counters."""
        self.stats = {
            "total_requests": 0,
            "blocked_by_layer": {key: 0 for key in self.stats["blocked_by_layer"]},
            "successful": 0,
            "warnings": 0
        }
