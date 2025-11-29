"""
Result Formatter for Dual Context Retrieval

CRITICAL REQUIREMENT (Effective 2025-11-27):
- BOTH keyword AND semantic results MUST be printed in output
- Side-by-side comparison for easy understanding
- Complete details (content, scores, metadata)
- MANDATORY for all production use

This allows users to:
- See exactly what each method returns
- Understand differences between keyword vs semantic
- Make informed decisions
- Validate both methods are working correctly
"""
from typing import Dict, List
import json


class ResultFormatter:
    """
    Formats dual retrieval results for comparison output.

    CRITICAL: This ensures BOTH results are visible for comparison.
    """

    @staticmethod
    def format_comparison_for_output(result: Dict, query: str) -> str:
        """
        Format BOTH keyword and semantic results for output display.

        Args:
            result: Output from retrieve_with_both_methods_validated()
            query: Original search query

        Returns:
            Formatted string showing BOTH results side-by-side
        """
        lines = []

        # Header
        lines.append("=" * 80)
        lines.append("🔍 DUAL SEARCH RESULTS COMPARISON")
        lines.append("=" * 80)
        lines.append(f"Query: '{query}'")
        lines.append("")

        # Confidence scores (if available)
        if 'keyword_confidence' in result:
            lines.append("📊 CONFIDENCE SCORES:")
            lines.append(f"   Keyword:  {result['keyword_confidence']:.1f}% "
                        f"({result.get('keyword_iterations', 0)} iterations)")
            lines.append(f"   Semantic: {result['semantic_confidence']:.1f}% "
                        f"({result.get('semantic_iterations', 0)} iterations)")
            lines.append("")

        # Keyword Results
        lines.append("=" * 80)
        lines.append("📚 KEYWORD SEARCH RESULTS")
        lines.append("=" * 80)
        lines.extend(ResultFormatter._format_keyword_results(
            result.get('keyword_results', [])
        ))

        # Semantic Results
        lines.append("")
        lines.append("=" * 80)
        lines.append("🧠 SEMANTIC SEARCH RESULTS")
        lines.append("=" * 80)
        lines.extend(ResultFormatter._format_semantic_results(
            result.get('semantic_results', [])
        ))

        # Comparison
        lines.append("")
        lines.append("=" * 80)
        lines.append("📈 COMPARISON ANALYSIS")
        lines.append("=" * 80)
        lines.extend(ResultFormatter._format_comparison(
            result.get('comparison', {})
        ))

        # Recommendation
        lines.append("")
        lines.append("=" * 80)
        lines.append("🎯 RECOMMENDATION")
        lines.append("=" * 80)
        lines.append(f"Recommended method: {result.get('recommendation', 'N/A')}")
        lines.append("")

        # Validation summary (if available)
        if 'validation_summary' in result:
            lines.append("=" * 80)
            lines.append("✅ VALIDATION SUMMARY")
            lines.append("=" * 80)
            summary = result['validation_summary']
            lines.append(f"   Keyword validated:  {'✅ YES' if summary.get('keyword_validated') else '❌ NO'}")
            lines.append(f"   Semantic validated: {'✅ YES' if summary.get('semantic_validated') else '❌ NO'}")
            lines.append(f"   Both validated:     {'✅ YES' if summary.get('both_validated') else '❌ NO'}")
            lines.append(f"   Production-ready:   {'✅ YES' if summary.get('production_ready') else '❌ NO'}")
            lines.append("")

        lines.append("=" * 80)

        return "\n".join(lines)

    @staticmethod
    def _format_keyword_results(results: List[Dict]) -> List[str]:
        """Format keyword search results with full details."""
        lines = []

        if not results:
            lines.append("   No results found")
            return lines

        lines.append(f"Total results: {len(results)}")
        lines.append("")

        for i, result in enumerate(results[:10], 1):  # Show top 10
            lines.append(f"[{i}] {'-' * 74}")

            # Extract content
            content = result.get('content', result.get('text', str(result)))
            if isinstance(content, dict):
                content = json.dumps(content, indent=2)

            # Show first 200 chars
            content_preview = str(content)[:200]
            if len(str(content)) > 200:
                content_preview += "..."

            lines.append(f"    Content: {content_preview}")

            # Show metadata if available
            if 'id' in result:
                lines.append(f"    ID: {result['id']}")
            if 'score' in result:
                lines.append(f"    Score: {result['score']:.3f}")
            if 'timestamp' in result:
                lines.append(f"    Timestamp: {result['timestamp']}")
            if 'retrieval_time' in result:
                lines.append(f"    Retrieval time: {result['retrieval_time']:.3f}s")

            lines.append("")

        if len(results) > 10:
            lines.append(f"... and {len(results) - 10} more results")
            lines.append("")

        return lines

    @staticmethod
    def _format_semantic_results(results: List[Dict]) -> List[str]:
        """Format semantic search results with full details."""
        lines = []

        if not results:
            lines.append("   No results found")
            return lines

        lines.append(f"Total results: {len(results)}")
        lines.append("")

        for i, result in enumerate(results[:10], 1):  # Show top 10
            lines.append(f"[{i}] {'-' * 74}")

            # Semantic results have 'message' and 'similarity'
            message = result.get('message', {})
            similarity = result.get('similarity', 0.0)

            lines.append(f"    Similarity: {similarity:.4f}")

            # Extract content from message
            content = message.get('content', message.get('text', str(message)))
            if isinstance(content, dict):
                content = json.dumps(content, indent=2)

            # Show first 200 chars
            content_preview = str(content)[:200]
            if len(str(content)) > 200:
                content_preview += "..."

            lines.append(f"    Content: {content_preview}")

            # Show metadata if available
            if 'id' in message:
                lines.append(f"    ID: {message['id']}")
            if 'timestamp' in message:
                lines.append(f"    Timestamp: {message['timestamp']}")
            if 'retrieval_time' in result:
                lines.append(f"    Retrieval time: {result['retrieval_time']:.3f}s")

            lines.append("")

        if len(results) > 10:
            lines.append(f"... and {len(results) - 10} more results")
            lines.append("")

        return lines

    @staticmethod
    def _format_comparison(comparison: Dict) -> List[str]:
        """Format comparison metrics."""
        lines = []

        if not comparison:
            lines.append("   No comparison data available")
            return lines

        overlap_pct = comparison.get('overlap_percentage', 0) * 100

        lines.append(f"Overlap: {overlap_pct:.1f}%")
        lines.append(f"   Overlapping results: {comparison.get('overlap_count', 0)}")
        lines.append(f"   Keyword unique: {comparison.get('keyword_unique_count', 0)}")
        lines.append(f"   Semantic unique: {comparison.get('semantic_unique_count', 0)}")
        lines.append("")

        lines.append(f"Total Results:")
        lines.append(f"   Keyword: {comparison.get('total_keyword', 0)}")
        lines.append(f"   Semantic: {comparison.get('total_semantic', 0)}")
        lines.append("")

        if 'keyword_confidence' in comparison:
            lines.append(f"Confidence Scores:")
            lines.append(f"   Keyword: {comparison.get('keyword_confidence', 0):.1f}%")
            lines.append(f"   Semantic: {comparison.get('semantic_confidence', 0):.1f}%")
            lines.append(f"   Both at 99%: {'✅ YES' if comparison.get('both_validated_to_99') else '❌ NO'}")

        return lines

    @staticmethod
    def format_for_logging(result: Dict, query: str) -> str:
        """
        Format results for logging (compact version).

        Includes summary but not full details.
        """
        parts = [
            f"Query: {query}",
            f"Keyword results: {len(result.get('keyword_results', []))}",
            f"Semantic results: {len(result.get('semantic_results', []))}",
        ]

        if 'keyword_confidence' in result:
            parts.append(f"Keyword confidence: {result['keyword_confidence']:.1f}%")
            parts.append(f"Semantic confidence: {result['semantic_confidence']:.1f}%")

        parts.append(f"Recommendation: {result.get('recommendation', 'N/A')}")

        return " | ".join(parts)
