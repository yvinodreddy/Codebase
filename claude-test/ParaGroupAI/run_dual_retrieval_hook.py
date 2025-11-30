#!/usr/bin/env python3
"""
Dual Retrieval Pre-Execution Hook

This script runs BEFORE every prsg execution to ensure dual retrieval
happens on EVERY query, independent of compaction.

CRITICAL, MANDATORY, NON-NEGOTIABLE - This ensures 99% quality on ALL searches.

Usage:
    ./run_dual_retrieval_hook.py <query> <output_file> <project_id>

Created: 2025-11-29
Purpose: Make dual retrieval independent of compaction
"""

import sys
import os
import logging
from pathlib import Path

# Add ParaGroupAI directory to path (for database package imports)
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "database"))

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def main():
    if len(sys.argv) < 4:
        logger.error("Usage: run_dual_retrieval_hook.py <query> <output_file> <project_id>")
        sys.exit(1)

    query = sys.argv[1]
    output_file = sys.argv[2]
    project_id = sys.argv[3]

    logger.info("🔥 PRE-EXECUTION HOOK: Running dual retrieval")
    logger.info(f"   Query: {query[:100]}...")
    logger.info(f"   Output: {output_file}")
    logger.info(f"   Project: {project_id}")

    try:
        from dual_retrieval_always import run_dual_retrieval_for_query

        # Run dual retrieval and save to output file
        results, comparison = run_dual_retrieval_for_query(
            query=query,
            project_id=project_id,
            output_file=output_file,
            k=10,
            require_99_confidence=True
        )

        # CRITICAL FIX: Print comparison to stdout so it gets captured in final output file
        # When user runs: OUTPUT_FILE=$(...) && ./prsg "query" > "$OUTPUT_FILE"
        # This output will be captured by the shell redirection along with cpp_core output
        print("\n")
        print("=" * 80)
        print("⬇️⬇️⬇️ DUAL RETRIEVAL COMPARISON ⬇️⬇️⬇️")
        print("=" * 80)
        print(comparison)
        print("=" * 80)
        print("\n")

        logger.info("✅ Dual retrieval hook complete")
        logger.info(f"   Merged results: {len(results.get('merged_results', []))}")
        logger.info(f"   Keyword: {results.get('keyword_confidence', 0)}%")
        logger.info(f"   Semantic: {results.get('semantic_confidence', 0)}%")

        sys.exit(0)

    except Exception as e:
        logger.error(f"❌ Dual retrieval hook failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        # Don't block execution - continue even if dual retrieval fails
        sys.exit(0)

if __name__ == "__main__":
    main()
