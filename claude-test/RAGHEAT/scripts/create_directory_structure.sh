#!/bin/bash

# RAGHEAT - Create Complete Directory Structure
# Generates production-ready project structure

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Creating RAGHEAT directory structure...${NC}"
echo ""

# Backend directories
echo -e "${GREEN}Creating backend structure...${NC}"
mkdir -p backend/{api,config,models,services,graph,analysis,utils,tests}
mkdir -p backend/api/{routes,middleware}
mkdir -p backend/models/{heat_propagation,options,valuation,risk,machine_learning,portfolio}
mkdir -p backend/graph
mkdir -p backend/analysis
mkdir -p backend/streaming
mkdir -p backend/tests/{unit,integration,e2e}

# Multi-Agent System (CrewAI)
echo -e "${GREEN}Creating multi-agent system structure...${NC}"
mkdir -p ragheat_crewai/{agents,coordination,workflows,synthesis,tools}

# Frontend directories
echo -e "${GREEN}Creating frontend structure...${NC}"
mkdir -p frontend/src/{components,hooks,services,store,utils,styles,assets}
mkdir -p frontend/src/components/{Layout,KnowledgeGraph,Trading,Risk,Analytics,Charts,HeatMap,News,Portfolio}
mkdir -p frontend/public

# Infrastructure
echo -e "${GREEN}Creating infrastructure structure...${NC}"
mkdir -p infrastructure/{neo4j,monitoring,docker}
mkdir -p infrastructure/neo4j
mkdir -p infrastructure/monitoring

# Services
echo -e "${GREEN}Creating services structure...${NC}"
mkdir -p services

# Scripts
echo -e "${GREEN}Creating scripts structure...${NC}"
mkdir -p scripts/{deployment,testing,maintenance}

# Documentation
echo -e "${GREEN}Creating documentation structure...${NC}"
mkdir -p docs/{api,architecture,guides,runbooks}

# Tests
echo -e "${GREEN}Creating tests structure...${NC}"
mkdir -p tests/{integration,performance,load,security}

# Data
echo -e "${GREEN}Creating data structure...${NC}"
mkdir -p data/{raw,processed,ontologies}

# Logs
mkdir -p logs

# Config
mkdir -p config

# Backups
mkdir -p .backups

echo ""
echo -e "${GREEN}Creating README files...${NC}"

# Backend README
cat > backend/README.md <<'EOL'
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
EOL

# Frontend README
cat > frontend/README.md <<'EOL'
# RAGHEAT Frontend

React-based frontend for RAGHEAT platform.

## Structure

- `src/components/` - React components
- `src/hooks/` - Custom React hooks
- `src/services/` - API and WebSocket clients
- `src/store/` - Redux state management
- `src/utils/` - Utility functions
- `src/styles/` - CSS and styling

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm start

# Build for production
npm run build

# Run tests
npm test
```
EOL

# CrewAI README
cat > ragheat_crewai/README.md <<'EOL'
# RAGHEAT Multi-Agent System

CrewAI-based multi-agent system for financial analysis.

## Agents

- Fundamental Analyst
- Sentiment Analyst
- Valuation Analyst
- Options Analyst
- Risk Manager
- Portfolio Coordinator
- Heat Diffusion Analyst
- Market Data Collector
- News Data Collector
- Social Media Collector
- And 7 more specialized agents

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run agent orchestrator
python -m coordination.agent_coordinator
```
EOL

# Infrastructure README
cat > infrastructure/README.md <<'EOL'
# RAGHEAT Infrastructure

Docker and cloud infrastructure configuration.

## Components

- Neo4j graph database
- Redis cache and message broker
- Prometheus monitoring
- Grafana dashboards
- Nginx reverse proxy

## Quick Start

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```
EOL

# Services README
cat > services/README.md <<'EOL'
# RAGHEAT Services

Microservices for data collection and processing.

## Services

- Multi-API Live Data Service
- News Aggregation Service
- Sentiment Analysis Service
- Options Data Service
- Historical Data Ingestion

## Quick Start

Each service can be run independently or via Docker Compose.
EOL

# Docs README
cat > docs/README.md <<'EOL'
# RAGHEAT Documentation

Comprehensive documentation for RAGHEAT platform.

## Contents

- `api/` - API documentation
- `architecture/` - System architecture
- `guides/` - User and developer guides
- `runbooks/` - Operational runbooks

## Documentation Standards

All documentation is written in Markdown and follows the [Documentation Style Guide](guides/STYLE_GUIDE.md).
EOL

echo ""
echo -e "${GREEN}Creating configuration files...${NC}"

# .gitignore
cat > .gitignore <<'EOL'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnp/
.pnp.js
coverage/
build/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.local
.env.*.local

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db

# Data
data/raw/
data/processed/
*.csv
*.json.backup

# Secrets
secrets/
*.key
*.pem

# Neo4j
neo4j/data/
neo4j/logs/

# Backups
.backups/*.backup
EOL

# .env.example
cat > .env.example <<'EOL'
# RAGHEAT Environment Configuration

# API Keys
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
ALPHA_VANTAGE_KEY=your_alpha_vantage_key
FINNHUB_KEY=your_finnhub_key
POLYGON_KEY=your_polygon_key
NEWS_API_KEY=your_news_api_key

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password

# Redis
REDIS_URL=redis://localhost:6379

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/ragheat

# FastAPI
API_HOST=0.0.0.0
API_PORT=8000
API_SECRET_KEY=your_secret_key_here

# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws

# Environment
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
EOL

# Docker Compose
cat > docker-compose.yml <<'EOL'
version: '3.8'

services:
  neo4j:
    image: neo4j:5.13-enterprise
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/ragheat123
      - NEO4J_ACCEPT_LICENSE_AGREEMENT=yes
    volumes:
      - neo4j-data:/data
      - neo4j-logs:/logs

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=ragheat
      - POSTGRES_USER=ragheat
      - POSTGRES_PASSWORD=ragheat123
    volumes:
      - postgres-data:/var/lib/postgresql/data

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./infrastructure/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  neo4j-data:
  neo4j-logs:
  redis-data:
  postgres-data:
  prometheus-data:
  grafana-data:
EOL

echo ""
echo -e "${GREEN}Creating placeholder files...${NC}"

# Create __init__.py files for Python packages
find backend ragheat_crewai services -type d -exec touch {}/__init__.py \; 2>/dev/null || true

# Create placeholder requirements.txt
cat > backend/requirements.txt <<'EOL'
# RAGHEAT Backend Dependencies

# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
neo4j==5.14.0
redis==5.0.1
psycopg2-binary==2.9.9
sqlalchemy==2.0.23

# Data Processing
pandas==2.1.3
numpy==1.26.2
scipy==1.11.4

# Machine Learning
scikit-learn==1.3.2
tensorflow==2.15.0
torch==2.1.1

# NLP
transformers==4.35.2
spacy==3.7.2

# Financial Data
yfinance==0.2.32
alpha-vantage==2.3.1

# AI/LLM
anthropic==0.7.0
openai==1.3.7
langchain==0.0.340
crewai==0.11.0

# Utilities
python-dotenv==1.0.0
pydantic==2.5.2
pyjwt==2.8.0
bcrypt==4.1.1
requests==2.31.0

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
httpx==0.25.2

# Development
black==23.11.0
flake8==6.1.0
mypy==1.7.1
EOL

cat > frontend/package.json <<'EOL'
{
  "name": "ragheat-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@reduxjs/toolkit": "^1.9.7",
    "react-redux": "^8.1.3",
    "@mui/material": "^5.14.20",
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "d3": "^7.8.5",
    "recharts": "^2.10.3",
    "axios": "^1.6.2",
    "socket.io-client": "^4.6.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "devDependencies": {
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.17.0",
    "react-scripts": "5.0.1"
  },
  "eslintConfig": {
    "extends": ["react-app"]
  }
}
EOL

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Directory structure created successfully!    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo "  1. Copy .env.example to .env and fill in your API keys"
echo "  2. Run: docker-compose up -d"
echo "  3. Install backend dependencies: cd backend && pip install -r requirements.txt"
echo "  4. Install frontend dependencies: cd frontend && npm install"
echo "  5. Start development!"
echo ""
