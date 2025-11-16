#!/bin/bash
echo "========================================"
echo "QUICK SERVICE VERIFICATION"
echo "========================================"
echo ""

echo "✅ Testing Port 8019 (Phase 19 Application)..."
curl -s -o /dev/null -w "   HTTP Status: %{http_code}\n" http://localhost:8019/api/health
echo ""

echo "========================================"
echo "OPEN IN BROWSER:"
echo "========================================"
echo "Main Dashboard: http://localhost:8019"
echo "API Docs:       http://localhost:8019/docs"
echo "========================================"
