#!/bin/bash
# Advanced Load Testing Execution Script

set -e

echo "================================================================================"
echo "🚀 ULTRATHINK LOAD TESTING SUITE"
echo "================================================================================"
echo ""

# Check if Locust is installed
if ! command -v locust &> /dev/null; then
    echo "📦 Installing Locust..."
    pip3 install locust -q
fi

BASE_URL="${1:-http://localhost:8000}"
echo "Target URL: $BASE_URL"
echo ""

# Test 1: Baseline Performance (10 users, 60 seconds)
echo "---"
echo "TEST 1: Baseline Performance"
echo "Users: 10 | Duration: 60s"
echo "---"
locust -f locustfile.py \
    --host="$BASE_URL" \
    --users=10 \
    --spawn-rate=2 \
    --run-time=60s \
    --headless \
    --html=baseline_report.html \
    --csv=baseline

echo ""

# Test 2: Sustained Load (50 users, 120 seconds)
echo "---"
echo "TEST 2: Sustained Load"
echo "Users: 50 | Duration: 120s"
echo "---"
locust -f locustfile.py \
    --host="$BASE_URL" \
    --users=50 \
    --spawn-rate=5 \
    --run-time=120s \
    --headless \
    --html=sustained_report.html \
    --csv=sustained

echo ""

# Test 3: Spike Test (100 users ramping quickly)
echo "---"
echo "TEST 3: Spike Traffic"
echo "Users: 100 | Duration: 60s | Spawn Rate: 20/s"
echo "---"
locust -f locustfile.py \
    --host="$BASE_URL" \
    --users=100 \
    --spawn-rate=20 \
    --run-time=60s \
    --headless \
    --html=spike_report.html \
    --csv=spike

echo ""

# Test 4: Stress Test (find breaking point)
echo "---"
echo "TEST 4: Stress Test"
echo "Users: 200 | Duration: 180s"
echo "---"
locust -f locustfile.py \
    --host="$BASE_URL" \
    --users=200 \
    --spawn-rate=10 \
    --run-time=180s \
    --headless \
    --html=stress_report.html \
    --csv=stress

echo ""
echo "================================================================================"
echo "✅ LOAD TESTING COMPLETE"
echo "================================================================================"
echo ""
echo "Reports generated:"
echo "  - baseline_report.html (10 users)"
echo "  - sustained_report.html (50 users)"
echo "  - spike_report.html (100 users, spike pattern)"
echo "  - stress_report.html (200 users, stress test)"
echo ""
