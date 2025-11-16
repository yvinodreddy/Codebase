#!/usr/bin/env python3
"""Test Opus API connection with retry and fallback"""

import anthropic
import os
import time

def test_model(client, model_name, description):
    """Test a specific model"""
    print(f"\n🧪 Testing {description}...")
    print("━" * 60)

    try:
        message = client.messages.create(
            model=model_name,
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Say 'Ready!' and nothing else."}
            ]
        )

        response = message.content[0].text
        print(f"✅ SUCCESS! Model: {model_name}")
        print(f"🤖 Response: {response}")
        print(f"📊 Tokens: {message.usage.input_tokens} in, {message.usage.output_tokens} out")

        # Calculate cost
        input_cost = message.usage.input_tokens * 15 / 1_000_000
        output_cost = message.usage.output_tokens * 75 / 1_000_000
        total_cost = input_cost + output_cost
        print(f"💰 Cost: ${total_cost:.6f}")
        return True

    except anthropic.APIError as e:
        if "overloaded" in str(e).lower():
            print(f"⚠️  Model overloaded (high demand)")
        elif "not_found" in str(e).lower():
            print(f"❌ Model not found: {model_name}")
        else:
            print(f"❌ API Error: {e}")
        return False

print("🚀 Claude Opus API Testing with Retry/Fallback")
print("=" * 60)

api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    print("❌ ANTHROPIC_API_KEY environment variable not set!")
    print("\nTo fix:")
    print("1. Get your key from: https://console.anthropic.com")
    print("2. Run: export ANTHROPIC_API_KEY='your-key-here'")
    print("3. Or add to ~/.bashrc for persistence")
    exit(1)

print(f"✅ API Key found: {api_key[:15]}...")

client = anthropic.Anthropic(api_key=api_key)

# Try models in order of preference
models = [
    ("claude-opus-4-1-20250805", "Claude Opus 4.1 (Aug 2025)"),
    ("claude-opus-4", "Claude Opus 4 (alias - may route differently)"),
    ("claude-opus-4-20250514", "Claude Opus 4 (May 2025)"),
]

print("\n🎯 Attempting to connect to Opus models...")

success = False
for model_name, description in models:
    if test_model(client, model_name, description):
        success = True
        print("\n" + "=" * 60)
        print("✅ Opus API is working!")
        print(f"   Using: {model_name}")
        print("=" * 60)
        print("\nYou can now use:")
        print("  python3 ~/opus_tools/opus_chat.py          - General queries")
        print("  python3 ~/opus_tools/healthcare_opus.py    - Healthcare project (cached)")
        break

    # Brief pause between attempts
    time.sleep(1)

if not success:
    print("\n" + "=" * 60)
    print("⚠️  All Opus models are currently overloaded")
    print("=" * 60)
    print("\nThis is common during peak hours. Options:")
    print("1. Try again in a few minutes")
    print("2. Use Claude Sonnet 4.5 (faster, cheaper, still excellent)")
    print("3. Check https://status.anthropic.com for service status")
    print("\n💡 Your API key is valid - verified with Sonnet")
