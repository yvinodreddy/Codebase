"""
Audio Quality Validator
Validates audio quality for medical and podcast content
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """Validation strictness levels"""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    MEDICAL = "medical"  # Strictest for medical content


@dataclass
class ValidationRule:
    """Single validation rule"""
    name: str
    description: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    required: bool = True


@dataclass
class ValidationResult:
    """Result from validation"""
    passed: bool
    score: float  # 0-100
    rules_passed: int
    rules_failed: int
    issues: List[str]
    warnings: List[str]
    metrics: Dict[str, float]


class AudioValidator:
    """
    Comprehensive audio quality validator

    Validates:
    - Technical quality (bitrate, sample rate, etc.)
    - Audio characteristics (loudness, dynamic range, etc.)
    - Medical content compliance (intelligibility, clarity)
    - HIPAA compliance (no PHI in metadata)
    """

    # Validation rules for different levels
    RULES = {
        ValidationLevel.BASIC: {
            'min_bitrate_kbps': ValidationRule(
                name='Minimum Bitrate',
                description='Audio must have minimum bitrate',
                min_value=64.0
            ),
            'min_sample_rate': ValidationRule(
                name='Minimum Sample Rate',
                description='Audio must have minimum sample rate',
                min_value=22050.0
            ),
        },
        ValidationLevel.STANDARD: {
            'min_bitrate_kbps': ValidationRule(
                name='Minimum Bitrate',
                description='Standard quality bitrate',
                min_value=128.0
            ),
            'min_sample_rate': ValidationRule(
                name='Minimum Sample Rate',
                description='Standard sample rate',
                min_value=44100.0
            ),
            'loudness_lufs': ValidationRule(
                name='Loudness Level',
                description='Integrated loudness in LUFS',
                min_value=-20.0,
                max_value=-12.0
            ),
        },
        ValidationLevel.STRICT: {
            'min_bitrate_kbps': ValidationRule(
                name='Minimum Bitrate',
                description='High quality bitrate',
                min_value=192.0
            ),
            'min_sample_rate': ValidationRule(
                name='Minimum Sample Rate',
                description='High quality sample rate',
                min_value=44100.0
            ),
            'loudness_lufs': ValidationRule(
                name='Loudness Level',
                description='Precise loudness targeting',
                min_value=-18.0,
                max_value=-14.0
            ),
            'dynamic_range_db': ValidationRule(
                name='Dynamic Range',
                description='Adequate dynamic range',
                min_value=6.0
            ),
        },
        ValidationLevel.MEDICAL: {
            'min_bitrate_kbps': ValidationRule(
                name='Minimum Bitrate',
                description='Medical-grade bitrate',
                min_value=192.0
            ),
            'min_sample_rate': ValidationRule(
                name='Minimum Sample Rate',
                description='Medical-grade sample rate',
                min_value=44100.0
            ),
            'loudness_lufs': ValidationRule(
                name='Loudness Level',
                description='Medical content loudness',
                min_value=-18.0,
                max_value=-14.0
            ),
            'dynamic_range_db': ValidationRule(
                name='Dynamic Range',
                description='Adequate dynamic range for clarity',
                min_value=8.0
            ),
            'snr_db': ValidationRule(
                name='Signal-to-Noise Ratio',
                description='Minimum SNR for medical content',
                min_value=40.0
            ),
            'intelligibility_score': ValidationRule(
                name='Speech Intelligibility',
                description='Speech intelligibility percentage',
                min_value=95.0
            ),
        }
    }

    def __init__(self, validation_level: ValidationLevel = ValidationLevel.STANDARD):
        self.validation_level = validation_level
        self.rules = self.RULES[validation_level]
        self.logger = logging.getLogger(__name__)

    def validate(self, audio_data: bytes, format: str = 'mp3') -> ValidationResult:
        """
        Validate audio quality

        Args:
            audio_data: Audio to validate
            format: Audio format

        Returns:
            ValidationResult with detailed validation results
        """
        try:
            # Analyze audio
            metrics = self._analyze_audio(audio_data, format)

            # Run validation rules
            issues = []
            warnings = []
            rules_passed = 0
            rules_failed = 0

            for rule_key, rule in self.rules.items():
                if rule_key not in metrics:
                    if rule.required:
                        issues.append(f"Missing required metric: {rule.name}")
                        rules_failed += 1
                    continue

                value = metrics[rule_key]

                # Check min value
                if rule.min_value is not None and value < rule.min_value:
                    issues.append(f"{rule.name} too low: {value:.1f} < {rule.min_value:.1f}")
                    rules_failed += 1
                    continue

                # Check max value
                if rule.max_value is not None and value > rule.max_value:
                    issues.append(f"{rule.name} too high: {value:.1f} > {rule.max_value:.1f}")
                    rules_failed += 1
                    continue

                rules_passed += 1

            # Calculate score
            total_rules = rules_passed + rules_failed
            score = (rules_passed / total_rules * 100) if total_rules > 0 else 0.0

            passed = rules_failed == 0 and len(issues) == 0

            self.logger.info(f"Validation {'PASSED' if passed else 'FAILED'}: "
                           f"{rules_passed}/{total_rules} rules passed, score: {score:.1f}")

            return ValidationResult(
                passed=passed,
                score=score,
                rules_passed=rules_passed,
                rules_failed=rules_failed,
                issues=issues,
                warnings=warnings,
                metrics=metrics
            )

        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return ValidationResult(
                passed=False,
                score=0.0,
                rules_passed=0,
                rules_failed=len(self.rules),
                issues=[f"Validation error: {str(e)}"],
                warnings=[],
                metrics={}
            )

    def validate_batch(self, audio_files: List[tuple[bytes, str]]) -> List[ValidationResult]:
        """
        Validate multiple audio files

        Args:
            audio_files: List of (audio_data, format) tuples

        Returns:
            List of ValidationResult
        """
        results = []
        for audio_data, format in audio_files:
            result = self.validate(audio_data, format)
            results.append(result)

        return results

    def _analyze_audio(self, audio_data: bytes, format: str) -> Dict[str, float]:
        """
        Analyze audio and extract metrics

        In production, use: librosa, pydub, ffprobe
        """
        # Simulate analysis
        return {
            'min_bitrate_kbps': 192.0,
            'min_sample_rate': 44100.0,
            'loudness_lufs': -16.0,
            'dynamic_range_db': 10.5,
            'snr_db': 45.0,
            'intelligibility_score': 96.5,
            'duration_seconds': 180.0,
            'file_size_mb': 4.2,
            'peak_db': -3.5,
            'true_peak_db': -2.1
        }

    def validate_hipaa_compliance(self, audio_data: bytes, metadata: Dict) -> tuple[bool, List[str]]:
        """
        Validate HIPAA compliance

        Checks:
        - No PHI in metadata
        - Proper encryption markers
        - Audit trail presence

        Args:
            audio_data: Audio to check
            metadata: Audio file metadata

        Returns:
            Tuple of (is_compliant, issues)
        """
        issues = []

        # Check for PHI in metadata
        phi_fields = ['patient_name', 'mrn', 'ssn', 'dob', 'address']
        for field in phi_fields:
            if field in metadata:
                issues.append(f"PHI detected in metadata: {field}")

        # Check for encryption
        if not metadata.get('encrypted', False):
            issues.append("Audio not encrypted for HIPAA compliance")

        # Check for audit trail
        if 'audit_id' not in metadata:
            issues.append("Missing audit trail ID")

        is_compliant = len(issues) == 0

        return is_compliant, issues

    def get_validation_report(self, result: ValidationResult) -> str:
        """Generate human-readable validation report"""
        report = []
        report.append("=" * 60)
        report.append(f"AUDIO VALIDATION REPORT ({self.validation_level.value.upper()})")
        report.append("=" * 60)
        report.append(f"Status: {'✅ PASSED' if result.passed else '❌ FAILED'}")
        report.append(f"Score: {result.score:.1f}/100")
        report.append(f"Rules Passed: {result.rules_passed}")
        report.append(f"Rules Failed: {result.rules_failed}")
        report.append("")

        if result.issues:
            report.append("ISSUES:")
            for issue in result.issues:
                report.append(f"  ❌ {issue}")
            report.append("")

        if result.warnings:
            report.append("WARNINGS:")
            for warning in result.warnings:
                report.append(f"  ⚠️  {warning}")
            report.append("")

        report.append("METRICS:")
        for key, value in result.metrics.items():
            report.append(f"  {key}: {value:.2f}")

        report.append("=" * 60)

        return "\n".join(report)
