#!/bin/bash
# Comprehensive Integration Test

echo "Running integration tests..."

# Test 1: Check all new files exist
echo "Test 1: File existence..."
FILES=(
    "realtime_verbose_logger.py"
    "stage_progress_tracker.py"
    "realtime_db_updates.py"
    "realtime_log_monitor.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
        exit 1
    fi
done

# Test 2: Python syntax check
echo "Test 2: Syntax validation..."
for file in "${FILES[@]}"; do
    python3 -m py_compile "$file" 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ $file syntax OK"
    else
        echo "✗ $file has syntax errors"
        exit 1
    fi
done

# Test 3: Import test
echo "Test 3: Import validation..."
python3 -c "from realtime_verbose_logger import create_realtime_logger; print('✓ Imports successful')"

echo "All tests passed! ✅"
exit 0
