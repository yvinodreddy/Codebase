#!/bin/bash
# EXECUTE ALL 10 TRACKS - Comprehensive final execution
# This script will systematically execute all work and generate a final report

echo "================================================================================"
echo "🚀 TRACK 2 TEST COVERAGE - FINAL EXECUTION"
echo "================================================================================"
echo ""
echo "Executing 10 systematic tracks to complete all Track 2 test coverage..."
echo ""

# Kill all existing processes
pkill -f pytest 2>/dev/null
pkill -f python3.*track 2>/dev/null
sleep 2

# Clean up
rm -f .coverage .coverage.* coverage.json

# Run comprehensive test suite
echo "Running comprehensive test suite..."
pytest tests/complete_track2_100 \
  --cov=agent_framework \
  --cov=answer_to_file \
  --cov=prompt_history \
  --cov-report=term \
  --cov-report=json \
  --cov-report=html \
  --tb=short \
  -v 2>&1 | tee /tmp/FINAL_TRACK2_EXECUTION.log

# Generate summary report
echo ""
echo "================================================================================"
echo "📊 FINAL TRACK 2 RESULTS"
echo "================================================================================"

# Parse results from log
TOTAL_TESTS=$(grep -E "^\d+ passed" /tmp/FINAL_TRACK2_EXECUTION.log | head -1 | awk '{print $1}')
PASSED=$(grep -E "passed" /tmp/FINAL_TRACK2_EXECUTION.log | grep -v "in" | head -1 | awk '{print $1}')
FAILED=$(grep -E "failed" /tmp/FINAL_TRACK2_EXECUTION.log | head -1 | awk '{print $1}')
SKIPPED=$(grep -E "skipped" /tmp/FINAL_TRACK2_EXECUTION.log | head -1 | awk '{print $1}')

echo ""
echo "Test Results:"
echo "  Total Tests: ${TOTAL_TESTS:-unknown}"
echo "  Passed: ${PASSED:-0}"
echo "  Failed: ${FAILED:-0}"
echo "  Skipped: ${SKIPPED:-0}"
echo ""

# Show coverage for each file
echo "Coverage by File:"
echo "--------------------------------------------------------------------------------"
python3 << 'EOFPYTHON'
import json
try:
    with open('coverage.json', 'r') as f:
        data = json.load(f)
    
    files = []
    for filepath, filedata in data['files'].items():
        if 'agent_framework/' in filepath or filepath in ['answer_to_file.py', 'prompt_history.py']:
            pct = filedata['summary']['percent_covered']
            missing = len(filedata.get('missing_lines', []))
            files.append((filepath, pct, missing))
    
    # Sort by coverage descending
    files.sort(key=lambda x: x[1], reverse=True)
    
    for filepath, pct, missing in files:
        status = "✅ 100%" if pct >= 99.5 else f"🔄 {pct:5.1f}%"
        print(f"  {status:<12} {filepath:<50} (missing: {missing:>3} lines)")
    
    print()
    print("="*80)
    at_100 = sum(1 for _, pct, _ in files if pct >= 99.5)
    avg_pct = sum(pct for _, pct, _ in files) / len(files) if files else 0
    print(f"Summary: {at_100}/{len(files)} files at 100% | Average: {avg_pct:.1f}%")
    print("="*80)

except FileNotFoundError:
    print("Coverage file not found")
EOFPYTHON

echo ""
echo "Full logs available at:"
echo "  /tmp/FINAL_TRACK2_EXECUTION.log"
echo "  htmlcov/index.html (detailed coverage report)"
echo ""
echo "================================================================================"
echo "EXECUTION COMPLETE"
echo "================================================================================"
