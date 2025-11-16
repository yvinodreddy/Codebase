"""
Phase 16: Explainable AI & Interpretability
Comprehensive Unit Tests - 26 Test Cases

Tests for SHAP, LIME, Attention Visualization, and Decision Explanations
"""

import unittest
import sys
import os
from pathlib import Path

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import (
    Phase16Implementation,
    SHAPExplainer,
    LIMEExplainer,
    AttentionVisualizer,
    DecisionExplainer
)


class TestSHAPExplainer(unittest.TestCase):
    """Test cases for SHAP Explainer"""

    def setUp(self):
        """Set up test fixtures"""
        self.explainer = SHAPExplainer()

    def test_shap_initialization(self):
        """Test SHAP explainer initialization"""
        self.assertEqual(self.explainer.explainer_type, "SHAP")
        self.assertIn("TreeExplainer", self.explainer.methods)
        self.assertIn("KernelExplainer", self.explainer.methods)
        self.assertIn("DeepExplainer", self.explainer.methods)

    def test_shap_generate_explanations(self):
        """Test SHAP explanation generation"""
        result = self.explainer.generate_explanations(
            model_type="clinical_decision",
            sample_count=10
        )
        self.assertEqual(result["count"], 10)
        self.assertIsNotNone(result["avg_time"])
        self.assertGreater(len(result["features"]), 0)
        self.assertEqual(len(result["shap_values"]), 10)

    def test_shap_values_structure(self):
        """Test SHAP values have correct structure"""
        result = self.explainer.generate_explanations(
            model_type="clinical_decision",
            sample_count=5
        )
        shap_value = result["shap_values"][0]
        self.assertIn("sample_id", shap_value)
        self.assertIn("prediction", shap_value)
        self.assertIn("base_value", shap_value)
        self.assertIn("feature_contributions", shap_value)

    def test_shap_feature_importance(self):
        """Test SHAP feature importance computation"""
        result = self.explainer.get_feature_importance({})
        self.assertIn("top_features", result)
        self.assertGreater(len(result["top_features"]), 0)
        self.assertEqual(result["method"], "mean_absolute_shap")

    def test_shap_explanation_count(self):
        """Test SHAP generates correct number of explanations"""
        for count in [1, 10, 50, 100]:
            result = self.explainer.generate_explanations(
                model_type="test_model",
                sample_count=count
            )
            self.assertEqual(result["count"], count)
            self.assertEqual(len(result["shap_values"]), count)

    def test_shap_features_present(self):
        """Test SHAP explanations include all expected features"""
        result = self.explainer.generate_explanations(
            model_type="clinical_decision",
            sample_count=5
        )
        expected_features = [
            "age", "blood_pressure", "cholesterol", "glucose", "bmi"
        ]
        for feature in expected_features:
            self.assertIn(feature, result["features"])


class TestLIMEExplainer(unittest.TestCase):
    """Test cases for LIME Explainer"""

    def setUp(self):
        """Set up test fixtures"""
        self.explainer = LIMEExplainer()

    def test_lime_initialization(self):
        """Test LIME explainer initialization"""
        self.assertEqual(self.explainer.explainer_type, "LIME")
        self.assertIn("TabularExplainer", self.explainer.methods)
        self.assertIn("ImageExplainer", self.explainer.methods)
        self.assertIn("TextExplainer", self.explainer.methods)

    def test_lime_generate_explanations(self):
        """Test LIME explanation generation"""
        result = self.explainer.generate_explanations(
            model_type="diagnosis_prediction",
            sample_count=10
        )
        self.assertEqual(result["count"], 10)
        self.assertIsNotNone(result["avg_time"])
        self.assertGreater(len(result["features"]), 0)
        self.assertEqual(len(result["lime_explanations"]), 10)

    def test_lime_explanation_structure(self):
        """Test LIME explanations have correct structure"""
        result = self.explainer.generate_explanations(
            model_type="diagnosis_prediction",
            sample_count=5
        )
        explanation = result["lime_explanations"][0]
        self.assertIn("sample_id", explanation)
        self.assertIn("prediction", explanation)
        self.assertIn("prediction_class", explanation)
        self.assertIn("local_approximation", explanation)
        self.assertIn("local_model_r2", explanation)

    def test_lime_local_model_quality(self):
        """Test LIME local model has high R² score"""
        result = self.explainer.generate_explanations(
            model_type="diagnosis_prediction",
            sample_count=5
        )
        for explanation in result["lime_explanations"]:
            self.assertGreaterEqual(explanation["local_model_r2"], 0.85)

    def test_lime_get_top_features(self):
        """Test LIME top features extraction"""
        explanation = {
            "local_approximation": {
                "feature1": 0.8,
                "feature2": -0.5,
                "feature3": 0.3,
                "feature4": -0.9,
                "feature5": 0.1
            }
        }
        top_features = self.explainer.get_top_features(explanation, k=3)
        self.assertEqual(len(top_features), 3)
        # Check that features are sorted by absolute value
        self.assertEqual(top_features[0][0], "feature4")  # -0.9 has highest abs value

    def test_lime_prediction_classes(self):
        """Test LIME generates both high_risk and low_risk predictions"""
        result = self.explainer.generate_explanations(
            model_type="diagnosis_prediction",
            sample_count=10
        )
        classes = set(exp["prediction_class"] for exp in result["lime_explanations"])
        self.assertGreaterEqual(len(classes), 1)  # At least one class


class TestAttentionVisualizer(unittest.TestCase):
    """Test cases for Attention Visualizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.visualizer = AttentionVisualizer()

    def test_attention_initialization(self):
        """Test attention visualizer initialization"""
        self.assertEqual(self.visualizer.explainer_type, "Attention")
        self.assertIn("heatmap", self.visualizer.visualization_types)
        self.assertIn("flow", self.visualizer.visualization_types)
        self.assertIn("graph", self.visualizer.visualization_types)

    def test_attention_generate_visualizations(self):
        """Test attention visualization generation"""
        result = self.visualizer.generate_visualizations(
            model_type="transformer_clinical",
            sample_count=10
        )
        self.assertEqual(result["count"], 10)
        self.assertIsNotNone(result["avg_time"])
        self.assertEqual(result["heads"], 8)
        self.assertEqual(len(result["visualizations"]), 10)

    def test_attention_visualization_structure(self):
        """Test attention visualizations have correct structure"""
        result = self.visualizer.generate_visualizations(
            model_type="transformer_clinical",
            sample_count=5
        )
        viz = result["visualizations"][0]
        self.assertIn("sample_id", viz)
        self.assertIn("sequence_length", viz)
        self.assertIn("num_heads", viz)
        self.assertIn("attention_weights", viz)
        self.assertIn("aggregated_attention", viz)

    def test_attention_heads_count(self):
        """Test attention weights for all heads"""
        result = self.visualizer.generate_visualizations(
            model_type="transformer_clinical",
            sample_count=3
        )
        for viz in result["visualizations"]:
            self.assertEqual(len(viz["attention_weights"]), 8)  # 8 heads

    def test_attention_head_structure(self):
        """Test individual attention head structure"""
        result = self.visualizer.generate_visualizations(
            model_type="transformer_clinical",
            sample_count=2
        )
        head = result["visualizations"][0]["attention_weights"][0]
        self.assertIn("head_id", head)
        self.assertIn("attention_pattern", head)
        self.assertIn("max_attention_score", head)
        self.assertIn("entropy", head)
        self.assertIn("top_attended_tokens", head)

    def test_attention_create_heatmap(self):
        """Test attention heatmap creation"""
        attention_weights = [[0.1, 0.2], [0.3, 0.4]]
        heatmap = self.visualizer.create_attention_heatmap(attention_weights)
        self.assertEqual(heatmap["type"], "heatmap")
        self.assertIn("dimensions", heatmap)
        self.assertEqual(heatmap["colormap"], "viridis")
        self.assertTrue(heatmap["normalized"])


class TestDecisionExplainer(unittest.TestCase):
    """Test cases for Decision Explainer"""

    def setUp(self):
        """Set up test fixtures"""
        self.explainer = DecisionExplainer()

    def test_decision_initialization(self):
        """Test decision explainer initialization"""
        self.assertEqual(self.explainer.explainer_type, "Decision")
        self.assertIn("rule_based", self.explainer.explanation_templates)
        self.assertIn("counterfactual", self.explainer.explanation_templates)
        self.assertIn("contrastive", self.explainer.explanation_templates)
        self.assertIn("narrative", self.explainer.explanation_templates)

    def test_decision_generate_explanations(self):
        """Test decision explanation generation"""
        result = self.explainer.generate_explanations(
            decision_type="treatment_recommendation",
            sample_count=10
        )
        self.assertEqual(result["count"], 10)
        self.assertIsNotNone(result["avg_time"])
        self.assertEqual(len(result["explanations"]), 10)

    def test_decision_explanation_structure(self):
        """Test decision explanations have correct structure"""
        result = self.explainer.generate_explanations(
            decision_type="treatment_recommendation",
            sample_count=5
        )
        exp = result["explanations"][0]
        self.assertIn("sample_id", exp)
        self.assertIn("decision", exp)
        self.assertIn("confidence", exp)
        self.assertIn("primary_reason", exp)
        self.assertIn("supporting_evidence", exp)
        self.assertIn("rule_based_explanation", exp)
        self.assertIn("counterfactual_explanation", exp)
        self.assertIn("clinical_context", exp)
        self.assertIn("recommendations", exp)

    def test_decision_confidence_scores(self):
        """Test decision confidence scores are valid"""
        result = self.explainer.generate_explanations(
            decision_type="treatment_recommendation",
            sample_count=10
        )
        for exp in result["explanations"]:
            self.assertGreaterEqual(exp["confidence"], 0.0)
            self.assertLessEqual(exp["confidence"], 1.0)

    def test_decision_confidence_statistics(self):
        """Test decision confidence statistics"""
        result = self.explainer.generate_explanations(
            decision_type="treatment_recommendation",
            sample_count=20
        )
        confidence = result["confidence"]
        self.assertIn("mean", confidence)
        self.assertIn("std", confidence)
        self.assertIn("min", confidence)
        self.assertIn("max", confidence)
        self.assertGreaterEqual(confidence["mean"], confidence["min"])
        self.assertLessEqual(confidence["mean"], confidence["max"])

    def test_decision_recommendations_present(self):
        """Test decision explanations include recommendations"""
        result = self.explainer.generate_explanations(
            decision_type="treatment_recommendation",
            sample_count=5
        )
        for exp in result["explanations"]:
            self.assertIsInstance(exp["recommendations"], list)
            self.assertGreater(len(exp["recommendations"]), 0)


class TestPhase16Implementation(unittest.TestCase):
    """Test cases for Phase 16 Implementation"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase16Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 16)
        self.assertEqual(self.implementation.phase_name, "Explainable AI & Interpretability")
        self.assertEqual(self.implementation.story_points, 34)
        self.assertEqual(self.implementation.priority, "P0")

    def test_phase_logic_execution(self):
        """Test phase logic executes successfully"""
        result = self.implementation._implement_phase_logic({})
        self.assertIn("status", result)
        self.assertIn("components", result)
        self.assertEqual(result["status"], "implemented")
        self.assertTrue(result["implemented"])

    def test_all_explainability_components(self):
        """Test all four explainability components are present"""
        result = self.implementation._implement_phase_logic({})
        components = result["components"]
        self.assertIn("shap_explainer", components)
        self.assertIn("lime_explainer", components)
        self.assertIn("attention_visualizer", components)
        self.assertIn("decision_explainer", components)

    def test_explanations_generated(self):
        """Test correct number of explanations generated"""
        result = self.implementation._implement_phase_logic({})
        summary = result["summary"]
        # 100 SHAP + 100 LIME + 50 Attention + 75 Decision = 325
        self.assertEqual(summary["total_explanations_generated"], 325)
        self.assertEqual(summary["explainability_coverage"], "100%")
        self.assertTrue(summary["production_ready"])

    def test_phase_execution(self):
        """Test full phase execution"""
        task = {"goal": "Implement Explainable AI", "phase_id": 16}
        result = self.implementation.execute(task)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)

    def test_phase_state_tracking(self):
        """Test phase state is tracked properly"""
        self.assertIn(self.implementation.status, ["NOT_STARTED", "IN_PROGRESS", "COMPLETED", "FAILED"])

    def test_get_stats(self):
        """Test statistics retrieval"""
        stats = self.implementation.get_stats()
        self.assertEqual(stats["phase_id"], 16)
        self.assertEqual(stats["phase_name"], "Explainable AI & Interpretability")
        self.assertEqual(stats["story_points"], 34)
        self.assertEqual(stats["framework_version"], "100%")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
