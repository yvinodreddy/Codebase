"""Basic bias detection guardrail."""
import re

class BiasDetectionGuardrail:
    """Detect demographic bias in responses."""

    BIAS_PATTERNS = {
        'age': ['young', 'old', 'elderly', 'youthful'],
        'gender': ['male', 'female', 'man', 'woman'],
        'race': ['white', 'black', 'asian', 'hispanic']
    }

    def check(self, text):
        """Check for bias."""
        detected = []
        for category, patterns in self.BIAS_PATTERNS.items():
            for pattern in patterns:
                if re.search(r'\b' + pattern + r'\b', text, re.I):
                    detected.append(f"{category}: {pattern}")

        return {
            'passed': len(detected) == 0,
            'detected_biases': detected
        }
