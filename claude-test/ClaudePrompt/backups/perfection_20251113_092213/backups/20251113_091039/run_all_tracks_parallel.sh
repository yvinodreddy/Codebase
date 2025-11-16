#!/usr/bin/env bash
#
# Run all 5 tracks in parallel for ULTRATHINK implementation
#
# This script launches 5 separate cpp executions simultaneously,
# each with its own timestamped output file.
#
# Usage:
#   ./run_all_tracks_parallel.sh
#

set -e  # Exit on error

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "=============================================================================="
echo "🚀 LAUNCHING ALL 5 TRACKS IN PARALLEL"
echo "=============================================================================="
echo "📁 Output directory: $SCRIPT_DIR/tmp/"
echo "⏱️  Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================================================================="
echo ""

# Track 1: Testing Infrastructure
TRACK1_PROMPT="Implement TRACK 1: Testing Infrastructure. Complete unit tests, bring coverage to 90%+, implement CI/CD pipeline with GitHub Actions, write integration tests. ZERO BREAKING CHANGES."

# Track 2: Quality & Code Analysis
TRACK2_PROMPT="Implement TRACK 2: Quality & Code Analysis. Setup black, pylint, mypy, isort. Code review automation, static type checking, complexity analysis, dependency management, quality metrics dashboard. ZERO BREAKING CHANGES."

# Track 3: Security & Validation
TRACK3_PROMPT="Implement TRACK 3: Security & Validation. Strengthen input sanitizer, bandit + safety automation, rate limiting with circuit breaker, security headers (CORS, CSP, HSTS), E2E test framework. ZERO BREAKING CHANGES."

# Track 4: Infrastructure & Caching
TRACK4_PROMPT="Implement TRACK 4: Infrastructure & Caching. diskcache response caching <50ms, keyring secrets management, structlog JSON logging, cProfile performance profiling, Prometheus metrics collection. ZERO BREAKING CHANGES."

# Track 5: Documentation & Deployment
TRACK5_PROMPT="Implement TRACK 5: Documentation & Deployment. setup.py for PyPI packaging, /health and /metrics endpoints, Sphinx documentation framework. ZERO BREAKING CHANGES."

# Launch all tracks in background
echo "🔥 Launching Track 1..."
"$SCRIPT_DIR/run_track.sh" 1 "$TRACK1_PROMPT" &
PID1=$!

echo "🔥 Launching Track 2..."
"$SCRIPT_DIR/run_track.sh" 2 "$TRACK2_PROMPT" &
PID2=$!

echo "🔥 Launching Track 3..."
"$SCRIPT_DIR/run_track.sh" 3 "$TRACK3_PROMPT" &
PID3=$!

echo "🔥 Launching Track 4..."
"$SCRIPT_DIR/run_track.sh" 4 "$TRACK4_PROMPT" &
PID4=$!

echo "🔥 Launching Track 5..."
"$SCRIPT_DIR/run_track.sh" 5 "$TRACK5_PROMPT" &
PID5=$!

echo ""
echo "=============================================================================="
echo "✅ ALL 5 TRACKS LAUNCHED"
echo "=============================================================================="
echo "Track 1 PID: $PID1"
echo "Track 2 PID: $PID2"
echo "Track 3 PID: $PID3"
echo "Track 4 PID: $PID4"
echo "Track 5 PID: $PID5"
echo ""
echo "⏳ Waiting for all tracks to complete..."
echo "=============================================================================="
echo ""

# Wait for all background jobs
wait $PID1
echo "✅ Track 1 completed"

wait $PID2
echo "✅ Track 2 completed"

wait $PID3
echo "✅ Track 3 completed"

wait $PID4
echo "✅ Track 4 completed"

wait $PID5
echo "✅ Track 5 completed"

echo ""
echo "=============================================================================="
echo "🎉 ALL 5 TRACKS COMPLETED SUCCESSFULLY"
echo "=============================================================================="
echo "📁 Output files location: $SCRIPT_DIR/tmp/"
echo "⏱️  Completed: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "📖 View outputs:"
echo "   ls -lh $SCRIPT_DIR/tmp/"
echo ""
echo "📊 Track-specific outputs:"
echo "   Track 1: ls $SCRIPT_DIR/tmp/*track1*.txt"
echo "   Track 2: ls $SCRIPT_DIR/tmp/*track2*.txt"
echo "   Track 3: ls $SCRIPT_DIR/tmp/*track3*.txt"
echo "   Track 4: ls $SCRIPT_DIR/tmp/*track4*.txt"
echo "   Track 5: ls $SCRIPT_DIR/tmp/*track5*.txt"
echo "=============================================================================="
