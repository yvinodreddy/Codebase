#!/bin/bash

# Auto-retry script for email campaign
# Retries sending emails every 15 minutes until all are sent successfully
# Uses relative paths - can be run from any location

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

LOG_FILE="logs/auto_retry.log"
RETRY_INTERVAL=900  # 15 minutes in seconds
MAX_ATTEMPTS=100    # Maximum attempts (25 hours worth)

echo "========================================" | tee -a "$LOG_FILE"
echo "AUTO-RETRY CAMPAIGN SCRIPT STARTED" | tee -a "$LOG_FILE"
echo "Started at: $(date)" | tee -a "$LOG_FILE"
echo "Retry interval: 15 minutes" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

attempt=1

while [ $attempt -le $MAX_ATTEMPTS ]; do
    echo "[$(date)] Attempt #$attempt - Running campaign..." | tee -a "$LOG_FILE"

    # Run the campaign script
    output=$(echo "yes" | python3 send_campaign.py --send-all 2>&1)

    # Check if campaign completed successfully
    if echo "$output" | grep -q "✅ Successfully sent:"; then
        sent_count=$(echo "$output" | grep "✅ Successfully sent:" | grep -o '[0-9]*' | head -1)
        failed_count=$(echo "$output" | grep "❌ Failed:" | grep -o '[0-9]*' | head -1)

        echo "[$(date)] Campaign completed: $sent_count sent, $failed_count failed" | tee -a "$LOG_FILE"

        if [ "$failed_count" = "0" ]; then
            echo "" | tee -a "$LOG_FILE"
            echo "========================================" | tee -a "$LOG_FILE"
            echo "🎉 SUCCESS! All emails sent!" | tee -a "$LOG_FILE"
            echo "Completed at: $(date)" | tee -a "$LOG_FILE"
            echo "Total attempts: $attempt" | tee -a "$LOG_FILE"
            echo "========================================" | tee -a "$LOG_FILE"

            # Create completion marker
            echo "Campaign completed successfully at $(date)" > logs/campaign_complete.txt
            echo "All candidates have received emails." >> logs/campaign_complete.txt

            exit 0
        fi
    fi

    # Check for pending emails
    if echo "$output" | grep -q "📤 Pending to send: 0"; then
        echo "" | tee -a "$LOG_FILE"
        echo "========================================" | tee -a "$LOG_FILE"
        echo "✅ All emails already sent!" | tee -a "$LOG_FILE"
        echo "========================================" | tee -a "$LOG_FILE"
        exit 0
    fi

    # Check if rate limited
    if echo "$output" | grep -q "Ratelimit.*exceeded"; then
        echo "[$(date)] ⚠️  Rate limited. Will retry in 15 minutes..." | tee -a "$LOG_FILE"
    else
        echo "[$(date)] Campaign incomplete. Will retry in 15 minutes..." | tee -a "$LOG_FILE"
    fi

    echo "" | tee -a "$LOG_FILE"

    # Don't sleep on the last attempt
    if [ $attempt -lt $MAX_ATTEMPTS ]; then
        sleep $RETRY_INTERVAL
    fi

    ((attempt++))
done

echo "[$(date)] ❌ Maximum attempts reached without complete success." | tee -a "$LOG_FILE"
echo "Please check logs and retry manually." | tee -a "$LOG_FILE"
exit 1
