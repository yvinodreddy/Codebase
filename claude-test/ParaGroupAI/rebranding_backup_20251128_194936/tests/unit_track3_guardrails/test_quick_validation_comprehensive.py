"""
Comprehensive tests for evaluation/quick_validation.py - Track: track3_guardrails
Target coverage: 90%
Tests REAL code execution with mocked external dependencies
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import json
import subprocess
from pathlib import Path
import sys

try:
    # Add parent directory to path to import quick_validation
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evaluation"))
    from quick_validation import (
        TEST_PROMPTS,
        run_claudeprompt,
        parse_confidence,
        parse_iterations,
        main
    )
except ImportError:
    pytest.skip("Cannot import quick_validation", allow_module_level=True)


class TestTestPrompts:
    """Test the TEST_PROMPTS data structure"""

    def test_test_prompts_structure(self):
        """Test that TEST_PROMPTS has correct structure"""
        assert isinstance(TEST_PROMPTS, dict)
        assert len(TEST_PROMPTS) == 5

        expected_categories = ["factual", "math_logic", "code_generation", "analysis", "edge_cases"]
        for category in expected_categories:
            assert category in TEST_PROMPTS

    def test_test_prompts_content(self):
        """Test that each category has correct number of prompts"""
        assert len(TEST_PROMPTS["factual"]) == 4
        assert len(TEST_PROMPTS["math_logic"]) == 4
        assert len(TEST_PROMPTS["code_generation"]) == 4
        assert len(TEST_PROMPTS["analysis"]) == 4
        assert len(TEST_PROMPTS["edge_cases"]) == 4

    def test_factual_prompts(self):
        """Test factual category prompts"""
        factual = TEST_PROMPTS["factual"]
        assert "capital of France" in factual[0]
        assert "Romeo and Juliet" in factual[1]
        assert "speed of light" in factual[2]
        assert "World War II" in factual[3]

    def test_math_logic_prompts(self):
        """Test math_logic category prompts"""
        math_logic = TEST_PROMPTS["math_logic"]
        assert "15% of 240" in math_logic[0]
        assert any("strawberry" in p for p in math_logic)


class TestParseConfidence:
    """Test parse_confidence function"""

    def test_parse_confidence_with_valid_output(self):
        """Test parsing confidence from valid output"""
        output = "Some text confidence: 95.5% more text"
        result = parse_confidence(output)
        assert result == 95.5

    def test_parse_confidence_without_percent_sign(self):
        """Test parsing confidence without percent sign"""
        output = "confidence: 87.3 other text"
        result = parse_confidence(output)
        assert result == 87.3

    def test_parse_confidence_case_insensitive(self):
        """Test case-insensitive matching"""
        output = "CONFIDENCE: 92.0%"
        result = parse_confidence(output)
        assert result == 92.0

    def test_parse_confidence_with_colon_space(self):
        """Test with colon and space"""
        output = "Confidence: 88.5%"
        result = parse_confidence(output)
        assert result == 88.5

    def test_parse_confidence_no_match(self):
        """Test when confidence not found"""
        output = "Some text without confidence score"
        result = parse_confidence(output)
        assert result == 0

    def test_parse_confidence_empty_string(self):
        """Test with empty string"""
        result = parse_confidence("")
        assert result == 0

    def test_parse_confidence_integer_value(self):
        """Test with integer confidence value"""
        output = "confidence: 95"
        result = parse_confidence(output)
        assert result == 95.0


class TestParseIterations:
    """Test parse_iterations function"""

    def test_parse_iterations_with_valid_output(self):
        """Test parsing iterations from valid output"""
        output = "Some text iteration: 3 more text"
        result = parse_iterations(output)
        assert result == 3

    def test_parse_iterations_case_insensitive(self):
        """Test case-insensitive matching"""
        output = "ITERATION: 5"
        result = parse_iterations(output)
        assert result == 5

    def test_parse_iterations_with_colon_space(self):
        """Test with colon and space"""
        output = "Iteration: 2"
        result = parse_iterations(output)
        assert result == 2

    def test_parse_iterations_no_match(self):
        """Test when iteration not found"""
        output = "Some text without iteration count"
        result = parse_iterations(output)
        assert result == 1  # Default value

    def test_parse_iterations_empty_string(self):
        """Test with empty string"""
        result = parse_iterations("")
        assert result == 1


class TestRunClaudeprompt:
    """Test run_claudeprompt function"""

    @patch('quick_validation.subprocess.run')
    @patch('quick_validation.time.time')
    def test_run_claudeprompt_success(self, mock_time, mock_subprocess):
        """Test successful execution of cpp command"""
        # Mock time
        mock_time.side_effect = [100.0, 105.5]  # Start and end time

        # Mock subprocess result
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Output with confidence: 95.5% iteration: 3"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        result = run_claudeprompt("Test prompt")

        assert result["success"] == True
        assert result["confidence"] == 95.5
        assert result["iterations"] == 3
        assert result["execution_time"] == 5.5
        assert result["output_length"] == len(mock_result.stdout)

    @patch('quick_validation.subprocess.run')
    @patch('quick_validation.time.time')
    def test_run_claudeprompt_timeout(self, mock_time, mock_subprocess):
        """Test timeout handling"""
        # Mock time
        mock_time.side_effect = [100.0, 405.0]  # Exceeds 300s timeout

        # Mock timeout exception
        mock_subprocess.side_effect = subprocess.TimeoutExpired(cmd=[], timeout=300)

        result = run_claudeprompt("Test prompt")

        assert result["success"] == False
        assert result["confidence"] == 0
        assert result["iterations"] == 0
        assert result["execution_time"] == 305.0
        assert "error" in result
        assert result["error"] == "Timeout"

    @patch('quick_validation.subprocess.run')
    @patch('quick_validation.time.time')
    def test_run_claudeprompt_exception(self, mock_time, mock_subprocess):
        """Test general exception handling"""
        # Mock time
        mock_time.side_effect = [100.0, 102.0]

        # Mock exception
        mock_subprocess.side_effect = Exception("Command failed")

        result = run_claudeprompt("Test prompt")

        assert result["success"] == False
        assert result["confidence"] == 0
        assert result["iterations"] == 0
        assert result["execution_time"] == 2.0
        assert "error" in result
        assert result["error"] == "Command failed"

    @patch('quick_validation.subprocess.run')
    @patch('quick_validation.time.time')
    def test_run_claudeprompt_command_format(self, mock_time, mock_subprocess):
        """Test that command is formatted correctly"""
        mock_time.side_effect = [100.0, 101.0]
        mock_result = Mock(returncode=0, stdout="test", stderr="")
        mock_subprocess.return_value = mock_result

        run_claudeprompt("My test prompt")

        # Verify subprocess.run was called with correct arguments
        mock_subprocess.assert_called_once()
        call_args = mock_subprocess.call_args

        assert call_args[0][0] == ["./cpp", "My test prompt", "--verbose"]
        assert call_args[1]["capture_output"] == True
        assert call_args[1]["text"] == True
        assert call_args[1]["timeout"] == 300


class TestMain:
    """Test main function"""

    @patch('quick_validation.run_claudeprompt')
    @patch('builtins.print')
    @patch('builtins.open', create=True)
    @patch('quick_validation.Path')
    def test_main_success_all_prompts(self, mock_path, mock_open, mock_print, mock_run):
        """Test main with all prompts succeeding"""
        # Mock run_claudeprompt to return success for all prompts
        mock_run.return_value = {
            "success": True,
            "confidence": 95.0,
            "iterations": 2,
            "execution_time": 5.0,
            "output_length": 100
        }

        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock Path for results file - properly handle path construction with / operator
        mock_path_instance = MagicMock()
        mock_parent = MagicMock()
        mock_grandparent = MagicMock()
        mock_results_dir = MagicMock()
        mock_results_file = MagicMock()

        # Set up the chain: Path(__file__).parent.parent / "results" / "file.json"
        mock_path.return_value = mock_path_instance
        mock_path_instance.parent = mock_parent
        mock_parent.parent = mock_grandparent
        mock_grandparent.__truediv__.return_value = mock_results_dir
        mock_results_dir.__truediv__.return_value = mock_results_file

        # Run main - should exit with 0 (success rate >= 80%)
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0

        # Verify run_claudeprompt was called 20 times (4 prompts × 5 categories)
        assert mock_run.call_count == 20

    @patch('quick_validation.run_claudeprompt')
    @patch('builtins.print')
    @patch('builtins.open', create=True)
    @patch('quick_validation.Path')
    def test_main_partial_failures(self, mock_path, mock_open, mock_print, mock_run):
        """Test main with some failures (success rate < 80%)"""
        # Mock run_claudeprompt to return mix of success and failure
        call_count = [0]
        def side_effect(prompt):
            call_count[0] += 1
            # 10 successes, 10 failures = 50% success rate
            if call_count[0] <= 10:
                return {
                    "success": True,
                    "confidence": 95.0,
                    "iterations": 2,
                    "execution_time": 5.0,
                    "output_length": 100
                }
            else:
                return {
                    "success": False,
                    "confidence": 0,
                    "iterations": 0,
                    "execution_time": 5.0,
                    "error": "Failed"
                }

        mock_run.side_effect = side_effect

        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock Path for results file - properly handle path construction with / operator
        mock_path_instance = MagicMock()
        mock_parent = MagicMock()
        mock_grandparent = MagicMock()
        mock_results_dir = MagicMock()
        mock_results_file = MagicMock()

        # Set up the chain: Path(__file__).parent.parent / "results" / "file.json"
        mock_path.return_value = mock_path_instance
        mock_path_instance.parent = mock_parent
        mock_parent.parent = mock_grandparent
        mock_grandparent.__truediv__.return_value = mock_results_dir
        mock_results_dir.__truediv__.return_value = mock_results_file

        # Run main - should exit with 1 (success rate < 80%)
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch('quick_validation.run_claudeprompt')
    @patch('builtins.print')
    @patch('builtins.open', create=True)
    @patch('quick_validation.Path')
    def test_main_all_failures(self, mock_path, mock_open, mock_print, mock_run):
        """Test main with all failures"""
        # Mock run_claudeprompt to always fail
        mock_run.return_value = {
            "success": False,
            "confidence": 0,
            "iterations": 0,
            "execution_time": 5.0,
            "error": "Failed"
        }

        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock Path for results file - properly handle path construction with / operator
        mock_path_instance = MagicMock()
        mock_parent = MagicMock()
        mock_grandparent = MagicMock()
        mock_results_dir = MagicMock()
        mock_results_file = MagicMock()

        # Set up the chain: Path(__file__).parent.parent / "results" / "file.json"
        mock_path.return_value = mock_path_instance
        mock_path_instance.parent = mock_parent
        mock_parent.parent = mock_grandparent
        mock_grandparent.__truediv__.return_value = mock_results_dir
        mock_results_dir.__truediv__.return_value = mock_results_file

        # Run main - should exit with 1
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1


def test_integration_parse_functions():
    """Integration test for parse functions"""
    output = """
    Some verbose output here
    confidence: 92.5%
    iteration: 4
    More output
    """

    confidence = parse_confidence(output)
    iterations = parse_iterations(output)

    assert confidence == 92.5
    assert iterations == 4


def test_edge_case_multiple_confidence_values():
    """Test parsing when multiple confidence values present"""
    output = "confidence: 50% later confidence: 95% final"
    result = parse_confidence(output)
    # Should match first occurrence
    assert result == 50.0


def test_edge_case_multiple_iteration_values():
    """Test parsing when multiple iteration values present"""
    output = "iteration: 1 later iteration: 5 final"
    result = parse_iterations(output)
    # Should match first occurrence
    assert result == 1


def test_test_prompts_total_count():
    """Test total number of prompts across all categories"""
    total = sum(len(prompts) for prompts in TEST_PROMPTS.values())
    assert total == 20  # 4 prompts × 5 categories


def test_test_prompts_all_strings():
    """Test that all prompts are non-empty strings"""
    for category, prompts in TEST_PROMPTS.items():
        for prompt in prompts:
            assert isinstance(prompt, str)
            assert len(prompt) > 0


@patch('quick_validation.subprocess.run')
@patch('quick_validation.time.time')
def test_run_claudeprompt_working_directory(mock_time, mock_subprocess):
    """Test that cpp is run from correct directory"""
    mock_time.side_effect = [100.0, 101.0]
    mock_result = Mock(returncode=0, stdout="test", stderr="")
    mock_subprocess.return_value = mock_result

    run_claudeprompt("Test")

    # Verify cwd parameter
    call_args = mock_subprocess.call_args
    assert "cwd" in call_args[1]
    # Should be parent.parent of quick_validation file location


@patch('quick_validation.subprocess.run')
@patch('quick_validation.time.time')
def test_run_claudeprompt_with_stderr_output(mock_time, mock_subprocess):
    """Test handling of stderr output"""
    mock_time.side_effect = [100.0, 105.0]
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "stdout confidence: 90%"
    mock_result.stderr = "stderr iteration: 2"
    mock_subprocess.return_value = mock_result

    result = run_claudeprompt("Test")

    # Both stdout and stderr should be included in output parsing
    assert result["success"] == True
    assert result["confidence"] == 90.0
    assert result["iterations"] == 2
