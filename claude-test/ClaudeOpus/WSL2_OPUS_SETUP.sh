#!/bin/bash
# WSL2 Opus 4.1 API Setup Script
# Run this in your WSL2 Ubuntu terminal

set -e  # Exit on error

echo "🚀 Setting up Opus 4.1 API in WSL2..."
echo "This will take about 5 minutes"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Installing..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# Install Anthropic SDK
echo "📦 Installing Anthropic Python SDK..."
pip3 install --user --break-system-packages anthropic
echo "✅ Anthropic SDK installed"
echo ""

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "🔑 API Key Setup"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Step 1: Get your API key"
    echo "   → Open: https://console.anthropic.com"
    echo "   → Click 'Get API Keys'"
    echo "   → Click 'Create Key'"
    echo "   → Copy the key (starts with sk-ant-...)"
    echo ""
    echo "Step 2: Paste your API key below"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    read -p "Enter your Anthropic API key: " api_key

    if [ -z "$api_key" ]; then
        echo "❌ No API key provided. Exiting."
        exit 1
    fi

    # Add to .bashrc
    echo "" >> ~/.bashrc
    echo "# Anthropic API Key (added by setup script)" >> ~/.bashrc
    echo "export ANTHROPIC_API_KEY=\"$api_key\"" >> ~/.bashrc

    # Set for current session
    export ANTHROPIC_API_KEY="$api_key"

    echo "✅ API key saved to ~/.bashrc"
    echo ""
fi

# Create helper scripts directory
mkdir -p ~/opus_tools
cd ~/opus_tools

# Create main helper script
cat > opus_chat.py << 'SCRIPT_END'
#!/usr/bin/env python3
"""
Opus 4.1 Chat Helper for WSL2
Quick access to unlimited Opus when Claude Code hits limits
"""

import anthropic
import os
import sys
import json
from datetime import datetime

def print_usage():
    print("""
🤖 Opus 4.1 Chat Helper

USAGE:
    python3 opus_chat.py                    # Interactive mode
    python3 opus_chat.py "your question"    # Quick question
    python3 opus_chat.py -f file.py         # Include file context
    python3 opus_chat.py -i                 # Interactive with history

EXAMPLES:
    # Quick architecture question
    python3 opus_chat.py "Design a FastAPI endpoint for FHIR data ingestion"

    # With code context
    python3 opus_chat.py -f my_code.py "Review this code for issues"

    # Interactive session
    python3 opus_chat.py -i
""")

def quick_query(question, context_file=None, use_cache=True):
    """Single query to Opus"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set!")
        print("Run: export ANTHROPIC_API_KEY='your-key'")
        return

    client = anthropic.Anthropic(api_key=api_key)

    # Build message
    message_content = question

    if context_file and os.path.exists(context_file):
        with open(context_file, 'r') as f:
            context = f.read()
        message_content = f"""Context from {context_file}:
```
{context}
```

Question: {question}
"""

    print("🤖 Calling Opus 4.1...")
    print("━" * 60)

    start_time = datetime.now()

    try:
        message = client.messages.create(
            model="claude-opus-4",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": message_content}
            ]
        )

        response = message.content[0].text
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print(response)
        print("\n" + "━" * 60)
        print(f"⏱️  Time: {duration:.1f}s")
        print(f"📊 Tokens: {message.usage.input_tokens} in, {message.usage.output_tokens} out")

        # Calculate cost
        input_cost = message.usage.input_tokens * 15 / 1_000_000
        output_cost = message.usage.output_tokens * 75 / 1_000_000
        total_cost = input_cost + output_cost

        print(f"💰 Cost: ${total_cost:.4f} (${input_cost:.4f} in + ${output_cost:.4f} out)")

    except anthropic.APIError as e:
        print(f"❌ API Error: {e}")
        return None

    return response

def interactive_mode():
    """Interactive chat session with Opus"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set!")
        return

    client = anthropic.Anthropic(api_key=api_key)

    print("🎯 Opus 4.1 Interactive Mode")
    print("━" * 60)
    print("Commands:")
    print("  /file <path>  - Add file context")
    print("  /clear        - Clear conversation")
    print("  /cost         - Show session cost")
    print("  /exit         - Exit")
    print("━" * 60)
    print()

    conversation = []
    total_cost = 0.0

    while True:
        try:
            user_input = input("👤 You: ").strip()

            if not user_input:
                continue

            if user_input == "/exit":
                print(f"\n💰 Total session cost: ${total_cost:.4f}")
                print("👋 Goodbye!")
                break

            if user_input == "/clear":
                conversation = []
                total_cost = 0.0
                print("🗑️  Conversation cleared")
                continue

            if user_input == "/cost":
                print(f"💰 Session cost so far: ${total_cost:.4f}")
                continue

            if user_input.startswith("/file "):
                filepath = user_input[6:].strip()
                if os.path.exists(filepath):
                    with open(filepath, 'r') as f:
                        content = f.read()
                    print(f"📁 Loaded {len(content)} chars from {filepath}")
                    user_input = f"Context from {filepath}:\n```\n{content}\n```"
                else:
                    print(f"❌ File not found: {filepath}")
                    continue

            conversation.append({"role": "user", "content": user_input})

            print("🤖 Opus: ", end="", flush=True)

            message = client.messages.create(
                model="claude-opus-4",
                max_tokens=4096,
                messages=conversation
            )

            response = message.content[0].text
            conversation.append({"role": "assistant", "content": response})

            print(response)

            # Calculate and show cost
            input_cost = message.usage.input_tokens * 15 / 1_000_000
            output_cost = message.usage.output_tokens * 75 / 1_000_000
            query_cost = input_cost + output_cost
            total_cost += query_cost

            print(f"\n💰 This query: ${query_cost:.4f} | Session total: ${total_cost:.4f}\n")

        except KeyboardInterrupt:
            print(f"\n\n💰 Total session cost: ${total_cost:.4f}")
            print("👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments - interactive mode
        interactive_mode()
    elif sys.argv[1] in ["-h", "--help"]:
        print_usage()
    elif sys.argv[1] == "-i":
        interactive_mode()
    elif sys.argv[1] == "-f":
        # File context mode
        if len(sys.argv) < 4:
            print("Usage: opus_chat.py -f <file> <question>")
            sys.exit(1)
        context_file = sys.argv[2]
        question = " ".join(sys.argv[3:])
        quick_query(question, context_file)
    else:
        # Quick question mode
        question = " ".join(sys.argv[1:])
        quick_query(question)
SCRIPT_END

chmod +x opus_chat.py

# Create healthcare project helper with caching
cat > healthcare_opus.py << 'SCRIPT_END'
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
            model="claude-opus-4",
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
SCRIPT_END

chmod +x healthcare_opus.py

# Create test script
cat > test_opus.py << 'SCRIPT_END'
#!/usr/bin/env python3
"""Test Opus API connection"""

import anthropic
import os

print("🧪 Testing Opus 4.1 API Connection...")
print("━" * 60)

api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    print("❌ ANTHROPIC_API_KEY environment variable not set!")
    print("\nTo fix:")
    print("1. Get your key from: https://console.anthropic.com")
    print("2. Run: export ANTHROPIC_API_KEY='your-key-here'")
    print("3. Or add to ~/.bashrc for persistence")
    exit(1)

print(f"✅ API Key found: {api_key[:15]}...")

try:
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-opus-4",
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Say 'Opus 4.1 is ready!' and nothing else."}
        ]
    )

    response = message.content[0].text
    print(f"\n🤖 Response: {response}")
    print(f"\n📊 Tokens used: {message.usage.input_tokens} in, {message.usage.output_tokens} out")
    print(f"💰 Cost: ${(message.usage.input_tokens * 15 + message.usage.output_tokens * 75) / 1_000_000:.6f}")
    print("\n✅ SUCCESS! Opus 4.1 is working via API!")
    print("━" * 60)
    print("\nYou can now use:")
    print("  python3 ~/opus_tools/opus_chat.py          - General queries")
    print("  python3 ~/opus_tools/healthcare_opus.py    - Healthcare project (cached)")

except anthropic.APIError as e:
    print(f"\n❌ API Error: {e}")
    print("\nPossible issues:")
    print("  - Invalid API key")
    print("  - No credits in account")
    print("  - Network connectivity")
    print("\nVisit: https://console.anthropic.com")
    exit(1)
SCRIPT_END

chmod +x test_opus.py

echo ""
echo "✅ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🧪 Testing your API connection..."
python3 test_opus.py
echo ""
echo "📚 Created Tools in ~/opus_tools/:"
echo ""
echo "1. opus_chat.py - General purpose Opus chat"
echo "   Usage: python3 ~/opus_tools/opus_chat.py"
echo ""
echo "2. healthcare_opus.py - Healthcare project (with caching)"
echo "   Usage: python3 ~/opus_tools/healthcare_opus.py 'your question'"
echo ""
echo "3. test_opus.py - Test API connection"
echo "   Usage: python3 ~/opus_tools/test_opus.py"
echo ""
echo "🎯 Quick Start:"
echo "   python3 ~/opus_tools/opus_chat.py -i"
echo ""
echo "💡 For your healthcare project:"
echo "   python3 ~/opus_tools/healthcare_opus.py 'Design the GNN architecture'"
echo ""
echo "🔑 Remember to reload your shell or run:"
echo "   source ~/.bashrc"
echo ""
echo "🚀 You're ready! No more 3-day quota waits!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
