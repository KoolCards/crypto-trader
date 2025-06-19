# Cron Job Setup Guide for fetch_live_price

This guide explains how to set up a cron job to run the fetch_live_price script daily.

## Files Created

1. `run_fetch_price_cron.sh` - Wrapper script for cron execution
2. `logs/cron_fetch_price.log` - Log file for cron output

## Step 1: Verify the Wrapper Script Works

Test the wrapper script manually:
```bash
./run_fetch_price_cron.sh
```

Check the log file:
```bash
cat logs/cron_fetch_price.log
```

## Step 2: Set Up the Cron Job

### Option A: Using crontab (Recommended)

1. Open your crontab for editing:
```bash
crontab -e
```

2. Add one of these lines depending on when you want it to run:

**Daily at 9:00 AM:**
```bash
0 9 * * * /Users/kris/dev/crypto_trader/run_fetch_price_cron.sh
```

**Daily at 12:00 PM (noon):**
```bash
0 12 * * * /Users/kris/dev/crypto_trader/run_fetch_price_cron.sh
```

**Daily at 6:00 PM:**
```bash
0 18 * * * /Users/kris/dev/crypto_trader/run_fetch_price_cron.sh
```

**Multiple times per day (9 AM and 6 PM):**
```bash
0 9,18 * * * /Users/kris/dev/crypto_trader/run_fetch_price_cron.sh
```

**Every hour:**
```bash
0 * * * * /Users/kris/dev/crypto_trader/run_fetch_price_cron.sh
```

### Option B: Using launchd (macOS specific)

Create a plist file for launchd:

1. Create `/Users/kris/Library/LaunchAgents/com.cryptotrader.fetchprice.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cryptotrader.fetchprice</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/kris/dev/crypto_trader/run_fetch_price_cron.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/kris/dev/crypto_trader/logs/launchd_fetch_price.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/kris/dev/crypto_trader/logs/launchd_fetch_price_error.log</string>
</dict>
</plist>
```

2. Load the job:
```bash
launchctl load ~/Library/LaunchAgents/com.cryptotrader.fetchprice.plist
```

## Step 3: Verify the Cron Job

### Check if cron is running:
```bash
sudo launchctl list | grep cron
```

### View your current crontab:
```bash
crontab -l
```

### Check cron logs:
```bash
tail -f logs/cron_fetch_price.log
```

## Step 4: Monitor and Troubleshoot

### Check if the job ran:
```bash
grep "$(date '+%Y-%m-%d')" logs/cron_fetch_price.log
```

### View recent log entries:
```bash
tail -20 logs/cron_fetch_price.log
```

### Test the script manually:
```bash
python3 -m data.live.fetch_live_price
```

## Cron Schedule Format

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday=0)
│ │ │ │ │
* * * * * command
```

## Common Cron Patterns

- `0 9 * * *` - Daily at 9:00 AM
- `0 9,18 * * *` - Daily at 9:00 AM and 6:00 PM
- `0 */6 * * *` - Every 6 hours
- `0 * * * *` - Every hour
- `*/15 * * * *` - Every 15 minutes
- `0 9 * * 1-5` - Weekdays at 9:00 AM

## Troubleshooting

### If the cron job doesn't run:

1. Check if cron is enabled:
```bash
sudo launchctl list | grep cron
```

2. Check system logs:
```bash
sudo log show --predicate 'process == "cron"' --last 1h
```

3. Verify file permissions:
```bash
ls -la run_fetch_price_cron.sh
```

4. Test the script manually:
```bash
./run_fetch_price_cron.sh
```

### If you get import errors:

The wrapper script uses `python3 -m data.live.fetch_live_price` which should work correctly. If you still get import errors, make sure:

1. All `__init__.py` files exist in the data directories
2. You're running from the correct project root
3. Python path is set correctly in the wrapper script

## Security Notes

- The script runs with your user permissions
- Logs are stored in the project directory
- Consider using environment variables for sensitive data
- Regularly check log files for errors

## Maintenance

### Rotate log files:
Add this to your crontab to rotate logs weekly:
```bash
0 8 * * 0 mv /Users/kris/dev/crypto_trader/logs/cron_fetch_price.log /Users/kris/dev/crypto_trader/logs/cron_fetch_price.log.$(date +\%Y\%m\%d)
```

### Monitor disk space:
Check log file sizes:
```bash
du -h logs/cron_fetch_price.log
``` 