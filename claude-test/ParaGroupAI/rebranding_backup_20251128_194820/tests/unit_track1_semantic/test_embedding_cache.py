"""Tests for embedding cache."""
import pytest
import numpy as np
from database.embedding_cache import EmbeddingCache
import tempfile
import os

@pytest.fixture
def temp_cache():
    """Create temporary cache for testing."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    cache = EmbeddingCache(cache_path=temp_file.name)
    yield cache
    os.unlink(temp_file.name)

def test_cache_store_and_retrieve(temp_cache):
    """Test basic store and retrieve."""
    embedding = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    temp_cache.set("test_msg_1", embedding)

    retrieved = temp_cache.get("test_msg_1")
    assert retrieved is not None
    assert np.allclose(retrieved, embedding)

def test_cache_miss_returns_none(temp_cache):
    """Test cache miss returns None."""
    assert temp_cache.get("nonexistent") is None

def test_cache_stats(temp_cache):
    """Test cache statistics."""
    embedding = np.array([0.1, 0.2, 0.3])
    temp_cache.set("msg1", embedding)
    temp_cache.set("msg2", embedding)
    temp_cache.get("msg1")
    temp_cache.get("msg1")

    stats = temp_cache.stats()
    assert stats['total_embeddings'] == 2
    assert stats['total_accesses'] >= 2

def test_cache_clear(temp_cache):
    """Test cache clear."""
    embedding = np.array([0.1, 0.2, 0.3])
    temp_cache.set("msg1", embedding)
    temp_cache.clear()

    assert temp_cache.get("msg1") is None
