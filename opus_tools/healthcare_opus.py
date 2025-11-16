#!/usr/bin/env python3
"""
Healthcare Project Opus Helper with Prompt Caching
Optimized for complex healthcare architecture queries
"""

import anthropic
import os
import sys

# Your healthcare project context (this gets cached!)
HEALTHCARE_CONTEXT = """
# Healthcare Dashboard Project

## Technology Stack
- Frontend: React with TypeScript
- Backend: Python FastAPI
- Database: PostgreSQL + Neo4j (graph database)
- ML/AI: PyTorch, HuggingFace Transformers
- Healthcare Standards: FHIR R4, HL7

## Core Components

### 1. Graph Neural Network (GNN) Layer
- Patient similarity analysis
- Disease correlation modeling
- Treatment outcome prediction
- Multi-hop reasoning over patient graphs

### 2. FHIR Integration Layer
- Patient resource ingestion
- Condition/Observation/Medication parsing
- EHR interoperability
- HL7 message handling

### 3. LLM Recommendation Engine
- Clinical decision support
- Treatment recommendations
- Drug interaction analysis
- Evidence-based suggestions

### 4. Multi-Patient Dashboard
- Doctor interface
- Patient selection and filtering
- Multi-disease visualization
- Real-time recommendation display
- Explainable AI insights

## Architecture Requirements
- HIPAA compliance mandatory
- Real-time performance (<2s response time)
- Support 1000+ concurrent patient records
- Explainable AI for clinical trust
- Audit logging for all recommendations

## Current Challenges
- Integrating GNN outputs with FHIR data model
- Real-time inference at scale
- Making recommendations explainable to clinicians
- Handling complex multi-disease scenarios
- Performance optimization for graph queries
"""

def cached_query(question):
    """
    Query Opus with cached healthcare context
    First query: ~$0.30 (cache write)
    Subsequent queries: ~$0.03 each (90% savings!)
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set!")
        return

    client = anthropic.Anthropic(api_key=api_key)

    print("🏥 Healthcare Project Opus (with caching)")
    print("━" * 60)
    print(f"📝 Question: {question}")
    print("━" * 60)

    try:
        message = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=4096,
            system=[
                {
                    "type": "text",
                    "text": HEALTHCARE_CONTEXT,
                    "cache_control": {"type": "ephemeral"}  # Cache this!
                }
            ],
            messages=[
                {"role": "user", "content": question}
            ]
        )

        response = message.content[0].text
        print(response)
        print("\n" + "━" * 60)

        # Show cache efficiency
        usage = message.usage

        # Check for cache hits
        cache_read = getattr(usage, 'cache_read_input_tokens', 0)
        cache_create = getattr(usage, 'cache_creation_input_tokens', 0)

        print(f"📊 Tokens: {usage.input_tokens} in, {usage.output_tokens} out")

        if cache_create > 0:
            print(f"📝 Cache CREATED: {cache_create} tokens (available for 5 min)")
            print("   → Next queries will be 90% cheaper!")

        if cache_read > 0:
            print(f"✅ Cache HIT: {cache_read} tokens read from cache")
            print("   → Saved 90% on context cost!")

        # Calculate cost
        input_cost = usage.input_tokens * 15 / 1_000_000

        # Cached tokens cost less
        if cache_read > 0:
            cache_savings = cache_read * 13.5 / 1_000_000  # Saved $13.50/M
            input_cost -= cache_savings

        output_cost = usage.output_tokens * 75 / 1_000_000
        total_cost = input_cost + output_cost

        print(f"💰 Cost: ${total_cost:.4f}")

        if cache_read > 0:
            uncached_cost = (usage.input_tokens + cache_read) * 15 / 1_000_000 + output_cost
            savings = uncached_cost - total_cost
            print(f"💵 Saved: ${savings:.4f} (cache hit)")

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

    return response

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
🏥 Healthcare Project Opus Helper

USAGE:
    python3 healthcare_opus.py "your question about the healthcare project"

EXAMPLES:
    python3 healthcare_opus.py "Design the GNN architecture for patient similarity"
    python3 healthcare_opus.py "How should FHIR data feed into the graph database?"
    python3 healthcare_opus.py "Design the recommendation engine API endpoints"

CACHING:
- First query: ~$0.30 (creates cache)
- Next queries (within 5 min): ~$0.03 each (90% savings!)
- Make multiple queries quickly to maximize savings
        """)
        sys.exit(0)

    question = " ".join(sys.argv[1:])
    cached_query(question)
