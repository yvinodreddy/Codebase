#!/usr/bin/env python3
"""
SwarmCare Phase 01: Comprehensive Test Suite for RAG Heat System
100% coverage target with unit, integration, and performance tests
Story Points: 60 | Generated: 2025-10-28
"""

import pytest
import asyncio
from datetime import datetime
from typing import List
import time

from rag_system import (
    RAGHeatSystem,
    MedicalDocument,
    DocumentChunk,
    DocumentChunker,
    EmbeddingEngine,
    VectorStore,
    KnowledgeGraphConnector,
    QueryResult
)


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_document():
    """Create a sample medical document for testing"""
    return MedicalDocument(
        document_id="test_doc_001",
        title="Test Medical Document",
        content="""
        This is a test medical document about diabetes mellitus.
        Type 2 diabetes is a chronic condition. Treatment includes metformin.
        Regular blood glucose monitoring is essential. Complications can include
        neuropathy and retinopathy. Lifestyle modifications are recommended.
        """,
        document_type="clinical_guideline",
        source="Test Suite",
        metadata={"test": True, "specialty": "Endocrinology"}
    )


@pytest.fixture
def chunker():
    """Create a document chunker instance"""
    return DocumentChunker(chunk_size=50, overlap=10)


@pytest.fixture
def embedding_engine():
    """Create an embedding engine instance"""
    return EmbeddingEngine(model_name="all-MiniLM-L6-v2")


@pytest.fixture
def vector_store():
    """Create a vector store instance"""
    return VectorStore(dimension=384)


@pytest.fixture
def rag_system():
    """Create a RAG system instance"""
    return RAGHeatSystem(
        chunk_size=50,
        chunk_overlap=10,
        embedding_model="all-MiniLM-L6-v2"
    )


# ============================================================================
# Unit Tests - Document Chunking
# ============================================================================

class TestDocumentChunker:
    """Test suite for document chunking functionality"""

    def test_chunker_initialization(self, chunker):
        """Test chunker initializes with correct parameters"""
        assert chunker.chunk_size == 50
        assert chunker.overlap == 10

    def test_chunk_document_creates_chunks(self, chunker, sample_document):
        """Test that document chunking creates chunks"""
        chunks = chunker.chunk_document(sample_document)
        assert len(chunks) > 0
        assert all(isinstance(c, DocumentChunk) for c in chunks)

    def test_chunk_metadata_preservation(self, chunker, sample_document):
        """Test that chunk metadata includes document metadata"""
        chunks = chunker.chunk_document(sample_document)
        for chunk in chunks:
            assert chunk.document_id == sample_document.document_id
            assert chunk.metadata["document_title"] == sample_document.title
            assert chunk.metadata["test"] is True

    def test_chunk_indexing(self, chunker, sample_document):
        """Test that chunks are properly indexed"""
        chunks = chunker.chunk_document(sample_document)
        for i, chunk in enumerate(chunks):
            assert chunk.chunk_index == i
            assert chunk.total_chunks == len(chunks)

    def test_chunk_id_generation(self, chunker, sample_document):
        """Test unique chunk ID generation"""
        chunks = chunker.chunk_document(sample_document)
        chunk_ids = [c.chunk_id for c in chunks]
        assert len(chunk_ids) == len(set(chunk_ids))  # All unique


# ============================================================================
# Unit Tests - Embedding Engine
# ============================================================================

class TestEmbeddingEngine:
    """Test suite for embedding generation"""

    def test_embedding_engine_initialization(self, embedding_engine):
        """Test embedding engine initializes correctly"""
        assert embedding_engine.model_name == "all-MiniLM-L6-v2"
        assert embedding_engine.dimension == 384

    def test_generate_single_embedding(self, embedding_engine):
        """Test single embedding generation"""
        text = "This is a test sentence"
        embedding = embedding_engine.generate_embedding(text)
        assert len(embedding) == 384
        assert all(isinstance(x, float) for x in embedding)

    def test_embeddings_are_deterministic(self, embedding_engine):
        """Test that same text produces same embedding"""
        text = "Consistent text"
        emb1 = embedding_engine.generate_embedding(text)
        emb2 = embedding_engine.generate_embedding(text)
        assert emb1 == emb2

    def test_batch_embedding_generation(self, embedding_engine):
        """Test batch embedding generation"""
        texts = ["Text one", "Text two", "Text three"]
        embeddings = embedding_engine.batch_generate_embeddings(texts)
        assert len(embeddings) == 3
        assert all(len(emb) == 384 for emb in embeddings)


# ============================================================================
# Unit Tests - Vector Store
# ============================================================================

class TestVectorStore:
    """Test suite for vector store operations"""

    def test_vector_store_initialization(self, vector_store):
        """Test vector store initializes empty"""
        assert vector_store.dimension == 384
        assert len(vector_store.chunks) == 0
        assert len(vector_store.vectors) == 0

    def test_add_chunks_to_store(self, vector_store, chunker, sample_document, embedding_engine):
        """Test adding chunks with embeddings to vector store"""
        chunks = chunker.chunk_document(sample_document)
        embeddings = embedding_engine.batch_generate_embeddings([c.content for c in chunks])

        vector_store.add_chunks(chunks, embeddings)

        assert len(vector_store.chunks) == len(chunks)
        assert len(vector_store.vectors) == len(chunks)

    def test_vector_search_returns_results(self, vector_store, chunker, sample_document, embedding_engine):
        """Test vector similarity search"""
        chunks = chunker.chunk_document(sample_document)
        embeddings = embedding_engine.batch_generate_embeddings([c.content for c in chunks])
        vector_store.add_chunks(chunks, embeddings)

        query_embedding = embedding_engine.generate_embedding("diabetes treatment")
        results, scores = vector_store.search(query_embedding, top_k=5)

        assert len(results) <= 5
        assert len(results) == len(scores)
        assert all(0 <= score <= 1 for score in scores)

    def test_cosine_similarity_calculation(self, vector_store):
        """Test cosine similarity calculation"""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        vec3 = [0.0, 1.0, 0.0]

        sim_same = vector_store._cosine_similarity(vec1, vec2)
        sim_orthogonal = vector_store._cosine_similarity(vec1, vec3)

        assert sim_same == pytest.approx(1.0)
        assert sim_orthogonal == pytest.approx(0.0)

    def test_get_stats(self, vector_store, chunker, sample_document, embedding_engine):
        """Test statistics retrieval"""
        chunks = chunker.chunk_document(sample_document)
        embeddings = embedding_engine.batch_generate_embeddings([c.content for c in chunks])
        vector_store.add_chunks(chunks, embeddings)

        stats = vector_store.get_stats()

        assert stats["total_chunks"] == len(chunks)
        assert stats["total_vectors"] == len(chunks)
        assert stats["dimension"] == 384
        assert stats["unique_documents"] == 1


# ============================================================================
# Integration Tests - RAG System
# ============================================================================

class TestRAGSystem:
    """Integration tests for complete RAG system"""

    def test_rag_system_initialization(self, rag_system):
        """Test RAG system initializes all components"""
        assert rag_system.chunker is not None
        assert rag_system.embedding_engine is not None
        assert rag_system.vector_store is not None
        assert rag_system.kg_connector is not None

    def test_document_ingestion_flow(self, rag_system, sample_document):
        """Test complete document ingestion pipeline"""
        result = rag_system.ingest_document(sample_document)

        assert result["status"] == "success"
        assert result["chunks_created"] > 0
        assert result["document_id"] == sample_document.document_id
        assert sample_document.document_id in rag_system.documents

    def test_query_execution_flow(self, rag_system, sample_document):
        """Test complete query execution pipeline"""
        # First ingest a document
        rag_system.ingest_document(sample_document)

        # Then query
        result = rag_system.query("diabetes treatment", top_k=3)

        assert isinstance(result, QueryResult)
        assert result.query == "diabetes treatment"
        assert len(result.chunks) <= 3
        assert len(result.scores) == len(result.chunks)

    def test_multiple_document_ingestion(self, rag_system):
        """Test ingesting multiple documents"""
        documents = [
            MedicalDocument(
                document_id=f"doc_{i}",
                title=f"Document {i}",
                content=f"Content about topic {i}. " * 10,
                document_type="clinical_note",
                source="Test"
            )
            for i in range(5)
        ]

        for doc in documents:
            rag_system.ingest_document(doc)

        stats = rag_system.get_system_stats()
        assert stats["documents_ingested"] == 5

    def test_knowledge_graph_context_retrieval(self, rag_system):
        """Test knowledge graph context is included in query results"""
        doc = MedicalDocument(
            document_id="diabetes_doc",
            title="Diabetes Guide",
            content="Diabetes mellitus treatment with metformin",
            document_type="clinical_guideline",
            source="Test"
        )

        rag_system.ingest_document(doc)
        result = rag_system.query("diabetes", include_kg_context=True)

        assert "ontology_context" in result.to_dict()

    def test_system_stats_accuracy(self, rag_system, sample_document):
        """Test system statistics are accurate"""
        initial_stats = rag_system.get_system_stats()

        rag_system.ingest_document(sample_document)
        rag_system.query("test query")

        final_stats = rag_system.get_system_stats()

        assert final_stats["documents_ingested"] == initial_stats["documents_ingested"] + 1
        assert final_stats["queries_processed"] == initial_stats["queries_processed"] + 1


# ============================================================================
# Performance Tests
# ============================================================================

class TestPerformance:
    """Performance and benchmark tests"""

    def test_ingestion_performance(self, rag_system):
        """Test document ingestion performance"""
        doc = MedicalDocument(
            document_id="perf_test",
            title="Performance Test",
            content="Content. " * 500,  # Large document
            document_type="clinical_note",
            source="Test"
        )

        start = time.time()
        result = rag_system.ingest_document(doc)
        duration = time.time() - start

        # Should complete in reasonable time
        assert duration < 5.0  # 5 seconds max
        assert result["status"] == "success"

    def test_query_performance(self, rag_system, sample_document):
        """Test query execution performance"""
        rag_system.ingest_document(sample_document)

        start = time.time()
        result = rag_system.query("test query")
        duration = time.time() - start

        # Should be fast
        assert duration < 1.0  # 1 second max
        assert result.processing_time_ms < 1000

    def test_batch_ingestion_performance(self, rag_system):
        """Test batch document ingestion"""
        documents = [
            MedicalDocument(
                document_id=f"batch_{i}",
                title=f"Batch Doc {i}",
                content=f"Medical content {i}. " * 50,
                document_type="clinical_note",
                source="Batch Test"
            )
            for i in range(10)
        ]

        start = time.time()
        for doc in documents:
            rag_system.ingest_document(doc)
        duration = time.time() - start

        # Should handle batch efficiently
        assert duration < 10.0  # 10 seconds for 10 docs
        stats = rag_system.get_system_stats()
        assert stats["documents_ingested"] == 10


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_query(self, rag_system, sample_document):
        """Test handling of empty queries"""
        rag_system.ingest_document(sample_document)
        # Should handle gracefully (mock implementation may not validate)
        result = rag_system.query("")
        assert isinstance(result, QueryResult)

    def test_query_before_ingestion(self, rag_system):
        """Test querying empty system"""
        result = rag_system.query("test")
        assert len(result.chunks) == 0

    def test_very_small_chunks(self):
        """Test with very small chunk size"""
        chunker = DocumentChunker(chunk_size=10, overlap=2)
        doc = MedicalDocument(
            document_id="small_chunks",
            title="Test",
            content="A. B. C. D. E. F. G. H. I. J.",
            document_type="clinical_note",
            source="Test"
        )
        chunks = chunker.chunk_document(doc)
        assert len(chunks) > 0


# ============================================================================
# Test Runner
# ============================================================================

def run_tests():
    """Run all tests and generate report"""
    print("=" * 80)
    print("🧪 RUNNING SWARMCARE RAG SYSTEM TEST SUITE")
    print("=" * 80)
    print()

    # Run pytest with coverage
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes",
        "-ra"
    ])

    return exit_code


if __name__ == "__main__":
    exit_code = run_tests()
    exit(exit_code)
