# SwarmCare RAG Heat System - API Documentation

**Version:** 1.0.0
**Base URL:** `http://localhost:8000`
**API Prefix:** `/api/v1`
**Story Points:** 60/60

---

## Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Request/Response Examples](#examples)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [SDKs](#sdks)

---

## Authentication

Currently, the API uses optional API key authentication. For production, configure the `API_KEY` environment variable.

```bash
# Request with API key
curl -H "X-API-Key: your-api-key-here" \
  http://localhost:8000/api/v1/query
```

---

## Endpoints

### System Health

#### GET `/health`

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 3600.5,
  "timestamp": "2025-10-28T07:00:00"
}
```

#### GET `/ready`

Readiness probe for Kubernetes.

**Response:**
```json
{
  "status": "ready",
  "timestamp": "2025-10-28T07:00:00"
}
```

---

### Document Management

#### POST `/api/v1/documents/ingest`

Ingest a medical document into the RAG system.

**Request Body:**
```json
{
  "document_id": "doc_001",
  "title": "Type 2 Diabetes Management Guidelines",
  "content": "Type 2 diabetes mellitus is a chronic metabolic disorder...",
  "document_type": "clinical_guideline",
  "source": "Medical Guidelines Database",
  "metadata": {
    "specialty": "Endocrinology",
    "year": 2024
  },
  "ontology_tags": ["SNOMED:73211009", "ICD10:E11"]
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `document_id` | string | Yes | Unique document identifier |
| `title` | string | Yes | Document title (1-500 chars) |
| `content` | string | Yes | Document content (min 10 chars) |
| `document_type` | string | Yes | One of: clinical_note, clinical_guideline, clinical_protocol, research_paper, etc. |
| `source` | string | Yes | Document source/origin |
| `metadata` | object | No | Additional metadata |
| `ontology_tags` | array | No | Related ontology codes |

**Response (201 Created):**
```json
{
  "document_id": "doc_001",
  "chunks_created": 5,
  "processing_time_ms": 245.3,
  "status": "success",
  "message": "Document ingested successfully with 5 chunks"
}
```

---

#### GET `/api/v1/documents/{document_id}`

Retrieve a specific document by ID.

**Response (200 OK):**
```json
{
  "document_id": "doc_001",
  "title": "Type 2 Diabetes Management Guidelines",
  "content": "Type 2 diabetes mellitus...",
  "document_type": "clinical_guideline",
  "source": "Medical Guidelines Database",
  "metadata": {
    "specialty": "Endocrinology",
    "year": 2024
  },
  "ontology_tags": ["SNOMED:73211009"],
  "created_at": "2025-10-28T07:00:00"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Document doc_999 not found",
  "message": "HTTPException(...)",
  "timestamp": "2025-10-28T07:00:00"
}
```

---

#### GET `/api/v1/documents`

List all documents with pagination.

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip` | integer | 0 | Number of documents to skip |
| `limit` | integer | 100 | Maximum number of documents to return |

**Example:**
```bash
GET /api/v1/documents?skip=0&limit=20
```

**Response (200 OK):**
```json
{
  "documents": [
    {
      "document_id": "doc_001",
      "title": "...",
      "document_type": "clinical_guideline",
      ...
    },
    ...
  ],
  "total": 150,
  "skip": 0,
  "limit": 20
}
```

---

#### DELETE `/api/v1/documents/{document_id}`

Delete a document from the system.

**Response (204 No Content):**
```
(Empty response body)
```

---

### Query/Search

#### POST `/api/v1/query`

Query the RAG system with semantic search.

**Request Body:**
```json
{
  "query": "What is the first-line treatment for type 2 diabetes?",
  "top_k": 5,
  "include_kg_context": true,
  "filters": {
    "specialty": "Endocrinology"
  }
}
```

**Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query (3-1000 chars) |
| `top_k` | integer | No | 5 | Number of results (1-50) |
| `include_kg_context` | boolean | No | true | Include knowledge graph context |
| `filters` | object | No | null | Optional metadata filters |

**Response (200 OK):**
```json
{
  "query": "What is the first-line treatment for type 2 diabetes?",
  "chunks": [
    {
      "chunk_id": "doc_001_chunk_0001",
      "document_id": "doc_001",
      "content": "Type 2 diabetes mellitus treatment includes metformin as first-line therapy...",
      "chunk_index": 1,
      "total_chunks": 5,
      "metadata": {
        "document_title": "Type 2 Diabetes Management Guidelines",
        "document_type": "clinical_guideline",
        "specialty": "Endocrinology"
      },
      "score": 0.8542
    },
    ...
  ],
  "ontology_context": {
    "matched_ontologies": [
      {
        "ontology": "SNOMED",
        "code": "73211009",
        "term": "Diabetes mellitus"
      },
      {
        "ontology": "ICD10",
        "code": "E11",
        "description": "Type 2 diabetes mellitus"
      }
    ],
    "treatment_pathways": [
      {
        "drug": "Metformin",
        "class": "Biguanides",
        "rxcui": "203134"
      }
    ]
  },
  "total_results": 5,
  "processing_time_ms": 125.4
}
```

---

### System Statistics

#### GET `/api/v1/stats`

Get comprehensive system statistics.

**Response (200 OK):**
```json
{
  "documents_ingested": 150,
  "chunks_created": 750,
  "queries_processed": 1250,
  "total_chunks": 750,
  "total_vectors": 750,
  "unique_documents": 150,
  "dimension": 384,
  "system_uptime_seconds": 86400.5,
  "system_start_time": "2025-10-27T07:00:00"
}
```

---

## Request/Response Examples

### Example 1: Ingest Clinical Guideline

```bash
curl -X POST http://localhost:8000/api/v1/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "guideline_hypertension_001",
    "title": "Essential Hypertension Treatment Protocol",
    "content": "Blood pressure goals for most patients are <130/80 mmHg. First-line agents include ACE inhibitors such as lisinopril, ARBs, calcium channel blockers, and thiazide diuretics. Lifestyle modifications are essential and include diet, exercise, and weight management.",
    "document_type": "clinical_protocol",
    "source": "Cardiology Department",
    "metadata": {
      "specialty": "Cardiology",
      "year": 2024,
      "evidence_level": "A"
    },
    "ontology_tags": ["SNOMED:38341003", "ICD10:I10"]
  }'
```

**Response:**
```json
{
  "document_id": "guideline_hypertension_001",
  "chunks_created": 2,
  "processing_time_ms": 156.8,
  "status": "success",
  "message": "Document ingested successfully with 2 chunks"
}
```

---

### Example 2: Semantic Search Query

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "treatment options for high blood pressure",
    "top_k": 3,
    "include_kg_context": true
  }'
```

**Response:**
```json
{
  "query": "treatment options for high blood pressure",
  "chunks": [
    {
      "chunk_id": "guideline_hypertension_001_chunk_0000",
      "document_id": "guideline_hypertension_001",
      "content": "Blood pressure goals for most patients are <130/80 mmHg. First-line agents include ACE inhibitors such as lisinopril...",
      "chunk_index": 0,
      "total_chunks": 2,
      "metadata": {
        "document_title": "Essential Hypertension Treatment Protocol",
        "specialty": "Cardiology",
        "evidence_level": "A"
      },
      "score": 0.9127
    },
    ...
  ],
  "ontology_context": {
    "matched_ontologies": [
      {
        "ontology": "SNOMED",
        "code": "38341003",
        "term": "Hypertensive disorder"
      }
    ],
    "treatment_pathways": [
      {
        "drug": "Lisinopril",
        "class": "ACE Inhibitors",
        "rxcui": "197361"
      }
    ]
  },
  "total_results": 3,
  "processing_time_ms": 98.3
}
```

---

### Example 3: Batch Document Ingestion

```python
import requests

documents = [
    {
        "document_id": f"batch_doc_{i}",
        "title": f"Clinical Document {i}",
        "content": f"Medical content for document {i}...",
        "document_type": "clinical_note",
        "source": "Batch Import"
    }
    for i in range(100)
]

url = "http://localhost:8000/api/v1/documents/ingest"

for doc in documents:
    response = requests.post(url, json=doc)
    print(f"Ingested {doc['document_id']}: {response.status_code}")
```

---

## Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "error": "Validation error",
  "message": "Field 'document_type' must be one of: clinical_note, clinical_guideline, ...",
  "timestamp": "2025-10-28T07:00:00"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Resource deleted successfully |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service not ready |

---

## Rate Limiting

**Default Limits:**
- 100 requests per minute per IP
- Configurable in Kubernetes Ingress

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1698480000
```

**Rate Limit Exceeded Response (429):**
```json
{
  "error": "Rate limit exceeded",
  "message": "Maximum 100 requests per minute. Retry after 60 seconds.",
  "timestamp": "2025-10-28T07:00:00"
}
```

---

## Python SDK Example

```python
import requests
from typing import List, Dict

class SwarmCareRAGClient:
    """Python client for SwarmCare RAG API"""

    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url
        self.headers = {}
        if api_key:
            self.headers["X-API-Key"] = api_key

    def ingest_document(self, document: Dict) -> Dict:
        """Ingest a document"""
        response = requests.post(
            f"{self.base_url}/api/v1/documents/ingest",
            json=document,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def query(self, query: str, top_k: int = 5) -> Dict:
        """Query the RAG system"""
        response = requests.post(
            f"{self.base_url}/api/v1/query",
            json={"query": query, "top_k": top_k},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_stats(self) -> Dict:
        """Get system statistics"""
        response = requests.get(
            f"{self.base_url}/api/v1/stats",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

# Usage
client = SwarmCareRAGClient()

# Ingest document
result = client.ingest_document({
    "document_id": "test_001",
    "title": "Test Document",
    "content": "Medical content...",
    "document_type": "clinical_note",
    "source": "API Client"
})
print(f"Ingested: {result['chunks_created']} chunks")

# Query
results = client.query("diabetes treatment", top_k=3)
print(f"Found {results['total_results']} results")

# Get stats
stats = client.get_stats()
print(f"System has {stats['documents_ingested']} documents")
```

---

## Interactive API Documentation

The API provides interactive documentation:

- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

These interfaces allow you to:
- Browse all endpoints
- See request/response schemas
- Test API calls directly
- Generate code samples

---

## Webhooks (Future Enhancement)

*Coming soon: Webhook notifications for document ingestion and query events*

---

**API Version:** 1.0.0
**Last Updated:** 2025-10-28
**Status:** Production Ready ✅
