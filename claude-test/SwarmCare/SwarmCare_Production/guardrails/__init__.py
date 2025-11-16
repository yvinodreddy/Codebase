"""
SwarmCare Guardrails Package
Production-ready multi-layer guardrail system for medical AI applications.
"""

from .azure_content_safety import (
    AzureContentSafetyValidator,
    PromptShieldsValidator,
    GroundednessDetector
)
from .medical_guardrails import (
    MedicalTerminologyValidator,
    PHIDetector,
    HIPAAComplianceValidator,
    MedicalFactChecker
)
from .multi_layer_system import MultiLayerGuardrailSystem
from .crewai_guardrails import (
    create_medical_guardrail,
    create_compliance_guardrail,
    create_quality_guardrail
)

__all__ = [
    "AzureContentSafetyValidator",
    "PromptShieldsValidator",
    "GroundednessDetector",
    "MedicalTerminologyValidator",
    "PHIDetector",
    "HIPAAComplianceValidator",
    "MedicalFactChecker",
    "MultiLayerGuardrailSystem",
    "create_medical_guardrail",
    "create_compliance_guardrail",
    "create_quality_guardrail",
]

__version__ = "1.0.0"
