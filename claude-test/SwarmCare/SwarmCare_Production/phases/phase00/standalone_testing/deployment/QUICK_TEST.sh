#!/bin/bash
echo "========================================"
echo "QUICK SERVICE VERIFICATION"
echo "========================================"
echo ""

echo "✅ Testing Port 8000 (FastAPI Dashboard)..."
curl -s -o /dev/null -w "   HTTP Status: %{http_code}\n" http://localhost:8000/api/health
echo ""

echo "✅ Testing Port 7474 (Neo4j Browser)..."
curl -s -o /dev/null -w "   HTTP Status: %{http_code}\n" http://localhost:7474
echo ""

echo "✅ Testing Port 6379 (Redis - via Docker)..."
echo -n "   Response: "
docker exec swarmcare-redis redis-cli ping 2>/dev/null
echo ""

echo "✅ Testing All API Endpoints..."
curl -s http://localhost:8000/api/services/status | python3 -m json.tool
echo ""

echo "========================================"
echo "OPEN IN BROWSER:"
echo "========================================"
echo "Main Dashboard: http://localhost:8000"
echo "API Docs:       http://localhost:8000/docs"
echo "Neo4j Browser:  http://localhost:7474"
echo ""
echo "Note: Redis (port 6379) is NOT accessible"
echo "in browser - this is NORMAL and CORRECT!"
echo "========================================"
