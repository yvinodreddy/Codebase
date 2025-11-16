#!/bin/bash
echo "========================================"
echo "QUICK SERVICE VERIFICATION"
echo "========================================"
echo ""

echo "✅ Testing Port 8023 (Phase 23 Application)..."
curl -s -o /dev/null -w "   HTTP Status: %{http_code}\n" http://localhost:8023/api/health
echo ""

echo "========================================"
echo "OPEN IN BROWSER:"
echo "========================================"
echo "Main Dashboard: http://localhost:8023"
echo "API Docs:       http://localhost:8023/docs"
echo "========================================"
