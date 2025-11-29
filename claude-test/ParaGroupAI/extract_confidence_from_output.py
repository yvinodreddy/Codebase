#!/usr/bin/env python3
"""
extract_confidence_from_output.py - Extract Confidence Score from cpp Output

PRODUCTION-READY IMPLEMENTATION (2025-11-16)
============================================

Parses cpp output files to extract the confidence score from the actual analysis.
This ensures the statusline displays the REAL confidence score, not a default value.

MULTIPLE EXTRACTION METHODS:
1. Parse "Confidence Score: XX%" or "Confidence: XX%"
2. Parse validation results if present
3. Parse from structured output sections
4. Fallback to calculating from guardrail layers

Usage:
    python3 extract_confidence_from_output.py <output_file>
    python3 extract_confidence_from_output.py --json <output_file>
"""

import re
import sys
import json
from pathlib import Path
from typing import Optional, Dict, List


class ConfidenceExtractor:
    """
    Multi-method confidence score extractor with production-ready reliability.

    Uses 5 different extraction methods with priority order:
    1. Explicit confidence score statements
    2. Validation results
    3. Structured output sections
    4. Guardrail layer analysis
    5. Quality scoring analysis
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = ""
        self.answer_section = ""  # Content after the answer marker
        self.confidence_scores = []
        self.extraction_methods = []

    def load_file(self) -> bool:
        """Load the output file and split into system/answer sections."""
        try:
            if not self.file_path.exists():
                return False

            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()

            # Split content into system output and answer section
            # Answer section starts after the ⬇️⬇️⬇️ marker
            answer_marker = '⬇️⬇️⬇️'
            if answer_marker in self.content:
                parts = self.content.split(answer_marker, 1)
                if len(parts) > 1:
                    self.answer_section = parts[1]

            # If no marker found, use last 25% of file as answer section
            if not self.answer_section:
                split_point = int(len(self.content) * 0.75)
                self.answer_section = self.content[split_point:]

            return len(self.content) > 0
        except Exception:
            return False

    def method1_explicit_confidence(self) -> Optional[float]:
        """
        Method 1: Extract explicit confidence score statements.

        PRIORITY ORDER:
        1. First search in answer section (after ⬇️⬇️⬇️ marker)
        2. Look for "Confidence Level:" pattern (highest priority)
        3. Look for other confidence patterns
        4. Fall back to system output only if nothing in answer

        Patterns:
        - Confidence Level: 85%
        - Confidence Score: 85%
        - Confidence: 85.5%
        - Final Confidence: 85%
        """
        # Priority patterns (order matters!)
        patterns = [
            (r'\*\*Confidence\s*Level:\s*(\d+(?:\.\d+)?)\s*%\*\*', 1),  # Highest: **Confidence Level: XX%**
            (r'Confidence\s*Level:\s*(\d+(?:\.\d+)?)\s*%', 1),          # High: Confidence Level: XX%
            (r'Confidence\s*Score:\s*(\d+(?:\.\d+)?)\s*%', 2),          # Medium: Confidence Score: XX%
            (r'Final\s*Confidence:\s*(\d+(?:\.\d+)?)\s*%', 2),          # Medium: Final Confidence: XX%
            (r'Confidence:\s*(\d+(?:\.\d+)?)\s*%', 3),                  # Low: Confidence: XX%
        ]

        # STEP 1: Search in answer section FIRST (highest priority)
        if self.answer_section:
            for pattern, priority_level in patterns:
                matches = re.findall(pattern, self.answer_section, re.IGNORECASE)
                if matches:
                    # Get the last (most recent) confidence score in answer
                    score = float(matches[-1])
                    self.confidence_scores.append({
                        'method': 'explicit_confidence_answer',
                        'score': score,
                        'priority': 1,  # Answer section always priority 1
                        'pattern_priority': priority_level,
                        'section': 'answer'
                    })
                    return score

        # STEP 2: Fall back to full content if nothing in answer section
        for pattern, priority_level in patterns:
            matches = re.findall(pattern, self.content, re.IGNORECASE)
            if matches:
                # Get the last (most recent) confidence score
                score = float(matches[-1])
                self.confidence_scores.append({
                    'method': 'explicit_confidence_system',
                    'score': score,
                    'priority': 5,  # Lower priority since from system output
                    'pattern_priority': priority_level,
                    'section': 'system'
                })
                return score

        return None

    def method2_validation_results(self) -> Optional[float]:
        """
        Method 2: Extract from validation results.

        Patterns:
        - "confidence": 85.5
        - is_acceptable: true, confidence: 85.0
        """
        patterns = [
            r'"confidence":\s*(\d+(?:\.\d+)?)',
            r'confidence["\']?:\s*(\d+(?:\.\d+)?)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, self.content, re.IGNORECASE)
            if matches:
                # Get the highest confidence score from validation
                scores = [float(m) for m in matches]
                score = max(scores)
                self.confidence_scores.append({
                    'method': 'validation_results',
                    'score': score,
                    'priority': 2
                })
                return score

        return None

    def method3_structured_sections(self) -> Optional[float]:
        """
        Method 3: Extract from structured output sections.

        Looks for confidence in structured sections like:
        - FINAL VERDICT
        - CONCLUSION
        - SUMMARY
        """
        section_patterns = [
            (r'FINAL VERDICT.*?Confidence:\s*(\d+(?:\.\d+)?)\s*%', re.DOTALL),
            (r'CONCLUSION.*?Confidence:\s*(\d+(?:\.\d+)?)\s*%', re.DOTALL),
            (r'SUMMARY.*?Confidence:\s*(\d+(?:\.\d+)?)\s*%', re.DOTALL),
        ]

        for pattern, flags in section_patterns:
            match = re.search(pattern, self.content, re.IGNORECASE | flags)
            if match:
                score = float(match.group(1))
                self.confidence_scores.append({
                    'method': 'structured_sections',
                    'score': score,
                    'priority': 3
                })
                return score

        return None

    def method4_guardrail_analysis(self) -> Optional[float]:
        """
        Method 4: Calculate from guardrail layer passes.

        Analyzes which guardrail layers passed and estimates confidence.
        """
        # Look for guardrail layer results
        layer_pattern = r'Layer\s*(\d+).*?(?:✅|PASS|passed)'
        passed_layers = re.findall(layer_pattern, self.content, re.IGNORECASE)

        if passed_layers:
            total_layers = 8  # System has 8 guardrail layers
            passed_count = len(set(passed_layers))

            # Calculate confidence based on passed layers
            # Each layer contributes to overall confidence
            base_confidence = 50.0  # Base confidence
            layer_contribution = (passed_count / total_layers) * 45.0  # Up to 45% from layers
            score = base_confidence + layer_contribution

            self.confidence_scores.append({
                'method': 'guardrail_analysis',
                'score': score,
                'priority': 4,
                'details': f'{passed_count}/{total_layers} layers passed'
            })
            return score

        return None

    def method5_quality_scoring(self) -> Optional[float]:
        """
        Method 5: Extract from quality scoring analysis.

        Looks for quality metrics and scoring.
        """
        # Look for quality scores
        quality_pattern = r'Quality\s*(?:Score)?:\s*(\d+(?:\.\d+)?)\s*[%/]'
        matches = re.findall(quality_pattern, self.content, re.IGNORECASE)

        if matches:
            # Average quality scores
            scores = [float(m) for m in matches]
            score = sum(scores) / len(scores)

            self.confidence_scores.append({
                'method': 'quality_scoring',
                'score': score,
                'priority': 5
            })
            return score

        return None

    def extract_all_methods(self) -> List[Dict]:
        """Run all extraction methods and collect results."""
        methods = [
            ('method1_explicit_confidence', self.method1_explicit_confidence),
            ('method2_validation_results', self.method2_validation_results),
            ('method3_structured_sections', self.method3_structured_sections),
            ('method4_guardrail_analysis', self.method4_guardrail_analysis),
            ('method5_quality_scoring', self.method5_quality_scoring),
        ]

        for method_name, method_func in methods:
            try:
                result = method_func()
                if result is not None:
                    self.extraction_methods.append(method_name)
            except Exception:
                pass

        return self.confidence_scores

    def get_best_confidence(self) -> Dict:
        """
        Get the best confidence score using priority ranking.

        Returns:
            Dictionary with confidence score and metadata
        """
        if not self.confidence_scores:
            return {
                'confidence': None,
                'method': 'none',
                'status': 'not_found',
                'all_scores': []
            }

        # Sort by priority (lower number = higher priority)
        sorted_scores = sorted(self.confidence_scores, key=lambda x: x['priority'])
        best = sorted_scores[0]

        return {
            'confidence': best['score'],
            'method': best['method'],
            'status': 'success',
            'all_scores': self.confidence_scores,
            'extraction_methods': self.extraction_methods
        }

    def extract(self) -> Dict:
        """
        Main extraction method.

        Returns:
            Dictionary with confidence score and extraction details
        """
        if not self.load_file():
            return {
                'confidence': None,
                'method': 'file_not_found',
                'status': 'error',
                'error': f'File not found: {self.file_path}'
            }

        self.extract_all_methods()
        return self.get_best_confidence()


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract confidence score from cpp output file'
    )
    parser.add_argument('file', help='Path to cpp output file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--verbose', action='store_true', help='Show all extraction details')

    args = parser.parse_args()

    extractor = ConfidenceExtractor(args.file)
    result = extractor.extract()

    if args.json:
        if not args.verbose:
            # Concise output
            output = {
                'confidence': result.get('confidence'),
                'status': result.get('status'),
                'method': result.get('method')
            }
        else:
            # Full details
            output = result

        print(json.dumps(output, indent=2))
    else:
        # Text output
        if result['status'] == 'success':
            print(f"Confidence: {result['confidence']:.1f}%")
            if args.verbose:
                print(f"Method: {result['method']}")
                print(f"All scores found: {len(result['all_scores'])}")
                for score in result['all_scores']:
                    print(f"  - {score['method']}: {score['score']:.1f}%")
        elif result['status'] == 'not_found':
            print("No confidence score found in output file")
            sys.exit(1)
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)


if __name__ == '__main__':
    main()
