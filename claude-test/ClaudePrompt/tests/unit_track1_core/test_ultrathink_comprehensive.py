"""
Comprehensive tests for ultrathink.py - Track: track1_core
Target coverage: 95%
Tests REAL code execution with mocked external dependencies
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open, call
import sys
import os
from pathlib import Path
from io import StringIO
import argparse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from ultrathink import (
        print_header, show_how_it_works, process_prompt,
        generate_framework_comparison, generate_3way_metrics_comparison,
        generate_web_prompt, main
    )
except ImportError as e:
    pytest.skip(f"Cannot import ultrathink: {e}", allow_module_level=True)


class TestPrintHeader:
    """Test print_header function"""

    @patch('builtins.print')
    def test_print_header_output(self, mock_print):
        """Test that print_header prints correct output"""
        print_header()

        # Verify header was printed
        assert mock_print.call_count >= 5

        # Check for key elements
        calls = [str(call) for call in mock_print.call_args_list]
        output = ''.join(calls)
        assert 'ULTRATHINK' in output
        assert 'Unified Orchestration System' in output


class TestShowHowItWorks:
    """Test show_how_it_works function"""

    @patch('builtins.print')
    def test_show_how_it_works_output(self, mock_print):
        """Test that show_how_it_works prints complete flow"""
        show_how_it_works()

        # Verify extensive output - show_how_it_works() prints a single multi-line string
        assert mock_print.call_count >= 1

        # Check for key stages in the printed content
        calls = [str(call) for call in mock_print.call_args_list]
        output = ''.join(calls)
        assert 'STAGE 1' in output or 'HOW ULTRATHINK WORKS' in output


class TestGenerateFrameworkComparison:
    """Test generate_framework_comparison function"""

    def test_framework_comparison_basic(self):
        """Test basic framework comparison generation"""
        result = generate_framework_comparison(
            prompt="test prompt",
            response_text="test response with many words here",
            confidence=99.5,
            iterations=1,
            duration=5.2,
            context_stats={'total_messages': 1, 'total_tokens': 1000, 'usage_percentage': 0.5}
        )

        assert isinstance(result, str)
        assert 'FRAMEWORK COMPARISON' in result
        assert '99.5' in result
        assert 'Direct Response' in result
        assert 'ULTRATHINK' in result

    def test_framework_comparison_with_multiple_iterations(self):
        """Test framework comparison with multiple refinement iterations"""
        result = generate_framework_comparison(
            prompt="complex task",
            response_text="detailed response",
            confidence=99.9,
            iterations=3,
            duration=15.7,
            context_stats={'total_messages': 3, 'total_tokens': 5000, 'usage_percentage': 2.5}
        )

        assert '99.9' in result
        assert '3' in result  # iteration count
        assert '15.7' in result or '15.70' in result  # duration


class TestGenerate3wayMetricsComparison:
    """Test generate_3way_metrics_comparison function"""

    def test_3way_metrics_comparison_structure(self):
        """Test that 3-way metrics comparison has correct structure"""
        result = generate_3way_metrics_comparison()

        assert isinstance(result, str)
        assert 'PERFORMANCE METRICS COMPARISON' in result
        assert '3-WAY FRAMEWORK COMPARISON' in result
        assert 'Claude Code' in result
        assert 'cpps (Before)' in result
        assert 'cpps (After)' in result

    def test_3way_metrics_includes_all_categories(self):
        """Test that all 8 metric categories are present"""
        result = generate_3way_metrics_comparison()

        # Check for all 8 categories
        assert '1. CONFIDENCE SCORE' in result
        assert '2. VALIDATION LAYERS' in result
        assert '3. CONTEXT MANAGEMENT' in result
        assert '4. VERIFICATION METHODS' in result
        assert '5. LATENCY & PERFORMANCE' in result
        assert '6. FAILURE RESILIENCE' in result
        assert '7. TEST COVERAGE' in result
        assert '8. QUALITY METRICS' in result

    def test_3way_metrics_includes_roi_analysis(self):
        """Test that ROI analysis is included"""
        result = generate_3way_metrics_comparison()

        assert 'ROI ANALYSIS' in result
        assert '$500K-$2M' in result or 'SAVINGS' in result


class TestGenerateWebPrompt:
    """Test generate_web_prompt function"""

    @patch('builtins.print')
    def test_generate_web_prompt_basic(self, mock_print):
        """Test web prompt generation"""
        generate_web_prompt("test prompt for web")

        # Verify output
        assert mock_print.call_count >= 3

        calls = [str(call) for call in mock_print.call_args_list]
        output = ''.join(calls)
        assert 'ULTRATHINK' in output
        assert 'test prompt for web' in output
        assert 'chat.claude.com' in output


class TestProcessPrompt:
    """Test process_prompt function"""

    @patch('ultrathink.sanitize_prompt')
    @patch('ultrathink.PromptHistoryManager')
    @patch('ultrathink.time.time')
    @patch('builtins.print')
    def test_process_prompt_claude_code_mode_basic(self, mock_print, mock_time, mock_history, mock_sanitize):
        """Test process_prompt in Claude Code mode (default)"""
        mock_time.return_value = 100.0
        mock_sanitize.return_value = "sanitized prompt"
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance

        result = process_prompt("test prompt", use_claude_api=False, verbose=False, quiet=False)

        assert result == True
        mock_sanitize.assert_called_once_with("test prompt")

    @patch('ultrathink.sanitize_prompt')
    @patch('ultrathink.SecurityError', Exception)
    @patch('builtins.print')
    def test_process_prompt_security_error(self, mock_print, mock_sanitize):
        """Test process_prompt with security error"""
        mock_sanitize.side_effect = Exception("Security violation")

        result = process_prompt("malicious prompt", use_claude_api=False)

        assert result == False

    @patch('ultrathink.sanitize_prompt')
    @patch('ultrathink.PromptHistoryManager')
    @patch('ultrathink.time.time')
    @patch('builtins.print')
    def test_process_prompt_quiet_mode(self, mock_print, mock_time, mock_history, mock_sanitize):
        """Test process_prompt with quiet flag"""
        mock_time.return_value = 100.0
        mock_sanitize.return_value = "sanitized prompt"
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance

        result = process_prompt("test", use_claude_api=False, quiet=True)

        assert result == True
        # Quiet mode should print less
        # Check that enhanced prompt was printed (it always is in Claude Code mode)
        calls = [str(call) for call in mock_print.call_args_list]
        output = ''.join(calls)
        assert 'ULTRATHINK' in output or 'Quiet Mode' in output

    @patch('ultrathink.sanitize_prompt')
    @patch('ultrathink.PromptHistoryManager')
    @patch('verbose_logger.VerboseLogger')
    @patch('ultrathink.time.time')
    @patch('builtins.print')
    def test_process_prompt_verbose_mode(self, mock_print, mock_time, mock_vlog, mock_history, mock_sanitize):
        """Test process_prompt with verbose flag"""
        mock_time.return_value = 100.0
        mock_sanitize.return_value = "test prompt"
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance

        # Mock VerboseLogger
        mock_vlog_instance = Mock()
        mock_vlog.return_value = mock_vlog_instance

        result = process_prompt("test", use_claude_api=False, verbose=True)

        assert result == True
        # Verbose mode should show stages
        mock_vlog.assert_called()

    @patch('ultrathink.os.getenv')
    @patch('ultrathink.sanitize_prompt')
    @patch('ultrathink.PromptHistoryManager')
    @patch('builtins.print')
    def test_process_prompt_api_mode_no_key(self, mock_print, mock_history, mock_sanitize, mock_getenv):
        """Test process_prompt with API mode but no API key"""
        mock_getenv.return_value = None
        mock_sanitize.return_value = "test"
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance

        result = process_prompt("test", use_claude_api=True)

        assert result == False
        # Should print error about missing API key
        calls = [str(call) for call in mock_print.call_args_list]
        output = ''.join(calls)
        assert 'ANTHROPIC_API_KEY' in output


class TestMain:
    """Test main function"""

    @patch('ultrathink.show_how_it_works')
    @patch('sys.argv', ['ultrathink', '--how'])
    def test_main_show_how_it_works(self, mock_show):
        """Test main with --how flag"""
        result = main()

        assert result == 0
        mock_show.assert_called_once()

    @patch('ultrathink.process_prompt')
    @patch('ultrathink.print_header')
    @patch('sys.argv', ['ultrathink', 'test prompt'])
    def test_main_with_prompt(self, mock_header, mock_process):
        """Test main with basic prompt"""
        mock_process.return_value = True

        result = main()

        assert result == 0
        mock_header.assert_called_once()
        mock_process.assert_called_once()

    @patch('ultrathink.generate_web_prompt')
    @patch('ultrathink.print_header')
    @patch('sys.argv', ['ultrathink', 'test prompt', '--web'])
    def test_main_with_web_flag(self, mock_header, mock_gen_web):
        """Test main with --web flag"""
        result = main()

        assert result == 0
        mock_gen_web.assert_called_once_with('test prompt')

    @patch('builtins.open', new_callable=mock_open, read_data='file content prompt')
    @patch('ultrathink.process_prompt')
    @patch('ultrathink.print_header')
    @patch('sys.argv', ['ultrathink', '--file', 'test.txt'])
    @patch('ultrathink.Path')
    def test_main_with_file_input(self, mock_path, mock_header, mock_process, mock_file):
        """Test main with --file flag"""
        # Mock Path operations for security check
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.resolve.return_value = mock_path_instance
        mock_path_instance.is_file.return_value = True

        # Mock cwd to pass security check
        mock_cwd = MagicMock()
        mock_path.cwd.return_value = mock_cwd
        mock_path_instance.relative_to.return_value = Path('test.txt')

        mock_process.return_value = True

        result = main()

        assert result == 0
        # Should process file content
        assert mock_process.called

    @patch('sys.argv', ['ultrathink', 'test', '--verbose'])
    @patch('ultrathink.process_prompt')
    @patch('ultrathink.print_header')
    def test_main_with_verbose_flag(self, mock_header, mock_process):
        """Test main with --verbose flag"""
        mock_process.return_value = True

        result = main()

        assert result == 0
        # Check that verbose=True was passed
        call_kwargs = mock_process.call_args[1]
        assert call_kwargs['verbose'] == True

    @patch('sys.argv', ['ultrathink', 'test', '--quiet'])
    @patch('ultrathink.process_prompt')
    @patch('ultrathink.print_header')
    def test_main_with_quiet_flag(self, mock_header, mock_process):
        """Test main with --quiet flag"""
        mock_process.return_value = True

        result = main()

        assert result == 0
        # Check that quiet=True was passed
        call_kwargs = mock_process.call_args[1]
        assert call_kwargs['quiet'] == True

    @patch('sys.argv', ['ultrathink', 'test', '--api'])
    @patch('ultrathink.process_prompt')
    @patch('ultrathink.print_header')
    def test_main_with_api_flag(self, mock_header, mock_process):
        """Test main with --api flag"""
        mock_process.return_value = True

        result = main()

        assert result == 0
        # Check that use_claude_api=True was passed
        call_kwargs = mock_process.call_args[1]
        assert call_kwargs['use_claude_api'] == True

    @patch('sys.argv', ['ultrathink', 'test', '--min-confidence', '95.5'])
    @patch('ultrathink.process_prompt')
    @patch('ultrathink.print_header')
    def test_main_with_min_confidence(self, mock_header, mock_process):
        """Test main with --min-confidence flag"""
        mock_process.return_value = True

        result = main()

        assert result == 0
        # Check that min_confidence was passed
        call_kwargs = mock_process.call_args[1]
        assert call_kwargs['min_confidence'] == 95.5

    @patch('sys.argv', ['ultrathink', '--history'])
    @patch('ultrathink.PromptHistoryManager')
    def test_main_with_history_flag(self, mock_history):
        """Test main with --history flag"""
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance
        mock_history_instance.get_all.return_value = []

        with patch('builtins.print'):
            result = main()

        assert result == 0
        mock_history_instance.get_all.assert_called_once()

    @patch('sys.argv', ['ultrathink', '--history-stats'])
    @patch('ultrathink.PromptHistoryManager')
    @patch('builtins.print')
    def test_main_with_history_stats(self, mock_print, mock_history):
        """Test main with --history-stats flag"""
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance
        mock_history_instance.get_statistics.return_value = {
            'total_prompts': 10,
            'total_successful': 9,
            'success_rate': 90.0,
            'total_failed': 1,
            'avg_duration_seconds': 5.5,
            'complexity_breakdown': {'SIMPLE': 5, 'MODERATE': 3, 'COMPLEX': 2},
            'mode_breakdown': {'claude_code': 8, 'api': 2},
            'agents_stats': {'min': 8, 'max': 25, 'avg': 12.5}
        }

        result = main()

        assert result == 0
        mock_history_instance.get_statistics.assert_called_once()

    @patch('sys.argv', ['ultrathink', '--search', 'keyword'])
    @patch('ultrathink.PromptHistoryManager')
    @patch('builtins.print')
    def test_main_with_search(self, mock_print, mock_history):
        """Test main with --search flag"""
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance
        mock_history_instance.search.return_value = [
            {
                'id': 1,
                'prompt': 'test keyword prompt',
                'timestamp': '2025-11-25',
                'complexity': 'SIMPLE',
                'agents_allocated': 8,
                'mode': 'claude_code',
                'duration_seconds': 5.5,
                'success': True
            }
        ]

        result = main()

        assert result == 0
        mock_history_instance.search.assert_called_once_with('keyword')

    @patch('sys.argv', ['ultrathink', '--reuse', '123'])
    @patch('ultrathink.PromptHistoryManager')
    @patch('ultrathink.process_prompt')
    @patch('ultrathink.print_header')
    @patch('builtins.print')
    def test_main_with_reuse(self, mock_print, mock_header, mock_process, mock_history):
        """Test main with --reuse flag"""
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance
        mock_history_instance.get_by_id.return_value = {
            'prompt': 'reused prompt',
            'complexity': 'MODERATE',
            'agents_allocated': 12,
            'timestamp': '2025-11-25',
            'flags': {'verbose': False, 'quiet': False}
        }
        mock_process.return_value = True

        result = main()

        assert result == 0
        mock_history_instance.get_by_id.assert_called_once_with(123)
        # Should process the reused prompt
        assert mock_process.called

    @patch('sys.argv', ['ultrathink', '--history-export', 'history.json'])
    @patch('ultrathink.PromptHistoryManager')
    @patch('builtins.print')
    def test_main_with_history_export(self, mock_print, mock_history):
        """Test main with --history-export flag"""
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance
        mock_history_instance.export_to_file.return_value = True

        result = main()

        assert result == 0
        mock_history_instance.export_to_file.assert_called_once_with('history.json', format='json')

    @patch('sys.argv', ['ultrathink', '--history-clear'])
    @patch('ultrathink.PromptHistoryManager')
    @patch('builtins.input', return_value='yes')
    @patch('builtins.print')
    def test_main_with_history_clear_confirmed(self, mock_print, mock_input, mock_history):
        """Test main with --history-clear flag (confirmed)"""
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance
        mock_history_instance.clear_history.return_value = True

        result = main()

        assert result == 0
        mock_history_instance.clear_history.assert_called_once_with(confirm=True)

    @patch('sys.argv', ['ultrathink', '--history-clear'])
    @patch('ultrathink.PromptHistoryManager')
    @patch('builtins.input', return_value='no')
    @patch('builtins.print')
    def test_main_with_history_clear_cancelled(self, mock_print, mock_input, mock_history):
        """Test main with --history-clear flag (cancelled)"""
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance

        result = main()

        assert result == 0
        # Should not clear history
        mock_history_instance.clear_history.assert_not_called()

    @patch('sys.argv', ['ultrathink'])
    @patch('builtins.print')
    def test_main_no_arguments(self, mock_print):
        """Test main with no arguments (should show help)"""
        with patch('sys.stdout', new=StringIO()):
            result = main()

        assert result == 0

    @patch('sys.argv', ['ultrathink', '--file', '/etc/passwd'])
    @patch('ultrathink.Path')
    @patch('builtins.print')
    def test_main_file_security_system_directory(self, mock_print, mock_path):
        """Test main with file in system directory (should be denied)"""
        # Mock Path for security check
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.resolve.return_value = mock_path_instance
        mock_path_instance.__str__.return_value = '/etc/passwd'

        # Mock cwd/home to fail security check
        mock_cwd = MagicMock()
        mock_home = MagicMock()
        mock_path.cwd.return_value = mock_cwd
        mock_path.home.return_value = mock_home
        mock_path_instance.relative_to.side_effect = ValueError("Not in allowed directory")

        result = main()

        assert result == 1  # Should fail with security error

    @patch('sys.argv', ['ultrathink', '--file', 'nonexistent.txt'])
    @patch('ultrathink.Path')
    @patch('builtins.print')
    def test_main_file_not_found(self, mock_print, mock_path):
        """Test main with non-existent file"""
        # Mock Path for file check
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.resolve.return_value = mock_path_instance
        mock_path_instance.is_file.return_value = False

        # Pass security check but fail file check
        mock_cwd = MagicMock()
        mock_path.cwd.return_value = mock_cwd
        mock_path_instance.relative_to.return_value = Path('nonexistent.txt')

        result = main()

        assert result == 1  # Should fail


class TestProcessPromptApiMode:
    """Test process_prompt with Claude API mode (comprehensive)"""

    @pytest.mark.skip(reason="API mode not supported - NEVER USE CLAUDE API per CLAUDE.md")
    @patch('ultrathink.os.getenv')
    @patch('ultrathink.sanitize_prompt')
    @patch('ultrathink.PromptHistoryManager')
    @patch('ultrathink.ClaudeOrchestrator')
    @patch('verbose_logger.VerboseLogger')
    @patch('ultrathink.time.time')
    @patch('builtins.print')
    def test_process_prompt_api_success(self, mock_print, mock_time, mock_vlog, mock_orchestrator, mock_history, mock_sanitize, mock_getenv):
        """Test successful API processing (SKIPPED - API mode not used)"""
        # Setup mocks
        mock_getenv.return_value = 'test-api-key'
        mock_sanitize.return_value = "test prompt"
        mock_time.return_value = 100.0  # Single value, repeatable (avoids StopIteration)

        # Mock history
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance

        # Mock orchestrator
        mock_orch_instance = Mock()
        mock_orchestrator.return_value = mock_orch_instance

        # Mock response
        mock_response = Mock()
        mock_response.final_confidence = 99.5
        mock_response.total_tokens = 1000
        mock_response.cost_estimate = 0.015
        mock_response.response_text = "Test response"
        mock_response.claude_model = "claude-sonnet-4-5"
        mock_response.orchestration_result = Mock()
        mock_response.orchestration_result.iterations_performed = 1
        mock_response.orchestration_result.total_duration_seconds = 5.5
        mock_response.orchestration_result.quality_metrics = {
            'context_management': {
                'total_messages': 1,
                'total_tokens': 1000,
                'usage_percentage': 0.5,
                'compactions_performed': 0,
                'total_tokens_saved': 0
            },
            'confidence_breakdown': {
                'guardrails': 100.0,
                'verification': 99.0
            }
        }
        mock_response.output_validation = {'success': True, 'confidence': 100.0}
        mock_response.verification_result = {'overall_passed': True, 'overall_confidence': 99.0, 'overall_message': 'All checks passed'}

        mock_orch_instance.process_with_validation.return_value = mock_response
        mock_orch_instance.get_statistics.return_value = {'cache_read_tokens': 0, 'cache_creation_tokens': 0}

        # Mock VerboseLogger
        mock_vlog_instance = Mock()
        mock_vlog.return_value = mock_vlog_instance

        # Execute
        result = process_prompt("test", use_claude_api=True, verbose=True)

        assert result == True
        mock_orch_instance.process_with_validation.assert_called_once()

    @patch('ultrathink.os.getenv')
    @patch('ultrathink.sanitize_prompt')
    @patch('ultrathink.PromptHistoryManager')
    @patch('ultrathink.ClaudeOrchestrator')
    @patch('verbose_logger.VerboseLogger')
    @patch('ultrathink.time.time')
    @patch('builtins.print')
    def test_process_prompt_api_exception(self, mock_print, mock_time, mock_vlog, mock_orchestrator, mock_history, mock_sanitize, mock_getenv):
        """Test API processing with exception"""
        mock_getenv.return_value = 'test-api-key'
        mock_sanitize.return_value = "test"
        mock_time.return_value = 100.0

        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance

        mock_orch_instance = Mock()
        mock_orchestrator.return_value = mock_orch_instance
        mock_orch_instance.process_with_validation.side_effect = Exception("API error")

        mock_vlog_instance = Mock()
        mock_vlog.return_value = mock_vlog_instance

        result = process_prompt("test", use_claude_api=True, verbose=True)

        assert result == False


class TestEdgeCases:
    """Test edge cases and error conditions"""

    @patch('ultrathink.sanitize_prompt')
    def test_process_prompt_empty_string(self, mock_sanitize):
        """Test processing empty prompt"""
        mock_sanitize.return_value = ""

        with patch('ultrathink.PromptHistoryManager'), \
             patch('builtins.print'):
            result = process_prompt("", use_claude_api=False)

        # Should still process (empty is valid)
        assert result == True

    @patch('ultrathink.sanitize_prompt')
    @patch('ultrathink.PromptHistoryManager')
    @patch('builtins.print')
    def test_process_prompt_very_long_prompt(self, mock_print, mock_history, mock_sanitize):
        """Test processing very long prompt (1000+ words)"""
        long_prompt = " ".join(["word"] * 1000)
        mock_sanitize.return_value = long_prompt
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance

        result = process_prompt(long_prompt, use_claude_api=False)

        assert result == True

    def test_generate_framework_comparison_zero_iterations(self):
        """Test framework comparison with 0 iterations (edge case)"""
        result = generate_framework_comparison(
            prompt="test",
            response_text="response",
            confidence=85.0,
            iterations=0,  # Edge case
            duration=0.5,
            context_stats={'total_messages': 0, 'total_tokens': 0, 'usage_percentage': 0}
        )

        assert isinstance(result, str)
        assert '85.0' in result or '85' in result

    @patch('sys.argv', ['ultrathink', '--file', 'test.txt'])
    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('ultrathink.Path')
    @patch('builtins.print')
    def test_main_file_read_error(self, mock_print, mock_path, mock_open):
        """Test main with file read error"""
        # Mock Path for security check
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.resolve.return_value = mock_path_instance
        mock_path_instance.is_file.return_value = True

        mock_cwd = MagicMock()
        mock_path.cwd.return_value = mock_cwd
        mock_path_instance.relative_to.return_value = Path('test.txt')

        result = main()

        assert result == 1  # Should fail with file read error


class TestComplexityDetection:
    """Test prompt complexity detection in process_prompt"""

    @patch('ultrathink.sanitize_prompt')
    @patch('ultrathink.PromptHistoryManager')
    @patch('verbose_logger.VerboseLogger')
    @patch('builtins.print')
    def test_complexity_simple(self, mock_print, mock_vlog, mock_history, mock_sanitize):
        """Test simple prompt complexity detection"""
        simple_prompt = "short"
        mock_sanitize.return_value = simple_prompt
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance
        mock_vlog_instance = Mock()
        mock_vlog.return_value = mock_vlog_instance

        result = process_prompt(simple_prompt, verbose=True)

        assert result == True
        # In verbose mode, complexity is detected and logged
        mock_vlog.assert_called()

    @patch('ultrathink.sanitize_prompt')
    @patch('ultrathink.PromptHistoryManager')
    @patch('verbose_logger.VerboseLogger')
    @patch('builtins.print')
    def test_complexity_moderate(self, mock_print, mock_vlog, mock_history, mock_sanitize):
        """Test moderate prompt complexity detection"""
        moderate_prompt = " ".join(["word"] * 30)  # 30 words
        mock_sanitize.return_value = moderate_prompt
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance
        mock_vlog_instance = Mock()
        mock_vlog.return_value = mock_vlog_instance

        result = process_prompt(moderate_prompt, verbose=True)

        assert result == True

    @patch('ultrathink.sanitize_prompt')
    @patch('ultrathink.PromptHistoryManager')
    @patch('verbose_logger.VerboseLogger')
    @patch('builtins.print')
    def test_complexity_complex(self, mock_print, mock_vlog, mock_history, mock_sanitize):
        """Test complex prompt complexity detection"""
        complex_prompt = " ".join(["word"] * 100)  # 100 words
        mock_sanitize.return_value = complex_prompt
        mock_history_instance = Mock()
        mock_history.return_value = mock_history_instance
        mock_vlog_instance = Mock()
        mock_vlog.return_value = mock_vlog_instance

        result = process_prompt(complex_prompt, verbose=True)

        assert result == True


# Test module imports
def test_module_imports():
    """Test that ultrathink module can be imported"""
    import ultrathink
    assert ultrathink is not None
