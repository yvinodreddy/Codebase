#!/usr/bin/env python3
"""
Quick Validation Study
Purpose: Generate preliminary evidence immediately
Dataset: 20 prompts (representative sample)
"""

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
import sys

# Test prompts across 5 categories
TEST_PROMPTS = {
    "factual": [
        "What is the capital of France?",
        "Who wrote Romeo and Juliet?",
        "What is the speed of light in vacuum?",
        "When did World War II end?"
    ],
    "math_logic": [
        "What is 15% of 240?",
        "If 5 machines make 5 widgets in 5 minutes, how many minutes for 100 machines to make 100 widgets?",
        "Solve: 2x + 5 = 15",
        "How many R's are in 'strawberry'?"
    ],
    "code_generation": [
        "Write a Python function to check if a number is prime",
        "Write a function to find the longest palindrome in a string",
        "Write a binary search algorithm in Python",
        "Write a function to reverse a linked list"
    ],
    "analysis": [
        "Compare pros and cons of microservices vs monolithic architecture",
        "Explain the difference between supervised and unsupervised learning",
        "What are the main causes of the 2008 financial crisis?",
        "Compare React, Vue, and Angular frameworks"
    ],
    "edge_cases": [
        "Is the following statement true or false: 'This statement is false'",
        "What happens when an irresistible force meets an immovable object?",
        "Can you divide by zero?",
        "What is the sound of one hand clapping?"
    ]
}

def run_claudeprompt(prompt):
    """Run prompt through ClaudePrompt and measure metrics"""
    start_time = time.time()

    try:
        # Run cpp command
        cmd = ["./cpp", prompt, "--verbose"]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=Path(__file__).parent.parent
        )

        execution_time = time.time() - start_time

        # Parse output for confidence score and iterations
        output = result.stdout + result.stderr
        confidence = parse_confidence(output)
        iterations = parse_iterations(output)

        return {
            "success": result.returncode == 0,
            "confidence": confidence,
            "iterations": iterations,
            "execution_time": execution_time,
            "output_length": len(result.stdout)
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "confidence": 0,
            "iterations": 0,
            "execution_time": time.time() - start_time,
            "error": "Timeout"
        }
    except Exception as e:
        return {
            "success": False,
            "confidence": 0,
            "iterations": 0,
            "execution_time": time.time() - start_time,
            "error": str(e)
        }

def parse_confidence(output):
    """Extract confidence score from output"""
    import re
    match = re.search(r'confidence[:\s]+([0-9.]+)%?', output, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return 0

def parse_iterations(output):
    """Extract iteration count from output"""
    import re
    match = re.search(r'iteration[:\s]+(\d+)', output, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 1

def main():
    print("===============================================================================")
    print("QUICK VALIDATION STUDY")
    print("===============================================================================\n")

    results = {
        "timestamp": datetime.now().isoformat(),
        "total_prompts": 0,
        "categories": {},
        "summary": {}
    }

    total_prompts = sum(len(prompts) for prompts in TEST_PROMPTS.values())
    results["total_prompts"] = total_prompts

    current = 0
    for category, prompts in TEST_PROMPTS.items():
        print(f"\n📋 Category: {category.upper()}")
        print(f"   Prompts: {len(prompts)}\n")

        category_results = []

        for prompt in prompts:
            current += 1
            print(f"   [{current}/{total_prompts}] Running: {prompt[:50]}...")

            result = run_claudeprompt(prompt)

            if result["success"]:
                print(f"       ✅ Success | Confidence: {result['confidence']:.1f}% | "
                      f"Iterations: {result['iterations']} | Time: {result['execution_time']:.1f}s")
            else:
                print(f"       ❌ Failed | Error: {result.get('error', 'Unknown')}")

            category_results.append({
                "prompt": prompt,
                **result
            })

        results["categories"][category] = category_results

    # Calculate summary statistics
    all_results = [r for cat in results["categories"].values() for r in cat]
    successful = [r for r in all_results if r["success"]]

    if successful:
        results["summary"] = {
            "success_rate": len(successful) / len(all_results) * 100,
            "avg_confidence": sum(r["confidence"] for r in successful) / len(successful),
            "avg_iterations": sum(r["iterations"] for r in successful) / len(successful),
            "avg_execution_time": sum(r["execution_time"] for r in successful) / len(successful),
            "total_successful": len(successful),
            "total_failed": len(all_results) - len(successful)
        }
    else:
        results["summary"] = {
            "success_rate": 0,
            "total_failed": len(all_results)
        }

    # Save results
    results_file = Path(__file__).parent.parent / "results" / f"quick_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("\n\n===============================================================================")
    print("SUMMARY")
    print("===============================================================================\n")
    print(f"Total Prompts:        {len(all_results)}")
    print(f"Successful:           {results['summary'].get('total_successful', 0)}")
    print(f"Failed:               {results['summary'].get('total_failed', 0)}")
    print(f"Success Rate:         {results['summary'].get('success_rate', 0):.1f}%")

    if successful:
        print(f"Avg Confidence:       {results['summary']['avg_confidence']:.1f}%")
        print(f"Avg Iterations:       {results['summary']['avg_iterations']:.1f}")
        print(f"Avg Execution Time:   {results['summary']['avg_execution_time']:.1f}s")

    print(f"\nResults saved: {results_file}")

    # Exit code based on success
    if results['summary'].get('success_rate', 0) >= 80:
        print("\n✅ PASS: Success rate >= 80%")
        sys.exit(0)
    else:
        print(f"\n❌ FAIL: Success rate < 80%")
        sys.exit(1)

if __name__ == "__main__":
    main()
