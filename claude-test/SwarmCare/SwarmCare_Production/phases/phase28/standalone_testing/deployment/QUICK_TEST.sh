#!/bin/bash
echo "========================================"
echo "QUICK SERVICE VERIFICATION"
echo "========================================"
echo ""

echo "✅ Testing Port 8028 (Phase 28 Application)..."
curl -s -o /dev/null -w "   HTTP Status: %{http_code}\n" http://localhost:8028/api/health
echo ""

echo "========================================"
echo "OPEN IN BROWSER:"
echo "========================================"
echo "Main Dashboard: http://localhost:8028"
echo "API Docs:       http://localhost:8028/docs"
echo "========================================"
