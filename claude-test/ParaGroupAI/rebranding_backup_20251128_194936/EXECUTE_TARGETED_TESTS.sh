#!/bin/bash

################################################################################
# EXECUTE_TARGETED_TESTS.sh
# Generates tests for low-coverage files using 20 parallel tasks
################################################################################

set -euo pipefail

echo "========================================="
echo "🎯 TARGETED TEST GENERATION (20 PARALLEL)"
echo "========================================="
echo ""

# Step 1: Validate input file
if [ ! -f "/tmp/low_coverage_files.txt" ]; then
    echo "❌ Error: /tmp/low_coverage_files.txt not found"
    exit 1
fi

TOTAL_FILES=$(wc -l < /tmp/low_coverage_files.txt)
echo "[INPUT] Low-coverage files: $TOTAL_FILES"

# Step 2: Setup
LOG_DIR="/tmp/targeted_tests_logs"
mkdir -p "$LOG_DIR"
rm -f "$LOG_DIR"/*

# Step 3: Divide into 20 batches
echo "[BATCHING] Dividing into 20 batches..."
BATCH_SIZE=$(( (TOTAL_FILES + 19) / 20 ))
cat /tmp/low_coverage_files.txt | split -l $BATCH_SIZE - "$LOG_DIR/batch_"

TOTAL_BATCHES=$(ls -1 "$LOG_DIR"/batch_* | wc -l)
echo "   Created $TOTAL_BATCHES batches (~$BATCH_SIZE files each)"
echo ""

# Step 4: Launch 20 parallel tasks
echo "[LAUNCH] Starting 20 parallel tasks..."
START_TIME=$(date +%s)
PIDS=()
TASK_ID=0

for batch_file in "$LOG_DIR"/batch_*; do
    if [ ! -f "$batch_file" ]; then
        continue
    fi

    TASK_ID=$((TASK_ID + 1))
    TASK_LOG="$LOG_DIR/task_${TASK_ID}.log"

    echo "[TASK $TASK_ID] Started at $(date)" > "$TASK_LOG"
    echo "[TASK $TASK_ID] Processing batch: $batch_file" >> "$TASK_LOG"

    # Launch task in background
    (
        CURRENT_TASK_ID=$TASK_ID
        CURRENT_BATCH_FILE="$batch_file"
        CURRENT_TASK_LOG="$TASK_LOG"

        while IFS= read -r source_file; do
            # Skip if file doesn't exist
            if [ ! -f "$source_file" ]; then
                echo "[TASK $CURRENT_TASK_ID] ⚠️  File not found: $source_file" >> "$CURRENT_TASK_LOG"
                continue
            fi

            filename=$(basename "$source_file" .py)
            test_file="tests/unit_real_coverage/test_${filename}_real.py"

            echo "[TASK $CURRENT_TASK_ID] Generating test for: $source_file" >> "$CURRENT_TASK_LOG"

            # Generate test
            if python3 generate_real_coverage_tests.py "$source_file" "$test_file" >> "$CURRENT_TASK_LOG" 2>&1; then
                echo "[TASK $CURRENT_TASK_ID] ✅ Generated: $test_file" >> "$CURRENT_TASK_LOG"
            else
                echo "[TASK $CURRENT_TASK_ID] ❌ Failed: $source_file" >> "$CURRENT_TASK_LOG"
            fi
        done < "$CURRENT_BATCH_FILE"

        echo "[TASK $CURRENT_TASK_ID] Finished at $(date)" >> "$CURRENT_TASK_LOG"
    ) &

    PIDS+=($!)
    echo "   Task $TASK_ID launched (PID: $!)"
done

TOTAL_TASKS=${#PIDS[@]}
echo ""
echo "✅ Launched $TOTAL_TASKS parallel tasks"
echo "📊 Monitor logs: $LOG_DIR/task_*.log"
echo ""

# Step 5: Wait for all tasks to complete
echo "[WAIT] Waiting for all tasks to complete..."
for pid in "${PIDS[@]}"; do
    wait $pid
done

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo ""
echo "========================================="
echo "✅ ALL TASKS COMPLETED"
echo "========================================="
echo "   Duration: ${ELAPSED}s"
echo "   Files processed: $TOTAL_FILES"
echo ""

# Step 6: Summary
echo "[SUMMARY] Counting generated tests..."
GENERATED=$(grep -h "✅ Generated:" "$LOG_DIR"/task_*.log | wc -l)
FAILED=$(grep -h "❌ Failed:" "$LOG_DIR"/task_*.log | wc -l)

echo "   ✅ Generated: $GENERATED"
echo "   ❌ Failed: $FAILED"
echo ""
echo "🎯 Targeted test generation complete!"
