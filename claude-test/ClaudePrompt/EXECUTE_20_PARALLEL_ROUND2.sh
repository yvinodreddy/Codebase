#!/bin/bash
set -euo pipefail

echo "🚀 STARTING ROUND 2: 20 PARALLEL TASKS FOR 99% COVERAGE"
echo "=================================================="
echo ""

# Setup
LOG_DIR="/tmp/round2_parallel_logs"
mkdir -p "$LOG_DIR"
mkdir -p tests/unit_real_coverage

# Split into 20 batches
TOTAL_FILES=$(wc -l < /tmp/low_coverage_files_round2.txt)
BATCH_SIZE=$(( (TOTAL_FILES + 19) / 20 ))

echo "📊 Total files: $TOTAL_FILES"
echo "📦 Batch size: $BATCH_SIZE files per task"
echo "⚡ Parallel tasks: 20"
echo ""

# Split files into batches
cat /tmp/low_coverage_files_round2.txt | split -l $BATCH_SIZE - "$LOG_DIR/batch_"

# Launch 20 parallel tasks
TASK_ID=0
PIDS=()

for batch_file in "$LOG_DIR"/batch_*; do
    TASK_ID=$((TASK_ID + 1))
    TASK_LOG="$LOG_DIR/task_${TASK_ID}.log"

    (
        echo "[TASK $TASK_ID] Started at $(date)" > "$TASK_LOG"
        echo "[TASK $TASK_ID] Processing batch: $batch_file" >> "$TASK_LOG"

        # Process each file in this batch
        while IFS= read -r source_file; do
            filename=$(basename "$source_file" .py)
            test_file="tests/unit_real_coverage/test_${filename}_real.py"

            # Skip if test already exists
            if [ -f "$test_file" ]; then
                echo "[TASK $TASK_ID] ⏭️  Skipped (exists): $test_file" >> "$TASK_LOG"
                continue
            fi

            echo "[TASK $TASK_ID] Generating test for: $source_file" >> "$TASK_LOG"

            # Generate test
            if python3 generate_real_coverage_tests.py "$source_file" "$test_file" >> "$TASK_LOG" 2>&1; then
                echo "[TASK $TASK_ID] ✅ Generated: $test_file" >> "$TASK_LOG"
            else
                echo "[TASK $TASK_ID] ❌ Failed: $source_file" >> "$TASK_LOG"
            fi
        done < "$batch_file"

        echo "[TASK $TASK_ID] Finished at $(date)" >> "$TASK_LOG"
    ) &

    PIDS+=($!)
    echo "✅ Launched task $TASK_ID (PID: ${PIDS[$((TASK_ID-1))]})"
done

echo ""
echo "⏳ Waiting for all 20 tasks to complete..."
echo ""

# Wait for all tasks
for i in "${!PIDS[@]}"; do
    wait "${PIDS[$i]}"
    echo "✅ Task $((i+1)) completed"
done

echo ""
echo "=================================================="
echo "✅ ALL 20 TASKS COMPLETED"
echo ""

# Summary
TOTAL_GENERATED=$(find tests/unit_real_coverage -name "test_*_real.py" | wc -l)
echo "📊 SUMMARY:"
echo "   Total test files now: $TOTAL_GENERATED"
echo "   Logs: $LOG_DIR/task_*.log"
echo ""
echo "🎯 Next: Run pytest to measure new coverage!"
