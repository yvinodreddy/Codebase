"""
Prompt Preprocessor
Analyzes and classifies user prompts to determine optimal processing strategy
"""

import logging
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class PromptAnalysis:
    """Analysis result from prompt preprocessing"""
    intent_type: str  # question, task, code_generation, analysis, multi_step, etc.
    complexity: str  # simple, moderate, complex, very_complex
    required_components: List[str]  # Which agent framework components needed
    requires_search: bool
    requires_verification: bool
    requires_code_generation: bool
    requires_parallel_processing: bool
    estimated_iterations: int
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "intent_type": self.intent_type,
            "complexity": self.complexity,
            "required_components": self.required_components,
            "requires_search": self.requires_search,
            "requires_verification": self.requires_verification,
            "requires_code_generation": self.requires_code_generation,
            "requires_parallel_processing": self.requires_parallel_processing,
            "estimated_iterations": self.estimated_iterations,
            "confidence": self.confidence,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


class PromptPreprocessor:
    """
    Intelligent prompt preprocessor that analyzes user input to determine
    optimal processing strategy for maximum accuracy.

    This is the first stage of the orchestration pipeline.
    """

    # Intent patterns
    INTENT_PATTERNS = {
        "question": [
            r"^(what|how|why|when|where|who|which|can you explain|tell me about)",
            r"\?$"
        ],
        "code_generation": [
            r"(write|create|generate|implement|build|develop)\s+(code|function|class|script|program)",
            r"(python|javascript|java|c\+\+|code|program)",
            r"(implement|create)\s+\w+\s+(that|to|for)"
        ],
        "analysis": [
            r"(analyze|examine|evaluate|assess|review|investigate|study)",
            r"(what\s+(is|are)\s+the\s+(difference|similarity|relationship))",
            r"(compare|contrast)"
        ],
        "task": [
            r"(do|perform|execute|run|process|handle)",
            r"(help me|assist|guide me)"
        ],
        "multi_step": [
            r"(first|then|next|after that|finally|step)",
            r"(multiple|several|various)\s+(steps|tasks|actions)"
        ],
        "search": [
            r"(find|search|locate|look for|discover)",
            r"(where is|show me|list all)"
        ]
    }

    # Complexity indicators
    COMPLEXITY_INDICATORS = {
        "very_complex": [
            r"(comprehensive|complete|full|entire|all|everything)",
            r"(multiple|several|many)\s+(components|parts|sections|features)",
            r"(integrate|orchestrate|coordinate)",
            r"(production|enterprise|scale)"
        ],
        "complex": [
            r"(system|architecture|framework|infrastructure)",
            r"(integrate|combine|merge)",
            r"(optimize|improve|enhance)"
        ],
        "moderate": [
            r"(implement|create|build|develop)",
            r"(function|class|module)"
        ],
        "simple": [
            r"^(what|how|why|is|can)",
            r"(simple|basic|quick|easy)"
        ]
    }

    def __init__(self):
        """Initialize prompt preprocessor"""
        self.analysis_log: List[PromptAnalysis] = []
        logger.info("PromptPreprocessor initialized")

    def analyze_prompt(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> PromptAnalysis:
        """
        Analyze prompt to determine optimal processing strategy.

        Args:
            prompt: User's input prompt
            context: Optional context (previous messages, user preferences, etc.)

        Returns:
            PromptAnalysis with processing strategy
        """
        logger.info("Analyzing prompt...")

        prompt_lower = prompt.lower()

        # 1. Classify intent
        intent_type = self._classify_intent(prompt_lower)
        logger.debug(f"Intent classified as: {intent_type}")

        # 2. Assess complexity
        complexity = self._assess_complexity(prompt_lower)
        logger.debug(f"Complexity assessed as: {complexity}")

        # 3. Determine required components
        required_components = self._determine_required_components(
            intent_type, complexity, prompt_lower
        )
        logger.debug(f"Required components: {required_components}")

        # 4. Analyze specific requirements
        requires_search = self._requires_search(prompt_lower)
        requires_verification = self._requires_verification(complexity, intent_type)
        requires_code_generation = self._requires_code_generation(intent_type, prompt_lower)
        requires_parallel_processing = self._requires_parallel_processing(complexity, prompt_lower)

        # 5. Estimate iterations needed
        estimated_iterations = self._estimate_iterations(complexity, intent_type)

        # 6. Calculate confidence
        confidence = self._calculate_analysis_confidence(prompt, intent_type, complexity)

        # 7. Extract metadata
        metadata = self._extract_metadata(prompt)

        analysis = PromptAnalysis(
            intent_type=intent_type,
            complexity=complexity,
            required_components=required_components,
            requires_search=requires_search,
            requires_verification=requires_verification,
            requires_code_generation=requires_code_generation,
            requires_parallel_processing=requires_parallel_processing,
            estimated_iterations=estimated_iterations,
            confidence=confidence,
            metadata=metadata
        )

        self.analysis_log.append(analysis)

        logger.info(
            f"Prompt analysis complete: intent={intent_type}, complexity={complexity}, "
            f"components={len(required_components)}, confidence={confidence:.2f}"
        )

        return analysis

    def _classify_intent(self, prompt: str) -> str:
        """Classify prompt intent"""
        scores = {}

        for intent, patterns in self.INTENT_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, prompt, re.IGNORECASE):
                    score += 1
            scores[intent] = score

        # Return intent with highest score, or "task" as default
        if max(scores.values()) == 0:
            return "task"

        return max(scores.items(), key=lambda x: x[1])[0]

    def _assess_complexity(self, prompt: str) -> str:
        """Assess prompt complexity"""
        # Check from most complex to least
        for complexity in ["very_complex", "complex", "moderate", "simple"]:
            patterns = self.COMPLEXITY_INDICATORS.get(complexity, [])
            for pattern in patterns:
                if re.search(pattern, prompt, re.IGNORECASE):
                    return complexity

        # Check length as fallback
        word_count = len(prompt.split())
        if word_count > 100:
            return "very_complex"
        elif word_count > 50:
            return "complex"
        elif word_count > 20:
            return "moderate"
        else:
            return "simple"

    def _determine_required_components(
        self, intent: str, complexity: str, prompt: str
    ) -> List[str]:
        """Determine which agent framework components are needed"""
        components = []

        # Always include context manager for long-running tasks
        if complexity in ["complex", "very_complex"]:
            components.append("context_manager")

        # Add feedback loop for iterative tasks
        if complexity in ["moderate", "complex", "very_complex"]:
            components.append("feedback_loop")

        # Add search for information retrieval
        if intent in ["search", "question"] or "find" in prompt or "search" in prompt:
            components.append("agentic_search")

        # Add code generator for code tasks
        if intent == "code_generation" or "code" in prompt or "implement" in prompt:
            components.append("code_generator")

        # Add verification for all non-simple tasks
        if complexity != "simple":
            components.append("verification_system")

        # Add subagent orchestrator for parallel tasks
        if complexity == "very_complex" or "multiple" in prompt or "parallel" in prompt:
            components.append("subagent_orchestrator")

        # Add MCP integration if external services mentioned
        if any(service in prompt for service in ["slack", "github", "google", "email", "calendar"]):
            components.append("mcp_integration")

        # Ensure at least feedback_loop is included
        if not components:
            components.append("feedback_loop")

        return components

    def _requires_search(self, prompt: str) -> bool:
        """Check if prompt requires search capabilities"""
        search_keywords = [
            "find", "search", "locate", "look for", "discover",
            "where is", "show me", "list all", "what files",
            "which functions", "analyze codebase"
        ]
        return any(keyword in prompt for keyword in search_keywords)

    def _requires_verification(self, complexity: str, intent: str) -> bool:
        """Check if verification is required"""
        # All complex tasks need verification
        if complexity in ["complex", "very_complex"]:
            return True
        # Code generation always needs verification
        if intent == "code_generation":
            return True
        return False

    def _requires_code_generation(self, intent: str, prompt: str) -> bool:
        """Check if code generation is required"""
        if intent == "code_generation":
            return True

        code_keywords = [
            "write code", "generate code", "implement", "create function",
            "create class", "write script", "develop", "build program"
        ]
        return any(keyword in prompt for keyword in code_keywords)

    def _requires_parallel_processing(self, complexity: str, prompt: str) -> bool:
        """Check if parallel processing is beneficial"""
        if complexity == "very_complex":
            return True

        parallel_indicators = [
            "multiple", "several", "many", "all", "various",
            "parallel", "simultaneously", "at the same time"
        ]
        return any(indicator in prompt for indicator in parallel_indicators)

    def _estimate_iterations(self, complexity: str, intent: str) -> int:
        """Estimate number of feedback loop iterations needed"""
        base_iterations = {
            "simple": 3,
            "moderate": 5,
            "complex": 8,
            "very_complex": 10
        }

        iterations = base_iterations.get(complexity, 5)

        # Increase for code generation (needs more refinement)
        if intent == "code_generation":
            iterations += 2

        return iterations

    def _calculate_analysis_confidence(
        self, prompt: str, intent: str, complexity: str
    ) -> float:
        """Calculate confidence in the analysis"""
        confidence = 0.7  # Base confidence

        # Higher confidence for clear intents
        if any(re.search(pattern, prompt, re.IGNORECASE)
               for pattern in self.INTENT_PATTERNS.get(intent, [])):
            confidence += 0.15

        # Lower confidence for very complex prompts
        if complexity == "very_complex":
            confidence -= 0.1

        # Higher confidence for specific keywords
        if len(prompt.split()) > 10:  # Detailed prompts = higher confidence
            confidence += 0.1

        return min(max(confidence, 0.0), 1.0)

    def _extract_metadata(self, prompt: str) -> Dict[str, Any]:
        """Extract metadata from prompt"""
        metadata = {
            "word_count": len(prompt.split()),
            "char_count": len(prompt),
            "has_question_mark": "?" in prompt,
            "has_code_block": "```" in prompt or "def " in prompt or "class " in prompt,
            "mentions_file": bool(re.search(r'\.(py|js|java|cpp|txt|md|json|xml)', prompt)),
            "mentions_medical": any(
                term in prompt.lower()
                for term in ["medical", "patient", "doctor", "clinical", "health", "diagnosis"]
            )
        }

        return metadata

    def get_statistics(self) -> Dict[str, Any]:
        """Get preprocessing statistics"""
        if not self.analysis_log:
            return {"error": "No prompts analyzed yet"}

        return {
            "total_prompts": len(self.analysis_log),
            "intents": {
                intent: sum(1 for a in self.analysis_log if a.intent_type == intent)
                for intent in set(a.intent_type for a in self.analysis_log)
            },
            "complexity_distribution": {
                complexity: sum(1 for a in self.analysis_log if a.complexity == complexity)
                for complexity in set(a.complexity for a in self.analysis_log)
            },
            "average_confidence": sum(a.confidence for a in self.analysis_log) / len(self.analysis_log),
            "average_estimated_iterations": sum(a.estimated_iterations for a in self.analysis_log) / len(self.analysis_log)
        }


if __name__ == "__main__":
    # Example usage
    preprocessor = PromptPreprocessor()

    print("=" * 80)
    print("PROMPT PREPROCESSOR EXAMPLE")
    print("=" * 80)

    test_prompts = [
        "What is the difference between supervised and unsupervised learning?",
        "Write a Python function to calculate the Fibonacci sequence",
        "Implement a comprehensive medical AI system with guardrails, feedback loops, and verification",
        "Find all files in the project that contain the word 'guardrail'",
        "Analyze the codebase and identify all security vulnerabilities"
    ]

    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n{i}. Analyzing: {prompt[:60]}...")
        analysis = preprocessor.analyze_prompt(prompt)

        print(f"   Intent: {analysis.intent_type}")
        print(f"   Complexity: {analysis.complexity}")
        print(f"   Required components: {', '.join(analysis.required_components)}")
        print(f"   Estimated iterations: {analysis.estimated_iterations}")
        print(f"   Confidence: {analysis.confidence:.2f}")

    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)
    stats = preprocessor.get_statistics()
    print(json.dumps(stats, indent=2))

    print("\n✅ Example complete")
