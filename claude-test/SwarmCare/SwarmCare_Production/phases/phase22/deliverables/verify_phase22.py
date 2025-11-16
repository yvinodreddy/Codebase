#!/usr/bin/env python3
"""
Phase 22: Continuous Learning & Federated ML
Automated Verification Script

Verifies:
1. Module imports successfully
2. Online learning system works
3. Federated learning coordinator works
4. Model version manager works
5. Model drift detector works
6. Integrated system works
7. All tests pass
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))


class Phase22Verifier:
    """Comprehensive verification for Phase 22"""

    def __init__(self, quick_mode=False):
        self.quick_mode = quick_mode
        self.results = []
        self.start_time = None

    def run_all_checks(self):
        """Run all verification checks"""
        self.start_time = time.time()

        checks = [
            ("Module Import", self.check_module_import),
            ("Online Learning System", self.check_online_learning),
            ("Federated Learning Coordinator", self.check_federated_coordinator),
            ("Model Version Manager", self.check_version_manager),
            ("Model Drift Detector", self.check_drift_detector),
            ("Integrated System", self.check_integrated_system),
        ]

        if not self.quick_mode:
            checks.extend([
                ("All Unit Tests", self.check_unit_tests),
                ("All Integration Tests", self.check_integration_tests),
            ])

        print("\n" + "="*80)
        print("PHASE 22: CONTINUOUS LEARNING & FEDERATED ML - VERIFICATION")
        print("="*80)
        print(f"Mode: {'Quick' if self.quick_mode else 'Full'}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")

        for check_name, check_func in checks:
            self.run_check(check_name, check_func)

        self.print_summary()
        return self.all_passed()

    def run_check(self, name, func):
        """Run a single check"""
        print(f"[{len(self.results)+1}/{6 if self.quick_mode else 8}] {name}...", end=" ", flush=True)

        start = time.time()
        try:
            func()
            duration_ms = (time.time() - start) * 1000
            self.results.append({
                "check": name,
                "status": "PASS",
                "duration_ms": round(duration_ms, 2)
            })
            print(f"✓ PASS ({duration_ms:.2f}ms)")
        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self.results.append({
                "check": name,
                "status": "FAIL",
                "duration_ms": round(duration_ms, 2),
                "error": str(e)
            })
            print(f"✗ FAIL ({duration_ms:.2f}ms)")
            print(f"   Error: {str(e)}")

    def check_module_import(self):
        """Check that module imports successfully"""
        from continuous_learning_system import (
            ContinuousLearningSystem,
            OnlineLearningSystem,
            FederatedLearningCoordinator,
            ModelVersionManager,
            ModelDriftDetector,
            ModelType,
            DeploymentStrategy,
            DriftType
        )

        # Verify classes exist
        assert ContinuousLearningSystem is not None
        assert OnlineLearningSystem is not None
        assert FederatedLearningCoordinator is not None
        assert ModelVersionManager is not None
        assert ModelDriftDetector is not None

        # Verify enums exist
        assert ModelType.DIAGNOSIS_PREDICTOR is not None
        assert DeploymentStrategy.GRADUAL_ROLLOUT is not None
        assert DriftType.PERFORMANCE_DRIFT is not None

    def check_online_learning(self):
        """Check online learning system"""
        from continuous_learning_system import OnlineLearningSystem, ModelType
        import numpy as np

        system = OnlineLearningSystem(ModelType.DIAGNOSIS_PREDICTOR)

        # Perform update
        data = np.random.randn(50, 20)
        labels = np.random.randint(0, 2, 50)

        update = system.incremental_update(data, labels)

        assert update is not None
        assert update.new_samples == 50
        assert update.validation_accuracy > 0.0
        assert update.training_loss >= 0.0
        assert len(update.update_id) > 0

        # Check statistics
        stats = system.get_update_statistics()
        assert stats["total_updates"] == 1
        assert stats["total_samples_processed"] == 50

    def check_federated_coordinator(self):
        """Check federated learning coordinator"""
        from continuous_learning_system import (
            FederatedLearningCoordinator,
            FederatedSite,
            ModelType
        )
        import numpy as np

        coordinator = FederatedLearningCoordinator(
            ModelType.READMISSION_RISK,
            privacy_epsilon=1.0,
            min_sites=2
        )

        # Register sites
        sites = [
            FederatedSite("SITE_A", "Hospital A", "Boston", 1000),
            FederatedSite("SITE_B", "Hospital B", "Chicago", 1500)
        ]

        for site in sites:
            coordinator.register_site(site)

        # Initiate round
        round_obj = coordinator.initiate_training_round()
        assert round_obj is not None
        assert round_obj.round_number == 1
        assert len(round_obj.participating_sites) == 2

        # Aggregate updates
        site_updates = {
            "SITE_A": np.random.randn(100),
            "SITE_B": np.random.randn(100)
        }

        aggregated, privacy_used = coordinator.aggregate_site_updates(site_updates)

        assert aggregated.shape == (100,)
        assert privacy_used > 0.0

    def check_version_manager(self):
        """Check model version manager"""
        from continuous_learning_system import (
            ModelVersionManager,
            ModelType,
            DeploymentStrategy
        )
        import numpy as np

        manager = ModelVersionManager(ModelType.MEDICATION_RECOMMENDER)

        # Create version
        params = np.random.randn(500)
        version = manager.create_version(
            accuracy=0.85,
            precision=0.83,
            recall=0.87,
            f1_score=0.85,
            training_samples=5000,
            model_params=params
        )

        assert version is not None
        assert version.accuracy == 0.85
        assert len(version.version_id) > 0

        # Deploy version
        success = manager.deploy_version(
            version.version_id,
            DeploymentStrategy.GRADUAL_ROLLOUT
        )

        assert success is True
        assert version.is_active is True
        assert version.deployment_percentage == 10.0

        # Increase rollout
        new_percentage = manager.increase_rollout(version.version_id, 40.0)
        assert new_percentage == 50.0

    def check_drift_detector(self):
        """Check model drift detector"""
        from continuous_learning_system import (
            ModelDriftDetector,
            ModelType,
            DriftType
        )

        detector = ModelDriftDetector(
            ModelType.DIAGNOSIS_PREDICTOR,
            performance_threshold=0.05,
            window_size=100
        )

        # Set baseline
        detector.set_baseline(0.90)
        assert detector.baseline_accuracy == 0.90

        # Record good predictions
        for _ in range(100):
            detector.record_prediction(0.9, True)

        alert = detector.check_drift()
        assert alert is None  # No drift with good predictions

        # Record bad predictions to trigger drift
        for _ in range(100):
            detector.record_prediction(0.5, False)

        alert = detector.check_drift()
        assert alert is not None
        assert alert.drift_type == DriftType.PERFORMANCE_DRIFT
        assert alert.severity > 0.0

    def check_integrated_system(self):
        """Check integrated continuous learning system"""
        from continuous_learning_system import (
            ContinuousLearningSystem,
            ModelType,
            DeploymentStrategy,
            FederatedSite
        )
        import numpy as np

        # Initialize system
        system = ContinuousLearningSystem(
            model_type=ModelType.CLINICAL_NLP,
            privacy_epsilon=1.0,
            enable_federated=True
        )

        assert system.model_type == ModelType.CLINICAL_NLP
        assert system.online_learning is not None
        assert system.version_manager is not None
        assert system.drift_detector is not None
        assert system.federated_coordinator is not None

        # Perform online update
        data = np.random.randn(50, 30)
        labels = np.random.randint(0, 3, 50)

        update = system.perform_online_update(data, labels)
        assert update is not None

        # Deploy version
        params = np.random.randn(1000)
        version_id = system.deploy_new_version(
            accuracy=0.88,
            precision=0.86,
            recall=0.90,
            f1_score=0.88,
            training_samples=5000,
            model_params=params,
            strategy=DeploymentStrategy.GRADUAL_ROLLOUT
        )

        assert len(version_id) > 0

        # Get system status
        status = system.get_system_status()
        assert "model_type" in status
        assert "online_learning" in status
        assert "versions" in status

    def check_unit_tests(self):
        """Run all unit tests"""
        import subprocess

        test_file = Path(__file__).parent.parent / "tests" / "test_continuous_learning_comprehensive.py"

        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            raise AssertionError(f"Unit tests failed:\n{result.stdout}\n{result.stderr}")

        # Parse test results
        if "OK" not in result.stdout and "100.0%" not in result.stdout:
            raise AssertionError("Not all unit tests passed")

    def check_integration_tests(self):
        """Run all integration tests"""
        import subprocess

        test_file = Path(__file__).parent.parent / "tests" / "test_integration_scenarios.py"

        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            raise AssertionError(f"Integration tests failed:\n{result.stdout}\n{result.stderr}")

        if "OK" not in result.stdout and "100.0%" not in result.stdout:
            raise AssertionError("Not all integration tests passed")

    def print_summary(self):
        """Print verification summary"""
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        total = len(self.results)
        success_rate = (passed / total * 100) if total > 0 else 0

        total_duration = sum(r["duration_ms"] for r in self.results)

        print("\n" + "="*80)
        print("VERIFICATION SUMMARY")
        print("="*80)
        print(f"Total Checks: {total}")
        print(f"Passed: {passed} ✓")
        print(f"Failed: {failed} ✗")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Total Duration: {total_duration:.2f}ms")
        print("="*80)

        if failed > 0:
            print("\nFailed Checks:")
            for r in self.results:
                if r["status"] == "FAIL":
                    print(f"  - {r['check']}: {r.get('error', 'Unknown error')}")
            print("="*80)

        # Save results
        self.save_results()

    def save_results(self):
        """Save verification results to JSON"""
        output = {
            "phase_id": 22,
            "phase_name": "Continuous Learning & Federated ML",
            "verification_mode": "quick" if self.quick_mode else "full",
            "timestamp": datetime.now().isoformat(),
            "total_checks": len(self.results),
            "passed": sum(1 for r in self.results if r["status"] == "PASS"),
            "failed": sum(1 for r in self.results if r["status"] == "FAIL"),
            "success_rate": sum(1 for r in self.results if r["status"] == "PASS") / len(self.results) * 100,
            "total_duration_ms": sum(r["duration_ms"] for r in self.results),
            "checks": self.results
        }

        output_file = Path(__file__).parent / "verification_report.json"

        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\nResults saved to: {output_file}")

    def all_passed(self):
        """Check if all verifications passed"""
        return all(r["status"] == "PASS" for r in self.results)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Verify Phase 22 Implementation")
    parser.add_argument("--quick", action="store_true", help="Run quick checks only (skip full tests)")
    args = parser.parse_args()

    verifier = Phase22Verifier(quick_mode=args.quick)
    success = verifier.run_all_checks()

    sys.exit(0 if success else 1)
