#!/usr/bin/env python3
"""Comprehensive test suite for code_review_automation.py - Target: 90%+ coverage"""
import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
from dataclasses import asdict
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from scripts.code_review_automation import CodeQualityMetrics, CodeReviewAutomation

class TestCodeQualityMetrics:
    def test_dataclass_initialization(self):
        metrics = CodeQualityMetrics(
            timestamp="2025-11-22 10:00:00",
            black_compliant=True,
            black_files_need_formatting=0,
            isort_compliant=True,
            isort_files_need_sorting=0,
            pylint_score=9.5,
            pylint_violations=2,
            mypy_errors=0,
            mypy_warnings=1,
            bandit_issues={"high": 0, "medium": 1, "low": 2},
            safety_vulnerabilities=0,
            test_coverage=95.5,
            tests_passed=100,
            tests_failed=0,
            tests_total=100
        )

        assert metrics.timestamp == "2025-11-22 10:00:00"
        assert metrics.pylint_score == 9.5
        assert metrics.test_coverage == 95.5

    def test_dataclass_to_dict(self):
        metrics = CodeQualityMetrics(
            timestamp="2025-11-22",
            black_compliant=False,
            black_files_need_formatting=3,
            isort_compliant=True,
            isort_files_need_sorting=0,
            pylint_score=8.0,
            pylint_violations=5,
            mypy_errors=2,
            mypy_warnings=3,
            bandit_issues={"high": 1, "medium": 2, "low": 3},
            safety_vulnerabilities=1,
            test_coverage=85.0,
            tests_passed=90,
            tests_failed=10,
            tests_total=100
        )

        metrics_dict = asdict(metrics)
        assert metrics_dict['black_compliant'] == False
        assert metrics_dict['bandit_issues']['high'] == 1

class TestCodeReviewAutomation:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "reports"
        self.reviewer = CodeReviewAutomation(str(self.output_dir))

    def teardown_method(self):
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        assert self.reviewer.output_dir == self.output_dir
        assert self.output_dir.exists()
        assert self.reviewer.results == {}

    @patch('subprocess.run')
    def test_run_black_compliant(self, mock_run):
        mock_run.return_value = Mock(returncode=0, stdout="", text=True)
        compliant, files = self.reviewer.run_black()
        assert compliant == True
        assert files == 0

    @patch('subprocess.run')
    def test_run_black_needs_formatting(self, mock_run):
        mock_run.return_value = Mock(
            returncode=1,
            stdout="would reformat file1.py\nwould reformat file2.py",
            text=True
        )
        compliant, files = self.reviewer.run_black()
        assert compliant == False
        assert files == 2

    @patch('subprocess.run', side_effect=Exception("Command failed"))
    def test_run_black_error(self, mock_run):
        compliant, files = self.reviewer.run_black()
        assert compliant == False
        assert files == 0

    @patch('subprocess.run')
    def test_run_isort_compliant(self, mock_run):
        mock_run.return_value = Mock(returncode=0, stdout="", text=True)
        compliant, files = self.reviewer.run_isort()
        assert compliant == True
        assert files == 0

    @patch('subprocess.run')
    def test_run_isort_needs_sorting(self, mock_run):
        mock_run.return_value = Mock(
            returncode=1,
            stdout="file1.py would be reformatted",
            text=True
        )
        compliant, files = self.reviewer.run_isort()
        assert compliant == False
        assert files == 1

    @patch('subprocess.run')
    def test_run_pylint(self, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Your code has been rated at 9.50/10\n*** Error in file.py",
            text=True
        )
        score, violations = self.reviewer.run_pylint()
        assert score == 9.5
        assert violations == 1

    @patch('subprocess.run', side_effect=Exception("Pylint failed"))
    def test_run_pylint_error(self, mock_run):
        score, violations = self.reviewer.run_pylint()
        assert score == 0.0
        assert violations == 0

    @patch('subprocess.run')
    def test_run_mypy(self, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout="error: Something\nerror: Another\nnote: A note",
            text=True
        )
        errors, warnings = self.reviewer.run_mypy()
        assert errors == 2
        assert warnings == 1

    @patch('subprocess.run')
    def test_run_bandit(self, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout=json.dumps({
                "results": [
                    {"issue_severity": "high"},
                    {"issue_severity": "medium"},
                    {"issue_severity": "medium"},
                    {"issue_severity": "low"}
                ]
            }),
            text=True
        )
        issues = self.reviewer.run_bandit()
        assert issues["high"] == 1
        assert issues["medium"] == 2
        assert issues["low"] == 1

    @patch('subprocess.run')
    def test_run_bandit_empty_results(self, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout=json.dumps({"results": []}),
            text=True
        )
        issues = self.reviewer.run_bandit()
        assert issues["high"] == 0
        assert issues["medium"] == 0
        assert issues["low"] == 0

    @patch('subprocess.run')
    def test_run_safety(self, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout=json.dumps([{"vulnerability": "test"}, {"vulnerability": "test2"}]),
            text=True
        )
        vulnerabilities = self.reviewer.run_safety()
        assert vulnerabilities == 2

    @patch('subprocess.run')
    def test_run_safety_no_vulnerabilities(self, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout=json.dumps([]),
            text=True
        )
        vulnerabilities = self.reviewer.run_safety()
        assert vulnerabilities == 0

    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_run_tests(self, mock_exists, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout=" PASSED PASSED FAILED PASSED",
            text=True
        )
        mock_exists.return_value = True

        with patch('builtins.open', mock_open(read_data=json.dumps({
            "totals": {"percent_covered": 92.5}
        }))):
            coverage, passed, failed, total = self.reviewer.run_tests()

            assert coverage == 92.5
            assert passed == 3
            assert failed == 1
            assert total == 4

    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_run_tests_no_coverage_file(self, mock_exists, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout=" PASSED PASSED",
            text=True
        )
        mock_exists.return_value = False

        coverage, passed, failed, total = self.reviewer.run_tests()

        assert coverage == 0.0
        assert passed == 2
        assert failed == 0
        assert total == 2

    def test_generate_report(self):
        metrics = CodeQualityMetrics(
            timestamp="2025-11-22 10:00:00",
            black_compliant=True,
            black_files_need_formatting=0,
            isort_compliant=True,
            isort_files_need_sorting=0,
            pylint_score=9.5,
            pylint_violations=2,
            mypy_errors=0,
            mypy_warnings=1,
            bandit_issues={"high": 0, "medium": 1, "low": 2},
            safety_vulnerabilities=0,
            test_coverage=95.5,
            tests_passed=100,
            tests_failed=0,
            tests_total=100
        )

        self.reviewer.generate_report(metrics)

        # Check JSON report exists
        json_files = list(self.output_dir.glob("report_*.json"))
        assert len(json_files) == 1

        # Check HTML report exists
        html_file = self.output_dir / "latest_report.html"
        assert html_file.exists()

        # Verify JSON content
        with open(json_files[0]) as f:
            data = json.load(f)
        assert data['test_coverage'] == 95.5

    def test_generate_html_report(self):
        metrics = CodeQualityMetrics(
            timestamp="2025-11-22 10:00:00",
            black_compliant=True,
            black_files_need_formatting=0,
            isort_compliant=False,
            isort_files_need_sorting=2,
            pylint_score=7.5,
            pylint_violations=10,
            mypy_errors=3,
            mypy_warnings=5,
            bandit_issues={"high": 1, "medium": 2, "low": 3},
            safety_vulnerabilities=1,
            test_coverage=85.0,
            tests_passed=90,
            tests_failed=10,
            tests_total=100
        )

        html = self.reviewer._generate_html_report(metrics)

        assert "Code Quality Report" in html
        assert "85.0%" in html
        assert "7.50/10" in html  # Pylint score
        assert "90/100" in html  # Tests passed
        assert "NEEDS IMPROVEMENT" in html  # Coverage < 90

    @patch.object(CodeReviewAutomation, 'run_black')
    @patch.object(CodeReviewAutomation, 'run_isort')
    @patch.object(CodeReviewAutomation, 'run_pylint')
    @patch.object(CodeReviewAutomation, 'run_mypy')
    @patch.object(CodeReviewAutomation, 'run_bandit')
    @patch.object(CodeReviewAutomation, 'run_safety')
    @patch.object(CodeReviewAutomation, 'run_tests')
    @patch.object(CodeReviewAutomation, 'generate_report')
    def test_run_full_review(self, mock_report, mock_tests, mock_safety, mock_bandit,
                            mock_mypy, mock_pylint, mock_isort, mock_black):
        mock_black.return_value = (True, 0)
        mock_isort.return_value = (True, 0)
        mock_pylint.return_value = (9.0, 5)
        mock_mypy.return_value = (0, 2)
        mock_bandit.return_value = {"high": 0, "medium": 1, "low": 2}
        mock_safety.return_value = 0
        mock_tests.return_value = (92.5, 95, 5, 100)

        metrics = self.reviewer.run_full_review()

        assert metrics.black_compliant == True
        assert metrics.pylint_score == 9.0
        assert metrics.test_coverage == 92.5
        assert metrics.tests_passed == 95
        assert metrics.tests_total == 100

        # Verify report was generated
        mock_report.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])