#!/bin/bash

# Cron job wrapper for fetch_live_price script
# This script sets up the proper environment and runs the price fetcher

# Set the project directory
PROJECT_DIR="/Users/kris/dev/crypto_trader"
cd "$PROJECT_DIR"

# Set up Python environment (adjust path if needed)
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Log file for cron output
LOG_FILE="$PROJECT_DIR/logs/cron_fetch_price.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Timestamp for logging
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Starting fetch_live_price cron job" >> "$LOG_FILE"

# Run the script as a module (recommended way)
python3 -m data.live.fetch_live_price >> "$LOG_FILE" 2>&1

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo "[$TIMESTAMP] fetch_live_price completed successfully" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] fetch_live_price failed with exit code $?" >> "$LOG_FILE"
fi

echo "[$TIMESTAMP] Cron job finished" >> "$LOG_FILE"
echo "----------------------------------------" >> "$LOG_FILE" 