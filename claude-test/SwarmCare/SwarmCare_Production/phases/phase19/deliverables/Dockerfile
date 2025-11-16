# Phase 19: Voice AI & Ambient Intelligence - Docker Image
# Production-ready container for voice-enabled clinical documentation

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=UTC

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY code/ /app/code/
COPY tests/ /app/tests/
COPY docs/ /app/docs/
COPY deliverables/verify_phase19.py /app/

# Create non-root user for security
RUN useradd -m -u 1000 voiceai && \
    chown -R voiceai:voiceai /app

USER voiceai

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "from code.voice_ai_system import VoiceAISystem; VoiceAISystem()" || exit 1

# Run verification on startup
RUN python3 verify_phase19.py --quick

# Default command
CMD ["python3", "-m", "code.voice_ai_system"]

# Metadata
LABEL maintainer="SwarmCare AI Team" \
      version="1.0" \
      description="Phase 19: Voice AI & Ambient Intelligence" \
      phase="19" \
      story_points="51"
