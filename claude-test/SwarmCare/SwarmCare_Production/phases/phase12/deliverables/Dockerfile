# Phase 12: Clinical Decision Support System - Docker Image
# Production-ready container for clinical decision support

FROM python:3.11-slim

# Metadata
LABEL maintainer="SwarmCare AI Team <team@swarmcare.ai>"
LABEL description="Clinical Decision Support System - Sepsis Detection, Drug Interactions, Early Warning Scores"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r cdsuser && useradd -r -g cdsuser cdsuser

# Copy application code
COPY code/ /app/code/
COPY tests/ /app/tests/
COPY docs/ /app/docs/

# Set Python path
ENV PYTHONPATH=/app/code:$PYTHONPATH

# Create log directory
RUN mkdir -p /var/log/cds && \
    chown -R cdsuser:cdsuser /var/log/cds

# Create data directory for audit logs
RUN mkdir -p /app/data && \
    chown -R cdsuser:cdsuser /app/data

# Switch to non-root user
USER cdsuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "from code.clinical_decision_support import assess_patient" || exit 1

# Expose port (if running as web service)
EXPOSE 8080

# Default command - run verification
CMD ["python3", "tests/test_clinical_decision_support.py"]

# Alternative command for running as service:
# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]
