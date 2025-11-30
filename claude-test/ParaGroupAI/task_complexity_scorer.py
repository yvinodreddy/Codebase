#!/usr/bin/env python3
"""
Task Complexity Scorer
Analyzes prompts to determine complexity and optimal agent count.

CRITICAL (2025-11-30): User requirement for dynamic agent scaling.
- Simple query → 2-3 agents
- Medium query → 5-10 agents
- Complex query → 20-50 agents
- Very complex query → 50-100 agents
- Massive query → 100-500 agents
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ComplexityAnalysis:
    """Result of complexity analysis"""
    score: int  # 0-100
    category: str  # simple, medium, complex, very_complex, massive
    agent_count: int  # Recommended agent count
    factors: Dict[str, int]  # Individual factor scores
    reasoning: str  # Why this complexity level


class TaskComplexityScorer:
    """
    Analyze task complexity and determine optimal agent count.

    Factors analyzed:
    1. Query length (longer = more complex)
    2. Number of requirements (more = more complex)
    3. Technical depth (keywords indicating deep analysis)
    4. Scope breadth (how many areas covered)
    5. Code presence (code review vs question)
    """

    # Keywords indicating high complexity
    DEEP_ANALYSIS_KEYWORDS = {
        'comprehensive', 'in-depth', 'detailed', 'thorough', 'complete',
        'full', 'entire', 'all', 'every', 'audit', 'review', 'analyze',
        'assessment', 'evaluation', 'investigation', 'diagnosis'
    }

    TECHNICAL_DEPTH_KEYWORDS = {
        'architecture', 'performance', 'security', 'scalability', 'reliability',
        'optimization', 'refactor', 'design pattern', 'best practices',
        'production', 'enterprise', 'mission-critical', 'high-availability'
    }

    CODE_REVIEW_INDICATORS = {
        'review', 'analyze code', 'codebase', 'refactor', 'improve',
        'fix bugs', 'optimize', 'test coverage', 'code quality'
    }

    def __init__(self):
        pass

    def analyze_complexity(self, prompt: str) -> ComplexityAnalysis:
        """
        Analyze prompt and return complexity score with agent recommendation.

        Args:
            prompt: User query/prompt to analyze

        Returns:
            ComplexityAnalysis with score (0-100), category, agent count, reasoning
        """
        # Initialize factor scores
        factors = {}

        # Factor 1: Query Length (0-20 points)
        factors['length'] = self._score_length(prompt)

        # Factor 2: Requirements Count (0-20 points)
        factors['requirements'] = self._score_requirements(prompt)

        # Factor 3: Technical Depth (0-20 points)
        factors['technical_depth'] = self._score_technical_depth(prompt)

        # Factor 4: Scope Breadth (0-20 points)
        factors['scope'] = self._score_scope(prompt)

        # Factor 5: Code Presence (0-20 points)
        factors['code_analysis'] = self._score_code_analysis(prompt)

        # Calculate total score (0-100)
        total_score = sum(factors.values())

        # Determine category and agent count
        category, agent_count, reasoning = self._determine_category(total_score, factors)

        return ComplexityAnalysis(
            score=total_score,
            category=category,
            agent_count=agent_count,
            factors=factors,
            reasoning=reasoning
        )

    def _score_length(self, prompt: str) -> int:
        """
        Score based on prompt length.

        0-5 points: < 50 chars (very short)
        6-10 points: 50-200 chars (short)
        11-15 points: 200-500 chars (medium)
        16-20 points: > 500 chars (long)
        """
        length = len(prompt)

        if length < 50:
            return 5
        elif length < 200:
            return 10
        elif length < 500:
            return 15
        else:
            return 20

    def _score_requirements(self, prompt: str) -> int:
        """
        Score based on number of requirements/tasks.

        Detect numbered lists, bullet points, "and" conjunctions, etc.
        """
        # Count numbered items (1. 2. 3. or 1) 2) 3))
        numbered = len(re.findall(r'\d+[\.\)]', prompt))

        # Count bullet points (-, *, •)
        bullets = len(re.findall(r'[\-\*•]\s+', prompt))

        # Count "and" conjunctions (indicates multiple requirements)
        ands = len(re.findall(r'\band\b', prompt.lower()))

        # Count commas (can indicate lists)
        commas = len(re.findall(r',', prompt))

        # Total requirement indicators
        total_indicators = numbered + bullets + (ands // 2) + (commas // 3)

        if total_indicators <= 1:
            return 5  # Single requirement
        elif total_indicators <= 3:
            return 10  # Few requirements
        elif total_indicators <= 7:
            return 15  # Multiple requirements
        else:
            return 20  # Many requirements

    def _score_technical_depth(self, prompt: str) -> int:
        """
        Score based on technical depth keywords.

        Deep analysis, architecture, performance, security, etc.
        """
        prompt_lower = prompt.lower()

        # Count deep analysis keywords
        deep_count = sum(1 for keyword in self.DEEP_ANALYSIS_KEYWORDS if keyword in prompt_lower)

        # Count technical depth keywords
        tech_count = sum(1 for keyword in self.TECHNICAL_DEPTH_KEYWORDS if keyword in prompt_lower)

        # Total depth indicators
        total_depth = deep_count + tech_count

        if total_depth == 0:
            return 5  # Surface-level
        elif total_depth <= 2:
            return 10  # Some depth
        elif total_depth <= 5:
            return 15  # Good depth
        else:
            return 20  # Very deep

    def _score_scope(self, prompt: str) -> int:
        """
        Score based on scope breadth.

        How many different areas/topics are covered?
        """
        prompt_lower = prompt.lower()

        # Areas to check
        areas = {
            'architecture': ['architecture', 'design', 'structure', 'component'],
            'performance': ['performance', 'speed', 'optimization', 'efficiency'],
            'security': ['security', 'authentication', 'authorization', 'vulnerability'],
            'testing': ['test', 'testing', 'coverage', 'validation'],
            'documentation': ['document', 'comment', 'readme', 'guide'],
            'deployment': ['deploy', 'production', 'release', 'ci/cd'],
            'database': ['database', 'sql', 'query', 'schema'],
            'api': ['api', 'endpoint', 'rest', 'graphql'],
            'ui': ['ui', 'interface', 'frontend', 'react', 'vue'],
            'backend': ['backend', 'server', 'service', 'microservice']
        }

        # Count how many areas are mentioned
        areas_mentioned = 0
        for area, keywords in areas.items():
            if any(keyword in prompt_lower for keyword in keywords):
                areas_mentioned += 1

        if areas_mentioned <= 1:
            return 5  # Narrow scope
        elif areas_mentioned <= 3:
            return 10  # Moderate scope
        elif areas_mentioned <= 5:
            return 15  # Broad scope
        else:
            return 20  # Very broad scope

    def _score_code_analysis(self, prompt: str) -> int:
        """
        Score based on code analysis requirements.

        Code review, refactoring, bug fixing = higher complexity
        """
        prompt_lower = prompt.lower()

        # Count code review indicators
        review_count = sum(1 for indicator in self.CODE_REVIEW_INDICATORS if indicator in prompt_lower)

        # Check for file paths (indicates codebase analysis)
        has_paths = bool(re.search(r'[\w/]+\.py|[\w/]+\.js|[\w/]+\.tsx', prompt))

        # Check for code blocks (``` or indented code)
        has_code_blocks = bool(re.search(r'```|    \w+', prompt))

        if review_count == 0 and not has_paths and not has_code_blocks:
            return 5  # No code analysis
        elif review_count <= 1 or has_paths or has_code_blocks:
            return 10  # Some code analysis
        elif review_count <= 3:
            return 15  # Significant code analysis
        else:
            return 20  # Extensive code analysis

    def _determine_category(self, score: int, factors: Dict[str, int]) -> Tuple[str, int, str]:
        """
        Map complexity score to category and agent count.

        Returns:
            (category, agent_count, reasoning)
        """
        if score <= 20:
            return (
                'simple',
                3,
                f"Simple query (score: {score}/100). Single straightforward task. "
                f"Factors: length={factors['length']}, requirements={factors['requirements']}, "
                f"technical_depth={factors['technical_depth']}"
            )
        elif score <= 40:
            return (
                'medium',
                8,
                f"Medium complexity (score: {score}/100). Multiple requirements or moderate depth. "
                f"Factors: length={factors['length']}, requirements={factors['requirements']}, "
                f"scope={factors['scope']}"
            )
        elif score <= 60:
            return (
                'complex',
                35,
                f"Complex query (score: {score}/100). Deep analysis with broad scope. "
                f"Factors: technical_depth={factors['technical_depth']}, scope={factors['scope']}, "
                f"code_analysis={factors['code_analysis']}"
            )
        elif score <= 80:
            return (
                'very_complex',
                75,
                f"Very complex query (score: {score}/100). Comprehensive analysis across multiple areas. "
                f"Factors: All factors high - requires significant parallel processing. "
                f"Total indicators suggest deep, broad, multi-faceted task."
            )
        else:
            return (
                'massive',
                150,
                f"Massive query (score: {score}/100). Extensive comprehensive review. "
                f"Factors: Maximum complexity across all dimensions. "
                f"Likely full codebase audit, architecture review, or large-scale refactoring. "
                f"Requires maximum parallelization (150 agents, can scale to 500 if needed)."
            )


def get_optimal_agent_count(prompt: str) -> int:
    """
    Convenience function to get optimal agent count for a prompt.

    Args:
        prompt: User query/prompt

    Returns:
        int: Recommended number of agents (2-500)
    """
    scorer = TaskComplexityScorer()
    analysis = scorer.analyze_complexity(prompt)
    return analysis.agent_count


def analyze_task_complexity(prompt: str) -> Dict:
    """
    Full complexity analysis with detailed breakdown.

    Args:
        prompt: User query/prompt

    Returns:
        dict: Complete analysis including score, category, agent_count, factors, reasoning
    """
    scorer = TaskComplexityScorer()
    analysis = scorer.analyze_complexity(prompt)

    return {
        'score': analysis.score,
        'category': analysis.category,
        'agent_count': analysis.agent_count,
        'factors': analysis.factors,
        'reasoning': analysis.reasoning
    }


# Example usage
if __name__ == "__main__":
    # Test with different query types
    test_queries = [
        "What is 2+2?",  # Simple
        "Explain user authentication with JWT tokens and provide code examples",  # Medium
        "Perform comprehensive code review of authentication system, analyze security vulnerabilities, recommend improvements, and provide refactored code with tests",  # Complex
        "Conduct full codebase audit covering architecture, performance, security, testing, documentation, deployment, and provide detailed report with specific recommendations for each area",  # Very Complex
        """Perform comprehensive analysis of entire codebase:
        1. Architecture review and design pattern analysis
        2. Performance profiling and optimization recommendations
        3. Security audit with vulnerability assessment
        4. Test coverage analysis and missing test identification
        5. Documentation completeness review
        6. Code quality metrics (complexity, maintainability, duplication)
        7. Dependency audit and version updates
        8. CI/CD pipeline optimization
        9. Deployment strategy recommendations
        10. Scalability and high-availability assessment
        Generate PDF report with executive summary, detailed findings, and implementation roadmap."""  # Massive
    ]

    scorer = TaskComplexityScorer()

    for query in test_queries:
        print(f"\nQuery: {query[:80]}...")
        analysis = scorer.analyze_complexity(query)
        print(f"Score: {analysis.score}/100")
        print(f"Category: {analysis.category}")
        print(f"Agent Count: {analysis.agent_count}")
        print(f"Factors: {analysis.factors}")
        print(f"Reasoning: {analysis.reasoning}")
        print("-" * 80)
