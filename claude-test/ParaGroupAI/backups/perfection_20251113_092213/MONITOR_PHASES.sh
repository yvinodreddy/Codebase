#!/bin/bash
################################################################################
# MONITOR ALL PHASES - Real-Time Status Display
################################################################################

clear
echo "================================================================================"
echo "📊 PARALLEL IMPLEMENTATION - LIVE MONITOR"
echo "================================================================================"
echo "Monitoring all 6 phases..."
echo "Press Ctrl+C to exit"
echo "================================================================================"
echo ""

while true; do
    # Clear previous output (keep header)
    tput cup 7 0
    tput ed

    for i in {1..6}; do
        logfile="parallel_implementation/logs/phase${i}.log"
        pidfile="parallel_implementation/pids/phase${i}.pid"

        # Phase name
        case $i in
            1) phase_name="Real-Time Logging";;
            2) phase_name="Streaming Reader";;
            3) phase_name="Guardrails Fixes";;
            4) phase_name="Dashboard Fixes";;
            5) phase_name="WebSocket Enhancement";;
            6) phase_name="Testing";;
        esac

        echo "Phase $i: $phase_name"

        # Check if running
        if [ -f "$pidfile" ]; then
            pid=$(cat "$pidfile")
            if ps -p $pid > /dev/null 2>&1; then
                echo "  Status: 🔄 RUNNING (PID: $pid)"
            else
                echo "  Status: ⏹  STOPPED"
            fi
        else
            echo "  Status: ⏸  NOT STARTED"
        fi

        # Check log for completion
        if [ -f "$logfile" ]; then
            if grep -q "SUCCESS ✅" "$logfile"; then
                echo "  Result: ✅ COMPLETED"
            elif grep -q "FAILED" "$logfile"; then
                echo "  Result: ❌ FAILED"
            else
                echo "  Result: ⏳ IN PROGRESS"
            fi

            # Show last log line
            last_line=$(tail -1 "$logfile" 2>/dev/null)
            if [ -n "$last_line" ]; then
                echo "  Latest: ${last_line:0:70}..."
            fi
        else
            echo "  Result: ⏸  NO LOG YET"
        fi

        echo ""
    done

    echo "================================================================================"
    echo "Updated: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Refreshing every 5 seconds..."

    sleep 5
done
