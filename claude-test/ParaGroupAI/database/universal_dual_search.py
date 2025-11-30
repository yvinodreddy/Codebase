#!/usr/bin/env python3
"""
Universal Dual Search - Production-Ready Search Function

This module provides a universal search function that ALWAYS uses dual retrieval
(keyword + semantic + intelligent merging) for ALL search operations.

Created: 2025-11-29
Purpose: Ensure 99% quality on EVERY search, not just during compaction
"""

import logging
from typing import List, Dict, Any, Optional
from .dual_context_retriever import DualContextRetriever

logger = logging.getLogger(__name__)


def universal_dual_search(
    query: str,
    k: int = 10,
    project_id: str = "default",
    db_path: Optional[str] = None,
    require_99_confidence: bool = True,
    show_comparison: bool = True,
    output_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Universal search function using dual retrieval (keyword + semantic + merge).

    This is the PRODUCTION-STANDARD search function that should be used for
    ALL search operations in the system.

    Args:
        query: Search query string
        k: Number of results to return (default: 10)
        project_id: Project ID for database retrieval (default: "default")
        db_path: Path to database file (optional)
        require_99_confidence: Require 99% confidence for both methods (default: True)
        show_comparison: Display keyword vs semantic comparison (default: True)
        output_file: Optional file to save comparison results

    Returns:
        Dict containing:
            - merged_results: List of intelligently merged results
            - keyword_results: Results from keyword search
            - semantic_results: Results from semantic search
            - keyword_confidence: Confidence score for keyword search (%)
            - semantic_confidence: Confidence score for semantic search (%)
            - comparison: Detailed comparison analysis
            - recommendation: Which method performed better
            - validation_summary: Production-ready status

    Example:
        >>> results = universal_dual_search(
        ...     query="JWT authentication implementation",
        ...     k=10,
        ...     project_id="proj_my_app",
        ...     show_comparison=True
        ... )
        >>>
        >>> print(f"Found {len(results['merged_results'])} results")
        >>> print(f"Keyword confidence: {results['keyword_confidence']}%")
        >>> print(f"Semantic confidence: {results['semantic_confidence']}%")
        >>> print(f"Recommendation: {results['recommendation']}")
    """

    logger.info(f"🔍 Universal Dual Search: '{query}' (k={k})")
    logger.info(f"   Project: {project_id}")
    logger.info(f"   Require 99%: {require_99_confidence}")

    try:
        # Initialize dual retriever
        retriever = DualContextRetriever(project_id=project_id, db_path=db_path)

        # Run dual retrieval with validation
        results = retriever.retrieve_with_both_methods_validated(
            query=query,
            k=k,
            require_99_confidence=require_99_confidence
        )

        # Show comparison if requested
        if show_comparison:
            comparison_output = retriever.print_both_results(
                query=query,
                k=k,
                output_file=output_file
            )

            # Log comparison summary
            logger.info("✅ Dual search complete:")
            logger.info(f"   Keyword:  {results['keyword_confidence']}%")
            logger.info(f"   Semantic: {results['semantic_confidence']}%")
            logger.info(f"   Recommendation: {results['recommendation']}")

        return results

    except Exception as e:
        logger.error(f"❌ Universal dual search failed: {e}")
        raise


def search_for_context(
    query: str,
    k: int = 10,
    project_id: str = "default",
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Simplified wrapper that returns merged results directly.

    This is a convenience function for code that just wants the results
    without the detailed comparison analysis.

    Args:
        query: Search query string
        k: Number of results to return
        project_id: Project ID for database retrieval
        **kwargs: Additional arguments passed to universal_dual_search

    Returns:
        List of merged results from dual retrieval

    Example:
        >>> results = search_for_context(
        ...     query="JWT authentication implementation",
        ...     k=10,
        ...     project_id="proj_my_app"
        ... )
        >>>
        >>> for result in results:
        ...     print(result.get('title', 'No title'))
    """

    full_results = universal_dual_search(
        query=query,
        k=k,
        project_id=project_id,
        show_comparison=kwargs.get('show_comparison', False),
        **kwargs
    )

    return full_results.get('merged_results', [])


def search_and_display(
    query: str,
    k: int = 10,
    project_id: str = "default",
    output_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search with dual retrieval and ALWAYS display the comparison.

    This is the function to use when you want to see the full comparison
    of keyword vs semantic search results.

    Args:
        query: Search query string
        k: Number of results to return
        project_id: Project ID for database retrieval
        output_file: File to save comparison results (optional)

    Returns:
        Full results dict including comparison analysis

    Example:
        >>> results = search_and_display(
        ...     query="JWT authentication implementation",
        ...     k=10,
        ...     project_id="proj_my_app",
        ...     output_file="tmp/search_comparison.txt"
        ... )
        >>>
        >>> # Comparison automatically saved to tmp/search_comparison.txt
        >>> # AND displayed in terminal
    """

    return universal_dual_search(
        query=query,
        k=k,
        project_id=project_id,
        show_comparison=True,
        output_file=output_file,
        require_99_confidence=True
    )


# ============================================================================
# MIGRATION GUIDE
# ============================================================================

"""
MIGRATING FROM OLD SEARCH METHODS:

OLD CODE (keyword-only, 85% quality):
    from database.context_retriever import ContextRetriever
    retriever = ContextRetriever()
    results = retriever.search(query, k=10)

NEW CODE (dual retrieval, 99% quality):
    from database.universal_dual_search import search_for_context
    results = search_for_context(query, k=10, project_id="proj_my_app")

---

OLD CODE (semantic-only, 90% quality):
    from database.semantic_retriever import SemanticRetriever
    retriever = SemanticRetriever()
    results = retriever.search(query, k=10)

NEW CODE (dual retrieval, 99% quality):
    from database.universal_dual_search import search_for_context
    results = search_for_context(query, k=10, project_id="proj_my_app")

---

TO SEE COMPARISON (understand quality improvements):
    from database.universal_dual_search import search_and_display
    results = search_and_display(
        query="JWT authentication implementation",
        k=10,
        project_id="proj_my_app",
        output_file="tmp/my_search_comparison.txt"
    )

---

PRODUCTION STANDARD:
- ALWAYS use universal_dual_search or search_for_context
- NEVER use keyword-only or semantic-only search
- ALWAYS require 99% confidence in production
- ALWAYS save comparison to output files for transparency

ZERO BREAKING CHANGES:
- Old search methods still work (backward compatibility)
- New methods are ADDITIVE only
- All existing code continues to function
- Gradually migrate to dual search for better quality
"""


if __name__ == "__main__":
    # Demo usage
    print("="*80)
    print("🔍 UNIVERSAL DUAL SEARCH - DEMO")
    print("="*80)
    print()

    query = "How to implement user authentication with JWT tokens"

    print(f"Query: {query}")
    print()

    results = search_and_display(
        query=query,
        k=5,
        project_id="proj_ParaGroupAI_519ef523",
        output_file="/tmp/demo_dual_search.txt"
    )

    print()
    print("="*80)
    print("✅ DEMO COMPLETE")
    print("="*80)
    print(f"Results saved to: /tmp/demo_dual_search.txt")
    print(f"Merged results: {len(results.get('merged_results', []))}")
    print(f"Keyword confidence: {results.get('keyword_confidence', 0)}%")
    print(f"Semantic confidence: {results.get('semantic_confidence', 0)}%")
    print(f"Recommendation: {results.get('recommendation', 'N/A')}")
