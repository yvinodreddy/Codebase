# Phase 22: Continuous Learning & Federated ML - Docker Image
# Production-ready container for continuous ML operations

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=UTC \
    MODEL_TYPE=diagnosis_predictor \
    PRIVACY_EPSILON=1.0 \
    ENABLE_FEDERATED=true

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir numpy

# Copy application code
COPY code/ /app/code/
COPY tests/ /app/tests/
COPY docs/ /app/docs/
COPY deliverables/verify_phase22.py /app/

# Create non-root user for security
RUN useradd -m -u 1000 mluser && \
    mkdir -p /app/models /app/logs && \
    chown -R mluser:mluser /app

USER mluser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "from code.continuous_learning_system import ContinuousLearningSystem" || exit 1

# Run verification on startup
RUN python3 verify_phase22.py --quick

# Default command
CMD ["python3", "-c", "from code.continuous_learning_system import ContinuousLearningSystem; print('Continuous Learning System Ready')"]

# Metadata
LABEL maintainer="SwarmCare AI Team" \
      version="1.0" \
      description="Phase 22: Continuous Learning & Federated ML" \
      phase="22" \
      story_points="46"
