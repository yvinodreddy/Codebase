#!/usr/bin/env python3
"""
Results Display Formatter
Formats and displays dual retrieval comparison results.

CRITICAL (2025-11-30): User requirement for displaying ALL results.
Must show:
1. Keyword search results (complete list)
2. Semantic search results (complete list)
3. Overlap results (items found by both methods)
4. Intelligent merge results (non-overlapping items based on quality)
"""

from typing import List, Dict, Optional, Any
from datetime import datetime


class ResultsDisplayFormatter:
    """
    Format dual retrieval results for answer section display.

    Shows keyword, semantic, overlap, and intelligent merge results
    with complete transparency.
    """

    def __init__(self):
        pass

    def format_all_results(
        self,
        query: str,
        keyword_results: List[Dict],
        semantic_results: List[Dict],
        overlap_results: List[Dict],
        merged_results: List[Dict],
        keyword_confidence: float,
        semantic_confidence: float,
        recommendation: str
    ) -> str:
        """
        Format all result types for display in answer section.

        Args:
            query: Original search query
            keyword_results: Results from keyword search
            semantic_results: Results from semantic search
            overlap_results: Items found by both methods
            merged_results: Intelligently merged final results
            keyword_confidence: Keyword search confidence (0-100)
            semantic_confidence: Semantic search confidence (0-100)
            recommendation: Which method to use ('keyword', 'semantic', 'both')

        Returns:
            str: Formatted display text
        """
        output = []

        # Header
        output.append("=" * 80)
        output.append("🔍 DUAL RETRIEVAL RESULTS COMPARISON")
        output.append("=" * 80)
        output.append(f"Query: '{query}'")
        output.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("")

        # Confidence scores
        output.append("📊 CONFIDENCE SCORES:")
        output.append(f"   Keyword:  {keyword_confidence:.1f}%")
        output.append(f"   Semantic: {semantic_confidence:.1f}%")
        output.append("")

        # Section 1: Keyword Search Results
        output.append("=" * 80)
        output.append("📚 KEYWORD SEARCH RESULTS")
        output.append("=" * 80)
        output.append(f"Total results: {len(keyword_results)}")
        output.append("")

        if keyword_results:
            for i, result in enumerate(keyword_results, 1):
                output.append(f"[{i}] " + "-" * 74)
                output.append(f"    ID: {result.get('id', 'N/A')}")
                output.append(f"    Score: {result.get('score', result.get('relevance_score', 0.0)):.3f}")

                # Title
                title = result.get('title', result.get('metadata', {}).get('title', 'No title'))
                output.append(f"    Title: {title}")

                # Content preview (first 150 chars)
                content = result.get('content', result.get('text', 'No content'))
                content_preview = content[:150] + "..." if len(content) > 150 else content
                output.append(f"    Content: {content_preview}")

                # Timestamp
                timestamp = result.get('timestamp', result.get('metadata', {}).get('timestamp', 'N/A'))
                output.append(f"    Timestamp: {timestamp}")

                output.append("")
        else:
            output.append("    (No keyword results found)")
            output.append("")

        # Section 2: Semantic Search Results
        output.append("=" * 80)
        output.append("🧠 SEMANTIC SEARCH RESULTS")
        output.append("=" * 80)
        output.append(f"Total results: {len(semantic_results)}")
        output.append("")

        if semantic_results:
            for i, result in enumerate(semantic_results, 1):
                output.append(f"[{i}] " + "-" * 74)
                output.append(f"    ID: {result.get('id', 'N/A')}")
                output.append(f"    Similarity: {result.get('similarity', result.get('score', 0.0)):.4f}")

                # Title
                title = result.get('title', result.get('metadata', {}).get('title', 'No title'))
                output.append(f"    Title: {title}")

                # Content preview (first 150 chars)
                content = result.get('content', result.get('text', 'No content'))
                content_preview = content[:150] + "..." if len(content) > 150 else content
                output.append(f"    Content: {content_preview}")

                # Timestamp
                timestamp = result.get('timestamp', result.get('metadata', {}).get('timestamp', 'N/A'))
                output.append(f"    Timestamp: {timestamp}")

                output.append("")
        else:
            output.append("    (No semantic results found)")
            output.append("")

        # Section 3: Overlap Analysis
        output.append("=" * 80)
        output.append("📈 OVERLAP ANALYSIS")
        output.append("=" * 80)

        # Calculate overlap percentage
        total_keyword = len(keyword_results)
        total_semantic = len(semantic_results)
        total_overlap = len(overlap_results)

        if total_keyword > 0 and total_semantic > 0:
            overlap_pct = (total_overlap / min(total_keyword, total_semantic)) * 100
        else:
            overlap_pct = 0.0

        output.append(f"Overlap: {overlap_pct:.1f}%")
        output.append(f"   Overlapping results: {total_overlap}")
        output.append(f"   Keyword unique: {total_keyword - total_overlap}")
        output.append(f"   Semantic unique: {total_semantic - total_overlap}")
        output.append("")

        if overlap_results:
            output.append("Items found by BOTH methods (high confidence):")
            output.append("")
            for i, result in enumerate(overlap_results, 1):
                title = result.get('title', result.get('metadata', {}).get('title', 'No title'))
                output.append(f"   {i}. {title}")
            output.append("")
        else:
            output.append("   (No overlapping results)")
            output.append("")

        # Section 4: Intelligent Merge Results
        output.append("=" * 80)
        output.append("🎯 INTELLIGENT MERGE RESULTS")
        output.append("=" * 80)
        output.append(f"Total merged results: {len(merged_results)}")
        output.append("")
        output.append("Merging Strategy:")
        output.append("   1. Include ALL overlapping results (found by both methods)")
        output.append("   2. Include high-quality unique results from keyword search")
        output.append("   3. Include high-quality unique results from semantic search")
        output.append("   4. Quality threshold: 50%+ (filters low-quality results)")
        output.append("")

        if merged_results:
            # Group by merge source
            overlap_items = [r for r in merged_results if r.get('merge_source') == 'overlap']
            keyword_unique_items = [r for r in merged_results if r.get('merge_source') == 'keyword_unique']
            semantic_unique_items = [r for r in merged_results if r.get('merge_source') == 'semantic_unique']

            output.append("Composition:")
            output.append(f"   - Overlap (both methods): {len(overlap_items)} results")
            output.append(f"   - Keyword unique (quality >= 50%): {len(keyword_unique_items)} results")
            output.append(f"   - Semantic unique (quality >= 50%): {len(semantic_unique_items)} results")
            output.append("")

            output.append("Merged Results (sorted by quality):")
            output.append("")

            for i, result in enumerate(merged_results, 1):
                output.append(f"[{i}] " + "-" * 74)
                output.append(f"    ID: {result.get('id', 'N/A')}")

                # Quality score
                quality_score = result.get('quality_score', 0.0)
                output.append(f"    Quality Score: {quality_score:.1%}")

                # Merge source
                merge_source = result.get('merge_source', 'unknown')
                merge_reason = result.get('merge_reason', 'N/A')
                output.append(f"    Source: {merge_source}")
                output.append(f"    Reason: {merge_reason}")

                # Title
                title = result.get('title', result.get('metadata', {}).get('title', 'No title'))
                output.append(f"    Title: {title}")

                # Content preview (first 150 chars)
                content = result.get('content', result.get('text', 'No content'))
                content_preview = content[:150] + "..." if len(content) > 150 else content
                output.append(f"    Content: {content_preview}")

                output.append("")
        else:
            output.append("    (No merged results)")
            output.append("")

        # Section 5: Recommendation
        output.append("=" * 80)
        output.append("✅ RECOMMENDATION")
        output.append("=" * 80)

        recommendation_text = {
            'keyword': "Use keyword search results (better BM25 scores)",
            'semantic': "Use semantic search results (better conceptual understanding)",
            'both': "Use merged results (best of both methods)",
            'error_both_failed': "⚠️ Both methods below confidence threshold"
        }.get(recommendation, f"Unknown recommendation: {recommendation}")

        output.append(f"Recommended approach: {recommendation_text}")
        output.append("")

        # Footer
        output.append("=" * 80)

        return "\n".join(output)

    def format_to_file(
        self,
        output_file: str,
        query: str,
        keyword_results: List[Dict],
        semantic_results: List[Dict],
        overlap_results: List[Dict],
        merged_results: List[Dict],
        keyword_confidence: float,
        semantic_confidence: float,
        recommendation: str
    ) -> None:
        """
        Format results and save to file.

        Args:
            output_file: Path to output file
            query: Original search query
            keyword_results: Results from keyword search
            semantic_results: Results from semantic search
            overlap_results: Items found by both methods
            merged_results: Intelligently merged final results
            keyword_confidence: Keyword search confidence (0-100)
            semantic_confidence: Semantic search confidence (0-100)
            recommendation: Which method to use
        """
        formatted = self.format_all_results(
            query=query,
            keyword_results=keyword_results,
            semantic_results=semantic_results,
            overlap_results=overlap_results,
            merged_results=merged_results,
            keyword_confidence=keyword_confidence,
            semantic_confidence=semantic_confidence,
            recommendation=recommendation
        )

        with open(output_file, 'w') as f:
            f.write(formatted)


# Example usage
if __name__ == "__main__":  # pragma: no cover
    # Test with sample data
    formatter = ResultsDisplayFormatter()

    # Sample results
    keyword_results = [
        {
            'id': 'msg_001',
            'score': 0.95,
            'title': 'JWT Authentication Implementation',
            'content': 'Complete guide to implementing JWT authentication with refresh tokens...',
            'timestamp': '2025-11-30T10:00:00Z'
        },
        {
            'id': 'msg_002',
            'score': 0.88,
            'title': 'OAuth 2.0 Setup',
            'content': 'Step-by-step OAuth 2.0 configuration for secure authentication...',
            'timestamp': '2025-11-30T09:30:00Z'
        }
    ]

    semantic_results = [
        {
            'id': 'msg_001',
            'similarity': 0.9234,
            'title': 'JWT Authentication Implementation',
            'content': 'Complete guide to implementing JWT authentication with refresh tokens...',
            'timestamp': '2025-11-30T10:00:00Z'
        },
        {
            'id': 'msg_003',
            'similarity': 0.8567,
            'title': 'Multi-Factor Authentication',
            'content': 'Building secure MFA systems with SMS and authenticator apps...',
            'timestamp': '2025-11-30T08:15:00Z'
        }
    ]

    overlap_results = [
        {
            'id': 'msg_001',
            'title': 'JWT Authentication Implementation',
            'content': 'Complete guide to implementing JWT authentication with refresh tokens...'
        }
    ]

    merged_results = [
        {
            'id': 'msg_001',
            'quality_score': 0.95,
            'merge_source': 'overlap',
            'merge_reason': 'Found by both methods (high confidence)',
            'title': 'JWT Authentication Implementation',
            'content': 'Complete guide to implementing JWT authentication with refresh tokens...'
        },
        {
            'id': 'msg_002',
            'quality_score': 0.78,
            'merge_source': 'keyword_unique',
            'merge_reason': 'High-quality keyword result (quality >= 50%)',
            'title': 'OAuth 2.0 Setup',
            'content': 'Step-by-step OAuth 2.0 configuration for secure authentication...'
        },
        {
            'id': 'msg_003',
            'quality_score': 0.82,
            'merge_source': 'semantic_unique',
            'merge_reason': 'High-quality semantic result (quality >= 50%)',
            'title': 'Multi-Factor Authentication',
            'content': 'Building secure MFA systems with SMS and authenticator apps...'
        }
    ]

    # Generate formatted output
    output = formatter.format_all_results(
        query="authentication implementation",
        keyword_results=keyword_results,
        semantic_results=semantic_results,
        overlap_results=overlap_results,
        merged_results=merged_results,
        keyword_confidence=99.3,
        semantic_confidence=99.1,
        recommendation='both'
    )

    print(output)

    # Save to file
    formatter.format_to_file(
        output_file="/tmp/results_display_example.txt",
        query="authentication implementation",
        keyword_results=keyword_results,
        semantic_results=semantic_results,
        overlap_results=overlap_results,
        merged_results=merged_results,
        keyword_confidence=99.3,
        semantic_confidence=99.1,
        recommendation='both'
    )

    print("\n" + "=" * 80)
    print("✅ Results saved to /tmp/results_display_example.txt")
    print("=" * 80)
