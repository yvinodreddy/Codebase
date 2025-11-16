#!/bin/bash
echo "========================================"
echo "QUICK SERVICE VERIFICATION"
echo "========================================"
echo ""

echo "✅ Testing Port 8018 (Phase 18 Application)..."
curl -s -o /dev/null -w "   HTTP Status: %{http_code}\n" http://localhost:8018/api/health
echo ""

echo "========================================"
echo "OPEN IN BROWSER:"
echo "========================================"
echo "Main Dashboard: http://localhost:8018"
echo "API Docs:       http://localhost:8018/docs"
echo "========================================"
