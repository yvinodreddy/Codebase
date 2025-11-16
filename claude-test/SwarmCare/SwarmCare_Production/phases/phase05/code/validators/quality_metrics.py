"""
Audio Quality Metrics Calculator
Calculates comprehensive audio quality metrics
"""

from typing import Dict
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class QualityScore:
    """Comprehensive quality score"""
    overall_score: float  # 0-100
    technical_score: float  # 0-100
    perceptual_score: float  # 0-100
    medical_suitability_score: float  # 0-100
    grade: str  # A+, A, B, C, D, F


class QualityMetrics:
    """
    Calculate comprehensive audio quality metrics

    Metrics include:
    - Technical: bitrate, sample rate, codec efficiency
    - Perceptual: loudness, dynamic range, distortion
    - Medical: intelligibility, clarity, consistency
    """

    # Quality grade thresholds
    GRADE_THRESHOLDS = {
        'A+': 95.0,
        'A': 85.0,
        'B': 75.0,
        'C': 65.0,
        'D': 50.0,
        'F': 0.0
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def calculate_quality_score(self, audio_data: bytes, format: str = 'mp3') -> QualityScore:
        """
        Calculate comprehensive quality score

        Args:
            audio_data: Audio to analyze
            format: Audio format

        Returns:
            QualityScore with detailed scores
        """
        try:
            # Analyze audio
            metrics = self._extract_metrics(audio_data, format)

            # Calculate sub-scores
            technical = self._calculate_technical_score(metrics)
            perceptual = self._calculate_perceptual_score(metrics)
            medical = self._calculate_medical_suitability_score(metrics)

            # Calculate overall score (weighted average)
            overall = (technical * 0.3 + perceptual * 0.4 + medical * 0.3)

            # Determine grade
            grade = self._determine_grade(overall)

            return QualityScore(
                overall_score=overall,
                technical_score=technical,
                perceptual_score=perceptual,
                medical_suitability_score=medical,
                grade=grade
            )

        except Exception as e:
            self.logger.error(f"Quality score calculation failed: {e}")
            return QualityScore(
                overall_score=0.0,
                technical_score=0.0,
                perceptual_score=0.0,
                medical_suitability_score=0.0,
                grade='F'
            )

    def _extract_metrics(self, audio_data: bytes, format: str) -> Dict[str, float]:
        """Extract audio metrics"""
        # In production, use librosa, essentia, or ffprobe
        return {
            'bitrate_kbps': 192.0,
            'sample_rate_hz': 44100.0,
            'channels': 2,
            'duration_sec': 180.0,
            'loudness_lufs': -16.0,
            'peak_db': -3.2,
            'true_peak_db': -1.8,
            'dynamic_range_db': 10.5,
            'snr_db': 45.0,
            'thd_percent': 0.5,  # Total Harmonic Distortion
            'intelligibility_pct': 96.5,
            'consistency_score': 92.0
        }

    def _calculate_technical_score(self, metrics: Dict[str, float]) -> float:
        """Calculate technical quality score"""
        score = 0.0

        # Bitrate score (0-30 points)
        bitrate = metrics.get('bitrate_kbps', 0)
        if bitrate >= 192:
            score += 30
        elif bitrate >= 128:
            score += 25
        elif bitrate >= 96:
            score += 20
        else:
            score += 10

        # Sample rate score (0-30 points)
        sample_rate = metrics.get('sample_rate_hz', 0)
        if sample_rate >= 48000:
            score += 30
        elif sample_rate >= 44100:
            score += 28
        elif sample_rate >= 32000:
            score += 20
        else:
            score += 10

        # Channels score (0-10 points)
        channels = metrics.get('channels', 1)
        score += 10 if channels == 2 else 7

        # SNR score (0-30 points)
        snr = metrics.get('snr_db', 0)
        if snr >= 45:
            score += 30
        elif snr >= 40:
            score += 25
        elif snr >= 35:
            score += 20
        else:
            score += 10

        return min(score, 100.0)

    def _calculate_perceptual_score(self, metrics: Dict[str, float]) -> float:
        """Calculate perceptual quality score"""
        score = 0.0

        # Loudness score (0-25 points)
        loudness = metrics.get('loudness_lufs', 0)
        if -18 <= loudness <= -14:
            score += 25
        elif -20 <= loudness <= -12:
            score += 20
        else:
            score += 10

        # Dynamic range score (0-25 points)
        dr = metrics.get('dynamic_range_db', 0)
        if dr >= 10:
            score += 25
        elif dr >= 8:
            score += 20
        elif dr >= 6:
            score += 15
        else:
            score += 10

        # THD score (0-25 points)
        thd = metrics.get('thd_percent', 100)
        if thd <= 0.5:
            score += 25
        elif thd <= 1.0:
            score += 20
        elif thd <= 2.0:
            score += 15
        else:
            score += 10

        # Peak level score (0-25 points)
        peak = metrics.get('true_peak_db', 0)
        if peak <= -1.0:
            score += 25
        elif peak <= 0.0:
            score += 20
        else:
            score += 10

        return min(score, 100.0)

    def _calculate_medical_suitability_score(self, metrics: Dict[str, float]) -> float:
        """Calculate medical content suitability score"""
        score = 0.0

        # Intelligibility score (0-50 points)
        intel = metrics.get('intelligibility_pct', 0)
        if intel >= 95:
            score += 50
        elif intel >= 90:
            score += 40
        elif intel >= 85:
            score += 30
        else:
            score += 20

        # Consistency score (0-25 points)
        consistency = metrics.get('consistency_score', 0)
        if consistency >= 90:
            score += 25
        elif consistency >= 80:
            score += 20
        else:
            score += 15

        # SNR for medical (0-25 points)
        snr = metrics.get('snr_db', 0)
        if snr >= 45:
            score += 25
        elif snr >= 40:
            score += 20
        else:
            score += 10

        return min(score, 100.0)

    def _determine_grade(self, score: float) -> str:
        """Determine letter grade from score"""
        for grade, threshold in self.GRADE_THRESHOLDS.items():
            if score >= threshold:
                return grade
        return 'F'

    def generate_quality_report(self, score: QualityScore, metrics: Dict[str, float]) -> str:
        """Generate detailed quality report"""
        report = []
        report.append("=" * 60)
        report.append("AUDIO QUALITY REPORT")
        report.append("=" * 60)
        report.append(f"Overall Score: {score.overall_score:.1f}/100 (Grade: {score.grade})")
        report.append("")
        report.append(f"Technical Quality: {score.technical_score:.1f}/100")
        report.append(f"Perceptual Quality: {score.perceptual_score:.1f}/100")
        report.append(f"Medical Suitability: {score.medical_suitability_score:.1f}/100")
        report.append("")
        report.append("DETAILED METRICS:")
        for key, value in metrics.items():
            report.append(f"  {key}: {value:.2f}")
        report.append("=" * 60)

        return "\n".join(report)
