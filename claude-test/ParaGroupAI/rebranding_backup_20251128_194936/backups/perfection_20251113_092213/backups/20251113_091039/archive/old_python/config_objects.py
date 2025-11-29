"""
Q3: Configuration Objects for Parameter Lists
Replaces long parameter lists with structured config objects

BEFORE (8+ parameters):
    orchestrator = MasterOrchestrator(
        min_confidence_score=96.0,
        max_refinement_iterations=5,
        enable_guardrails=True,
        guardrail_threshold=2,
        context_window=200000,
        compact_threshold=0.85,
        enable_verification=True,
        verification_methods=['rules', 'code', 'llm']
    )

AFTER (1 config object):
    config = OrchestratorConfig(
        confidence=ConfidenceConfig(min_score=96.0),
        iteration=IterationConfig(max_refinements=5),
        guardrails=GuardrailsConfig(enabled=True, threshold=2),
        context=ContextConfig(window=200000, compact_threshold=0.85),
        verification=VerificationConfig(enabled=True, methods=['rules', 'code', 'llm'])
    )
    orchestrator = MasterOrchestrator(config)

BENEFITS:
- Fewer parameters to pass around
- Self-documenting (grouped by purpose)
- Easy to extend (add new fields to config)
- Validation in one place
- Immutable by default
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


# ==========================================
# ENUMS FOR TYPE SAFETY
# ==========================================

class IntentType(Enum):
    """Prompt intent types"""
    QUESTION = "question"
    CODE_GENERATION = "code_generation"
    TASK = "task"
    ANALYSIS = "analysis"


class ComplexityLevel(Enum):
    """Task complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


class VerificationMethod(Enum):
    """Verification methods"""
    RULES = "rules"
    CODE = "code"
    LLM = "llm"


# ==========================================
# CONFIDENCE CONFIGURATION
# ==========================================

@dataclass(frozen=True)
class ConfidenceConfig:
    """
    Confidence scoring configuration.

    Attributes:
        min_score: Minimum confidence score to accept (0-100)
        production_target: Target confidence for production (99-100)
        verification_threshold: Minimum for individual verifications (90-100)
    """
    min_score: float = 96.0
    production_target: float = 99.0
    verification_threshold: float = 95.0

    def __post_init__(self):
        """Validate configuration"""
        if not 0 <= self.min_score <= 100:
            raise ValueError("min_score must be between 0 and 100")
        if not 0 <= self.production_target <= 100:
            raise ValueError("production_target must be between 0 and 100")
        if not 0 <= self.verification_threshold <= 100:
            raise ValueError("verification_threshold must be between 0 and 100")


# ==========================================
# ITERATION CONFIGURATION
# ==========================================

@dataclass(frozen=True)
class IterationConfig:
    """
    Feedback loop iteration configuration.

    Attributes:
        max_refinements: Maximum refinement iterations (3-10)
        enable_adaptive_limits: Allow extending iterations if making progress
        progress_extension: Additional iterations when making progress (1-5)
    """
    max_refinements: int = 5
    enable_adaptive_limits: bool = True
    progress_extension: int = 3

    def __post_init__(self):
        """Validate configuration"""
        if not 1 <= self.max_refinements <= 20:
            raise ValueError("max_refinements must be between 1 and 20")
        if not 1 <= self.progress_extension <= 10:
            raise ValueError("progress_extension must be between 1 and 10")


# ==========================================
# GUARDRAILS CONFIGURATION
# ==========================================

@dataclass(frozen=True)
class GuardrailsConfig:
    """
    Multi-layer guardrails configuration.

    Attributes:
        enabled: Enable guardrail validation
        content_threshold: Content safety threshold (0-4, higher=stricter)
        enable_prompt_shields: Enable jailbreak prevention
        enable_content_filtering: Enable harmful content detection
        enable_phi_detection: Enable PHI detection
        enable_medical_validation: Enable medical terminology validation
        enable_groundedness_check: Enable factual accuracy checks
        groundedness_threshold: Groundedness score threshold (0-100)
        max_retries: Maximum retries on guardrail failures (1-10)
    """
    enabled: bool = True
    content_threshold: int = 2
    enable_prompt_shields: bool = True
    enable_content_filtering: bool = True
    enable_phi_detection: bool = True
    enable_medical_validation: bool = True
    enable_groundedness_check: bool = True
    groundedness_threshold: int = 20
    max_retries: int = 5

    def __post_init__(self):
        """Validate configuration"""
        if not 0 <= self.content_threshold <= 4:
            raise ValueError("content_threshold must be between 0 and 4")
        if not 0 <= self.groundedness_threshold <= 100:
            raise ValueError("groundedness_threshold must be between 0 and 100")
        if not 1 <= self.max_retries <= 20:
            raise ValueError("max_retries must be between 1 and 20")


# ==========================================
# CONTEXT CONFIGURATION
# ==========================================

@dataclass(frozen=True)
class ContextConfig:
    """
    Context management configuration.

    Attributes:
        window_tokens: Maximum tokens in context (10k-200k)
        compact_threshold: Trigger compaction at this % (0.5-0.95)
        keep_recent: Number of recent messages to preserve (5-20)
        tokens_per_char: Token estimation factor (0.2-0.3)
    """
    window_tokens: int = 200_000
    compact_threshold: float = 0.85
    keep_recent: int = 10
    tokens_per_char: float = 0.25

    def __post_init__(self):
        """Validate configuration"""
        if not 10_000 <= self.window_tokens <= 500_000:
            raise ValueError("window_tokens must be between 10k and 500k")
        if not 0.5 <= self.compact_threshold <= 0.99:
            raise ValueError("compact_threshold must be between 0.5 and 0.99")
        if not 1 <= self.keep_recent <= 50:
            raise ValueError("keep_recent must be between 1 and 50")
        if not 0.1 <= self.tokens_per_char <= 0.5:
            raise ValueError("tokens_per_char must be between 0.1 and 0.5")


# ==========================================
# VERIFICATION CONFIGURATION
# ==========================================

@dataclass(frozen=True)
class VerificationConfig:
    """
    Multi-method verification configuration.

    Attributes:
        enabled: Enable verification
        methods: List of verification methods to use
        require_all_pass: Require all methods to pass (vs. majority)
        llm_verification_threshold: Minimum score for LLM verification (0-100)
    """
    enabled: bool = True
    methods: List[str] = field(default_factory=lambda: ["rules", "code", "llm"])
    require_all_pass: bool = False
    llm_verification_threshold: float = 90.0

    def __post_init__(self):
        """Validate configuration"""
        valid_methods = {"rules", "code", "llm"}
        invalid = set(self.methods) - valid_methods
        if invalid:
            raise ValueError(f"Invalid verification methods: {invalid}")

        if not 0 <= self.llm_verification_threshold <= 100:
            raise ValueError("llm_verification_threshold must be between 0 and 100")


# ==========================================
# SECURITY CONFIGURATION
# ==========================================

@dataclass(frozen=True)
class SecurityConfig:
    """
    Security features configuration.

    Attributes:
        enable_api_key_masking: Mask API keys in logs
        enable_rate_limiting: Enable rate limiting
        rate_limit_calls: Maximum calls per window (100-1000)
        rate_limit_window_seconds: Time window for rate limiting (60-3600)
        enable_input_sanitization: Enable prompt injection prevention
        sanitization_level: Level of sanitization (1-3)
        enable_security_logging: Enable security event logging
    """
    enable_api_key_masking: bool = True
    enable_rate_limiting: bool = True
    rate_limit_calls: int = 500
    rate_limit_window_seconds: int = 360
    enable_input_sanitization: bool = True
    sanitization_level: int = 1  # 1=minimal, 2=balanced, 3=production
    enable_security_logging: bool = True

    def __post_init__(self):
        """Validate configuration"""
        if not 10 <= self.rate_limit_calls <= 10_000:
            raise ValueError("rate_limit_calls must be between 10 and 10,000")
        if not 30 <= self.rate_limit_window_seconds <= 7200:
            raise ValueError("rate_limit_window_seconds must be between 30 and 7200")
        if self.sanitization_level not in [1, 2, 3]:
            raise ValueError("sanitization_level must be 1, 2, or 3")


# ==========================================
# PERFORMANCE CONFIGURATION
# ==========================================

@dataclass(frozen=True)
class PerformanceConfig:
    """
    Performance optimization configuration.

    Attributes:
        enable_parallel_guardrails: Enable P1 (parallel guardrail validation)
        enable_incremental_tokens: Enable P2 (incremental token counting)
        enable_overlapped_iterations: Enable P3 (overlapped iteration execution)
        executor_threads: Number of threads for parallel execution (1-8)
    """
    enable_parallel_guardrails: bool = True
    enable_incremental_tokens: bool = True
    enable_overlapped_iterations: bool = True
    executor_threads: int = 2

    def __post_init__(self):
        """Validate configuration"""
        if not 1 <= self.executor_threads <= 16:
            raise ValueError("executor_threads must be between 1 and 16")


# ==========================================
# MASTER ORCHESTRATOR CONFIGURATION
# ==========================================

@dataclass(frozen=True)
class OrchestratorConfig:
    """
    Q3: Master configuration object for orchestrator.

    This replaces 15+ individual parameters with a single config object.

    Example:
        >>> config = OrchestratorConfig.create_default()
        >>> orchestrator = MasterOrchestrator(config)

        >>> # Customize specific settings
        >>> config = OrchestratorConfig(
        ...     confidence=ConfidenceConfig(min_score=98.0),
        ...     iteration=IterationConfig(max_refinements=10),
        ...     security=SecurityConfig(rate_limit_calls=1000)
        ... )
    """
    confidence: ConfidenceConfig = field(default_factory=ConfidenceConfig)
    iteration: IterationConfig = field(default_factory=IterationConfig)
    guardrails: GuardrailsConfig = field(default_factory=GuardrailsConfig)
    context: ContextConfig = field(default_factory=ContextConfig)
    verification: VerificationConfig = field(default_factory=VerificationConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)

    @staticmethod
    def create_default() -> 'OrchestratorConfig':
        """Create default configuration"""
        return OrchestratorConfig()

    @staticmethod
    def create_production() -> 'OrchestratorConfig':
        """Create production-optimized configuration"""
        return OrchestratorConfig(
            confidence=ConfidenceConfig(min_score=99.0, production_target=99.5),
            iteration=IterationConfig(max_refinements=10, enable_adaptive_limits=True),
            guardrails=GuardrailsConfig(
                enabled=True,
                content_threshold=3,  # Stricter
                enable_prompt_shields=True,
                enable_content_filtering=True,
                enable_phi_detection=True,
                enable_medical_validation=True,
                enable_groundedness_check=True
            ),
            context=ContextConfig(window_tokens=200_000, compact_threshold=0.80),
            verification=VerificationConfig(
                enabled=True,
                methods=["rules", "code", "llm"],
                require_all_pass=True  # Stricter
            ),
            security=SecurityConfig(
                enable_api_key_masking=True,
                enable_rate_limiting=True,
                rate_limit_calls=500,
                rate_limit_window_seconds=360,
                enable_input_sanitization=True,
                sanitization_level=3,  # Production level
                enable_security_logging=True
            ),
            performance=PerformanceConfig(
                enable_parallel_guardrails=True,
                enable_incremental_tokens=True,
                enable_overlapped_iterations=True,
                executor_threads=4
            )
        )

    @staticmethod
    def create_development() -> 'OrchestratorConfig':
        """Create development-friendly configuration"""
        return OrchestratorConfig(
            confidence=ConfidenceConfig(min_score=90.0),
            iteration=IterationConfig(max_refinements=5),
            guardrails=GuardrailsConfig(
                enabled=False,  # Disabled for faster dev iteration
                content_threshold=2
            ),
            context=ContextConfig(window_tokens=100_000, compact_threshold=0.90),
            verification=VerificationConfig(
                enabled=True,
                methods=["rules"],  # Faster verification
                require_all_pass=False
            ),
            security=SecurityConfig(
                enable_api_key_masking=True,
                enable_rate_limiting=False,  # No rate limiting in dev
                enable_input_sanitization=True,
                sanitization_level=1,  # Minimal
                enable_security_logging=False
            ),
            performance=PerformanceConfig(
                enable_parallel_guardrails=False,
                enable_incremental_tokens=True,
                enable_overlapped_iterations=False,
                executor_threads=1
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "confidence": {
                "min_score": self.confidence.min_score,
                "production_target": self.confidence.production_target,
                "verification_threshold": self.confidence.verification_threshold
            },
            "iteration": {
                "max_refinements": self.iteration.max_refinements,
                "enable_adaptive_limits": self.iteration.enable_adaptive_limits,
                "progress_extension": self.iteration.progress_extension
            },
            "guardrails": {
                "enabled": self.guardrails.enabled,
                "content_threshold": self.guardrails.content_threshold,
                "enable_prompt_shields": self.guardrails.enable_prompt_shields,
                "enable_content_filtering": self.guardrails.enable_content_filtering,
                "enable_phi_detection": self.guardrails.enable_phi_detection,
                "enable_medical_validation": self.guardrails.enable_medical_validation,
                "enable_groundedness_check": self.guardrails.enable_groundedness_check,
                "groundedness_threshold": self.guardrails.groundedness_threshold,
                "max_retries": self.guardrails.max_retries
            },
            "context": {
                "window_tokens": self.context.window_tokens,
                "compact_threshold": self.context.compact_threshold,
                "keep_recent": self.context.keep_recent,
                "tokens_per_char": self.context.tokens_per_char
            },
            "verification": {
                "enabled": self.verification.enabled,
                "methods": self.verification.methods,
                "require_all_pass": self.verification.require_all_pass,
                "llm_verification_threshold": self.verification.llm_verification_threshold
            },
            "security": {
                "enable_api_key_masking": self.security.enable_api_key_masking,
                "enable_rate_limiting": self.security.enable_rate_limiting,
                "rate_limit_calls": self.security.rate_limit_calls,
                "rate_limit_window_seconds": self.security.rate_limit_window_seconds,
                "enable_input_sanitization": self.security.enable_input_sanitization,
                "sanitization_level": self.security.sanitization_level,
                "enable_security_logging": self.security.enable_security_logging
            },
            "performance": {
                "enable_parallel_guardrails": self.performance.enable_parallel_guardrails,
                "enable_incremental_tokens": self.performance.enable_incremental_tokens,
                "enable_overlapped_iterations": self.performance.enable_overlapped_iterations,
                "executor_threads": self.performance.executor_threads
            }
        }


# ==========================================
# USAGE EXAMPLES
# ==========================================

if __name__ == "__main__":
    print("=" * 70)
    print("Q3: CONFIGURATION OBJECTS EXAMPLES")
    print("=" * 70)

    # Example 1: Default configuration
    print("\n1. DEFAULT CONFIGURATION:")
    print("-" * 70)
    default_config = OrchestratorConfig.create_default()
    print(f"Min confidence: {default_config.confidence.min_score}%")
    print(f"Max iterations: {default_config.iteration.max_refinements}")
    print(f"Guardrails enabled: {default_config.guardrails.enabled}")
    print(f"Rate limit: {default_config.security.rate_limit_calls} calls / {default_config.security.rate_limit_window_seconds}s")

    # Example 2: Production configuration
    print("\n2. PRODUCTION CONFIGURATION:")
    print("-" * 70)
    prod_config = OrchestratorConfig.create_production()
    print(f"Min confidence: {prod_config.confidence.min_score}%")
    print(f"Max iterations: {prod_config.iteration.max_refinements}")
    print(f"Sanitization level: {prod_config.security.sanitization_level} (production)")
    print(f"Verification: {prod_config.verification.methods}")
    print(f"Require all pass: {prod_config.verification.require_all_pass}")

    # Example 3: Development configuration
    print("\n3. DEVELOPMENT CONFIGURATION:")
    print("-" * 70)
    dev_config = OrchestratorConfig.create_development()
    print(f"Min confidence: {dev_config.confidence.min_score}%")
    print(f"Guardrails enabled: {dev_config.guardrails.enabled}")
    print(f"Rate limiting: {dev_config.security.enable_rate_limiting}")
    print(f"Verification methods: {dev_config.verification.methods}")

    # Example 4: Custom configuration
    print("\n4. CUSTOM CONFIGURATION:")
    print("-" * 70)
    custom_config = OrchestratorConfig(
        confidence=ConfidenceConfig(min_score=98.0),
        iteration=IterationConfig(max_refinements=8),
        security=SecurityConfig(
            rate_limit_calls=1000,
            rate_limit_window_seconds=600,
            sanitization_level=2
        ),
        performance=PerformanceConfig(
            enable_parallel_guardrails=True,
            enable_incremental_tokens=True,
            enable_overlapped_iterations=True,
            executor_threads=4
        )
    )
    print(f"Min confidence: {custom_config.confidence.min_score}%")
    print(f"Max iterations: {custom_config.iteration.max_refinements}")
    print(f"Rate limit: {custom_config.security.rate_limit_calls} calls / {custom_config.security.rate_limit_window_seconds}s")
    print(f"Executor threads: {custom_config.performance.executor_threads}")

    # Example 5: Export to dictionary
    print("\n5. EXPORT TO DICTIONARY:")
    print("-" * 70)
    config_dict = default_config.to_dict()
    import json
    print(json.dumps(config_dict, indent=2))

    # Example 6: Validation
    print("\n6. CONFIGURATION VALIDATION:")
    print("-" * 70)
    try:
        invalid = OrchestratorConfig(
            confidence=ConfidenceConfig(min_score=150.0)  # Invalid
        )
    except ValueError as e:
        print(f"✅ Validation caught error: {e}")

    print("\n" + "=" * 70)
    print("✅ Q3 implementation complete!")
    print("=" * 70)
    print("\nBENEFITS:")
    print("- Replaced 15+ parameters with 1 config object")
    print("- Self-documenting with grouped settings")
    print("- Built-in validation")
    print("- Immutable by default (frozen dataclasses)")
    print("- Easy presets (default/production/development)")
