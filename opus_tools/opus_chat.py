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
            model="claude-opus-4-20250514",
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
                model="claude-opus-4-20250514",
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
