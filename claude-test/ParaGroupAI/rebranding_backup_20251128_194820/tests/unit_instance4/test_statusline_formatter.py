#!/usr/bin/env python3
"""Comprehensive test suite for statusline_formatter.py - Target: 90%+ coverage"""
import pytest
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from statusline_formatter import StatuslineFormatter

class TestStatuslineFormatter:
    def setup_method(self):
        self.formatter = StatuslineFormatter(instance_mode=False)
        self.instance_formatter = StatuslineFormatter(instance_mode=True)
    
    def test_initialization(self):
        assert self.formatter.instance_mode == False
        assert self.instance_formatter.instance_mode == True
    
    def test_format_agents_simple(self):
        result = self.formatter.format_agents(25)
        assert result == "Agents: 25"
    
    def test_format_agents_with_total(self):
        result = self.formatter.format_agents(25, total=100)
        assert result == "Agents: 25/100"
    
    def test_format_agents_instance_mode(self):
        result = self.instance_formatter.format_agents(25, total=145, instance_count=5)
        assert result == "Agents: 25/145 (5)"
    
    def test_format_tokens(self):
        result = self.formatter.format_tokens(15000, 200000, show_percentage=True)
        assert result == "Tokens: 15k/200k (7.5%)"
    
    def test_format_tokens_no_percentage(self):
        result = self.formatter.format_tokens(15000, 200000, show_percentage=False)
        assert result == "Tokens: 15k/200k"
    
    def test_format_confidence_valid(self):
        result = self.formatter.format_confidence(99.2)
        assert result == "Conf: 99.2%"
    
    def test_format_confidence_zero(self):
        result = self.formatter.format_confidence(0)
        assert result == "Conf: --"
    
    def test_format_status(self):
        result = self.formatter.format_status("🟢 OPTIMAL")
        assert result == "Status: 🟢 OPTIMAL"
    
    def test_format_all_shared_mode(self):
        result = self.formatter.format_all(
            current_agents=25, tokens_used=15000, tokens_total=200000,
            confidence=99.2, status="🟢 OPTIMAL"
        )
        assert "Agents: 25" in result
        assert "Tokens: 15k/200k (7.5%)" in result
        assert "Conf: 99.2%" in result
        assert "Status: 🟢 OPTIMAL" in result
    
    def test_format_all_instance_mode(self):
        result = self.instance_formatter.format_all(
            current_agents=25, total_agents=145, instance_count=5,
            tokens_used=15000, tokens_total=200000,
            confidence=99.2, status="🟢 OPTIMAL"
        )
        assert "Agents: 25/145 (5)" in result
    
    def test_format_compact(self):
        result = self.formatter.format_compact(
            current_agents=25, tokens_pct=7.5, confidence=99.2
        )
        assert "A:25" in result
        assert "T:7.5%" in result
        assert "C:99.2%" in result
    
    def test_format_compact_instance_mode(self):
        result = self.instance_formatter.format_compact(
            current_agents=25, total_agents=145, instance_count=5,
            tokens_pct=7.5, confidence=99.2
        )
        assert "A:25/145(5)" in result
    
    def test_format_json(self):
        result = self.formatter.format_json(
            current_agents=25, tokens_used=15000, tokens_total=200000,
            confidence=99.2, status="🟢 OPTIMAL"
        )
        data = json.loads(result)
        assert data["agents"]["current"] == 25
        assert data["tokens"]["used"] == 15000
        assert data["confidence"] == 99.2
    
    def test_parse_metrics_dict(self):
        metrics = {
            'agents': 25, 'total_agents': 145, 'instance_count': 5,
            'tokens_used': 15000, 'tokens_total': 200000,
            'confidence': 99.2, 'status': '🟢 OPTIMAL'
        }
        result = self.formatter.parse_metrics_dict(metrics)
        assert result['current_agents'] == 25
        assert result['total_agents'] == 145
        assert result['instance_count'] == 5

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
