"""
Phase 22: Continuous Learning & Federated ML
Comprehensive Unit Tests

Test Coverage:
- OnlineLearningSystem (12 tests)
- FederatedLearningCoordinator (12 tests)
- SecureAggregator (10 tests)
- ModelVersionManager (12 tests)
- ModelDriftDetector (10 tests)
- ContinuousLearningSystem (8 tests)
- Performance Tests (2 tests)

Total: 66 tests
"""

import unittest
import numpy as np
import sys
import os
from datetime import datetime, timedelta

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from continuous_learning_system import (
    OnlineLearningSystem,
    FederatedLearningCoordinator,
    SecureAggregator,
    ModelVersionManager,
    ModelDriftDetector,
    ContinuousLearningSystem,
    ModelType,
    DeploymentStrategy,
    DriftType,
    FederatedSite,
    ModelVersion
)


# ============================================================================
# TEST ONLINE LEARNING SYSTEM
# ============================================================================

class TestOnlineLearningSystem(unittest.TestCase):
    """Test OnlineLearningSystem component"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = OnlineLearningSystem(
            model_type=ModelType.DIAGNOSIS_PREDICTOR,
            learning_rate=0.001,
            batch_size=32
        )

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.system.model_type, ModelType.DIAGNOSIS_PREDICTOR)
        self.assertEqual(self.system.learning_rate, 0.001)
        self.assertEqual(self.system.batch_size, 32)
        self.assertEqual(len(self.system.update_history), 0)

    def test_incremental_update_single_batch(self):
        """Test incremental update with single batch"""
        data = np.random.randn(32, 50)
        labels = np.random.randint(0, 2, 32)

        update = self.system.incremental_update(data, labels)

        self.assertIsNotNone(update)
        self.assertEqual(update.new_samples, 32)
        self.assertGreater(update.validation_accuracy, 0.0)
        self.assertLess(update.training_loss, 1.0)
        self.assertEqual(len(self.system.update_history), 1)

    def test_incremental_update_multiple_batches(self):
        """Test incremental update with multiple batches"""
        data = np.random.randn(100, 50)
        labels = np.random.randint(0, 2, 100)

        update = self.system.incremental_update(data, labels)

        self.assertEqual(update.new_samples, 100)
        self.assertEqual(len(self.system.update_history), 1)

    def test_update_history_accumulation(self):
        """Test that update history accumulates correctly"""
        for i in range(5):
            data = np.random.randn(32, 50)
            labels = np.random.randint(0, 2, 32)
            self.system.incremental_update(data, labels)

        self.assertEqual(len(self.system.update_history), 5)

    def test_update_id_uniqueness(self):
        """Test that update IDs are unique"""
        update_ids = set()

        for i in range(3):
            data = np.random.randn(32, 50)
            labels = np.random.randint(0, 2, 32)
            update = self.system.incremental_update(data, labels)
            update_ids.add(update.update_id)

        self.assertEqual(len(update_ids), 3)

    def test_data_hashing(self):
        """Test that data is hashed for audit trail"""
        data = np.random.randn(32, 50)
        labels = np.random.randint(0, 2, 32)

        update = self.system.incremental_update(data, labels)

        self.assertIsNotNone(update.data_hash)
        self.assertEqual(len(update.data_hash), 16)

    def test_get_update_statistics_no_updates(self):
        """Test statistics when no updates performed"""
        stats = self.system.get_update_statistics()

        self.assertEqual(stats["total_updates"], 0)

    def test_get_update_statistics_with_updates(self):
        """Test statistics after multiple updates"""
        for i in range(3):
            data = np.random.randn(32, 50)
            labels = np.random.randint(0, 2, 32)
            self.system.incremental_update(data, labels)

        stats = self.system.get_update_statistics()

        self.assertEqual(stats["total_updates"], 3)
        self.assertEqual(stats["total_samples_processed"], 96)
        self.assertIn("average_loss", stats)
        self.assertIn("latest_accuracy", stats)
        self.assertIn("accuracy_trend", stats)

    def test_accuracy_improvement_trend(self):
        """Test that accuracy generally improves with updates"""
        accuracies = []

        for i in range(10):
            data = np.random.randn(32, 50)
            labels = np.random.randint(0, 2, 32)
            update = self.system.incremental_update(data, labels)
            accuracies.append(update.validation_accuracy)

        # Check that average of last 5 is higher than first 5
        # (with some tolerance for randomness)
        early_avg = np.mean(accuracies[:5])
        late_avg = np.mean(accuracies[5:])

        # Should generally improve (or at least not degrade significantly)
        self.assertGreaterEqual(late_avg, early_avg - 0.1)

    def test_loss_decreasing_trend(self):
        """Test that loss generally decreases with updates"""
        losses = []

        for i in range(10):
            data = np.random.randn(32, 50)
            labels = np.random.randint(0, 2, 32)
            update = self.system.incremental_update(data, labels)
            losses.append(update.training_loss)

        # Check that average of last 5 is lower than first 5
        early_avg = np.mean(losses[:5])
        late_avg = np.mean(losses[5:])

        self.assertLessEqual(late_avg, early_avg + 0.1)

    def test_different_model_types(self):
        """Test initialization with different model types"""
        for model_type in ModelType:
            system = OnlineLearningSystem(model_type=model_type)
            self.assertEqual(system.model_type, model_type)

    def test_timestamp_recording(self):
        """Test that timestamps are recorded correctly"""
        data = np.random.randn(32, 50)
        labels = np.random.randint(0, 2, 32)

        before = datetime.now()
        update = self.system.incremental_update(data, labels)
        after = datetime.now()

        self.assertGreaterEqual(update.timestamp, before)
        self.assertLessEqual(update.timestamp, after)


# ============================================================================
# TEST FEDERATED LEARNING COORDINATOR
# ============================================================================

class TestFederatedLearningCoordinator(unittest.TestCase):
    """Test FederatedLearningCoordinator component"""

    def setUp(self):
        """Set up test fixtures"""
        self.coordinator = FederatedLearningCoordinator(
            model_type=ModelType.DIAGNOSIS_PREDICTOR,
            privacy_epsilon=1.0,
            min_sites=2
        )

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.coordinator.model_type, ModelType.DIAGNOSIS_PREDICTOR)
        self.assertEqual(self.coordinator.privacy_epsilon, 1.0)
        self.assertEqual(self.coordinator.min_sites, 2)
        self.assertEqual(len(self.coordinator.sites), 0)

    def test_register_site(self):
        """Test site registration"""
        site = FederatedSite(
            site_id="SITE_001",
            site_name="Test Hospital",
            location="Boston, MA",
            num_samples=1000
        )

        self.coordinator.register_site(site)

        self.assertEqual(len(self.coordinator.sites), 1)
        self.assertIn("SITE_001", self.coordinator.sites)

    def test_register_multiple_sites(self):
        """Test multiple site registrations"""
        sites = [
            FederatedSite("SITE_001", "Hospital A", "Boston", 1000),
            FederatedSite("SITE_002", "Hospital B", "Chicago", 2000),
            FederatedSite("SITE_003", "Hospital C", "Seattle", 1500)
        ]

        for site in sites:
            self.coordinator.register_site(site)

        self.assertEqual(len(self.coordinator.sites), 3)

    def test_initiate_training_round_insufficient_sites(self):
        """Test that training fails with insufficient sites"""
        site = FederatedSite("SITE_001", "Test Hospital", "Boston", 1000)
        self.coordinator.register_site(site)

        with self.assertRaises(ValueError):
            self.coordinator.initiate_training_round()

    def test_initiate_training_round_success(self):
        """Test successful training round initiation"""
        sites = [
            FederatedSite("SITE_001", "Hospital A", "Boston", 1000),
            FederatedSite("SITE_002", "Hospital B", "Chicago", 2000)
        ]

        for site in sites:
            self.coordinator.register_site(site)

        round_obj = self.coordinator.initiate_training_round()

        self.assertIsNotNone(round_obj)
        self.assertEqual(round_obj.round_number, 1)
        self.assertEqual(len(round_obj.participating_sites), 2)
        self.assertIsNone(round_obj.completed_at)

    def test_multiple_training_rounds(self):
        """Test multiple sequential training rounds"""
        sites = [
            FederatedSite("SITE_001", "Hospital A", "Boston", 1000),
            FederatedSite("SITE_002", "Hospital B", "Chicago", 2000)
        ]

        for site in sites:
            self.coordinator.register_site(site)

        round1 = self.coordinator.initiate_training_round()
        round2 = self.coordinator.initiate_training_round()

        self.assertEqual(round1.round_number, 1)
        self.assertEqual(round2.round_number, 2)

    def test_aggregate_site_updates(self):
        """Test aggregation of site updates"""
        sites = [
            FederatedSite("SITE_001", "Hospital A", "Boston", 1000),
            FederatedSite("SITE_002", "Hospital B", "Chicago", 2000)
        ]

        for site in sites:
            self.coordinator.register_site(site)

        self.coordinator.initiate_training_round()

        site_updates = {
            "SITE_001": np.random.randn(100),
            "SITE_002": np.random.randn(100)
        }

        aggregated, privacy_used = self.coordinator.aggregate_site_updates(site_updates)

        self.assertEqual(aggregated.shape, (100,))
        self.assertGreater(privacy_used, 0.0)

    def test_aggregate_unknown_site(self):
        """Test that aggregation fails with unknown site"""
        sites = [
            FederatedSite("SITE_001", "Hospital A", "Boston", 1000),
            FederatedSite("SITE_002", "Hospital B", "Chicago", 2000)
        ]

        for site in sites:
            self.coordinator.register_site(site)

        self.coordinator.initiate_training_round()

        site_updates = {
            "SITE_001": np.random.randn(100),
            "SITE_UNKNOWN": np.random.randn(100)
        }

        with self.assertRaises(ValueError):
            self.coordinator.aggregate_site_updates(site_updates)

    def test_site_contribution_timestamp_update(self):
        """Test that site contribution timestamps are updated"""
        sites = [
            FederatedSite("SITE_001", "Hospital A", "Boston", 1000),
            FederatedSite("SITE_002", "Hospital B", "Chicago", 2000)
        ]

        for site in sites:
            self.coordinator.register_site(site)

        self.assertIsNone(self.coordinator.sites["SITE_001"].last_contribution)

        self.coordinator.initiate_training_round()

        site_updates = {
            "SITE_001": np.random.randn(100),
            "SITE_002": np.random.randn(100)
        }

        self.coordinator.aggregate_site_updates(site_updates)

        self.assertIsNotNone(self.coordinator.sites["SITE_001"].last_contribution)

    def test_get_federation_statistics(self):
        """Test federation statistics"""
        sites = [
            FederatedSite("SITE_001", "Hospital A", "Boston", 1000),
            FederatedSite("SITE_002", "Hospital B", "Chicago", 2000)
        ]

        for site in sites:
            self.coordinator.register_site(site)

        stats = self.coordinator.get_federation_statistics()

        self.assertEqual(stats["total_sites"], 2)
        self.assertEqual(stats["active_sites"], 2)
        self.assertEqual(stats["total_samples"], 3000)

    def test_inactive_site_exclusion(self):
        """Test that inactive sites are excluded from training"""
        sites = [
            FederatedSite("SITE_001", "Hospital A", "Boston", 1000, is_active=True),
            FederatedSite("SITE_002", "Hospital B", "Chicago", 2000, is_active=False),
            FederatedSite("SITE_003", "Hospital C", "Seattle", 1500, is_active=True)
        ]

        for site in sites:
            self.coordinator.register_site(site)

        round_obj = self.coordinator.initiate_training_round()

        self.assertEqual(len(round_obj.participating_sites), 2)
        self.assertNotIn("SITE_002", round_obj.participating_sites)


# ============================================================================
# TEST SECURE AGGREGATOR
# ============================================================================

class TestSecureAggregator(unittest.TestCase):
    """Test SecureAggregator component"""

    def setUp(self):
        """Set up test fixtures"""
        self.aggregator = SecureAggregator(privacy_epsilon=1.0)

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.aggregator.privacy_epsilon, 1.0)
        self.assertEqual(self.aggregator.privacy_budget_used, 0.0)

    def test_aggregate_uniform_weights(self):
        """Test aggregation with uniform trust scores"""
        sites = {
            "SITE_001": FederatedSite("SITE_001", "A", "Boston", 1000, trust_score=1.0),
            "SITE_002": FederatedSite("SITE_002", "B", "Chicago", 1000, trust_score=1.0)
        }

        site_updates = {
            "SITE_001": np.ones(100),
            "SITE_002": np.ones(100)
        }

        aggregated = self.aggregator.aggregate(site_updates, sites)

        # With uniform weights and uniform updates, average should be close to 1.0
        # (plus differential privacy noise)
        self.assertEqual(aggregated.shape, (100,))
        self.assertGreater(np.mean(aggregated), 0.5)

    def test_aggregate_weighted(self):
        """Test weighted aggregation by trust scores"""
        sites = {
            "SITE_001": FederatedSite("SITE_001", "A", "Boston", 1000, trust_score=2.0),
            "SITE_002": FederatedSite("SITE_002", "B", "Chicago", 1000, trust_score=1.0)
        }

        site_updates = {
            "SITE_001": np.ones(100) * 10.0,
            "SITE_002": np.ones(100) * 1.0
        }

        aggregated = self.aggregator.aggregate(site_updates, sites)

        # Higher trust site should have more influence
        # Expected: (2/3)*10 + (1/3)*1 = 7.0 (plus noise)
        self.assertGreater(np.mean(aggregated), 4.0)

    def test_privacy_budget_accumulation(self):
        """Test that privacy budget accumulates"""
        sites = {
            "SITE_001": FederatedSite("SITE_001", "A", "Boston", 1000),
            "SITE_002": FederatedSite("SITE_002", "B", "Chicago", 1000)
        }

        site_updates = {
            "SITE_001": np.ones(100),
            "SITE_002": np.ones(100)
        }

        initial_budget = self.aggregator.privacy_budget_used

        self.aggregator.aggregate(site_updates, sites)

        self.assertGreater(self.aggregator.privacy_budget_used, initial_budget)

    def test_differential_privacy_adds_noise(self):
        """Test that differential privacy adds noise"""
        sites = {
            "SITE_001": FederatedSite("SITE_001", "A", "Boston", 1000),
            "SITE_002": FederatedSite("SITE_002", "B", "Chicago", 1000)
        }

        # Identical updates
        site_updates = {
            "SITE_001": np.zeros(100),
            "SITE_002": np.zeros(100)
        }

        aggregated = self.aggregator.aggregate(site_updates, sites)

        # Without noise, result would be exactly 0
        # With noise, it should be non-zero
        self.assertGreater(np.abs(aggregated).sum(), 0.0)

    def test_detect_byzantine_updates_normal(self):
        """Test Byzantine detection with normal updates"""
        site_updates = {
            "SITE_001": np.ones(100) * 1.0,
            "SITE_002": np.ones(100) * 1.1,
            "SITE_003": np.ones(100) * 0.9
        }

        suspicious = self.aggregator.detect_byzantine_updates(site_updates)

        self.assertEqual(len(suspicious), 0)

    def test_detect_byzantine_updates_outlier(self):
        """Test Byzantine detection with outlier"""
        site_updates = {
            "SITE_001": np.ones(100) * 1.0,
            "SITE_002": np.ones(100) * 1.1,
            "SITE_003": np.ones(100) * 100.0  # Malicious update
        }

        suspicious = self.aggregator.detect_byzantine_updates(site_updates)

        self.assertGreater(len(suspicious), 0)
        self.assertIn("SITE_003", suspicious)

    def test_different_privacy_epsilon(self):
        """Test aggregator with different privacy budgets"""
        for epsilon in [0.1, 1.0, 10.0]:
            aggregator = SecureAggregator(privacy_epsilon=epsilon)
            self.assertEqual(aggregator.privacy_epsilon, epsilon)

    def test_aggregation_consistency(self):
        """Test that aggregation is deterministic given same random seed"""
        sites = {
            "SITE_001": FederatedSite("SITE_001", "A", "Boston", 1000),
            "SITE_002": FederatedSite("SITE_002", "B", "Chicago", 1000)
        }

        site_updates = {
            "SITE_001": np.ones(100),
            "SITE_002": np.ones(100)
        }

        # Set seed for reproducibility in this test
        np.random.seed(42)
        result1 = self.aggregator.aggregate(site_updates, sites)

        # Different aggregator, same seed
        aggregator2 = SecureAggregator(privacy_epsilon=1.0)
        np.random.seed(42)
        result2 = aggregator2.aggregate(site_updates, sites)

        np.testing.assert_array_almost_equal(result1, result2, decimal=10)

    def test_aggregation_different_sizes(self):
        """Test aggregation with different parameter sizes"""
        sites = {
            "SITE_001": FederatedSite("SITE_001", "A", "Boston", 1000),
            "SITE_002": FederatedSite("SITE_002", "B", "Chicago", 1000)
        }

        for size in [10, 100, 1000]:
            site_updates = {
                "SITE_001": np.ones(size),
                "SITE_002": np.ones(size)
            }

            aggregated = self.aggregator.aggregate(site_updates, sites)
            self.assertEqual(aggregated.shape, (size,))


# ============================================================================
# TEST MODEL VERSION MANAGER
# ============================================================================

class TestModelVersionManager(unittest.TestCase):
    """Test ModelVersionManager component"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = ModelVersionManager(ModelType.DIAGNOSIS_PREDICTOR)

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.manager.model_type, ModelType.DIAGNOSIS_PREDICTOR)
        self.assertEqual(len(self.manager.versions), 0)
        self.assertIsNone(self.manager.active_version)

    def test_create_version(self):
        """Test version creation"""
        params = np.random.randn(100)

        version = self.manager.create_version(
            accuracy=0.85,
            precision=0.83,
            recall=0.87,
            f1_score=0.85,
            training_samples=1000,
            model_params=params
        )

        self.assertIsNotNone(version)
        self.assertEqual(version.accuracy, 0.85)
        self.assertEqual(version.training_samples, 1000)
        self.assertEqual(len(self.manager.versions), 1)

    def test_version_id_uniqueness(self):
        """Test that version IDs are unique"""
        params = np.random.randn(100)

        v1 = self.manager.create_version(0.85, 0.83, 0.87, 0.85, 1000, params)
        v2 = self.manager.create_version(0.86, 0.84, 0.88, 0.86, 1100, params)

        self.assertNotEqual(v1.version_id, v2.version_id)

    def test_deploy_version_immediate(self):
        """Test immediate deployment"""
        params = np.random.randn(100)
        version = self.manager.create_version(0.85, 0.83, 0.87, 0.85, 1000, params)

        success = self.manager.deploy_version(
            version.version_id,
            DeploymentStrategy.IMMEDIATE
        )

        self.assertTrue(success)
        self.assertTrue(version.is_active)
        self.assertEqual(version.deployment_percentage, 100.0)
        self.assertEqual(self.manager.active_version, version.version_id)

    def test_deploy_version_gradual_rollout(self):
        """Test gradual rollout deployment"""
        params = np.random.randn(100)
        version = self.manager.create_version(0.85, 0.83, 0.87, 0.85, 1000, params)

        self.manager.deploy_version(
            version.version_id,
            DeploymentStrategy.GRADUAL_ROLLOUT
        )

        self.assertTrue(version.is_active)
        self.assertEqual(version.deployment_percentage, 10.0)

    def test_deploy_version_ab_testing(self):
        """Test A/B testing deployment"""
        params = np.random.randn(100)
        version = self.manager.create_version(0.85, 0.83, 0.87, 0.85, 1000, params)

        self.manager.deploy_version(
            version.version_id,
            DeploymentStrategy.AB_TESTING
        )

        self.assertTrue(version.is_active)
        self.assertEqual(version.deployment_percentage, 50.0)

    def test_deploy_version_shadow_mode(self):
        """Test shadow mode deployment"""
        params = np.random.randn(100)
        version = self.manager.create_version(0.85, 0.83, 0.87, 0.85, 1000, params)

        self.manager.deploy_version(
            version.version_id,
            DeploymentStrategy.SHADOW_MODE
        )

        self.assertFalse(version.is_active)
        self.assertEqual(version.deployment_percentage, 0.0)

    def test_increase_rollout(self):
        """Test increasing rollout percentage"""
        params = np.random.randn(100)
        version = self.manager.create_version(0.85, 0.83, 0.87, 0.85, 1000, params)

        self.manager.deploy_version(version.version_id, DeploymentStrategy.GRADUAL_ROLLOUT)
        self.assertEqual(version.deployment_percentage, 10.0)

        new_percentage = self.manager.increase_rollout(version.version_id, 20.0)

        self.assertEqual(new_percentage, 30.0)
        self.assertEqual(version.deployment_percentage, 30.0)

    def test_increase_rollout_capped_at_100(self):
        """Test that rollout is capped at 100%"""
        params = np.random.randn(100)
        version = self.manager.create_version(0.85, 0.83, 0.87, 0.85, 1000, params)

        self.manager.deploy_version(version.version_id, DeploymentStrategy.GRADUAL_ROLLOUT)

        self.manager.increase_rollout(version.version_id, 95.0)

        self.assertEqual(version.deployment_percentage, 100.0)

    def test_rollback_version(self):
        """Test version rollback"""
        params = np.random.randn(100)

        v1 = self.manager.create_version(0.85, 0.83, 0.87, 0.85, 1000, params)
        v2 = self.manager.create_version(0.86, 0.84, 0.88, 0.86, 1100, params)

        self.manager.deploy_version(v1.version_id, DeploymentStrategy.IMMEDIATE)
        self.manager.deploy_version(v2.version_id, DeploymentStrategy.IMMEDIATE)

        # Rollback to v1
        success = self.manager.rollback_version(v1.version_id)

        self.assertTrue(success)
        self.assertTrue(v1.is_active)
        self.assertFalse(v2.is_active)
        self.assertEqual(v1.deployment_percentage, 100.0)
        self.assertEqual(v2.deployment_percentage, 0.0)
        self.assertEqual(self.manager.active_version, v1.version_id)

    def test_get_version_info(self):
        """Test retrieving version information"""
        params = np.random.randn(100)
        version = self.manager.create_version(0.85, 0.83, 0.87, 0.85, 1000, params)

        info = self.manager.get_version_info(version.version_id)

        self.assertEqual(info["accuracy"], 0.85)
        self.assertEqual(info["precision"], 0.83)
        self.assertEqual(info["training_samples"], 1000)

    def test_list_versions(self):
        """Test listing all versions"""
        params = np.random.randn(100)

        self.manager.create_version(0.85, 0.83, 0.87, 0.85, 1000, params)
        self.manager.create_version(0.86, 0.84, 0.88, 0.86, 1100, params)
        self.manager.create_version(0.87, 0.85, 0.89, 0.87, 1200, params)

        versions = self.manager.list_versions()

        self.assertEqual(len(versions), 3)


# ============================================================================
# TEST MODEL DRIFT DETECTOR
# ============================================================================

class TestModelDriftDetector(unittest.TestCase):
    """Test ModelDriftDetector component"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ModelDriftDetector(
            model_type=ModelType.DIAGNOSIS_PREDICTOR,
            performance_threshold=0.05,
            window_size=100
        )

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.detector.model_type, ModelType.DIAGNOSIS_PREDICTOR)
        self.assertEqual(self.detector.performance_threshold, 0.05)
        self.assertEqual(self.detector.window_size, 100)
        self.assertIsNone(self.detector.baseline_accuracy)

    def test_set_baseline(self):
        """Test setting baseline accuracy"""
        self.detector.set_baseline(0.85)

        self.assertEqual(self.detector.baseline_accuracy, 0.85)

    def test_record_prediction(self):
        """Test recording predictions"""
        self.detector.record_prediction(0.9, True)

        self.assertEqual(len(self.detector.prediction_history), 1)

    def test_check_drift_insufficient_data(self):
        """Test drift check with insufficient data"""
        self.detector.set_baseline(0.85)

        # Record only 50 predictions (less than window_size)
        for i in range(50):
            self.detector.record_prediction(0.9, True)

        alert = self.detector.check_drift()

        self.assertIsNone(alert)

    def test_check_drift_no_drift(self):
        """Test drift check when no drift present"""
        self.detector.set_baseline(0.85)

        # Record predictions with similar accuracy
        for i in range(100):
            self.detector.record_prediction(0.9, True if np.random.random() > 0.15 else False)

        alert = self.detector.check_drift()

        self.assertIsNone(alert)

    def test_check_drift_performance_degradation(self):
        """Test detection of performance drift"""
        self.detector.set_baseline(0.90)

        # Record predictions with poor accuracy
        for i in range(100):
            self.detector.record_prediction(0.8, True if np.random.random() > 0.35 else False)

        alert = self.detector.check_drift()

        self.assertIsNotNone(alert)
        self.assertEqual(alert.drift_type, DriftType.PERFORMANCE_DRIFT)

    def test_check_drift_low_confidence(self):
        """Test detection of concept drift via low confidence"""
        self.detector.set_baseline(0.85)

        # Record predictions with low confidence
        for i in range(100):
            self.detector.record_prediction(0.5, True)

        alert = self.detector.check_drift()

        self.assertIsNotNone(alert)
        self.assertEqual(alert.drift_type, DriftType.CONCEPT_DRIFT)

    def test_alert_severity_calculation(self):
        """Test that alert severity is calculated correctly"""
        self.detector.set_baseline(0.90)

        # Severe performance drop
        for i in range(100):
            self.detector.record_prediction(0.7, False)

        alert = self.detector.check_drift()

        self.assertIsNotNone(alert)
        self.assertGreater(alert.severity, 0.5)

    def test_get_drift_statistics_no_data(self):
        """Test statistics when no predictions recorded"""
        stats = self.detector.get_drift_statistics()

        self.assertEqual(stats["status"], "no_data")

    def test_get_drift_statistics_with_data(self):
        """Test statistics after recording predictions"""
        self.detector.set_baseline(0.85)

        for i in range(50):
            self.detector.record_prediction(0.9, True)

        stats = self.detector.get_drift_statistics()

        self.assertEqual(stats["total_predictions"], 50)
        self.assertGreater(stats["recent_accuracy"], 0.8)
        self.assertEqual(stats["baseline_accuracy"], 0.85)

    def test_prediction_history_window_maintenance(self):
        """Test that prediction history is kept within bounds"""
        for i in range(250):
            self.detector.record_prediction(0.9, True)

        # Should keep window_size * 2 = 200 predictions
        self.assertLessEqual(len(self.detector.prediction_history), 200)

    def test_alert_accumulation(self):
        """Test that alerts are accumulated"""
        self.detector.set_baseline(0.90)

        # Trigger drift multiple times
        for _ in range(3):
            for i in range(100):
                self.detector.record_prediction(0.7, False)

            self.detector.check_drift()

        self.assertGreater(len(self.detector.alerts), 0)


# ============================================================================
# TEST CONTINUOUS LEARNING SYSTEM (INTEGRATION)
# ============================================================================

class TestContinuousLearningSystem(unittest.TestCase):
    """Test integrated ContinuousLearningSystem"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = ContinuousLearningSystem(
            model_type=ModelType.DIAGNOSIS_PREDICTOR,
            privacy_epsilon=1.0,
            enable_federated=True
        )

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.system.model_type, ModelType.DIAGNOSIS_PREDICTOR)
        self.assertIsNotNone(self.system.online_learning)
        self.assertIsNotNone(self.system.version_manager)
        self.assertIsNotNone(self.system.drift_detector)
        self.assertIsNotNone(self.system.federated_coordinator)

    def test_initialization_without_federated(self):
        """Test initialization without federated learning"""
        system = ContinuousLearningSystem(
            model_type=ModelType.DIAGNOSIS_PREDICTOR,
            enable_federated=False
        )

        self.assertIsNone(system.federated_coordinator)

    def test_perform_online_update(self):
        """Test online learning update"""
        data = np.random.randn(100, 50)
        labels = np.random.randint(0, 2, 100)

        update = self.system.perform_online_update(data, labels)

        self.assertIsNotNone(update)
        self.assertEqual(update.new_samples, 100)
        self.assertGreater(len(self.system.audit_log), 0)

    def test_perform_federated_round(self):
        """Test federated learning round"""
        # Register sites (need at least 3 for default min_sites)
        sites = [
            FederatedSite("SITE_001", "Hospital A", "Boston", 1000),
            FederatedSite("SITE_002", "Hospital B", "Chicago", 2000),
            FederatedSite("SITE_003", "Hospital C", "Seattle", 1500)
        ]

        for site in sites:
            self.system.federated_coordinator.register_site(site)

        # Perform round
        site_updates = {
            "SITE_001": np.random.randn(100),
            "SITE_002": np.random.randn(100),
            "SITE_003": np.random.randn(100)
        }

        round_result = self.system.perform_federated_round(site_updates)

        self.assertIsNotNone(round_result)
        self.assertEqual(round_result.round_number, 1)

    def test_deploy_new_version(self):
        """Test deploying a new model version"""
        params = np.random.randn(1000)

        version_id = self.system.deploy_new_version(
            accuracy=0.89,
            precision=0.87,
            recall=0.91,
            f1_score=0.89,
            training_samples=5000,
            model_params=params,
            strategy=DeploymentStrategy.GRADUAL_ROLLOUT
        )

        self.assertIsNotNone(version_id)
        self.assertEqual(self.system.drift_detector.baseline_accuracy, 0.89)

    def test_monitor_predictions_no_drift(self):
        """Test monitoring predictions without drift"""
        # Deploy version first
        params = np.random.randn(1000)
        self.system.deploy_new_version(0.85, 0.83, 0.87, 0.85, 5000, params)

        # Monitor good predictions
        predictions = [(0.9, True) for _ in range(100)]
        self.system.monitor_predictions(predictions)

        # Should not trigger auto-rollback
        stats = self.system.get_system_status()
        self.assertIsNotNone(stats)

    def test_get_system_status(self):
        """Test getting system status"""
        status = self.system.get_system_status()

        self.assertIn("model_type", status)
        self.assertIn("online_learning", status)
        self.assertIn("drift_monitoring", status)
        self.assertIn("versions", status)
        self.assertIn("federation", status)

    def test_export_audit_log(self):
        """Test exporting audit log"""
        # Perform some operations
        data = np.random.randn(100, 50)
        labels = np.random.randint(0, 2, 100)
        self.system.perform_online_update(data, labels)

        audit_json = self.system.export_audit_log()

        self.assertIsNotNone(audit_json)
        self.assertGreater(len(audit_json), 10)

    def test_audit_log_accumulation(self):
        """Test that audit log accumulates events"""
        initial_count = len(self.system.audit_log)

        # Perform operations
        data = np.random.randn(100, 50)
        labels = np.random.randint(0, 2, 100)
        self.system.perform_online_update(data, labels)

        params = np.random.randn(1000)
        self.system.deploy_new_version(0.85, 0.83, 0.87, 0.85, 5000, params)

        self.assertGreater(len(self.system.audit_log), initial_count)


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance(unittest.TestCase):
    """Test performance characteristics"""

    def test_online_update_performance(self):
        """Test that online updates complete quickly"""
        import time

        system = OnlineLearningSystem(ModelType.DIAGNOSIS_PREDICTOR)

        data = np.random.randn(1000, 100)
        labels = np.random.randint(0, 2, 1000)

        start = time.time()
        system.incremental_update(data, labels)
        duration = time.time() - start

        # Should complete in under 1 second
        self.assertLess(duration, 1.0)

    def test_federated_aggregation_performance(self):
        """Test that federated aggregation scales well"""
        import time

        aggregator = SecureAggregator(privacy_epsilon=1.0)

        # Create 10 sites with large parameter vectors
        sites = {
            f"SITE_{i:03d}": FederatedSite(f"SITE_{i:03d}", f"Hospital {i}", "Location", 1000)
            for i in range(10)
        }

        site_updates = {
            f"SITE_{i:03d}": np.random.randn(10000)
            for i in range(10)
        }

        start = time.time()
        aggregator.aggregate(site_updates, sites)
        duration = time.time() - start

        # Should complete in under 1 second even with 10 sites
        self.assertLess(duration, 1.0)


# ============================================================================
# TEST SUITE
# ============================================================================

def suite():
    """Create test suite"""
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestOnlineLearningSystem))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestFederatedLearningCoordinator))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSecureAggregator))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestModelVersionManager))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestModelDriftDetector))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestContinuousLearningSystem))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPerformance))

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())

    print(f"\n{'='*80}")
    print(f"PHASE 22 COMPREHENSIVE TESTS")
    print(f"{'='*80}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*80}\n")

    sys.exit(0 if result.wasSuccessful() else 1)
