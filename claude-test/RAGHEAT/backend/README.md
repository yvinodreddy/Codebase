# RAGHEAT Backend

FastAPI-based backend for RAGHEAT financial intelligence platform.

## Structure

- `api/` - FastAPI application and routes
- `config/` - Configuration files
- `models/` - Data models and business logic
- `services/` - Business services
- `graph/` - Neo4j knowledge graph operations
- `analysis/` - Financial analysis modules
- `streaming/` - WebSocket and real-time streaming
- `tests/` - Test suites

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
cd api
python -m uvicorn main:app --reload

# Run tests
pytest tests/
```
