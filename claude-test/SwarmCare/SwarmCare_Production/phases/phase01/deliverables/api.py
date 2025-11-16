#!/usr/bin/env python3
"""
SwarmCare Phase 01: FastAPI REST API for RAG Heat System
Production-ready API with async support, validation, and monitoring
Story Points: 60 | Priority: P0
"""

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
import logging
from pathlib import Path

# Import our RAG system
from rag_system import (
    RAGHeatSystem,
    MedicalDocument,
    QueryResult
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SwarmCare RAG Heat System API",
    description="Production RAG system for medical document retrieval and query processing",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG system instance
rag_system: Optional[RAGHeatSystem] = None


# ============================================================================
# Pydantic Models for Request/Response Validation
# ============================================================================

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    timestamp: str


class DocumentIngestRequest(BaseModel):
    document_id: str = Field(..., description="Unique document identifier")
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=10, description="Document content")
    document_type: str = Field(..., description="Type of document")
    source: str = Field(..., description="Document source")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    ontology_tags: List[str] = Field(default_factory=list)

    @validator('document_type')
    def validate_document_type(cls, v):
        allowed_types = [
            'clinical_note', 'clinical_guideline', 'clinical_protocol',
            'research_paper', 'case_study', 'drug_information',
            'diagnostic_guideline', 'treatment_plan', 'patient_education'
        ]
        if v not in allowed_types:
            raise ValueError(f'document_type must be one of: {", ".join(allowed_types)}')
        return v


class DocumentIngestResponse(BaseModel):
    document_id: str
    chunks_created: int
    processing_time_ms: float
    status: str
    message: str


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000, description="Search query")
    top_k: int = Field(default=5, ge=1, le=50, description="Number of results to return")
    include_kg_context: bool = Field(default=True, description="Include knowledge graph context")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Optional filters")


class ChunkResponse(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    chunk_index: int
    total_chunks: int
    metadata: Dict[str, Any]
    score: float


class QueryResponse(BaseModel):
    query: str
    chunks: List[ChunkResponse]
    ontology_context: Dict[str, Any]
    total_results: int
    processing_time_ms: float


class SystemStatsResponse(BaseModel):
    documents_ingested: int
    chunks_created: int
    queries_processed: int
    total_chunks: int
    total_vectors: int
    unique_documents: int
    dimension: int
    system_uptime_seconds: float
    system_start_time: str


class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: str


# ============================================================================
# Dependency Injection
# ============================================================================

async def get_rag_system() -> RAGHeatSystem:
    """Dependency to get RAG system instance"""
    if rag_system is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG system not initialized"
        )
    return rag_system


# ============================================================================
# API Endpoints
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    global rag_system
    logger.info("🚀 Starting SwarmCare RAG Heat System API...")

    try:
        rag_system = RAGHeatSystem(
            chunk_size=512,
            chunk_overlap=128,
            embedding_model="all-MiniLM-L6-v2",
            neo4j_uri="bolt://neo4j:7687"  # Kubernetes service name
        )
        logger.info("✅ RAG system initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG system: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global rag_system
    logger.info("🛑 Shutting down SwarmCare RAG Heat System API...")

    if rag_system:
        rag_system.kg_connector.close()
        logger.info("✅ Cleaned up RAG system")


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check(rag: RAGHeatSystem = Depends(get_rag_system)):
    """Health check endpoint"""
    stats = rag.get_system_stats()

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        uptime_seconds=stats.get("system_uptime_seconds", 0),
        timestamp=datetime.now().isoformat()
    )


@app.get("/ready", tags=["System"])
async def readiness_check(rag: RAGHeatSystem = Depends(get_rag_system)):
    """Readiness check for Kubernetes"""
    return {"status": "ready", "timestamp": datetime.now().isoformat()}


@app.post(
    "/api/v1/documents/ingest",
    response_model=DocumentIngestResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Documents"]
)
async def ingest_document(
    request: DocumentIngestRequest,
    rag: RAGHeatSystem = Depends(get_rag_system)
):
    """
    Ingest a medical document into the RAG system

    This endpoint:
    - Chunks the document intelligently
    - Generates embeddings
    - Stores in vector database
    - Tags with ontology terms from knowledge graph
    """
    try:
        # Create medical document
        document = MedicalDocument(
            document_id=request.document_id,
            title=request.title,
            content=request.content,
            document_type=request.document_type,
            source=request.source,
            metadata=request.metadata,
            ontology_tags=request.ontology_tags
        )

        # Ingest document
        result = rag.ingest_document(document)

        return DocumentIngestResponse(
            document_id=result["document_id"],
            chunks_created=result["chunks_created"],
            processing_time_ms=result["processing_time_ms"],
            status="success",
            message=f"Document ingested successfully with {result['chunks_created']} chunks"
        )

    except Exception as e:
        logger.error(f"❌ Error ingesting document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest document: {str(e)}"
        )


@app.post(
    "/api/v1/query",
    response_model=QueryResponse,
    tags=["Query"]
)
async def query_rag_system(
    request: QueryRequest,
    rag: RAGHeatSystem = Depends(get_rag_system)
):
    """
    Query the RAG system with semantic search

    This endpoint:
    - Generates query embedding
    - Performs vector similarity search
    - Retrieves knowledge graph context
    - Returns ranked results with relevance scores
    """
    try:
        # Execute query
        result = rag.query(
            query_text=request.query,
            top_k=request.top_k,
            include_kg_context=request.include_kg_context
        )

        # Format response
        chunks = [
            ChunkResponse(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                content=chunk.content,
                chunk_index=chunk.chunk_index,
                total_chunks=chunk.total_chunks,
                metadata=chunk.metadata,
                score=score
            )
            for chunk, score in zip(result.chunks, result.scores)
        ]

        return QueryResponse(
            query=result.query,
            chunks=chunks,
            ontology_context=result.ontology_context,
            total_results=result.total_results,
            processing_time_ms=result.processing_time_ms
        )

    except Exception as e:
        logger.error(f"❌ Error processing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(e)}"
        )


@app.get(
    "/api/v1/documents/{document_id}",
    tags=["Documents"]
)
async def get_document(
    document_id: str,
    rag: RAGHeatSystem = Depends(get_rag_system)
):
    """Get document by ID"""
    if document_id not in rag.documents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found"
        )

    document = rag.documents[document_id]
    return document.to_dict()


@app.get(
    "/api/v1/documents",
    tags=["Documents"]
)
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    rag: RAGHeatSystem = Depends(get_rag_system)
):
    """List all documents with pagination"""
    documents = list(rag.documents.values())
    total = len(documents)

    return {
        "documents": [doc.to_dict() for doc in documents[skip:skip+limit]],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@app.get(
    "/api/v1/stats",
    response_model=SystemStatsResponse,
    tags=["System"]
)
async def get_system_stats(rag: RAGHeatSystem = Depends(get_rag_system)):
    """Get comprehensive system statistics"""
    stats = rag.get_system_stats()

    return SystemStatsResponse(**stats)


@app.delete(
    "/api/v1/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Documents"]
)
async def delete_document(
    document_id: str,
    rag: RAGHeatSystem = Depends(get_rag_system)
):
    """Delete a document from the system"""
    if document_id not in rag.documents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found"
        )

    # Remove document and its chunks
    del rag.documents[document_id]

    # Remove chunks from vector store
    chunk_ids_to_remove = [
        chunk_id for chunk_id, chunk in rag.vector_store.chunks.items()
        if chunk.document_id == document_id
    ]

    for chunk_id in chunk_ids_to_remove:
        del rag.vector_store.chunks[chunk_id]
        del rag.vector_store.vectors[chunk_id]

    logger.info(f"✅ Deleted document {document_id} and {len(chunk_ids_to_remove)} chunks")

    return None


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            message=str(exc),
            timestamp=datetime.now().isoformat()
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            message=str(exc),
            timestamp=datetime.now().isoformat()
        ).dict()
    )


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
