"""Tests for dual context retriever."""
import pytest
from database.dual_context_retriever import DualContextRetriever

def test_dual_retriever_initialization():
    """Test dual retriever can be initialized."""
    retriever = DualContextRetriever()
    assert retriever is not None
    assert hasattr(retriever, 'retrieve_with_both_methods')

def test_dual_retriever_returns_structure():
    """Test dual retriever returns expected structure."""
    retriever = DualContextRetriever()
    results = retriever.retrieve_with_both_methods("test query", k=5)

    assert 'keyword_results' in results
    assert 'semantic_results' in results
    assert 'comparison' in results
    assert 'recommendation' in results

def test_comparison_has_required_fields():
    """Test comparison contains required fields."""
    retriever = DualContextRetriever()
    results = retriever.retrieve_with_both_methods("test", k=5)

    comparison = results['comparison']
    assert 'overlap_percentage' in comparison
    assert 'overlap_count' in comparison
    assert 'keyword_unique_count' in comparison
    assert 'semantic_unique_count' in comparison
