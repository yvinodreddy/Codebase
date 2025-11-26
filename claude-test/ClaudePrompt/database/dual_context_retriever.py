"""Dual retrieval: keyword AND semantic search with comparison."""
from database.context_retriever import ContextRetriever
from database.semantic_retriever import SemanticRetriever
from typing import Dict, List
import concurrent.futures
import time
import logging

logger = logging.getLogger(__name__)

class DualContextRetriever:
    """Provides BOTH keyword and semantic search with side-by-side comparison."""

    def __init__(self):
        logger.info("Initializing DualContextRetriever")
        try:
            self.keyword_retriever = ContextRetriever()
            logger.info("Keyword retriever: OK")
        except Exception as e:
            logger.error(f"Keyword retriever failed: {e}")
            self.keyword_retriever = None

        try:
            self.semantic_retriever = SemanticRetriever()
            logger.info("Semantic retriever: OK")
        except Exception as e:
            logger.error(f"Semantic retriever failed: {e}")
            self.semantic_retriever = None

    def retrieve_with_both_methods(self, query: str, k: int = 10) -> Dict:
        """
        Run BOTH keyword and semantic search, return BOTH results for comparison.

        This is the key feature: user sees BOTH methods side-by-side!
        """
        logger.info(f"Dual retrieval for query: {query[:50]}...")

        # Get all messages for semantic search
        messages = self._get_all_messages()

        # Run both methods in parallel
        keyword_results = []
        semantic_results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Submit both tasks
            if self.keyword_retriever:
                keyword_future = executor.submit(
                    self._keyword_search_safe, query, k
                )

            if self.semantic_retriever:
                semantic_future = executor.submit(
                    self._semantic_search_safe, query, messages, k
                )

            # Get results
            if self.keyword_retriever:
                keyword_results = keyword_future.result()

            if self.semantic_retriever:
                semantic_results = semantic_future.result()

        # Compare results
        comparison = self._compare_results(keyword_results, semantic_results)

        return {
            'keyword_results': keyword_results,
            'semantic_results': semantic_results,
            'comparison': comparison,
            'recommendation': self._recommend_method(comparison)
        }

    def _keyword_search_safe(self, query: str, k: int) -> List[Dict]:
        """Safe keyword search with error handling."""
        try:
            if self.keyword_retriever:
                return self.keyword_retriever.retrieve(query, limit=k)
        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
        return []

    def _semantic_search_safe(self, query: str, messages: List[Dict], k: int) -> List[Dict]:
        """Safe semantic search with error handling."""
        try:
            if self.semantic_retriever:
                return self.semantic_retriever.retrieve(query, messages, k)
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
        return []

    def _get_all_messages(self) -> List[Dict]:
        """Get all messages from database."""
        # For now, return empty list
        # TODO: Integrate with actual context database
        return []

    def _compare_results(self, keyword_results, semantic_results):
        """Compare the two result sets."""
        keyword_ids = {r.get('id', i) for i, r in enumerate(keyword_results)}
        semantic_ids = {r['message'].get('id', i) for i, r in enumerate(semantic_results)}

        overlap_ids = keyword_ids & semantic_ids

        return {
            'overlap_percentage': len(overlap_ids) / max(len(keyword_ids), 1) if keyword_ids else 0,
            'overlap_count': len(overlap_ids),
            'keyword_unique_count': len(keyword_ids - overlap_ids),
            'semantic_unique_count': len(semantic_ids - overlap_ids),
            'keyword_time': keyword_results[0].get('retrieval_time', 0) if keyword_results else 0,
            'semantic_time': semantic_results[0].get('retrieval_time', 0) if semantic_results else 0,
            'total_keyword': len(keyword_results),
            'total_semantic': len(semantic_results)
        }

    def _recommend_method(self, comparison):
        """Recommend which method to use based on comparison."""
        overlap_pct = comparison['overlap_percentage']

        if overlap_pct >= 0.9:
            return 'keyword'  # Fast and accurate enough
        elif overlap_pct < 0.5:
            return 'both'  # Different results, use both for comprehensive coverage
        else:
            return 'semantic'  # Better semantic understanding
