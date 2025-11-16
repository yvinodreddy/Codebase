# Phase 25: Patient-Facing XAI - Docker Image

FROM python:3.11-slim

# Metadata
LABEL maintainer="SwarmCare Production Team"
LABEL version="1.0.0"
LABEL description="Patient-Facing XAI Service"

# Set working directory
WORKDIR /app

# Install system dependencies (minimal - we use stdlib only)
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY code/patient_facing_xai_core.py /app/
COPY code/implementation.py /app/
COPY deliverables/patient_xai_config.json /app/config.json

# Create logs directory
RUN mkdir -p /var/log/patient-xai

# Create non-root user for security
RUN useradd -m -u 1000 xaiuser && \
    chown -R xaiuser:xaiuser /app /var/log/patient-xai

USER xaiuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python3 -c "from implementation import Phase25Implementation; impl = Phase25Implementation(); print('healthy')" || exit 1

# Expose ports
EXPOSE 8080 9090

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    HIPAA_MODE=enabled \
    LOG_LEVEL=INFO

# Run application
CMD ["python3", "implementation.py"]
