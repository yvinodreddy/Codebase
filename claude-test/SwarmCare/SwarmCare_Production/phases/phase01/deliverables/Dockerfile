# SwarmCare Phase 01: RAG Heat System - Production Dockerfile
# Multi-stage build for optimized production deployment
# Story Points: 60 | Generated: 2025-10-28

# ============================================================================
# Stage 1: Builder - Install dependencies and download models
# ============================================================================
FROM python:3.11-slim as builder

WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Download embedding model (cached for faster startup)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# ============================================================================
# Stage 2: Runtime - Minimal production image
# ============================================================================
FROM python:3.11-slim

LABEL maintainer="SwarmCare Team"
LABEL description="RAG Heat System API for medical document retrieval"
LABEL version="1.0.0"

# Create non-root user for security
RUN useradd -m -u 1000 swarmcare && \
    mkdir -p /app /models && \
    chown -R swarmcare:swarmcare /app /models

WORKDIR /app

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /home/swarmcare/.local
COPY --from=builder /root/.cache /home/swarmcare/.cache

# Copy application code
COPY --chown=swarmcare:swarmcare rag_system.py .
COPY --chown=swarmcare:swarmcare api.py .

# Switch to non-root user
USER swarmcare

# Set Python path
ENV PATH=/home/swarmcare/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose API port
EXPOSE 8000

# Run application with uvicorn
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
