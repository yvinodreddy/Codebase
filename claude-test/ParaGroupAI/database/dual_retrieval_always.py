#!/usr/bin/env python3
"""
Dual Retrieval Always - Run on EVERY Search

This module ensures dual retrieval runs on EVERY user query,
independent of context compaction.

Created: 2025-11-29
Purpose: Achieve 99% quality on ALL searches, not just during compaction
"""

import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    # Try relative import first (when used as module)
    from .dual_context_retriever import DualContextRetriever
    DUAL_RETRIEVAL_AVAILABLE = True
except ImportError:
    try:
        # Try absolute import (when run as script)
        from dual_context_retriever import DualContextRetriever
        DUAL_RETRIEVAL_AVAILABLE = True
    except ImportError:
        DUAL_RETRIEVAL_AVAILABLE = False
        logger.warning("DualContextRetriever not available")


def run_dual_retrieval_for_query(
    query: str,
    project_id: str,
    output_file: Optional[str] = None,
    k: int = 10,
    require_99_confidence: bool = True
) -> Tuple[Dict[str, Any], str]:
    """
    Run dual retrieval for a query and save comparison to output file.

    This function runs on EVERY query, independent of compaction.
    It ensures 99% quality on ALL searches, not just when compaction triggers.

    Args:
        query: User's search query
        project_id: Project identifier for database retrieval
        output_file: Path to output file for saving comparison
        k: Number of results to retrieve (default: 10)
        db_path: Optional database path
        require_99_confidence: Require 99% confidence validation

    Returns:
        Tuple of (results_dict, comparison_output_str)
            - results_dict: Full dual retrieval results with merged results
            - comparison_output_str: Formatted comparison for output file

    Example:
        >>> results, comparison = run_dual_retrieval_for_query(
        ...     query="JWT authentication",
        ...     project_id="proj_my_app",
        ...     output_file="/tmp/output.txt",
        ...     k=10
        ... )
        >>> print(f"Got {len(results['merged_results'])} results")
        >>> # Comparison already saved to /tmp/output.txt
    """

    logger.info("🔥 DUAL RETRIEVAL ALWAYS: Running for query")
    logger.info(f"   Query: {query[:100]}...")
    logger.info(f"   Project: {project_id}")
    logger.info(f"   Output: {output_file}")

    if not DUAL_RETRIEVAL_AVAILABLE:
        logger.error("❌ Dual retrieval not available - missing DualContextRetriever")
        return {}, ""

    try:
        # Initialize dual context retriever (db_path handled internally)
        retriever = DualContextRetriever(project_id=project_id)

        # Run dual retrieval with 99% validation
        logger.info("   Running dual retrieval with 99% validation...")
        results = retriever.retrieve_with_both_methods_validated(
            query=query,
            k=k,
            require_99_confidence=require_99_confidence
        )

        # Generate comparison output from ALREADY RETRIEVED results (no second retrieval!)
        logger.info("   Generating comparison output...")
        from database.result_formatter import ResultFormatter
        comparison_output = ResultFormatter.format_comparison_for_output(results, query)

        # Save comparison to output file if provided
        if output_file:
            try:
                logger.info(f"   Saving comparison to: {output_file}")

                # Ensure output directory exists
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # Append comparison with clear visual markers
                with open(output_file, 'a') as f:
                    f.write("\n\n")
                    f.write("=" * 80 + "\n")
                    f.write("⬇️⬇️⬇️ DUAL RETRIEVAL COMPARISON ⬇️⬇️⬇️\n")
                    f.write("=" * 80 + "\n")
                    f.write(comparison_output)
                    f.write("\n")
                    f.write("=" * 80 + "\n")
                    f.write("\n")

                logger.info("   ✅ Comparison saved to output file")

            except Exception as e:
                logger.error(f"   ❌ Failed to save comparison: {e}")

        # Log summary
        logger.info("✅ Dual retrieval complete:")
        logger.info(f"   Keyword confidence:  {results.get('keyword_confidence', 0)}%")
        logger.info(f"   Semantic confidence: {results.get('semantic_confidence', 0)}%")
        logger.info(f"   Merged results: {len(results.get('merged_results', []))}")
        logger.info(f"   Recommendation: {results.get('recommendation', 'N/A')}")

        return results, comparison_output

    except Exception as e:
        logger.error(f"❌ Dual retrieval failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {}, ""


def save_comparison_to_file(
    comparison_output: str,
    output_file: str,
    timestamp: Optional[str] = None
) -> bool:
    """
    Save dual retrieval comparison to output file with visual markers.

    Args:
        comparison_output: Formatted comparison text
        output_file: Path to output file
        timestamp: Optional timestamp string

    Returns:
        True if saved successfully, False otherwise
    """

    try:
        # Ensure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate timestamp if not provided
        if not timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append comparison with clear visual markers
        with open(output_file, 'a') as f:
            f.write("\n\n")
            f.write("=" * 80 + "\n")
            f.write("⬇️⬇️⬇️ DUAL RETRIEVAL COMPARISON ⬇️⬇️⬇️\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write("=" * 80 + "\n")
            f.write(comparison_output)
            f.write("\n")
            f.write("=" * 80 + "\n")
            f.write("\n")

        logger.info(f"✅ Comparison saved to: {output_file}")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to save comparison: {e}")
        return False


def get_dual_retrieval_summary(results: Dict[str, Any]) -> str:
    """
    Get a concise summary of dual retrieval results.

    Args:
        results: Dual retrieval results dict

    Returns:
        Formatted summary string
    """

    if not results:
        return "Dual retrieval not available"

    merged_count = len(results.get('merged_results', []))
    keyword_conf = results.get('keyword_confidence', 0)
    semantic_conf = results.get('semantic_confidence', 0)
    recommendation = results.get('recommendation', 'N/A')

    summary = f"""
Dual Retrieval Summary:
  - Merged results: {merged_count}
  - Keyword confidence: {keyword_conf}%
  - Semantic confidence: {semantic_conf}%
  - Recommendation: {recommendation}
  - Status: {'✅ Production-ready' if keyword_conf >= 99 and semantic_conf >= 99 else '⚠️ Needs validation'}
"""

    return summary.strip()


if __name__ == "__main__":
    # Demo usage
    print("=" * 80)
    print("🔥 DUAL RETRIEVAL ALWAYS - DEMO")
    print("=" * 80)
    print()

    test_query = "How to implement JWT authentication with refresh tokens"
    test_output_file = "/tmp/dual_retrieval_always_demo.txt"

    print(f"Query: {test_query}")
    print(f"Output file: {test_output_file}")
    print()

    results, comparison = run_dual_retrieval_for_query(
        query=test_query,
        project_id="proj_ParaGroupAI_519ef523",
        output_file=test_output_file,
        k=5
    )

    print()
    print("=" * 80)
    print("✅ DEMO COMPLETE")
    print("=" * 80)
    print()
    print(get_dual_retrieval_summary(results))
    print()
    print(f"Full comparison saved to: {test_output_file}")
    print()
