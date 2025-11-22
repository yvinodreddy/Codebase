#!/bin/bash

echo "======================================================================"
echo "🔍 RUNNING COVERAGE ANALYSIS FOR 16 TARGET MODULES"
echo "======================================================================"

# Run pytest with coverage for specific modules
pytest tests/unit_instance3/ \
    --cov=fix_test_files_complete \
    --cov=generate_100_percent_tests \
    --cov=generate_effective_tests \
    --cov=generate_real_coverage_tests \
    --cov=generate_real_test_fixed \
    --cov=generate_real_test_implementations \
    --cov=generate_real_tests_for_module \
    --cov=get_coverage_quickly \
    --cov=get_live_context_metrics \
    --cov=high_scale_orchestrator \
    --cov=instance_id_manager \
    --cov=large_scale_error_handler \
    --cov=live_metrics_tracker \
    --cov=master_orchestrator \
    --cov=metrics_aggregator \
    --cov=metrics_state_persistence \
    --cov-report=term \
    --cov-report=html \
    --tb=short \
    -q 2>&1 | tee coverage_report.txt

echo ""
echo "======================================================================"
echo "📊 COVERAGE SUMMARY"
echo "======================================================================"

# Extract and display the coverage summary
grep -E "^(fix_test_files_complete|generate_100_percent_tests|generate_effective_tests|generate_real_coverage_tests|generate_real_test_fixed|generate_real_test_implementations|generate_real_tests_for_module|get_coverage_quickly|get_live_context_metrics|high_scale_orchestrator|instance_id_manager|large_scale_error_handler|live_metrics_tracker|master_orchestrator|metrics_aggregator|metrics_state_persistence|TOTAL)" coverage_report.txt

echo ""
echo "📁 HTML report available at: htmlcov/index.html"
echo "======================================================================"