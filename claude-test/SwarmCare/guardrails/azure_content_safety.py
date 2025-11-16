"""
Azure AI Content Safety Integration
Implements Prompt Shields, Content Filtering, and Groundedness Detection
"""

import os
import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
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


class AzureContentSafetyValidator:
    """
    Azure AI Content Safety API integration for text analysis.
    Checks for: Hate, Sexual, Violence, Self-Harm content.
    """

    def __init__(self):
        self.endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("CONTENT_SAFETY_KEY")
        self.api_version = os.getenv("CONTENT_SAFETY_API_VERSION", "2024-09-01")

        if not self.endpoint or not self.key:
            raise ValueError("CONTENT_SAFETY_ENDPOINT and CONTENT_SAFETY_KEY must be set in environment")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(requests.RequestException)
    )
    def analyze_text(self, text: str, threshold: int = 2) -> ValidationResult:
        """
        Analyze text for harmful content.

        Args:
            text: Text to analyze
            threshold: Severity threshold (0=Safe, 2=Low, 4=Medium, 6=High)

        Returns:
            ValidationResult with analysis results
        """
        try:
            url = f"{self.endpoint}/contentsafety/text:analyze?api-version={self.api_version}"

            headers = {
                "Ocp-Apim-Subscription-Key": self.key,
                "Content-Type": "application/json"
            }

            payload = {
                "text": text[:10000],  # Max 10,000 characters
                "categories": ["Hate", "Sexual", "Violence", "SelfHarm"],
                "outputType": "FourSeverityLevels"
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()

            # Process results
            blocked_categories = []
            max_severity = 0

            for category_analysis in result.get("categoriesAnalysis", []):
                category_name = category_analysis.get("category")
                severity = category_analysis.get("severity", 0)

                max_severity = max(max_severity, severity)

                if severity >= threshold:
                    blocked_categories.append({
                        "category": category_name,
                        "severity": severity
                    })

            if blocked_categories:
                return ValidationResult(
                    passed=False,
                    layer="azure_content_safety",
                    message=f"Content contains harmful material: {blocked_categories}",
                    severity=max_severity,
                    details={"blocked_categories": blocked_categories, "raw_result": result}
                )

            return ValidationResult(
                passed=True,
                layer="azure_content_safety",
                message="Content is safe",
                severity=max_severity,
                details={"categories_analysis": result.get("categoriesAnalysis")}
            )

        except requests.RequestException as e:
            logger.error(f"Azure Content Safety API error: {e}")
            return ValidationResult(
                passed=False,
                layer="azure_content_safety",
                message=f"API error: {str(e)}",
                details={"error": str(e)}
            )
        except Exception as e:
            logger.error(f"Unexpected error in content safety validation: {e}")
            return ValidationResult(
                passed=False,
                layer="azure_content_safety",
                message=f"Validation error: {str(e)}",
                details={"error": str(e)}
            )


class PromptShieldsValidator:
    """
    Azure Prompt Shields for jailbreak and injection attack detection.
    """

    def __init__(self):
        self.endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("CONTENT_SAFETY_KEY")
        self.api_version = os.getenv("CONTENT_SAFETY_API_VERSION", "2024-09-01")

        if not self.endpoint or not self.key:
            raise ValueError("CONTENT_SAFETY_ENDPOINT and CONTENT_SAFETY_KEY must be set in environment")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(requests.RequestException)
    )
    def check_prompt_safety(
        self,
        user_prompt: str,
        documents: Optional[List[str]] = None
    ) -> ValidationResult:
        """
        Check if prompt contains jailbreak attempts or injection attacks.

        Args:
            user_prompt: User's input text
            documents: Optional list of external documents being processed

        Returns:
            ValidationResult with safety status
        """
        try:
            url = f"{self.endpoint}/contentsafety/text:shieldPrompt?api-version={self.api_version}"

            headers = {
                "Ocp-Apim-Subscription-Key": self.key,
                "Content-Type": "application/json"
            }

            payload = {
                "userPrompt": user_prompt[:10000]
            }

            if documents:
                payload["documents"] = [doc[:10000] for doc in documents]

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()

            # Check for attacks
            user_attack = result.get("userPromptAnalysis", {}).get("attackDetected", False)
            doc_attacks = [
                doc.get("attackDetected", False)
                for doc in result.get("documentsAnalysis", [])
            ]

            attack_detected = user_attack or any(doc_attacks)

            if attack_detected:
                attack_details = {
                    "user_prompt_attack": user_attack,
                    "document_attacks": doc_attacks
                }
                return ValidationResult(
                    passed=False,
                    layer="prompt_shields",
                    message="Jailbreak or injection attack detected",
                    details={"attack_details": attack_details, "raw_result": result}
                )

            return ValidationResult(
                passed=True,
                layer="prompt_shields",
                message="No security threats detected",
                details={"raw_result": result}
            )

        except requests.RequestException as e:
            logger.error(f"Prompt Shields API error: {e}")
            return ValidationResult(
                passed=False,
                layer="prompt_shields",
                message=f"API error: {str(e)}",
                details={"error": str(e)}
            )
        except Exception as e:
            logger.error(f"Unexpected error in prompt shields validation: {e}")
            return ValidationResult(
                passed=False,
                layer="prompt_shields",
                message=f"Validation error: {str(e)}",
                details={"error": str(e)}
            )


class GroundednessDetector:
    """
    Azure Groundedness Detection for validating AI outputs against source material.
    Critical for RAG-based medical applications.
    """

    def __init__(self):
        self.endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("CONTENT_SAFETY_KEY")
        self.api_version = os.getenv("CONTENT_SAFETY_API_VERSION", "2024-09-01")
        self.threshold = int(os.getenv("GUARDRAIL_GROUNDEDNESS_THRESHOLD", "20"))

        if not self.endpoint or not self.key:
            raise ValueError("CONTENT_SAFETY_ENDPOINT and CONTENT_SAFETY_KEY must be set in environment")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(requests.RequestException)
    )
    def detect_groundedness(
        self,
        output_text: str,
        source_documents: List[str],
        query: Optional[str] = None,
        domain: str = "Medical"
    ) -> ValidationResult:
        """
        Check if output is grounded in source material.

        Args:
            output_text: AI-generated text to validate
            source_documents: Source documents used for generation
            query: Optional user query
            domain: Domain type (Medical, Generic, etc.)

        Returns:
            ValidationResult with groundedness status
        """
        if not source_documents:
            return ValidationResult(
                passed=True,
                layer="groundedness_detection",
                message="Skipped (no source documents provided)"
            )

        try:
            url = f"{self.endpoint}/contentsafety/text:detectGroundedness?api-version={self.api_version}"

            headers = {
                "Ocp-Apim-Subscription-Key": self.key,
                "Content-Type": "application/json"
            }

            payload = {
                "domain": domain,
                "task": "QnA",
                "text": output_text[:10000],
                "groundingSources": [doc[:10000] for doc in source_documents],
                "reasoning": False
            }

            if query:
                payload["qna"] = {"query": query}

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()

            ungrounded = result.get("ungroundedDetected", False)
            percentage = result.get("ungroundedPercentage", 0.0)

            if ungrounded and percentage > self.threshold:
                return ValidationResult(
                    passed=False,
                    layer="groundedness_detection",
                    message=f"Output contains {percentage}% ungrounded content (threshold: {self.threshold}%)",
                    severity=int(percentage),
                    details={"ungrounded_percentage": percentage, "raw_result": result}
                )

            return ValidationResult(
                passed=True,
                layer="groundedness_detection",
                message=f"Output is grounded (ungrounded: {percentage}%)",
                severity=int(percentage),
                details={"ungrounded_percentage": percentage, "raw_result": result}
            )

        except requests.RequestException as e:
            logger.warning(f"Groundedness Detection API error: {e}")
            # Don't fail on groundedness errors in production
            return ValidationResult(
                passed=True,
                layer="groundedness_detection",
                message=f"Skipped due to API error: {str(e)}",
                details={"error": str(e), "non_blocking": True}
            )
        except Exception as e:
            logger.warning(f"Unexpected error in groundedness detection: {e}")
            return ValidationResult(
                passed=True,
                layer="groundedness_detection",
                message=f"Skipped due to error: {str(e)}",
                details={"error": str(e), "non_blocking": True}
            )
