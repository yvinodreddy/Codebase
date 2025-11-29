#!/usr/bin/env python3
"""
Comparative Benchmarking Setup
Purpose: Prepare infrastructure for 200 prompts × 8 platforms comparison
Status: INDEPENDENT - can run in parallel with all other tasks
"""

import json
from pathlib import Path
from datetime import datetime

# Create prompt categories
PROMPT_CATEGORIES = {
    "factual": {
        "description": "Verifiable factual questions",
        "count": 20,
        "examples": [
            "What is the capital of France?",
            "Who wrote Romeo and Juliet?",
            "What is the speed of light in vacuum?",
            "When did World War II end?",
            "What is the largest ocean on Earth?"
        ]
    },
    "math_logic": {
        "description": "Mathematical and logical reasoning",
        "count": 20,
        "examples": [
            "What is 15% of 240?",
            "If 5 machines make 5 widgets in 5 minutes, how many minutes for 100 machines to make 100 widgets?",
            "Solve: 2x + 5 = 15",
            "How many R's are in 'strawberry'?",
            "What is the next number in the sequence: 2, 4, 8, 16, ?"
        ]
    },
    "code_generation": {
        "description": "Programming tasks",
        "count": 20,
        "examples": [
            "Write a Python function to check if a number is prime",
            "Write a function to find the longest palindrome in a string",
            "Write a binary search algorithm in Python",
            "Write a function to reverse a linked list",
            "Implement quicksort in Python"
        ]
    },
    # Add remaining 7 categories...
}

def setup_infrastructure():
    """Set up directory structure and template files"""
    base_dir = Path(__file__).parent.parent

    # Create directories
    dirs = [
        base_dir / "evaluation/prompts",
        base_dir / "evaluation/responses",
        base_dir / "evaluation/scripts",
        base_dir / "results/comparative"
    ]

    for platforms in ["claudeprompt", "claude_code", "claude_web", "chatgpt", "gemini"]:
        dirs.append(base_dir / f"evaluation/responses/{platform}")

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Save prompt templates
    prompts_file = base_dir / "evaluation/prompts/all_prompts.json"
    with open(prompts_file, 'w') as f:
        json.dump(PROMPT_CATEGORIES, f, indent=2)

    print(f"✅ Infrastructure setup complete")
    print(f"   Prompts file: {prompts_file}")
    print(f"   Response directories created for 5 platforms")
    print(f"   Ready for data collection phase")

    return {
        "status": "complete",
        "timestamp": datetime.now().isoformat(),
        "prompts_file": str(prompts_file),
        "total_categories": len(PROMPT_CATEGORIES)
    }

if __name__ == "__main__":
    result = setup_infrastructure()
    print(f"\n📊 Setup Summary:")
    print(f"   Status: {result['status']}")
    print(f"   Categories: {result['total_categories']}")
