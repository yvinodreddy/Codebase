#!/usr/bin/env python3
"""
Unit Tests for Task Complexity Scorer
Tests all 5 scoring factors and category mapping.

Target: 90%+ code coverage
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from task_complexity_scorer import (
    TaskComplexityScorer,
    ComplexityAnalysis,
    get_optimal_agent_count,
    analyze_task_complexity
)


class TestTaskComplexityScorer:
    """Test suite for TaskComplexityScorer class"""

    def setup_method(self):
        """Set up test instance"""
        self.scorer = TaskComplexityScorer()

    # ========================================
    # Test _score_length()
    # ========================================

    def test_score_length_very_short(self):
        """Test length scoring for very short prompts (< 50 chars)"""
        prompt = "What is 2+2?"  # 13 chars
        score = self.scorer._score_length(prompt)
        assert score == 5, "Very short prompts should score 5 points"

    def test_score_length_short(self):
        """Test length scoring for short prompts (50-200 chars)"""
        prompt = "A" * 100  # 100 chars
        score = self.scorer._score_length(prompt)
        assert score == 10, "Short prompts (50-200) should score 10 points"

    def test_score_length_medium(self):
        """Test length scoring for medium prompts (200-500 chars)"""
        prompt = "A" * 300  # 300 chars
        score = self.scorer._score_length(prompt)
        assert score == 15, "Medium prompts (200-500) should score 15 points"

    def test_score_length_long(self):
        """Test length scoring for long prompts (> 500 chars)"""
        prompt = "A" * 600  # 600 chars
        score = self.scorer._score_length(prompt)
        assert score == 20, "Long prompts (>500) should score 20 points"

    # ========================================
    # Test _score_requirements()
    # ========================================

    def test_score_requirements_single(self):
        """Test requirements scoring for single requirement"""
        prompt = "Implement authentication"
        score = self.scorer._score_requirements(prompt)
        assert score == 5, "Single requirement should score 5 points"

    def test_score_requirements_numbered(self):
        """Test requirements scoring with numbered list"""
        prompt = """
        1. Implement authentication
        2. Add database
        3. Create API
        """
        score = self.scorer._score_requirements(prompt)
        assert score >= 10, "Numbered list should score at least 10 points"

    def test_score_requirements_bullets(self):
        """Test requirements scoring with bullet points"""
        prompt = """
        - Implement authentication
        - Add database
        - Create API
        """
        score = self.scorer._score_requirements(prompt)
        assert score >= 10, "Bullet points should score at least 10 points"

    def test_score_requirements_many(self):
        """Test requirements scoring with many requirements"""
        prompt = """
        1. Feature A
        2. Feature B
        3. Feature C
        4. Feature D
        5. Feature E
        6. Feature F
        7. Feature G
        8. Feature H
        """
        score = self.scorer._score_requirements(prompt)
        assert score == 20, "Many requirements should score 20 points"

    # ========================================
    # Test _score_technical_depth()
    # ========================================

    def test_score_technical_depth_none(self):
        """Test technical depth scoring with no keywords"""
        prompt = "What is the answer?"
        score = self.scorer._score_technical_depth(prompt)
        assert score == 5, "No technical keywords should score 5 points"

    def test_score_technical_depth_some(self):
        """Test technical depth scoring with some keywords"""
        prompt = "Perform comprehensive analysis of the system"
        score = self.scorer._score_technical_depth(prompt)
        assert score >= 10, "Some technical keywords should score at least 10 points"

    def test_score_technical_depth_deep(self):
        """Test technical depth scoring with many keywords"""
        prompt = """
        Perform comprehensive in-depth analysis of architecture,
        performance, security, and scalability
        """
        score = self.scorer._score_technical_depth(prompt)
        assert score >= 15, "Many technical keywords should score at least 15 points"

    def test_score_technical_depth_very_deep(self):
        """Test technical depth scoring with extensive keywords"""
        prompt = """
        Comprehensive detailed thorough complete full analysis of
        architecture performance security scalability reliability
        optimization
        """
        score = self.scorer._score_technical_depth(prompt)
        assert score == 20, "Extensive technical keywords should score 20 points"

    # ========================================
    # Test _score_scope()
    # ========================================

    def test_score_scope_narrow(self):
        """Test scope scoring with narrow focus"""
        prompt = "Fix the login bug"
        score = self.scorer._score_scope(prompt)
        assert score == 5, "Narrow scope should score 5 points"

    def test_score_scope_moderate(self):
        """Test scope scoring with moderate breadth"""
        prompt = "Improve authentication and add API documentation"
        score = self.scorer._score_scope(prompt)
        assert score >= 10, "Moderate scope should score at least 10 points"

    def test_score_scope_broad(self):
        """Test scope scoring with broad coverage"""
        prompt = """
        Analyze architecture, improve performance, review security,
        add testing, update documentation
        """
        score = self.scorer._score_scope(prompt)
        assert score >= 15, "Broad scope should score at least 15 points"

    def test_score_scope_very_broad(self):
        """Test scope scoring with very broad coverage"""
        prompt = """
        Review architecture design, optimize performance efficiency,
        audit security authentication, improve testing coverage,
        update documentation, review deployment production, analyze
        database queries, refactor API endpoints, enhance UI interface,
        improve backend services
        """
        score = self.scorer._score_scope(prompt)
        assert score == 20, "Very broad scope should score 20 points"

    # ========================================
    # Test _score_code_analysis()
    # ========================================

    def test_score_code_analysis_none(self):
        """Test code analysis scoring with no indicators"""
        prompt = "What is authentication?"
        score = self.scorer._score_code_analysis(prompt)
        assert score == 5, "No code analysis should score 5 points"

    def test_score_code_analysis_some(self):
        """Test code analysis scoring with some indicators"""
        prompt = "Review the authentication code"
        score = self.scorer._score_code_analysis(prompt)
        assert score >= 10, "Some code analysis should score at least 10 points"

    def test_score_code_analysis_with_paths(self):
        """Test code analysis scoring with file paths"""
        prompt = "Analyze auth/login.py and api/routes.js"
        score = self.scorer._score_code_analysis(prompt)
        assert score >= 10, "File paths should score at least 10 points"

    def test_score_code_analysis_extensive(self):
        """Test code analysis scoring with extensive indicators"""
        prompt = """
        Review codebase, analyze code quality, refactor improve,
        fix bugs optimize
        ```python
        def example():
            pass
        ```
        """
        score = self.scorer._score_code_analysis(prompt)
        assert score >= 10, "Extensive code analysis should score at least 10 points"

    # ========================================
    # Test analyze_complexity()
    # ========================================

    def test_analyze_complexity_simple(self):
        """Test complexity analysis for simple query"""
        prompt = "What is 2+2?"
        analysis = self.scorer.analyze_complexity(prompt)

        assert isinstance(analysis, ComplexityAnalysis)
        assert analysis.score <= 30, "Simple query should score ≤ 30"
        assert analysis.category in ['simple', 'medium'], "Very short queries may score as medium"
        assert analysis.agent_count in [3, 8]
        assert 'factors' in dir(analysis)
        assert 'reasoning' in dir(analysis)

    def test_analyze_complexity_medium(self):
        """Test complexity analysis for medium query"""
        prompt = """
        Explain user authentication with JWT tokens.
        Include code examples and best practices.
        """
        analysis = self.scorer.analyze_complexity(prompt)

        assert 20 < analysis.score <= 40, "Medium query should score 21-40"
        assert analysis.category == 'medium'
        assert analysis.agent_count == 8

    def test_analyze_complexity_complex(self):
        """Test complexity analysis for complex query"""
        prompt = """
        Perform comprehensive code review of authentication system.
        1. Analyze security vulnerabilities
        2. Review architecture design
        3. Recommend improvements
        4. Provide refactored code with tests
        """
        analysis = self.scorer.analyze_complexity(prompt)

        assert analysis.score >= 60, "Complex query with many indicators scores higher"
        assert analysis.category in ['complex', 'very_complex']
        assert analysis.agent_count in [35, 75]

    def test_analyze_complexity_very_complex(self):
        """Test complexity analysis for very complex query"""
        prompt = """
        Conduct full codebase audit covering:
        1. Architecture review and design pattern analysis
        2. Performance profiling and optimization recommendations
        3. Security audit with vulnerability assessment
        4. Test coverage analysis and missing test identification
        5. Documentation completeness review
        6. Code quality metrics (complexity, maintainability, duplication)
        """
        analysis = self.scorer.analyze_complexity(prompt)

        assert 60 < analysis.score <= 80, "Very complex query should score 61-80"
        assert analysis.category == 'very_complex'
        assert analysis.agent_count == 75

    def test_analyze_complexity_massive(self):
        """Test complexity analysis for massive query"""
        prompt = """
        Perform comprehensive analysis of entire codebase:
        1. Architecture review and design pattern analysis with detailed documentation
        2. Performance profiling and optimization recommendations with benchmarks
        3. Security audit with vulnerability assessment and remediation plans
        4. Test coverage analysis and missing test identification with examples
        5. Documentation completeness review and update recommendations
        6. Code quality metrics including complexity, maintainability, duplication
        7. Dependency audit and version updates with migration guides
        8. CI/CD pipeline optimization and deployment strategy recommendations
        9. Scalability and high-availability assessment with implementation roadmap
        10. Generate comprehensive PDF report with executive summary
        """
        analysis = self.scorer.analyze_complexity(prompt)

        assert analysis.score > 80, "Massive query should score > 80"
        assert analysis.category == 'massive'
        assert analysis.agent_count == 150

    # ========================================
    # Test _determine_category()
    # ========================================

    def test_determine_category_boundaries(self):
        """Test category determination at boundary values"""
        factors = {'length': 5, 'requirements': 5, 'technical_depth': 5, 'scope': 5, 'code_analysis': 5}

        # Test each boundary
        test_cases = [
            (20, 'simple', 3),
            (40, 'medium', 8),
            (60, 'complex', 35),
            (80, 'very_complex', 75),
            (100, 'massive', 150)
        ]

        for score, expected_category, expected_agents in test_cases:
            category, agent_count, reasoning = self.scorer._determine_category(score, factors)
            assert category == expected_category
            assert agent_count == expected_agents
            assert isinstance(reasoning, str)
            assert len(reasoning) > 0

    # ========================================
    # Test get_optimal_agent_count()
    # ========================================

    def test_get_optimal_agent_count_simple(self):
        """Test optimal agent count for simple query"""
        prompt = "What is 2+2?"
        agent_count = get_optimal_agent_count(prompt)
        assert agent_count in [3, 8], "Simple query should recommend 3 or 8 agents"

    def test_get_optimal_agent_count_complex(self):
        """Test optimal agent count for complex query"""
        prompt = """
        Comprehensive code review with security audit,
        performance optimization, and architecture analysis
        """
        agent_count = get_optimal_agent_count(prompt)
        assert agent_count >= 8, "Complex query should recommend at least 8 agents"

    # ========================================
    # Test analyze_task_complexity()
    # ========================================

    def test_analyze_task_complexity_returns_dict(self):
        """Test that analyze_task_complexity returns proper dict"""
        prompt = "Simple question"
        result = analyze_task_complexity(prompt)

        assert isinstance(result, dict)
        assert 'score' in result
        assert 'category' in result
        assert 'agent_count' in result
        assert 'factors' in result
        assert 'reasoning' in result

    def test_analyze_task_complexity_factors_dict(self):
        """Test that factors is a proper dict with all keys"""
        prompt = "Test query"
        result = analyze_task_complexity(prompt)

        factors = result['factors']
        assert isinstance(factors, dict)
        assert 'length' in factors
        assert 'requirements' in factors
        assert 'technical_depth' in factors
        assert 'scope' in factors
        assert 'code_analysis' in factors

    # ========================================
    # Edge Cases
    # ========================================

    def test_empty_prompt(self):
        """Test handling of empty prompt"""
        prompt = ""
        analysis = self.scorer.analyze_complexity(prompt)
        assert analysis.score == 25  # All factors at minimum: 5 each
        assert analysis.category == 'medium'

    def test_whitespace_only_prompt(self):
        """Test handling of whitespace-only prompt"""
        prompt = "     \n\n\t\t    "
        analysis = self.scorer.analyze_complexity(prompt)
        assert analysis.score == 25  # All factors at minimum
        assert analysis.category == 'medium'

    def test_special_characters_prompt(self):
        """Test handling of special characters"""
        prompt = "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/"
        analysis = self.scorer.analyze_complexity(prompt)
        assert isinstance(analysis, ComplexityAnalysis)
        assert analysis.score >= 0

    def test_unicode_prompt(self):
        """Test handling of Unicode characters"""
        prompt = "分析系统架构 🚀 Проверить безопасность"
        analysis = self.scorer.analyze_complexity(prompt)
        assert isinstance(analysis, ComplexityAnalysis)
        assert analysis.score >= 0

    def test_very_long_prompt(self):
        """Test handling of very long prompt (10000+ chars)"""
        prompt = "A" * 10000
        analysis = self.scorer.analyze_complexity(prompt)
        assert analysis.score >= 20  # Length should be maxed at 20
        assert isinstance(analysis, ComplexityAnalysis)


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
