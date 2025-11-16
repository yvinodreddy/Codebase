#!/usr/bin/env python3
"""Test Opus API connection"""

import anthropic
import os

print("🧪 Testing Opus 4 API Connection...")
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
        model="claude-opus-4-20250514",
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Say 'Opus 4 is ready!' and nothing else."}
        ]
    )

    response = message.content[0].text
    print(f"\n🤖 Response: {response}")
    print(f"\n📊 Tokens used: {message.usage.input_tokens} in, {message.usage.output_tokens} out")
    print(f"💰 Cost: ${(message.usage.input_tokens * 15 + message.usage.output_tokens * 75) / 1_000_000:.6f}")
    print("\n✅ SUCCESS! Opus 4 is working via API!")
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
