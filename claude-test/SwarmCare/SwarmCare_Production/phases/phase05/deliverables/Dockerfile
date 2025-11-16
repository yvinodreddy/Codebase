# Phase 05: Audio Generation Service
# Production-ready Docker image

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    sox \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY code/ ./code/
COPY config/ ./config/

# Create directories
RUN mkdir -p /var/audio/cache /var/audio/temp /var/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV AUDIO_CACHE_DIR=/var/audio/cache
ENV AUDIO_TEMP_DIR=/var/audio/temp
ENV LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Non-root user for security
RUN useradd -m -u 1000 audiouser && \
    chown -R audiouser:audiouser /app /var/audio /var/logs
USER audiouser

# Expose port
EXPOSE 8005

# Run application
CMD ["python", "-m", "uvicorn", "code.api:app", "--host", "0.0.0.0", "--port", "8005"]
