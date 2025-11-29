#!/usr/bin/env python3
"""
End-to-End Test Framework
Provides utilities for testing complete workflows through the system
"""
import subprocess
import tempfile
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import time


@dataclass
class E2ETestResult:
    """Result from an E2E test execution"""
    success: bool
    duration_seconds: float
    output: str
    exit_code: int
    errors: List[str]
    metrics: Dict[str, Any]


class E2ETestFramework:
    """
    Framework for end-to-end testing of ULTRATHINK system

    Example:
        framework = E2ETestFramework()
        result = framework.run_ultrathink_workflow(
            prompt="What is 2+2?",
            expected_in_output=["4"]
        )
        assert result.success
    """

    def __init__(self, timeout: int = 300):
        self.timeout = timeout
        self.temp_dir = Path(tempfile.mkdtemp())

    def run_ultrathink_workflow(
        self,
        prompt: str,
        verbose: bool = True,
        expected_in_output: Optional[List[str]] = None,
        expected_not_in_output: Optional[List[str]] = None,
        min_output_lines: int = 0,
    ) -> E2ETestResult:
        """
        Run complete ULTRATHINK workflow and validate output

        Args:
            prompt: Input prompt
            verbose: Use verbose mode
            expected_in_output: Strings that must appear in output
            expected_not_in_output: Strings that must NOT appear
            min_output_lines: Minimum expected output lines

        Returns:
            E2ETestResult with test results
        """
        errors = []
        start_time = time.time()

        # Create output file
        output_file = self.temp_dir / f"e2e_output_{int(time.time())}.txt"

        # Build command
        cmd = ["./cpp", prompt]
        if verbose:
            cmd.append("--verbose")

        # Run command
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=Path.cwd()
            )

            output = result.stdout + result.stderr
            exit_code = result.returncode
            duration = time.time() - start_time

            # Write output to file
            output_file.write_text(output)

            # Validate output
            if expected_in_output:
                for expected in expected_in_output:
                    if expected not in output:
                        errors.append(f"Expected string not found: '{expected}'")

            if expected_not_in_output:
                for not_expected in expected_not_in_output:
                    if not_expected in output:
                        errors.append(f"Unexpected string found: '{not_expected}'")

            output_lines = len(output.split("\n"))
            if output_lines < min_output_lines:
                errors.append(
                    f"Output too short: {output_lines} lines (expected >= {min_output_lines})"
                )

            # Extract metrics
            metrics = self._extract_metrics(output)

            return E2ETestResult(
                success=(exit_code == 0 and len(errors) == 0),
                duration_seconds=duration,
                output=output,
                exit_code=exit_code,
                errors=errors,
                metrics=metrics
            )

        except subprocess.TimeoutExpired:
            return E2ETestResult(
                success=False,
                duration_seconds=self.timeout,
                output="",
                exit_code=-1,
                errors=[f"Test timed out after {self.timeout}s"],
                metrics={}
            )
        except Exception as e:
            return E2ETestResult(
                success=False,
                duration_seconds=time.time() - start_time,
                output="",
                exit_code=-1,
                errors=[f"Test failed with exception: {str(e)}"],
                metrics={}
            )

    def run_dashboard_test(
        self,
        port: int = 8889,
        timeout: int = 10
    ) -> E2ETestResult:
        """
        Test dashboard server startup and response

        Args:
            port: Dashboard port
            timeout: Timeout in seconds

        Returns:
            E2ETestResult with test results
        """
        errors = []
        start_time = time.time()

        try:
            # Try to connect to dashboard
            import requests
            response = requests.get(f"http://localhost:{port}/api/state", timeout=timeout)

            if response.status_code == 200:
                data = response.json()
                metrics = {
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "tracks_count": len(data.get("tracks", [])),
                }
                return E2ETestResult(
                    success=True,
                    duration_seconds=time.time() - start_time,
                    output=json.dumps(data, indent=2),
                    exit_code=0,
                    errors=[],
                    metrics=metrics
                )
            else:
                errors.append(f"Unexpected status code: {response.status_code}")

        except Exception as e:
            errors.append(f"Dashboard test failed: {str(e)}")

        return E2ETestResult(
            success=False,
            duration_seconds=time.time() - start_time,
            output="",
            exit_code=-1,
            errors=errors,
            metrics={}
        )

    def _extract_metrics(self, output: str) -> Dict[str, Any]:
        """Extract metrics from ULTRATHINK output"""
        metrics = {}

        # Extract agent count
        if "agents (max:" in output.lower():
            try:
                line = [l for l in output.split("\n") if "agents (max:" in l.lower()][0]
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.lower() == "spawning":
                        agents = int(parts[i+1])
                        metrics["agents_allocated"] = agents
                        break
            except:
                pass

        # Extract stages completed
        stages = sum(1 for line in output.split("\n") if "STAGE" in line and "completed" in line)
        metrics["stages_completed"] = stages

        # Extract guardrail layers
        layers = sum(1 for line in output.split("\n") if "Layer" in line and "✅ PASS" in line)
        metrics["guardrail_layers_passed"] = layers

        return metrics

    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
