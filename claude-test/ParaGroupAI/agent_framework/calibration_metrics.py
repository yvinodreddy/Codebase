"""Basic calibration metrics."""
import numpy as np

def calculate_brier_score(predictions, ground_truth):
    """Calculate Brier score."""
    return np.mean((np.array(predictions) - np.array(ground_truth)) ** 2)

def calculate_confidence_interval(data, confidence=0.95):
    """Calculate confidence interval."""
    mean = np.mean(data)
    std = np.std(data)
    margin = 1.96 * std  # 95% CI
    return (mean - margin, mean + margin)
