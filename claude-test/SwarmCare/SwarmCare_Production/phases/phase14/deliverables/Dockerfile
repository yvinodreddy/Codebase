# Phase 14: Medical Imaging System
# Production Dockerfile

FROM python:3.11-slim

LABEL maintainer="SwarmCare Team <support@swarmcare.example.com>"
LABEL version="1.0.0"
LABEL description="Medical Imaging Analysis System - HIPAA Compliant"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ../../../requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir numpy>=1.21.0 pillow>=9.0.0

# Optional: Install DICOM support
RUN pip install --no-cache-dir pydicom>=2.3.0 || true

# Copy application code
COPY code/ /app/code/
COPY tests/ /app/tests/
COPY docs/ /app/docs/

# Create data directories
RUN mkdir -p /data/medical-images /data/results /var/log/medical-imaging

# Set Python path
ENV PYTHONPATH="/app/code:${PYTHONPATH}"

# Environment variables
ENV APP_ENV=production \
    APP_PORT=8080 \
    LOG_LEVEL=INFO \
    HIPAA_MODE=enabled \
    PHI_DETECTION=enabled

# Expose ports
EXPOSE 8080 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run as non-root user
RUN useradd -r -u 1000 -s /bin/false medical-imaging && \
    chown -R medical-imaging:medical-imaging /app /data /var/log/medical-imaging

USER medical-imaging

# Start application
CMD ["python3", "-u", "code/implementation.py"]
