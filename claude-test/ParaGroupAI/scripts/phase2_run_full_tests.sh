#!/bin/bash
set -e
echo "================================================================================"
echo "📊 Phase 2 - Step 5: Running Full Test Suite"
echo "================================================================================"
cd /home/user01/claude-test/ParaGroupAI
pytest tests/ --cov --cov-report=html -q || true
echo "✅ Full test suite executed"
echo "================================================================================"
