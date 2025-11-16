"""
Comprehensive Test Suite for Phase 08: Production Deployment
Tests deployment automation, monitoring, and security
"""

import unittest
import subprocess
import json
from pathlib import Path
import sys
import os

# Add code directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'code'))

from deployment.deployment_manager import DeploymentManager, DeploymentConfig, DeploymentStatus


class TestHelmCharts(unittest.TestCase):
    """Test Helm chart configuration"""

    def setUp(self):
        self.helm_path = Path(__file__).parent.parent / 'deliverables' / 'helm'

    def test_chart_yaml_exists(self):
        """Test Chart.yaml exists"""
        chart_file = self.helm_path / 'Chart.yaml'
        self.assertTrue(chart_file.exists())

    def test_values_yaml_exists(self):
        """Test values.yaml exists"""
        values_file = self.helm_path / 'values.yaml'
        self.assertTrue(values_file.exists())

    def test_helm_lint(self):
        """Test Helm chart linting"""
        if self._helm_installed():
            result = subprocess.run(
                ['helm', 'lint', str(self.helm_path)],
                capture_output=True,
                text=True
            )
            self.assertEqual(result.returncode, 0, f"Helm lint failed: {result.stderr}")

    def test_templates_exist(self):
        """Test essential templates exist"""
        templates_dir = self.helm_path / 'templates'
        required_templates = ['deployment.yaml', 'service.yaml', '_helpers.tpl']

        for template in required_templates:
            template_file = templates_dir / template
            self.assertTrue(template_file.exists(), f"Template missing: {template}")

    def _helm_installed(self) -> bool:
        """Check if Helm is installed"""
        try:
            subprocess.run(['helm', 'version'], capture_output=True, check=True)
            return True
        except:
            return False


class TestKubernetesManifests(unittest.TestCase):
    """Test Kubernetes manifest files"""

    def setUp(self):
        self.security_path = Path(__file__).parent.parent / 'deliverables' / 'security'
        self.monitoring_path = Path(__file__).parent.parent / 'deliverables' / 'monitoring'

    def test_rbac_manifest_exists(self):
        """Test RBAC manifest exists"""
        rbac_file = self.security_path / 'rbac.yaml'
        self.assertTrue(rbac_file.exists())

    def test_network_policies_exist(self):
        """Test network policies exist"""
        np_file = self.security_path / 'network-policies.yaml'
        self.assertTrue(np_file.exists())

    def test_pod_security_policies_exist(self):
        """Test pod security policies exist"""
        psp_file = self.security_path / 'pod-security.yaml'
        self.assertTrue(psp_file.exists())

    def test_prometheus_config_exists(self):
        """Test Prometheus configuration exists"""
        prom_file = self.monitoring_path / 'prometheus-values.yaml'
        self.assertTrue(prom_file.exists())

    def test_grafana_dashboards_exist(self):
        """Test Grafana dashboards exist"""
        grafana_file = self.monitoring_path / 'grafana-dashboards.yaml'
        self.assertTrue(grafana_file.exists())


class TestCICDPipelines(unittest.TestCase):
    """Test CI/CD pipeline configurations"""

    def setUp(self):
        self.cicd_path = Path(__file__).parent.parent / 'deliverables' / 'cicd'

    def test_github_actions_workflow_exists(self):
        """Test GitHub Actions workflow exists"""
        gh_file = self.cicd_path / 'github-actions-deploy.yaml'
        self.assertTrue(gh_file.exists())

    def test_argocd_application_exists(self):
        """Test ArgoCD application exists"""
        argocd_file = self.cicd_path / 'argocd-application.yaml'
        self.assertTrue(argocd_file.exists())


class TestTerraform(unittest.TestCase):
    """Test Terraform configuration"""

    def setUp(self):
        self.terraform_path = Path(__file__).parent.parent / 'deliverables' / 'terraform'

    def test_main_tf_exists(self):
        """Test main.tf exists"""
        main_file = self.terraform_path / 'main.tf'
        self.assertTrue(main_file.exists())

    def test_variables_tf_exists(self):
        """Test variables.tf exists"""
        vars_file = self.terraform_path / 'variables.tf'
        self.assertTrue(vars_file.exists())

    def test_outputs_tf_exists(self):
        """Test outputs.tf exists"""
        outputs_file = self.terraform_path / 'outputs.tf'
        self.assertTrue(outputs_file.exists())

    def test_terraform_validate(self):
        """Test Terraform validation"""
        if self._terraform_installed():
            # Initialize
            subprocess.run(
                ['terraform', 'init'],
                cwd=str(self.terraform_path),
                capture_output=True
            )

            # Validate
            result = subprocess.run(
                ['terraform', 'validate'],
                cwd=str(self.terraform_path),
                capture_output=True,
                text=True
            )
            # Note: May fail if backend is not configured, which is OK for testing
            self.assertIn('Success', result.stdout + result.stderr)

    def _terraform_installed(self) -> bool:
        """Check if Terraform is installed"""
        try:
            subprocess.run(['terraform', 'version'], capture_output=True, check=True)
            return True
        except:
            return False


class TestDeploymentScripts(unittest.TestCase):
    """Test deployment automation scripts"""

    def setUp(self):
        self.scripts_path = Path(__file__).parent.parent / 'deliverables' / 'scripts'

    def test_deploy_script_exists(self):
        """Test deploy.sh exists and is executable"""
        deploy_script = self.scripts_path / 'deploy.sh'
        self.assertTrue(deploy_script.exists())
        self.assertTrue(os.access(deploy_script, os.X_OK))

    def test_rollback_script_exists(self):
        """Test rollback.sh exists and is executable"""
        rollback_script = self.scripts_path / 'rollback.sh'
        self.assertTrue(rollback_script.exists())
        self.assertTrue(os.access(rollback_script, os.X_OK))

    def test_backup_restore_script_exists(self):
        """Test backup-restore.sh exists and is executable"""
        backup_script = self.scripts_path / 'backup-restore.sh'
        self.assertTrue(backup_script.exists())
        self.assertTrue(os.access(backup_script, os.X_OK))


class TestDeploymentManager(unittest.TestCase):
    """Test deployment manager Python code"""

    def test_deployment_manager_initialization(self):
        """Test DeploymentManager initialization"""
        config = DeploymentConfig(
            namespace="test",
            helm_release="test-release",
            chart_path="./chart"
        )
        manager = DeploymentManager(config)
        self.assertEqual(manager.config.namespace, "test")

    def test_deployment_config_defaults(self):
        """Test DeploymentConfig default values"""
        config = DeploymentConfig(
            namespace="test",
            helm_release="test-release",
            chart_path="./chart"
        )
        self.assertEqual(config.timeout, 600)
        self.assertTrue(config.wait)
        self.assertTrue(config.atomic)


class TestProductionReadiness(unittest.TestCase):
    """Test production readiness requirements"""

    def test_all_required_files_exist(self):
        """Test all required production files exist"""
        base_path = Path(__file__).parent.parent

        required_files = [
            'deliverables/helm/Chart.yaml',
            'deliverables/helm/values.yaml',
            'deliverables/security/rbac.yaml',
            'deliverables/security/network-policies.yaml',
            'deliverables/monitoring/prometheus-values.yaml',
            'deliverables/cicd/github-actions-deploy.yaml',
            'deliverables/terraform/main.tf',
            'deliverables/scripts/deploy.sh',
        ]

        for file_path in required_files:
            full_path = base_path / file_path
            self.assertTrue(full_path.exists(), f"Required file missing: {file_path}")

    def test_minimum_file_sizes(self):
        """Test files meet minimum size requirements"""
        base_path = Path(__file__).parent.parent

        min_sizes = {
            'deliverables/helm/Chart.yaml': 500,
            'deliverables/helm/values.yaml': 2000,
            'deliverables/terraform/main.tf': 5000,
            'deliverables/scripts/deploy.sh': 2000,
        }

        for file_path, min_size in min_sizes.items():
            full_path = base_path / file_path
            if full_path.exists():
                actual_size = full_path.stat().st_size
                self.assertGreaterEqual(
                    actual_size,
                    min_size,
                    f"{file_path} is too small: {actual_size} < {min_size} bytes"
                )


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHelmCharts))
    suite.addTests(loader.loadTestsFromTestCase(TestKubernetesManifests))
    suite.addTests(loader.loadTestsFromTestCase(TestCICDPipelines))
    suite.addTests(loader.loadTestsFromTestCase(TestTerraform))
    suite.addTests(loader.loadTestsFromTestCase(TestDeploymentScripts))
    suite.addTests(loader.loadTestsFromTestCase(TestDeploymentManager))
    suite.addTests(loader.loadTestsFromTestCase(TestProductionReadiness))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
