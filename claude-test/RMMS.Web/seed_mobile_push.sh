#!/bin/bash

BASE_URL="https://localhost:7106"

echo "🚀 Seeding Mobile & Push Notification data..."
echo ""

# Generate Push Notifications
echo "📊 Sending 100 Push Notifications..."
TARGETS=("All Devices" "Android Only" "iOS Only" "Push Enabled Only")
TITLES=("Production Complete" "Order Confirmed" "Low Stock Alert" "Payment Received" "Shipment Dispatched" "New Message" "System Update" "Inventory Alert" "Batch Complete" "General Notification")

for i in {1..100}; do
    TARGET=${TARGETS[$((RANDOM % 4))]}
    TITLE=${TITLES[$((RANDOM % 10))]}
    
    curl -k -s -X POST "$BASE_URL/PushNotifications/SendNew" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "title=$TITLE $i" \
        -d "body=Notification message body for test #$i - Important update from RMMS system" \
        -d "target=$TARGET" \
        -d "customData={\"id\":$i,\"type\":\"test\",\"priority\":\"normal\"}" \
        > /dev/null 2>&1
    
    if [ $((i % 20)) -eq 0 ]; then
        echo "   Sent $i Push Notifications..."
    fi
    
    # Small delay to avoid overwhelming the system
    sleep 0.05
done
echo "   ✓ Completed 100 Push Notifications"
echo ""

# Simulate connections for SignalR
echo "📊 Simulating 20 SignalR connections..."
for i in {1..20}; do
    curl -k -s -X POST "$BASE_URL/SignalRConsole/SimulateConnection" > /dev/null 2>&1
    sleep 0.05
done
echo "   ✓ Simulated 20 connections"
echo ""

# Send broadcast messages
echo "📊 Sending 30 SignalR broadcast messages..."
MESSAGES=(
    "System maintenance scheduled for tonight"
    "New production batch started"
    "Order processing complete"
    "Inventory levels updated"
    "Sales report generated"
    "Payment confirmation received"
    "Shipment tracking updated"
    "Customer notification sent"
    "Analytics data refreshed"
    "Dashboard metrics updated"
)

for i in {1..30}; do
    MSG="${MESSAGES[$((RANDOM % 10))]} - Message #$i"
    
    curl -k -s -X POST "$BASE_URL/SignalRConsole/BroadcastMessage" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "message=$MSG" \
        > /dev/null 2>&1
    
    if [ $((i % 10)) -eq 0 ]; then
        echo "   Sent $i broadcast messages..."
    fi
    
    sleep 0.05
done
echo "   ✓ Completed 30 broadcast messages"
echo ""

# Record realtime metrics
echo "📊 Recording 50 realtime metrics..."
for i in {1..50}; do
    METRIC_TYPE=$((RANDOM % 5))
    VALUE=$((50 + RANDOM % 450))
    TYPE_NAME="Metric Type $METRIC_TYPE"
    
    curl -k -s -X POST "$BASE_URL/RealtimeMonitoring/RecordMetric" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "metricType=$TYPE_NAME" \
        -d "value=$VALUE" \
        > /dev/null 2>&1
    
    if [ $((i % 10)) -eq 0 ]; then
        echo "   Recorded $i metrics..."
    fi
    
    sleep 0.05
done
echo "   ✓ Completed 50 realtime metrics"
echo ""

echo "============================================================"
echo "✅ MOBILE & MONITORING DATA SEEDING COMPLETE"
echo "============================================================"
echo ""
echo "📊 Summary:"
echo "   • Push Notifications: 100 sent"
echo "   • SignalR Connections: 20 simulated"
echo "   • SignalR Messages: 30 broadcast"
echo "   • Realtime Metrics: 50 recorded"
echo ""
echo "🎯 All Phase 4 pages now have comprehensive test data!"
