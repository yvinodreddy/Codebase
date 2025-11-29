"""
CrewAI Guardrails Integration
Guardrail functions designed for CrewAI tasks with medical AI focus
"""

import logging
from typing import Tuple, Any, Dict, List, Optional
from crewai import TaskOutput
import json

try:
    from .multi_layer_system import MultiLayerGuardrailSystem
except ImportError:
    from multi_layer_system import MultiLayerGuardrailSystem

logger = logging.getLogger(__name__)

# Global guardrail system instance
_guardrail_system = None


def get_guardrail_system() -> MultiLayerGuardrailSystem:
    """Get or create global guardrail system instance."""
    global _guardrail_system
    if _guardrail_system is None:
        _guardrail_system = MultiLayerGuardrailSystem()
    return _guardrail_system


# ==========================================
# MEDICAL KNOWLEDGE EXTRACTION GUARDRAILS
# ==========================================

def medical_knowledge_extraction_guardrail(result: TaskOutput) -> Tuple[bool, Any]:
    """
    Guardrail for medical knowledge extraction tasks.

    Validates:
    - Medical terminology usage
    - PHI absence
    - Content safety
    - Proper structure
    """
    try:
        content = str(result)
        system = get_guardrail_system()

        # Validate output
        validation_result = system.process_with_guardrails(
            user_input="Medical knowledge extraction task",
            output=content,
            content_type="medical_knowledge"
        )

        if not validation_result["success"]:
            blocked_at = validation_result["blocked_at"]
            error_log = validation_result["validation_log"]

            # Find the failing layer
            failed_layer = next(
                (log for log in error_log if not log["passed"]),
                {"message": "Unknown validation error"}
            )

            error_message = f"Medical knowledge extraction validation failed at {blocked_at}: {failed_layer['message']}"
            logger.warning(f"Guardrail failure: {error_message}")

            return (False, error_message)

        # Log warnings
        if validation_result.get("warnings", 0) > 0:
            warnings = [
                log.get("details", {}).get("warnings", [])
                for log in validation_result["validation_log"]
                if log.get("details") and "warnings" in log.get("details", {})
            ]
            logger.info(f"Validation passed with warnings: {warnings}")

        return (True, content)

    except Exception as e:
        logger.error(f"Error in medical knowledge extraction guardrail: {e}")
        return (False, f"Guardrail error: {str(e)}")


# ==========================================
# CLINICAL CASE SYNTHESIS GUARDRAILS
# ==========================================

def clinical_case_synthesis_guardrail(result: TaskOutput) -> Tuple[bool, Any]:
    """
    Guardrail for clinical case presentation synthesis.

    Validates:
    - HIPAA compliance
    - PHI absence (de-identified content)
    - Medical accuracy
    - Proper disclaimers
    """
    try:
        content = str(result)
        system = get_guardrail_system()

        # Validate output
        validation_result = system.process_with_guardrails(
            user_input="Clinical case synthesis task",
            output=content,
            content_type="clinical_case"
        )

        if not validation_result["success"]:
            blocked_at = validation_result["blocked_at"]
            error_log = validation_result["validation_log"]

            failed_layer = next(
                (log for log in error_log if not log["passed"]),
                {"message": "Unknown validation error"}
            )

            # Provide specific feedback for medical cases
            if "phi" in blocked_at.lower():
                error_message = f"PHI detected in clinical case. Ensure all patient data is de-identified: {failed_layer['message']}"
            elif "hipaa" in blocked_at.lower():
                error_message = f"HIPAA compliance issue. Add proper disclaimers and anonymization indicators: {failed_layer['message']}"
            else:
                error_message = f"Clinical case validation failed at {blocked_at}: {failed_layer['message']}"

            logger.warning(f"Guardrail failure: {error_message}")
            return (False, error_message)

        return (True, content)

    except Exception as e:
        logger.error(f"Error in clinical case synthesis guardrail: {e}")
        return (False, f"Guardrail error: {str(e)}")


# ==========================================
# MEDICAL DIALOGUE GUARDRAILS
# ==========================================

def medical_dialogue_guardrail(result: TaskOutput) -> Tuple[bool, Any]:
    """
    Guardrail for doctor-patient and doctor-doctor dialogues.

    Validates:
    - Appropriate medical communication
    - Content safety
    - Professional tone
    - Medical accuracy
    """
    try:
        content = str(result)
        system = get_guardrail_system()

        # Check for dialogue structure
        if not (":" in content or "Doctor:" in content or "Patient:" in content):
            return (False, "Dialogue must contain proper speaker labels (e.g., 'Doctor:', 'Patient:')")

        # Validate output
        validation_result = system.process_with_guardrails(
            user_input="Medical dialogue generation task",
            output=content,
            content_type="medical_dialogue"
        )

        if not validation_result["success"]:
            blocked_at = validation_result["blocked_at"]
            error_log = validation_result["validation_log"]

            failed_layer = next(
                (log for log in error_log if not log["passed"]),
                {"message": "Unknown validation error"}
            )

            error_message = f"Medical dialogue validation failed at {blocked_at}: {failed_layer['message']}"
            logger.warning(f"Guardrail failure: {error_message}")

            return (False, error_message)

        return (True, content)

    except Exception as e:
        logger.error(f"Error in medical dialogue guardrail: {e}")
        return (False, f"Guardrail error: {str(e)}")


# ==========================================
# COMPLIANCE VALIDATION GUARDRAILS
# ==========================================

def compliance_validation_guardrail(result: TaskOutput) -> Tuple[bool, Any]:
    """
    Guardrail for compliance validation tasks.

    Ensures:
    - All required compliance checks performed
    - Proper documentation
    - Risk assessment completed
    """
    try:
        content = str(result)
        system = get_guardrail_system()

        # Check for required compliance elements
        required_elements = [
            "compliance",
            "validation",
            "approved" or "not approved",
            "risk"
        ]

        content_lower = content.lower()
        missing_elements = [
            elem for elem in required_elements
            if elem.lower() not in content_lower
        ]

        if missing_elements:
            return (False, f"Compliance report missing required elements: {', '.join(missing_elements)}")

        # Validate output
        validation_result = system.process_with_guardrails(
            user_input="Compliance validation task",
            output=content,
            content_type="compliance_report"
        )

        if not validation_result["success"]:
            blocked_at = validation_result["blocked_at"]
            error_log = validation_result["validation_log"]

            failed_layer = next(
                (log for log in error_log if not log["passed"]),
                {"message": "Unknown validation error"}
            )

            error_message = f"Compliance validation failed at {blocked_at}: {failed_layer['message']}"
            logger.warning(f"Guardrail failure: {error_message}")

            return (False, error_message)

        return (True, content)

    except Exception as e:
        logger.error(f"Error in compliance validation guardrail: {e}")
        return (False, f"Guardrail error: {str(e)}")


# ==========================================
# PODCAST SCRIPT GUARDRAILS
# ==========================================

def podcast_script_guardrail(result: TaskOutput) -> Tuple[bool, Any]:
    """
    Guardrail for podcast script generation.

    Validates:
    - Proper script structure
    - Medical disclaimers present
    - Content safety
    - Educational value
    """
    try:
        content = str(result)
        system = get_guardrail_system()

        # Check for required podcast elements
        required_elements = [
            "introduction",
            "educational" or "education",
            "disclaimer" or "not medical advice"
        ]

        content_lower = content.lower()
        missing_elements = [
            elem for elem in required_elements
            if not any(part in content_lower for part in elem.split(" or "))
        ]

        if missing_elements:
            return (False, f"Podcast script missing required elements: {', '.join(missing_elements)}")

        # Validate output
        validation_result = system.process_with_guardrails(
            user_input="Podcast script generation task",
            output=content,
            content_type="medical_education"
        )

        if not validation_result["success"]:
            blocked_at = validation_result["blocked_at"]
            error_log = validation_result["validation_log"]

            failed_layer = next(
                (log for log in error_log if not log["passed"]),
                {"message": "Unknown validation error"}
            )

            error_message = f"Podcast script validation failed at {blocked_at}: {failed_layer['message']}"
            logger.warning(f"Guardrail failure: {error_message}")

            return (False, error_message)

        return (True, content)

    except Exception as e:
        logger.error(f"Error in podcast script guardrail: {e}")
        return (False, f"Guardrail error: {str(e)}")


# ==========================================
# QUALITY ASSURANCE GUARDRAILS
# ==========================================

def quality_assurance_guardrail(result: TaskOutput) -> Tuple[bool, Any]:
    """
    Guardrail for final quality assurance review.

    Validates:
    - Comprehensive review performed
    - Quality score provided
    - Approval status clear
    - Recommendations included
    """
    try:
        content = str(result)
        system = get_guardrail_system()

        # Check for required QA elements
        required_elements = [
            "quality",
            "review",
            "approved" or "not approved" or "approval status",
            "score" or "rating"
        ]

        content_lower = content.lower()
        missing_elements = [
            elem for elem in required_elements
            if not any(part in content_lower for part in elem.split(" or "))
        ]

        if missing_elements:
            return (False, f"Quality assurance report missing required elements: {', '.join(missing_elements)}")

        # Validate output
        validation_result = system.process_with_guardrails(
            user_input="Quality assurance review task",
            output=content,
            content_type="quality_report"
        )

        if not validation_result["success"]:
            blocked_at = validation_result["blocked_at"]
            error_log = validation_result["validation_log"]

            failed_layer = next(
                (log for log in error_log if not log["passed"]),
                {"message": "Unknown validation error"}
            )

            error_message = f"Quality assurance validation failed at {blocked_at}: {failed_layer['message']}"
            logger.warning(f"Guardrail failure: {error_message}")

            return (False, error_message)

        return (True, content)

    except Exception as e:
        logger.error(f"Error in quality assurance guardrail: {e}")
        return (False, f"Guardrail error: {str(e)}")


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def create_medical_guardrail(
    check_phi: bool = True,
    check_terminology: bool = True,
    check_facts: bool = True,
    content_type: str = "medical_education"
):
    """
    Create a custom medical guardrail function.

    Args:
        check_phi: Enable PHI detection
        check_terminology: Enable medical terminology validation
        check_facts: Enable medical fact checking
        content_type: Type of content being validated

    Returns:
        Guardrail function compatible with CrewAI tasks
    """
    def custom_guardrail(result: TaskOutput) -> Tuple[bool, Any]:
        try:
            content = str(result)
            system = get_guardrail_system()

            validation_result = system.process_with_guardrails(
                user_input=f"Custom {content_type} task",
                output=content,
                content_type=content_type
            )

            if not validation_result["success"]:
                failed_layer = next(
                    (log for log in validation_result["validation_log"] if not log["passed"]),
                    {"message": "Unknown validation error"}
                )
                return (False, f"Validation failed: {failed_layer['message']}")

            return (True, content)

        except Exception as e:
            logger.error(f"Error in custom guardrail: {e}")
            return (False, f"Guardrail error: {str(e)}")

    return custom_guardrail


def create_compliance_guardrail(strict: bool = True):
    """
    Create a HIPAA compliance guardrail.

    Args:
        strict: If True, fail on any compliance issues; if False, warn only

    Returns:
        Guardrail function compatible with CrewAI tasks
    """
    return compliance_validation_guardrail if strict else lambda result: (True, str(result))


def create_quality_guardrail(min_quality_score: float = 0.8):
    """
    Create a quality assurance guardrail.

    Args:
        min_quality_score: Minimum quality score (0.0-1.0)

    Returns:
        Guardrail function compatible with CrewAI tasks
    """
    return quality_assurance_guardrail
