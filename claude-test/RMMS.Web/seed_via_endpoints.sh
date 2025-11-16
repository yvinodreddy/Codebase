#!/bin/bash

BASE_URL="https://localhost:7106"
COOKIE_FILE="/tmp/rmms_cookies.txt"

echo "🚀 Seeding data via application endpoints..."
echo ""

# Function to generate API keys
echo "📊 Generating 50 API Keys..."
for i in {1..50}; do
    RATE_LIMIT=$((1000 + RANDOM % 9000))
    IS_ACTIVE=$((RANDOM % 2))
    
    curl -k -s -X POST "$BASE_URL/ApiKeys/GenerateApiKey" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "name=API Key $i" \
        -d "description=Test API key number $i for comprehensive testing" \
        -d "rateLimit=$RATE_LIMIT" \
        -d "permissions=read,write,delete" \
        -d "expiresAt=$(date -d '+1 year' +%Y-%m-%d)" \
        -b "$COOKIE_FILE" -c "$COOKIE_FILE" > /dev/null 2>&1
    
    if [ $((i % 10)) -eq 0 ]; then
        echo "   Generated $i API Keys..."
    fi
done
echo "   ✓ Completed 50 API Keys"
echo ""

# Generate Webhooks
echo "📊 Generating 50 Webhooks..."
EVENTS=("ProductionComplete" "OrderCreated" "OrderUpdated" "LowStock" "PaymentReceived" "ShipmentDispatched" "CustomerCreated" "InventoryUpdate" "BatchComplete" "All")

for i in {1..50}; do
    EVENT_TYPE=${EVENTS[$((RANDOM % 10))]}
    
    curl -k -s -X POST "$BASE_URL/Webhooks/Create" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "Name=Webhook $i" \
        -d "Url=https://api.example.com/webhook$i" \
        -d "EventType=$EVENT_TYPE" \
        -d "Method=POST" \
        -d "Headers={\"Authorization\":\"Bearer token$i\"}" \
        -d "TimeoutSeconds=30" \
        -b "$COOKIE_FILE" -c "$COOKIE_FILE" > /dev/null 2>&1
    
    if [ $((i % 10)) -eq 0 ]; then
        echo "   Generated $i Webhooks..."
    fi
done
echo "   ✓ Completed 50 Webhooks"
echo ""

# Generate Integrations
echo "📊 Generating 50 Integrations..."
TYPES=("ERP" "CRM" "Accounting" "Logistics" "Payment" "Warehouse" "Analytics" "Communication" "Other")

for i in {1..50}; do
    INT_TYPE=${TYPES[$((RANDOM % 9))]}
    
    curl -k -s -X POST "$BASE_URL/Integrations/Create" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "Name=Integration $i" \
        -d "IntegrationType=$INT_TYPE" \
        -d "Description=Test integration $i" \
        -d "Endpoint=https://integration$i.example.com/api" \
        -b "$COOKIE_FILE" -c "$COOKIE_FILE" > /dev/null 2>&1
    
    if [ $((i % 10)) -eq 0 ]; then
        echo "   Generated $i Integrations..."
    fi
done
echo "   ✓ Completed 50 Integrations"
echo ""

echo "============================================================"
echo "✅ SEEDING COMPLETE VIA ENDPOINTS"
echo "============================================================"
echo ""
echo "📊 Summary:"
echo "   • API Keys: 50 generated"
echo "   • Webhooks: 50 generated"
echo "   • Integrations: 50 generated"
echo ""
echo "🎯 Refresh your browser to see the data!"
