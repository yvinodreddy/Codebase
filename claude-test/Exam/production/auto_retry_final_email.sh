#!/bin/bash

# Auto-retry script for final email to Romika Chauhan
# Will retry every 15 minutes until successful

LOG_FILE="auto_retry_log.txt"
RETRY_INTERVAL=900  # 15 minutes in seconds
MAX_ATTEMPTS=100    # Maximum attempts (25 hours worth)

echo "========================================" | tee -a "$LOG_FILE"
echo "AUTO-RETRY SCRIPT STARTED" | tee -a "$LOG_FILE"
echo "Started at: $(date)" | tee -a "$LOG_FILE"
echo "Target: Romika Chauhan (romi.chauhan2275@gmail.com)" | tee -a "$LOG_FILE"
echo "Retry interval: 15 minutes" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

attempt=1

while [ $attempt -le $MAX_ATTEMPTS ]; do
    echo "[$(date)] Attempt #$attempt - Trying to send final email..." | tee -a "$LOG_FILE"

    # Run the email script
    output=$(echo "yes" | python3 send_with_company_email.py --send-all 2>&1)

    # Check if it was successful
    if echo "$output" | grep -q "✅ Successfully sent: 1"; then
        echo "" | tee -a "$LOG_FILE"
        echo "========================================" | tee -a "$LOG_FILE"
        echo "🎉 SUCCESS! Final email sent!" | tee -a "$LOG_FILE"
        echo "Completed at: $(date)" | tee -a "$LOG_FILE"
        echo "Total attempts: $attempt" | tee -a "$LOG_FILE"
        echo "========================================" | tee -a "$LOG_FILE"

        # Save the successful output
        echo "$output" > final_email_success.log

        # Create a completion marker file
        echo "Campaign completed successfully at $(date)" > CAMPAIGN_COMPLETE.txt
        echo "All 55/55 candidates have received the technical assessment invitation." >> CAMPAIGN_COMPLETE.txt

        echo "" | tee -a "$LOG_FILE"
        echo "✅ ALL 55/55 CANDIDATES HAVE NOW RECEIVED THE EMAIL!" | tee -a "$LOG_FILE"
        echo "" | tee -a "$LOG_FILE"

        exit 0
    fi

    # Check if still rate limited
    if echo "$output" | grep -q "Ratelimit.*exceeded"; then
        echo "[$(date)] ⚠️  Still rate limited. Will retry in 15 minutes..." | tee -a "$LOG_FILE"
    else
        # Some other error occurred
        echo "[$(date)] ❌ Unexpected error occurred:" | tee -a "$LOG_FILE"
        echo "$output" | tail -5 | tee -a "$LOG_FILE"
        echo "[$(date)] Will retry in 15 minutes..." | tee -a "$LOG_FILE"
    fi

    echo "" | tee -a "$LOG_FILE"

    # Don't sleep on the last attempt
    if [ $attempt -lt $MAX_ATTEMPTS ]; then
        sleep $RETRY_INTERVAL
    fi

    ((attempt++))
done

echo "[$(date)] ❌ Maximum attempts reached without success." | tee -a "$LOG_FILE"
echo "Please check manually or contact support." | tee -a "$LOG_FILE"
exit 1
