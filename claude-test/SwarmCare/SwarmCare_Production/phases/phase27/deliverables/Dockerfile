FROM python:3.12-slim

WORKDIR /app

# Copy application files
COPY ../code /app/code
COPY requirements-clinical-trial.txt /app/

# Install optional dependencies (if any)
RUN pip install --no-cache-dir -r requirements-clinical-trial.txt

# Expose ports
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python3 -c "import sys; sys.path.insert(0, '/app/code'); from trial_lifecycle_core import ClinicalTrialLifecycleSystem; system = ClinicalTrialLifecycleSystem(); print('healthy')"

CMD ["python3", "code/implementation.py"]
