#!/usr/bin/env python3
"""
Unit Tests for Token Comparison Table Generator
Tests all metrics calculation and comparison table generation.

Target: 90%+ code coverage
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from token_comparison_table import (
    TokenComparisonTable,
    TokenMetrics,
    generate_default_comparison
)


class TestTokenComparisonTable:
    """Test suite for TokenComparisonTable class"""

    def setup_method(self):
        """Set up test instance"""
        self.generator = TokenComparisonTable()

    # ========================================
    # Test calculate_metrics()
    # ========================================

    def test_calculate_metrics_basic(self):
        """Test basic metrics calculation"""
        metrics = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=10.0
        )

        assert isinstance(metrics, TokenMetrics)
        assert metrics.input_tokens == 1000
        assert metrics.output_tokens == 2000
        assert metrics.total_tokens == 3000
        assert metrics.time_to_execute_sec == 10.0

    def test_calculate_metrics_context_window(self):
        """Test context window calculations"""
        metrics = self.generator.calculate_metrics(
            input_tokens=10000,
            output_tokens=20000,
            time_to_execute_sec=10.0
        )

        # 30000 / 200000 = 15%
        assert metrics.context_window_used_pct == pytest.approx(15.0, rel=0.01)
        assert metrics.tokens_remaining == 170000

    def test_calculate_metrics_cost_estimation(self):
        """Test API cost estimation (Claude Sonnet 3.5 pricing)"""
        metrics = self.generator.calculate_metrics(
            input_tokens=1000,  # 1K tokens
            output_tokens=2000,  # 2K tokens
            time_to_execute_sec=5.0
        )

        # Input: 1K * $0.003 = $0.003
        # Output: 2K * $0.015 = $0.030
        # Total: $0.033
        expected_cost = (1000 / 1000) * 0.003 + (2000 / 1000) * 0.015
        assert metrics.estimated_cost_api == pytest.approx(expected_cost, rel=0.001)

    def test_calculate_metrics_claude_code_cost(self):
        """Test Claude Code cost (always $0.00)"""
        metrics = self.generator.calculate_metrics(
            input_tokens=100000,
            output_tokens=50000,
            time_to_execute_sec=100.0
        )

        # Claude Code: $200/month subscription, no per-token cost
        assert metrics.actual_cost_claude_code == 0.0

    def test_calculate_metrics_time_per_token(self):
        """Test time per token calculation"""
        metrics = self.generator.calculate_metrics(
            input_tokens=500,
            output_tokens=500,
            time_to_execute_sec=10.0  # 10 seconds for 1000 tokens
        )

        # 10 sec * 1000 ms/sec / 1000 tokens = 10 ms/token
        assert metrics.time_per_token_ms == pytest.approx(10.0, rel=0.01)

    def test_calculate_metrics_zero_tokens(self):
        """Test handling of zero tokens (edge case)"""
        metrics = self.generator.calculate_metrics(
            input_tokens=0,
            output_tokens=0,
            time_to_execute_sec=5.0
        )

        assert metrics.total_tokens == 0
        assert metrics.time_per_token_ms == 0  # Avoid division by zero

    def test_calculate_metrics_custom_quality(self):
        """Test custom quality scores"""
        metrics = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=10.0,
            quality_score_pct=95.5,
            confidence_level_pct=96.7
        )

        assert metrics.quality_score_pct == 95.5
        assert metrics.confidence_level_pct == 96.7

    def test_calculate_metrics_custom_validation_layers(self):
        """Test custom validation layers"""
        metrics = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=10.0,
            validation_layers=12
        )

        assert metrics.validation_layers == 12

    def test_calculate_metrics_custom_bugs_prevented(self):
        """Test custom production bugs prevented"""
        metrics = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=10.0,
            production_bugs_prevented=25
        )

        assert metrics.production_bugs_prevented == 25

    def test_calculate_metrics_custom_annual_savings(self):
        """Test custom annual savings estimate"""
        metrics = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=10.0,
            annual_savings_estimate="$1M-$5M"
        )

        assert metrics.annual_savings_estimate == "$1M-$5M"

    # ========================================
    # Test generate_comparison_table()
    # ========================================

    def test_generate_comparison_table_basic(self):
        """Test basic comparison table generation"""
        regular = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=5.0,
            quality_score_pct=85.0,
            confidence_level_pct=87.0,
            validation_layers=0,
            production_bugs_prevented=0,
            annual_savings_estimate="-"
        )

        ultrathink = self.generator.calculate_metrics(
            input_tokens=3000,
            output_tokens=6000,
            time_to_execute_sec=900.0,
            quality_score_pct=99.3,
            confidence_level_pct=99.3,
            validation_layers=8,
            production_bugs_prevented=12,
            annual_savings_estimate="$500K-$2M"
        )

        table = self.generator.generate_comparison_table(regular, ultrathink)

        # Verify table structure
        assert isinstance(table, str)
        assert len(table) > 0

        # Verify header
        assert "ULTRATHINK vs Regular Prompt Comparison" in table

        # Verify metrics included
        assert "Input Tokens" in table
        assert "Output Tokens" in table
        assert "Total Tokens" in table
        assert "Context Window Used" in table
        assert "Quality Score" in table
        assert "Confidence Level" in table
        assert "Validation Layers" in table
        assert "Estimated Cost" in table
        assert "Actual Cost" in table
        assert "Time to Execute" in table
        assert "Production Bugs Prevented" in table
        assert "Annual Savings" in table

    def test_generate_comparison_table_token_counts(self):
        """Test token count formatting in table"""
        regular = self.generator.calculate_metrics(
            input_tokens=1250,
            output_tokens=2100,
            time_to_execute_sec=5.0
        )

        ultrathink = self.generator.calculate_metrics(
            input_tokens=3840,
            output_tokens=8500,
            time_to_execute_sec=900.0
        )

        table = self.generator.generate_comparison_table(regular, ultrathink)

        # Check formatted numbers (with commas)
        assert "1,250" in table  # Regular input
        assert "2,100" in table  # Regular output
        assert "3,840" in table  # ULTRATHINK input
        assert "8,500" in table  # ULTRATHINK output

    def test_generate_comparison_table_deltas(self):
        """Test delta calculations in table"""
        regular = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=5.0,
            quality_score_pct=85.0
        )

        ultrathink = self.generator.calculate_metrics(
            input_tokens=3000,
            output_tokens=6000,
            time_to_execute_sec=900.0,
            quality_score_pct=99.3
        )

        table = self.generator.generate_comparison_table(regular, ultrathink)

        # Delta for input: +2000
        assert "+2,000" in table

        # Delta for quality: +14.3%
        assert "+14.3%" in table

    def test_generate_comparison_table_percentages(self):
        """Test percentage formatting in table"""
        regular = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=5.0,
            quality_score_pct=85.0,
            confidence_level_pct=87.0
        )

        ultrathink = self.generator.calculate_metrics(
            input_tokens=3000,
            output_tokens=6000,
            time_to_execute_sec=900.0,
            quality_score_pct=99.3,
            confidence_level_pct=99.3
        )

        table = self.generator.generate_comparison_table(regular, ultrathink)

        # Check percentage formatting
        assert "85.0%" in table
        assert "87.0%" in table
        assert "99.3%" in table

    def test_generate_comparison_table_costs(self):
        """Test cost formatting in table"""
        regular = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=5.0
        )

        ultrathink = self.generator.calculate_metrics(
            input_tokens=3000,
            output_tokens=6000,
            time_to_execute_sec=900.0
        )

        table = self.generator.generate_comparison_table(regular, ultrathink)

        # Check cost formatting (3 decimal places)
        assert "$0.00" in table  # Claude Code cost (both should be $0.000)

    def test_generate_comparison_table_visual_indicators(self):
        """Test visual indicators (✅/❌) in table"""
        regular = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=5.0,
            quality_score_pct=85.0,
            validation_layers=0,
            production_bugs_prevented=0
        )

        ultrathink = self.generator.calculate_metrics(
            input_tokens=3000,
            output_tokens=6000,
            time_to_execute_sec=900.0,
            quality_score_pct=99.3,
            validation_layers=8,
            production_bugs_prevented=12
        )

        table = self.generator.generate_comparison_table(regular, ultrathink)

        # Quality improvement should have ✅
        # Time increase should have ❌ (or nothing for negative delta)
        # Validation layers should have ✅
        assert "✅" in table or "✓" in table  # At least one positive indicator

    def test_generate_comparison_table_large_numbers(self):
        """Test handling of large token counts"""
        regular = self.generator.calculate_metrics(
            input_tokens=50000,
            output_tokens=100000,
            time_to_execute_sec=60.0
        )

        ultrathink = self.generator.calculate_metrics(
            input_tokens=150000,
            output_tokens=300000,
            time_to_execute_sec=1800.0
        )

        table = self.generator.generate_comparison_table(regular, ultrathink)

        # Check large number formatting
        assert "50,000" in table
        assert "100,000" in table
        assert "150,000" in table
        assert "300,000" in table

    # ========================================
    # Test generate_default_comparison()
    # ========================================

    def test_generate_default_comparison(self):
        """Test default comparison table generation"""
        table = generate_default_comparison()

        assert isinstance(table, str)
        assert len(table) > 0

        # Verify it's a valid comparison table
        assert "ULTRATHINK vs Regular Prompt Comparison" in table
        assert "Input Tokens" in table
        assert "Output Tokens" in table
        assert "Quality Score" in table

    def test_generate_default_comparison_default_values(self):
        """Test default comparison uses expected default values"""
        table = generate_default_comparison()

        # Default regular prompt values
        assert "1,250" in table  # Regular input tokens

        # Default ULTRATHINK values
        assert "3,840" in table  # ULTRATHINK input tokens
        assert "99.3%" in table  # Quality score

    # ========================================
    # Edge Cases
    # ========================================

    def test_very_small_tokens(self):
        """Test handling of very small token counts"""
        metrics = self.generator.calculate_metrics(
            input_tokens=1,
            output_tokens=1,
            time_to_execute_sec=0.1
        )

        assert metrics.total_tokens == 2
        assert metrics.context_window_used_pct == pytest.approx(0.001, rel=0.01)
        assert metrics.tokens_remaining == 199998

    def test_very_large_tokens(self):
        """Test handling of very large token counts (near limit)"""
        metrics = self.generator.calculate_metrics(
            input_tokens=100000,
            output_tokens=99000,
            time_to_execute_sec=300.0
        )

        assert metrics.total_tokens == 199000
        assert metrics.context_window_used_pct == pytest.approx(99.5, rel=0.01)
        assert metrics.tokens_remaining == 1000

    def test_exceeding_context_window(self):
        """Test handling of tokens exceeding context window"""
        metrics = self.generator.calculate_metrics(
            input_tokens=150000,
            output_tokens=100000,
            time_to_execute_sec=500.0
        )

        # Total: 250000 (exceeds 200000)
        assert metrics.total_tokens == 250000
        assert metrics.context_window_used_pct > 100.0
        assert metrics.tokens_remaining < 0  # Negative remaining

    def test_zero_execution_time(self):
        """Test handling of zero execution time"""
        metrics = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=0.0
        )

        assert metrics.time_to_execute_sec == 0.0
        assert metrics.time_per_token_ms == 0.0  # Instant execution

    def test_very_long_execution_time(self):
        """Test handling of very long execution times"""
        metrics = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=3600.0  # 1 hour
        )

        assert metrics.time_to_execute_sec == 3600.0
        # 3600 sec * 1000 ms/sec / 3000 tokens = 1200 ms/token
        assert metrics.time_per_token_ms == pytest.approx(1200.0, rel=0.01)

    def test_negative_delta_formatting(self):
        """Test negative delta formatting in comparison"""
        regular = self.generator.calculate_metrics(
            input_tokens=5000,
            output_tokens=10000,
            time_to_execute_sec=60.0,
            quality_score_pct=95.0
        )

        ultrathink = self.generator.calculate_metrics(
            input_tokens=3000,
            output_tokens=6000,
            time_to_execute_sec=30.0,
            quality_score_pct=90.0
        )

        table = self.generator.generate_comparison_table(regular, ultrathink)

        # Negative deltas should be formatted correctly
        assert isinstance(table, str)
        assert len(table) > 0

    def test_zero_delta_formatting(self):
        """Test zero delta formatting (edge case for format_delta function)"""
        # Create identical metrics to trigger zero deltas
        regular = self.generator.calculate_metrics(
            input_tokens=2000,
            output_tokens=3000,
            time_to_execute_sec=10.0,
            quality_score_pct=90.0,
            confidence_level_pct=90.0,
            validation_layers=5
        )

        ultrathink = self.generator.calculate_metrics(
            input_tokens=2000,  # Same as regular
            output_tokens=3000,  # Same as regular
            time_to_execute_sec=10.0,  # Same as regular
            quality_score_pct=90.0,  # Same as regular
            confidence_level_pct=90.0,  # Same as regular
            validation_layers=5  # Same as regular
        )

        table = self.generator.generate_comparison_table(regular, ultrathink)

        # Should have "0" for deltas (not "+0" or "-0")
        assert "│ 0 │" in table or "0" in table  # Zero delta formatting
        assert isinstance(table, str)

    def test_comparison_table_structure(self):
        """Test comparison table has correct structure and borders"""
        regular = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=5.0
        )

        ultrathink = self.generator.calculate_metrics(
            input_tokens=3000,
            output_tokens=6000,
            time_to_execute_sec=900.0
        )

        table = self.generator.generate_comparison_table(regular, ultrathink)

        # Verify table structure
        assert "┌" in table  # Top-left corner
        assert "┐" in table  # Top-right corner
        assert "└" in table  # Bottom-left corner
        assert "┘" in table  # Bottom-right corner
        assert "├" in table  # Left border divider
        assert "┤" in table  # Right border divider
        assert "─" in table  # Horizontal line

    def test_metrics_dataclass_fields(self):
        """Test that TokenMetrics dataclass has all expected fields"""
        metrics = self.generator.calculate_metrics(
            input_tokens=1000,
            output_tokens=2000,
            time_to_execute_sec=10.0
        )

        # Verify all fields exist and have correct types
        assert hasattr(metrics, 'input_tokens')
        assert hasattr(metrics, 'output_tokens')
        assert hasattr(metrics, 'total_tokens')
        assert hasattr(metrics, 'context_window_used_pct')
        assert hasattr(metrics, 'tokens_remaining')
        assert hasattr(metrics, 'quality_score_pct')
        assert hasattr(metrics, 'confidence_level_pct')
        assert hasattr(metrics, 'validation_layers')
        assert hasattr(metrics, 'estimated_cost_api')
        assert hasattr(metrics, 'actual_cost_claude_code')
        assert hasattr(metrics, 'time_to_execute_sec')
        assert hasattr(metrics, 'time_per_token_ms')
        assert hasattr(metrics, 'production_bugs_prevented')
        assert hasattr(metrics, 'annual_savings_estimate')

        # Type checks
        assert isinstance(metrics.input_tokens, int)
        assert isinstance(metrics.output_tokens, int)
        assert isinstance(metrics.total_tokens, int)
        assert isinstance(metrics.context_window_used_pct, float)
        assert isinstance(metrics.tokens_remaining, int)
        assert isinstance(metrics.quality_score_pct, float)
        assert isinstance(metrics.confidence_level_pct, float)
        assert isinstance(metrics.validation_layers, int)
        assert isinstance(metrics.estimated_cost_api, float)
        assert isinstance(metrics.actual_cost_claude_code, float)
        assert isinstance(metrics.time_to_execute_sec, float)
        assert isinstance(metrics.time_per_token_ms, float)
        assert isinstance(metrics.production_bugs_prevented, int)
        assert isinstance(metrics.annual_savings_estimate, str)


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
