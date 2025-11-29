#!/bin/bash
################################################################################
# EXECUTE WHEN COVERAGE RUN COMPLETES
# This script analyzes coverage and generates targeted tests to reach 100%
################################################################################

echo "================================================================================"
echo "🎯 100% COVERAGE COMPLETION SCRIPT"
echo "================================================================================"

# Check if coverage data exists
if [ ! -f coverage.json ]; then
    echo "❌ coverage.json not found"
    echo "Coverage tests may still be running. Please wait..."
    echo ""
    echo "You can check the status with:"
    echo "  ps aux | grep pytest | grep -v grep"
    exit 1
fi

echo "✅ Coverage data found!"
echo ""

# Run the systematic analyzer
echo "📊 Running systematic coverage analyzer..."
python3 achieve_100_percent_coverage.py

echo ""
echo "================================================================================"
echo "📋 FINAL SUMMARY REPORT"
echo "================================================================================"

# Extract overall coverage
COVERAGE=$(python3 -c "import json; d=json.load(open('coverage.json')); print(f'{d[\"totals\"][\"percent_covered\"]:.2f}')")

echo "📊 Overall Coverage: $COVERAGE%"
echo ""

# Count files by coverage level
echo "📁 Files by Coverage Level:"
python3 << 'PYEOF'
import json

with open('coverage.json') as f:
    data = json.load(f)

excellent = 0  # >= 90%
good = 0       # >= 75%
needs_work = 0 # >= 50%
critical = 0   # < 50%

for file_path, file_data in data.get('files', {}).items():
    if 'test_' in file_path or '__init__' in file_path or '/tests/' in file_path:
        continue

    percent = file_data.get('summary', {}).get('percent_covered', 0)

    if percent >= 90:
        excellent += 1
    elif percent >= 75:
        good += 1
    elif percent >= 50:
        needs_work += 1
    else:
        critical += 1

print(f"  ✅ Excellent (≥90%):  {excellent} files")
print(f"  ⭐ Good (75-89%):     {good} files")
print(f"  ⚠️  Needs Work (50-74%): {needs_work} files")
print(f"  ❌ Critical (<50%):   {critical} files")
print(f"\n  Total Production Files: {excellent + good + needs_work + critical}")
PYEOF

echo ""
echo "================================================================================"
echo "📊 VIEW DETAILED COVERAGE REPORT"
echo "================================================================================"
echo ""
echo "Open the HTML coverage report to see line-by-line details:"
echo "  file://$(pwd)/htmlcov/index.html"
echo ""
echo "Or if using WSL:"
echo "  explorer.exe htmlcov/index.html"
echo ""

echo "================================================================================"
echo "🎯 NEXT STEPS TO REACH 100% COVERAGE"
echo "================================================================================"
echo ""
echo "1. Review the priority files listed above"
echo "2. Open htmlcov/index.html to see uncovered lines"
echo "3. Add targeted tests for uncovered code paths"
echo "4. Re-run: pytest tests/ --cov=. --cov-report=html"
echo "5. Repeat until all files reach ≥90% coverage"
echo ""
echo "================================================================================"
