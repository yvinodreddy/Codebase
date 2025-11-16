#!/usr/bin/env python3
"""
Simple test to verify Claude API works directly
"""

import os
import anthropic

# Get API key
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ ANTHROPIC_API_KEY not set")
    exit(1)

# Create client
client = anthropic.Anthropic(api_key=api_key)

# Simple test query
print("Testing Claude API directly...")
print("Query: What is 5+5?")
print()

try:
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",  # Latest Sonnet 4.5 model
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "What is 5+5?"}
        ]
    )

    print("✅ SUCCESS!")
    print(f"\nResponse: {message.content[0].text}")
    print(f"\nTokens used: {message.usage.input_tokens + message.usage.output_tokens}")

except Exception as e:
    print(f"❌ ERROR: {e}")
    exit(1)
