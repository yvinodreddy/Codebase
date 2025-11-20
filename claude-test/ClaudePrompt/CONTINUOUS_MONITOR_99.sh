#!/bin/bash
# Continuous monitoring script for 99% coverage push
# Provides updates every 2 minutes

LOG_FILE="/tmp/continuous_99_monitor.log"
ITERATION=0
START_TIME=$(date +%s)

echo "================================" | tee -a "$LOG_FILE"
echo "🚀 CONTINUOUS 99% COVERAGE PUSH" | tee -a "$LOG_FILE"
echo "   Started: $(date)" | tee -a "$LOG_FILE"
echo "   Target: 99%" | tee -a "$LOG_FILE"
echo "   Updates: Every 2 minutes" | tee -a "$LOG_FILE"
echo "================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

while true; do
    ITERATION=$((ITERATION + 1))
    ELAPSED=$(( $(date +%s) - START_TIME ))
    ELAPSED_MIN=$((ELAPSED / 60))

    echo "[$(date +%H:%M:%S)] ⏱️  ITERATION $ITERATION (Elapsed: ${ELAPSED_MIN}m)" | tee -a "$LOG_FILE"

    # Measure current coverage
    if pytest tests/ --cov=. --cov-report=json -q > /dev/null 2>&1; then
        COVERAGE=$(python3 -c "import json; data=json.load(open('coverage.json')); print(f'{data[\"totals\"][\"percent_covered\"]:.2f}')" 2>/dev/null || echo "ERROR")

        if [ "$COVERAGE" != "ERROR" ]; then
            echo "   📊 Current Coverage: ${COVERAGE}%" | tee -a "$LOG_FILE"

            # Check if target reached
            if (( $(echo "$COVERAGE >= 99" | bc -l) )); then
                echo "" | tee -a "$LOG_FILE"
                echo "🎉🎉🎉 TARGET REACHED! 🎉🎉🎉" | tee -a "$LOG_FILE"
                echo "   Final Coverage: ${COVERAGE}%" | tee -a "$LOG_FILE"
                echo "   Total Time: ${ELAPSED_MIN} minutes" | tee -a "$LOG_FILE"
                exit 0
            fi

            GAP=$(python3 -c "print(f'{99 - float(\"$COVERAGE\"):.2f}')")
            echo "   📈 Gap to target: ${GAP}%" | tee -a "$LOG_FILE"
        else
            echo "   ❌ Coverage measurement failed" | tee -a "$LOG_FILE"
        fi
    else
        echo "   ⚠️  Pytest errors detected" | tee -a "$LOG_FILE"
    fi

    # Count test files
    TEST_COUNT=$(find tests/ -name "test_*.py" -type f | wc -l)
    echo "   📝 Total test files: $TEST_COUNT" | tee -a "$LOG_FILE"

    echo "" | tee -a "$LOG_FILE"

    # Wait 2 minutes before next check
    sleep 120
done
