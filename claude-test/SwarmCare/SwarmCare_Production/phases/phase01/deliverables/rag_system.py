#!/usr/bin/env python3
"""
SwarmCare Phase 01: Production RAG Heat System
Comprehensive Document Ingestion, NLP, Query Pipeline, Knowledge Graph Integration
Story Points: 60 | Priority: P0
"""

import os
import hashlib
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import re

# For production, these would be real imports
# from sentence_transformers import SentenceTransformer
# from transformers import AutoTokenizer
# import weaviate
# from neo4j import GraphDatabase

@dataclass
class DocumentChunk:
    """Represents a chunk of a document for RAG retrieval"""
    chunk_id: str
    document_id: str
    content: str
    chunk_index: int
    total_chunks: int
    metadata: Dict = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class MedicalDocument:
    """Represents a medical document in the system"""
    document_id: str
    title: str
    content: str
    document_type: str  # clinical_note, research_paper, guideline, etc.
    source: str
    metadata: Dict = field(default_factory=dict)
    ontology_tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class QueryResult:
    """Represents a RAG query result"""
    query: str
    chunks: List[DocumentChunk]
    scores: List[float]
    ontology_context: Dict = field(default_factory=dict)
    total_results: int = 0
    processing_time_ms: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "query": self.query,
            "chunks": [c.to_dict() for c in self.chunks],
            "scores": self.scores,
            "ontology_context": self.ontology_context,
            "total_results": self.total_results,
            "processing_time_ms": self.processing_time_ms
        }


class DocumentChunker:
    """Intelligent document chunking with overlap for RAG"""

    def __init__(self, chunk_size: int = 512, overlap: int = 128):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(self, document: MedicalDocument) -> List[DocumentChunk]:
        """
        Split document into overlapping chunks for RAG retrieval
        Uses sliding window approach with semantic boundaries
        """
        content = document.content
        chunks = []

        # Simple sentence-based chunking (production would use spaCy/nltk)
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]

        current_chunk = []
        current_length = 0
        chunk_index = 0

        for sentence in sentences:
            sentence_length = len(sentence.split())

            if current_length + sentence_length > self.chunk_size and current_chunk:
                # Create chunk
                chunk_content = '. '.join(current_chunk) + '.'
                chunk_id = self._generate_chunk_id(document.document_id, chunk_index)

                chunks.append(DocumentChunk(
                    chunk_id=chunk_id,
                    document_id=document.document_id,
                    content=chunk_content,
                    chunk_index=chunk_index,
                    total_chunks=0,  # Will update later
                    metadata={
                        "document_title": document.title,
                        "document_type": document.document_type,
                        **document.metadata
                    }
                ))

                # Overlap: keep last few sentences
                overlap_sentences = current_chunk[-(self.overlap // 50):]
                current_chunk = overlap_sentences
                current_length = sum(len(s.split()) for s in current_chunk)
                chunk_index += 1

            current_chunk.append(sentence)
            current_length += sentence_length

        # Add final chunk
        if current_chunk:
            chunk_content = '. '.join(current_chunk) + '.'
            chunk_id = self._generate_chunk_id(document.document_id, chunk_index)
            chunks.append(DocumentChunk(
                chunk_id=chunk_id,
                document_id=document.document_id,
                content=chunk_content,
                chunk_index=chunk_index,
                total_chunks=0,
                metadata={
                    "document_title": document.title,
                    "document_type": document.document_type,
                    **document.metadata
                }
            ))

        # Update total chunks
        total = len(chunks)
        for chunk in chunks:
            chunk.total_chunks = total

        return chunks

    def _generate_chunk_id(self, document_id: str, chunk_index: int) -> str:
        """Generate unique chunk ID"""
        return f"{document_id}_chunk_{chunk_index:04d}"


class EmbeddingEngine:
    """Generates embeddings for RAG retrieval"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.dimension = 384  # for all-MiniLM-L6-v2
        # In production: self.model = SentenceTransformer(model_name)
        print(f"✅ Embedding engine initialized: {model_name} (dim={self.dimension})")

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text"""
        # In production: return self.model.encode(text).tolist()
        # For demo, return mock embedding
        import random
        random.seed(hash(text) % (2**32))
        return [random.random() for _ in range(self.dimension)]

    def batch_generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts efficiently"""
        # In production: return self.model.encode(texts).tolist()
        return [self.generate_embedding(text) for text in texts]


class VectorStore:
    """In-memory vector store (production would use Weaviate/Pinecone/Chroma)"""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.chunks: Dict[str, DocumentChunk] = {}
        self.vectors: Dict[str, List[float]] = {}
        print(f"✅ Vector store initialized (dimension={dimension})")

    def add_chunks(self, chunks: List[DocumentChunk], embeddings: List[List[float]]):
        """Add chunks with their embeddings to the vector store"""
        for chunk, embedding in zip(chunks, embeddings):
            self.chunks[chunk.chunk_id] = chunk
            self.vectors[chunk.chunk_id] = embedding
            chunk.embedding = embedding
        print(f"✅ Added {len(chunks)} chunks to vector store")

    def search(self, query_embedding: List[float], top_k: int = 10) -> Tuple[List[DocumentChunk], List[float]]:
        """Search for similar chunks using cosine similarity"""
        if not self.vectors:
            return [], []

        # Calculate cosine similarity
        similarities = []
        for chunk_id, vector in self.vectors.items():
            similarity = self._cosine_similarity(query_embedding, vector)
            similarities.append((chunk_id, similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Get top k
        top_results = similarities[:top_k]
        chunks = [self.chunks[chunk_id] for chunk_id, _ in top_results]
        scores = [score for _, score in top_results]

        return chunks, scores

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    def get_stats(self) -> Dict:
        """Get vector store statistics"""
        return {
            "total_chunks": len(self.chunks),
            "total_vectors": len(self.vectors),
            "dimension": self.dimension,
            "unique_documents": len(set(c.document_id for c in self.chunks.values()))
        }


class KnowledgeGraphConnector:
    """Connects to Neo4j knowledge graph from Phase 00"""

    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password"):
        self.uri = uri
        self.user = user
        self.connected = False
        # In production: self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print(f"✅ Knowledge graph connector initialized ({uri})")

    def get_ontology_context(self, query: str, limit: int = 5) -> Dict:
        """
        Get relevant ontology context from Neo4j knowledge graph
        Connects to the 7,050 medical entities from Phase 00
        """
        # In production, this would query Neo4j
        # Example query:
        # MATCH (s:SNOMED) WHERE s.term CONTAINS $keyword RETURN s LIMIT $limit

        keywords = query.lower().split()
        context = {
            "matched_ontologies": [],
            "related_concepts": [],
            "treatment_pathways": [],
            "diagnostic_tests": []
        }

        # Mock response (production would query real Neo4j)
        if any(k in "diabetes" for k in keywords):
            context["matched_ontologies"] = [
                {"ontology": "SNOMED", "code": "73211009", "term": "Diabetes mellitus"},
                {"ontology": "ICD10", "code": "E11", "description": "Type 2 diabetes mellitus"}
            ]
            context["treatment_pathways"] = [
                {"drug": "Metformin", "class": "Biguanides", "rxcui": "203134"}
            ]

        return context

    def close(self):
        """Close connection to knowledge graph"""
        # In production: self.driver.close()
        pass


class RAGHeatSystem:
    """
    Production RAG Heat System

    Integrates:
    - Document ingestion and chunking
    - Vector embeddings and similarity search
    - Knowledge graph integration (Phase 00)
    - Query pipeline with ranking
    """

    def __init__(self,
                 chunk_size: int = 512,
                 chunk_overlap: int = 128,
                 embedding_model: str = "all-MiniLM-L6-v2",
                 neo4j_uri: str = "bolt://localhost:7687"):

        print("=" * 80)
        print("🚀 Initializing RAG Heat System")
        print("=" * 80)

        self.chunker = DocumentChunker(chunk_size=chunk_size, overlap=chunk_overlap)
        self.embedding_engine = EmbeddingEngine(model_name=embedding_model)
        self.vector_store = VectorStore(dimension=self.embedding_engine.dimension)
        self.kg_connector = KnowledgeGraphConnector(uri=neo4j_uri)

        self.documents: Dict[str, MedicalDocument] = {}
        self.stats = {
            "documents_ingested": 0,
            "chunks_created": 0,
            "queries_processed": 0,
            "system_start_time": datetime.now().isoformat()
        }

        print("=" * 80)
        print("✅ RAG Heat System initialized successfully")
        print("=" * 80)
        print()

    def ingest_document(self, document: MedicalDocument) -> Dict:
        """
        Ingest a medical document into the RAG system

        Steps:
        1. Chunk the document
        2. Generate embeddings
        3. Store in vector database
        4. Tag with ontology terms
        """
        start_time = datetime.now()

        print(f"📄 Ingesting document: {document.title}")

        # Step 1: Chunk document
        chunks = self.chunker.chunk_document(document)
        print(f"   ✅ Created {len(chunks)} chunks")

        # Step 2: Generate embeddings
        chunk_texts = [c.content for c in chunks]
        embeddings = self.embedding_engine.batch_generate_embeddings(chunk_texts)
        print(f"   ✅ Generated {len(embeddings)} embeddings")

        # Step 3: Add to vector store
        self.vector_store.add_chunks(chunks, embeddings)

        # Step 4: Store document
        self.documents[document.document_id] = document

        # Update stats
        self.stats["documents_ingested"] += 1
        self.stats["chunks_created"] += len(chunks)

        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        return {
            "document_id": document.document_id,
            "chunks_created": len(chunks),
            "processing_time_ms": processing_time,
            "status": "success"
        }

    def query(self, query_text: str, top_k: int = 5, include_kg_context: bool = True) -> QueryResult:
        """
        Query the RAG system with semantic search + knowledge graph context

        Steps:
        1. Generate query embedding
        2. Search vector store for similar chunks
        3. Get knowledge graph context (if enabled)
        4. Rank and return results
        """
        start_time = datetime.now()

        print(f"🔍 Processing query: {query_text}")

        # Step 1: Generate query embedding
        query_embedding = self.embedding_engine.generate_embedding(query_text)
        print(f"   ✅ Generated query embedding")

        # Step 2: Vector similarity search
        chunks, scores = self.vector_store.search(query_embedding, top_k=top_k)
        print(f"   ✅ Found {len(chunks)} relevant chunks")

        # Step 3: Knowledge graph context
        kg_context = {}
        if include_kg_context:
            kg_context = self.kg_connector.get_ontology_context(query_text)
            print(f"   ✅ Retrieved knowledge graph context")

        # Step 4: Create result
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        self.stats["queries_processed"] += 1

        result = QueryResult(
            query=query_text,
            chunks=chunks,
            scores=scores,
            ontology_context=kg_context,
            total_results=len(chunks),
            processing_time_ms=processing_time
        )

        print(f"   ✅ Query processed in {processing_time:.2f}ms")
        print()

        return result

    def get_system_stats(self) -> Dict:
        """Get comprehensive system statistics"""
        vector_stats = self.vector_store.get_stats()

        return {
            **self.stats,
            **vector_stats,
            "system_uptime_seconds": (
                datetime.now() - datetime.fromisoformat(self.stats["system_start_time"])
            ).total_seconds()
        }

    def export_state(self, output_path: Path):
        """Export system state for persistence"""
        state = {
            "stats": self.get_system_stats(),
            "documents": {doc_id: doc.to_dict() for doc_id, doc in self.documents.items()},
            "vector_store_size": len(self.vector_store.chunks),
            "exported_at": datetime.now().isoformat()
        }

        with open(output_path, 'w') as f:
            json.dump(state, f, indent=2)

        print(f"✅ System state exported to {output_path}")


def main():
    """Demonstration of RAG Heat System"""

    print("\n" + "=" * 80)
    print("SWARMCARE PHASE 01: RAG HEAT SYSTEM DEMONSTRATION")
    print("=" * 80)
    print()

    # Initialize RAG system
    rag = RAGHeatSystem(
        chunk_size=512,
        chunk_overlap=128,
        embedding_model="all-MiniLM-L6-v2"
    )

    # Create sample medical documents
    documents = [
        MedicalDocument(
            document_id="doc_001",
            title="Type 2 Diabetes Management Guidelines",
            content="""
            Type 2 diabetes mellitus is a chronic metabolic disorder characterized by insulin resistance
            and relative insulin deficiency. First-line treatment typically involves metformin, along with
            lifestyle modifications including diet and exercise. Blood glucose monitoring is essential for
            optimal management. Hemoglobin A1c should be measured every 3-6 months. Complications can include
            diabetic neuropathy, retinopathy, and nephropathy. Regular screening is recommended for all patients.
            """,
            document_type="clinical_guideline",
            source="Medical Guidelines Database",
            metadata={"specialty": "Endocrinology", "year": 2024}
        ),
        MedicalDocument(
            document_id="doc_002",
            title="Hypertension Treatment Protocol",
            content="""
            Essential hypertension affects millions of patients worldwide. Treatment goals include maintaining
            blood pressure below 130/80 mmHg for most patients. First-line agents include ACE inhibitors like
            lisinopril, ARBs, calcium channel blockers, and thiazide diuretics. Combination therapy may be
            necessary for adequate control. Regular monitoring and medication adherence are critical for
            preventing cardiovascular complications such as stroke and myocardial infarction.
            """,
            document_type="clinical_protocol",
            source="Cardiology Department",
            metadata={"specialty": "Cardiology", "year": 2024}
        ),
        MedicalDocument(
            document_id="doc_003",
            title="Pneumonia Diagnosis and Management",
            content="""
            Community-acquired pneumonia requires prompt diagnosis and treatment. Chest X-ray is the standard
            diagnostic modality. Laboratory tests should include complete blood count and inflammatory markers.
            Empiric antibiotic therapy should be initiated promptly, with coverage for Streptococcus pneumoniae
            and atypical organisms. Severity assessment using CURB-65 or PSI score guides disposition decisions.
            Most patients can be managed as outpatients with oral antibiotics.
            """,
            document_type="clinical_guideline",
            source="Infectious Disease Guidelines",
            metadata={"specialty": "Pulmonology", "year": 2024}
        )
    ]

    # Ingest documents
    print("📚 INGESTING MEDICAL DOCUMENTS")
    print("-" * 80)
    for doc in documents:
        result = rag.ingest_document(doc)
        print(f"   Document {result['document_id']}: {result['chunks_created']} chunks in {result['processing_time_ms']:.2f}ms")
    print()

    # Process queries
    print("🔍 PROCESSING QUERIES")
    print("-" * 80)

    queries = [
        "What is the first-line treatment for type 2 diabetes?",
        "How should hypertension be managed?",
        "What diagnostic tests are needed for pneumonia?"
    ]

    for query_text in queries:
        result = rag.query(query_text, top_k=3)
        print(f"Query: {query_text}")
        print(f"Results: {result.total_results} chunks in {result.processing_time_ms:.2f}ms")
        if result.chunks:
            print(f"Top result: {result.chunks[0].metadata.get('document_title', 'N/A')}")
            print(f"Relevance score: {result.scores[0]:.4f}")
        print()

    # Show system statistics
    print("📊 SYSTEM STATISTICS")
    print("-" * 80)
    stats = rag.get_system_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    print()

    # Export state
    output_path = Path("rag_system_state.json")
    rag.export_state(output_path)

    print("=" * 80)
    print("✅ RAG HEAT SYSTEM DEMONSTRATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
