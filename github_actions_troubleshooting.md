# GitHub Actions Troubleshooting Guide

## 🔐 Permission Issues

### Problem: "Write access to repository is not granted"

**Solution 1: Use the updated workflow (Recommended)**
The workflow has been updated with proper permissions:
```yaml
permissions:
  contents: write  # Allow writing to repository
  actions: read    # Allow reading actions
```

**Solution 2: Check repository settings**
1. Go to your repository on GitHub
2. Click **Settings** → **Actions** → **General**
3. Under "Workflow permissions", select:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**

**Solution 3: Use Personal Access Token (if needed)**
1. Create a Personal Access Token:
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token (classic)
   - Select `repo` scope
2. Add to repository secrets:
   - Go to repository → Settings → Secrets and variables → Actions
   - Add new secret: `PAT` with your token value
3. Update workflow to use PAT:
```yaml
- name: Checkout code
  uses: actions/checkout@v4
  with:
    token: ${{ secrets.PAT }}
```

---

## 🚀 Common Issues & Solutions

### Issue 1: Import errors in GitHub Actions
**Error**: `ModuleNotFoundError: No module named 'data'`

**Solution**: The workflow uses `python -m data.live.fetch_live_price` which should work. If you still get errors:
1. Ensure all `__init__.py` files exist
2. Check that the project structure is correct
3. Verify `requirements.txt` includes all dependencies

### Issue 2: Workflow not running on schedule
**Problem**: Scheduled workflow doesn't execute

**Solutions**:
1. **Check timezone**: GitHub Actions runs in UTC
   - Your cron: `0 20 * * *` = 8:00 PM UTC
   - Convert to your local timezone
2. **Verify cron syntax**: Use [crontab.guru](https://crontab.guru) to validate
3. **Check repository activity**: GitHub may pause workflows on inactive repos

### Issue 3: Data not being committed
**Problem**: Workflow runs but data isn't saved to repository

**Solutions**:
1. Check if the Parquet file is being created
2. Verify the file path matches the workflow
3. Check the commit step in the logs

---

## 🔧 Debugging Steps

### Step 1: Test locally first
```bash
# Test the script locally
python3 -m data.live.fetch_live_price

# Check if data file is created
ls -la data/ethereum_price.parquet
```

### Step 2: Check workflow logs
1. Go to your repository → Actions tab
2. Click on the failed workflow run
3. Check each step's logs for errors

### Step 3: Test workflow manually
1. Go to Actions tab
2. Click "Fetch Ethereum Price" workflow
3. Click "Run workflow" button
4. Monitor the execution

### Step 4: Verify file paths
The workflow expects:
- Data file: `data/ethereum_price.parquet`
- Logs: `logs/` directory

---

## 📋 Workflow Configuration

### Current Schedule
```yaml
schedule:
  - cron: '0 20 * * *'  # Daily at 8:00 PM UTC
```

### Common Schedule Options
```yaml
# Daily at 9 AM UTC
- cron: '0 9 * * *'

# Twice daily (9 AM and 6 PM UTC)
- cron: '0 9,18 * * *'

# Every 6 hours
- cron: '0 */6 * * *'

# Every hour
- cron: '0 * * * *'

# Weekdays only at 9 AM UTC
- cron: '0 9 * * 1-5'
```

---

## 🛠️ Manual Testing

### Test the workflow manually:
1. Go to your GitHub repository
2. Click **Actions** tab
3. Click **Fetch Ethereum Price** workflow
4. Click **Run workflow** button
5. Select branch (usually `main`)
6. Click **Run workflow**

### Expected behavior:
1. ✅ Workflow starts
2. ✅ Python environment is set up
3. ✅ Dependencies are installed
4. ✅ Script runs and fetches price
5. ✅ Data file is created
6. ✅ Data is committed to repository
7. ✅ Artifacts are uploaded

---

## 📊 Monitoring

### Check if workflow ran today:
```bash
# Look for today's date in the repository
git log --oneline --since="1 day ago" | grep "Update Ethereum price data"
```

### View recent commits:
```bash
git log --oneline -10
```

### Check data file:
```bash
ls -la data/ethereum_price.parquet
```

---

## 🚨 Emergency Fixes

### If workflow is completely broken:
1. **Disable the commit step temporarily**:
   Comment out the "Commit and push data" step in the workflow
2. **Run manually** to test the script
3. **Fix issues** and re-enable the commit step

### If you need to reset:
1. Delete the workflow file
2. Re-create it with the corrected version
3. Push the changes
4. Re-enable GitHub Actions

---

## 📞 Getting Help

### GitHub Actions Documentation:
- [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Permissions](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
- [Scheduled events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)

### Debugging Resources:
- [GitHub Actions debugging](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows)
- [Workflow logs](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/using-workflow-run-logs) 