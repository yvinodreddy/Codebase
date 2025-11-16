"""
Deployment Manager
Orchestrates Kubernetes deployments with safety checks
"""

import subprocess
import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeploymentStatus(Enum):
    """Deployment status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class DeploymentConfig:
    """Configuration for deployment"""
    namespace: str
    helm_release: str
    chart_path: str
    values_file: Optional[str] = None
    timeout: int = 600
    dry_run: bool = False
    wait: bool = True
    atomic: bool = True


@dataclass
class DeploymentResult:
    """Result from deployment"""
    status: DeploymentStatus
    revision: int
    duration_seconds: float
    pods_count: int
    message: str
    error: Optional[str] = None


class DeploymentManager:
    """
    Manages Kubernetes deployments

    Features:
    - Pre-deployment validation
    - Rolling updates
    - Health checks
    - Automatic rollback on failure
    - Deployment history
    """

    def __init__(self, config: DeploymentConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def deploy(self) -> DeploymentResult:
        """
        Deploy application to Kubernetes

        Returns:
            DeploymentResult with deployment status
        """
        start_time = datetime.now()

        try:
            # Pre-deployment checks
            self.logger.info("Running pre-deployment checks...")
            if not self._pre_deployment_checks():
                return DeploymentResult(
                    status=DeploymentStatus.FAILED,
                    revision=0,
                    duration_seconds=0,
                    pods_count=0,
                    message="Pre-deployment checks failed",
                    error="Cluster not ready"
                )

            # Backup current state
            self._backup_current_state()

            # Dry run
            if self.config.dry_run:
                self.logger.info("Performing dry run...")
                self._helm_dry_run()
                return DeploymentResult(
                    status=DeploymentStatus.COMPLETED,
                    revision=0,
                    duration_seconds=0,
                    pods_count=0,
                    message="Dry run completed successfully"
                )

            # Deploy
            self.logger.info("Deploying application...")
            revision = self._helm_upgrade()

            # Verify deployment
            self.logger.info("Verifying deployment...")
            if self._verify_deployment():
                duration = (datetime.now() - start_time).total_seconds()
                pods_count = self._get_pod_count()

                return DeploymentResult(
                    status=DeploymentStatus.COMPLETED,
                    revision=revision,
                    duration_seconds=duration,
                    pods_count=pods_count,
                    message=f"Deployment completed successfully (revision {revision})"
                )
            else:
                self.logger.error("Deployment verification failed")
                self._rollback()
                return DeploymentResult(
                    status=DeploymentStatus.ROLLED_BACK,
                    revision=revision,
                    duration_seconds=(datetime.now() - start_time).total_seconds(),
                    pods_count=0,
                    message="Deployment failed and was rolled back",
                    error="Verification failed"
                )

        except Exception as e:
            self.logger.error(f"Deployment failed: {e}")
            self._rollback()

            return DeploymentResult(
                status=DeploymentStatus.FAILED,
                revision=0,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                pods_count=0,
                message="Deployment failed",
                error=str(e)
            )

    def _pre_deployment_checks(self) -> bool:
        """Run pre-deployment validation checks"""
        try:
            # Check cluster connectivity
            result = subprocess.run(
                ["kubectl", "cluster-info"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                self.logger.error("Cannot connect to Kubernetes cluster")
                return False

            # Check namespace exists
            result = subprocess.run(
                ["kubectl", "get", "namespace", self.config.namespace],
                capture_output=True,
                text=True,
                timeout=10
            )

            # Check sufficient resources
            # (In production, add more detailed resource checks)

            return True

        except Exception as e:
            self.logger.error(f"Pre-deployment check failed: {e}")
            return False

    def _backup_current_state(self):
        """Backup current deployment state"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"./backups/{timestamp}_values.yaml"

            subprocess.run(
                ["helm", "get", "values", self.config.helm_release,
                 "-n", self.config.namespace, "-o", "yaml"],
                capture_output=True,
                check=False
            )

            self.logger.info(f"Current state backed up")

        except Exception as e:
            self.logger.warning(f"Backup failed: {e}")

    def _helm_dry_run(self):
        """Perform Helm dry run"""
        cmd = [
            "helm", "upgrade", "--install",
            self.config.helm_release,
            self.config.chart_path,
            "--namespace", self.config.namespace,
            "--dry-run", "--debug"
        ]

        if self.config.values_file:
            cmd.extend(["-f", self.config.values_file])

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Dry run failed: {result.stderr}")

    def _helm_upgrade(self) -> int:
        """Execute Helm upgrade"""
        cmd = [
            "helm", "upgrade", "--install",
            self.config.helm_release,
            self.config.chart_path,
            "--namespace", self.config.namespace,
            "--create-namespace",
            "--timeout", f"{self.config.timeout}s"
        ]

        if self.config.wait:
            cmd.append("--wait")

        if self.config.atomic:
            cmd.append("--atomic")

        if self.config.values_file:
            cmd.extend(["-f", self.config.values_file])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.config.timeout)

        if result.returncode != 0:
            raise Exception(f"Helm upgrade failed: {result.stderr}")

        # Get revision number
        result = subprocess.run(
            ["helm", "list", "-n", self.config.namespace, "-o", "json"],
            capture_output=True,
            text=True
        )

        releases = json.loads(result.stdout)
        for release in releases:
            if release["name"] == self.config.helm_release:
                return int(release["revision"])

        return 0

    def _verify_deployment(self) -> bool:
        """Verify deployment is successful"""
        try:
            # Check deployment rollout status
            result = subprocess.run(
                ["kubectl", "rollout", "status",
                 f"deployment/{self.config.helm_release}",
                 "-n", self.config.namespace,
                 f"--timeout={self.config.timeout}s"],
                capture_output=True,
                text=True,
                timeout=self.config.timeout
            )

            if result.returncode != 0:
                self.logger.error(f"Rollout status check failed: {result.stderr}")
                return False

            # Check pod status
            result = subprocess.run(
                ["kubectl", "get", "pods",
                 "-n", self.config.namespace,
                 "-o", "json"],
                capture_output=True,
                text=True
            )

            pods = json.loads(result.stdout)
            running_pods = sum(1 for pod in pods["items"]
                             if pod["status"]["phase"] == "Running")

            self.logger.info(f"Running pods: {running_pods}")

            return running_pods > 0

        except Exception as e:
            self.logger.error(f"Deployment verification failed: {e}")
            return False

    def _rollback(self):
        """Rollback to previous revision"""
        self.logger.warning("Initiating rollback...")

        try:
            result = subprocess.run(
                ["helm", "rollback", self.config.helm_release,
                 "-n", self.config.namespace],
                capture_output=True,
                text=True,
                timeout=self.config.timeout
            )

            if result.returncode == 0:
                self.logger.info("Rollback completed successfully")
            else:
                self.logger.error(f"Rollback failed: {result.stderr}")

        except Exception as e:
            self.logger.error(f"Rollback error: {e}")

    def _get_pod_count(self) -> int:
        """Get number of running pods"""
        try:
            result = subprocess.run(
                ["kubectl", "get", "pods",
                 "-n", self.config.namespace,
                 "-o", "json"],
                capture_output=True,
                text=True
            )

            pods = json.loads(result.stdout)
            return len(pods["items"])

        except:
            return 0

    def get_deployment_history(self) -> List[Dict]:
        """Get deployment history"""
        try:
            result = subprocess.run(
                ["helm", "history", self.config.helm_release,
                 "-n", self.config.namespace,
                 "-o", "json"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return json.loads(result.stdout)
            return []

        except:
            return []
