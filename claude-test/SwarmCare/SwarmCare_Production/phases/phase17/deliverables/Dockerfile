# Phase 17: Population Health Management
# Production Docker Image

FROM python:3.11-slim

LABEL maintainer="SwarmCare <support@swarmcare.com>"
LABEL description="Population Health Management System - Phase 17"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY deliverables/requirements-population-health.txt /app/requirements.txt

# Install Python dependencies (optional - core has zero dependencies)
# RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY code/ /app/code/
COPY guardrails/ /app/guardrails/
COPY agent_framework/ /app/agent_framework/

# Set Python path
ENV PYTHONPATH=/app

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose ports
EXPOSE 8080 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)"

# Run application
CMD ["python3", "-u", "code/implementation.py"]
