FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy ClaudePrompt
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt || true

# Create results directory
RUN mkdir -p /results

# Default command: run validation
CMD ["python3", "validation/run_validation.py"]
