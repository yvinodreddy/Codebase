#!/usr/bin/env python3
"""Comprehensive test suite for prompt_preprocessor.py - Target: 90%+ coverage"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from prompt_preprocessor import PromptPreprocessor, PromptAnalysis

class TestPromptAnalysis:
    def test_initialization(self):
        analysis = PromptAnalysis(
            intent_type="question", complexity="simple",
            required_components=["search"], requires_search=True,
            requires_verification=False, requires_code_generation=False,
            requires_parallel_processing=False, estimated_iterations=3,
            confidence=0.85
        )
        assert analysis.intent_type == "question"
        assert analysis.complexity == "simple"
        assert analysis.confidence == 0.85
    
    def test_to_dict(self):
        analysis = PromptAnalysis(
            intent_type="task", complexity="moderate",
            required_components=["verification"], requires_search=False,
            requires_verification=True, requires_code_generation=False,
            requires_parallel_processing=False, estimated_iterations=5,
            confidence=0.9
        )
        result = analysis.to_dict()
        assert result["intent_type"] == "task"
        assert result["complexity"] == "moderate"
        assert result["confidence"] == 0.9

class TestPromptPreprocessor:
    def setup_method(self):
        self.preprocessor = PromptPreprocessor()
    
    def test_initialization(self):
        assert len(self.preprocessor.analysis_log) == 0
    
    def test_classify_intent_question(self):
        result = self.preprocessor._classify_intent("what is python?")
        assert result == "question"
    
    def test_classify_intent_code_generation(self):
        result = self.preprocessor._classify_intent("write a python function")
        assert result == "code_generation"
    
    def test_assess_complexity_simple(self):
        result = self.preprocessor._assess_complexity("what is 2+2")
        assert result == "simple"
    
    def test_assess_complexity_very_complex(self):
        result = self.preprocessor._assess_complexity("comprehensive system " * 20)
        assert result == "very_complex"
    
    def test_analyze_prompt_simple(self):
        analysis = self.preprocessor.analyze_prompt("What is 2+2?")
        assert analysis.intent_type == "question"
        assert analysis.complexity == "simple"
    
    def test_analyze_prompt_complex(self):
        prompt = "Implement a comprehensive medical AI system with guardrails"
        analysis = self.preprocessor.analyze_prompt(prompt)
        assert analysis.complexity in ["complex", "very_complex"]
        assert analysis.requires_verification == True
    
    def test_get_statistics(self):
        self.preprocessor.analyze_prompt("test1")
        self.preprocessor.analyze_prompt("test2")
        stats = self.preprocessor.get_statistics()
        assert stats["total_prompts"] == 2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
