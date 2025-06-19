# Cloud Deployment Guide for fetch_live_price

This guide covers multiple cloud service options for running your fetch_live_price script 24/7.

## 🚀 Option 1: GitHub Actions (Recommended - Free)

### Setup:
1. **Push your code to GitHub** (if not already done)
2. **The workflow is already created** in `.github/workflows/fetch_price.yml`
3. **Enable GitHub Actions** in your repository settings

### Features:
- ✅ **Free** for public repositories
- ✅ **2000 minutes/month** for private repos
- ✅ **Automatic scheduling** with cron syntax
- ✅ **Manual triggering** via GitHub UI
- ✅ **Artifact storage** for data files
- ✅ **Email notifications** on failures

### Customization:
- **Change schedule**: Edit the `cron: '0 9 * * *'` line
- **Multiple times per day**: Add more cron entries
- **Timezone**: GitHub Actions runs in UTC

### Example schedules:
```yaml
# Daily at 9 AM UTC
- cron: '0 9 * * *'

# Twice daily (9 AM and 6 PM UTC)
- cron: '0 9,18 * * *'

# Every 6 hours
- cron: '0 */6 * * *'

# Every hour
- cron: '0 * * * *'
```

---

## ☁️ Option 2: AWS Lambda + EventBridge

### Setup:
1. **Create Lambda function** with this code:

```python
import json
import boto3
import requests
from datetime import datetime, date
import pandas as pd
import io

def lambda_handler(event, context):
    # Fetch price
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    price = data['ethereum']['usd']
    
    # Store in S3
    s3 = boto3.client('s3')
    bucket_name = 'your-crypto-data-bucket'
    
    # Create CSV data
    csv_data = f"{date.today()},{price},{datetime.now().isoformat()}\n"
    
    # Append to existing file or create new
    try:
        existing_data = s3.get_object(Bucket=bucket_name, Key='ethereum_prices.csv')['Body'].read().decode()
        csv_data = existing_data + csv_data
    except:
        csv_data = "date,price,timestamp\n" + csv_data
    
    s3.put_object(Bucket=bucket_name, Key='ethereum_prices.csv', Body=csv_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Price: ${price:,.2f}')
    }
```

2. **Create S3 bucket** for data storage
3. **Set up EventBridge rule** for scheduling
4. **Configure IAM permissions**

### Cost: ~$1-5/month

---

## 🔧 Option 3: Google Cloud Functions + Cloud Scheduler

### Setup:
1. **Deploy function** to Google Cloud Functions
2. **Create Cloud Scheduler job**
3. **Set up Cloud Storage** for data

### Cost: ~$1-3/month

---

## 🐳 Option 4: Docker + Cloud Run (Google Cloud)

### Create Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "data.live.fetch_live_price"]
```

### Deploy to Cloud Run with cron:
```bash
gcloud run deploy fetch-price --source . --platform managed
gcloud scheduler jobs create http fetch-price-job \
  --schedule="0 9 * * *" \
  --uri="YOUR_CLOUD_RUN_URL" \
  --http-method=POST
```

---

## 📊 Option 5: Heroku Scheduler (Simplest)

### Setup:
1. **Deploy to Heroku**:
```bash
heroku create your-crypto-app
git push heroku main
```

2. **Add scheduler addon**:
```bash
heroku addons:create scheduler:standard
```

3. **Configure in Heroku dashboard**:
   - Command: `python -m data.live.fetch_live_price`
   - Frequency: Daily at 9:00 AM

### Cost: Free tier available

---

## 🔄 Data Synchronization

### Option A: Git-based (GitHub Actions)
- Data is committed back to your repository
- Easy to track changes and history
- Free storage

### Option B: Cloud Storage (AWS S3, Google Cloud Storage)
- Scalable and reliable
- Can store large amounts of data
- Cost-effective

### Option C: Database (MongoDB Atlas, PostgreSQL)
- Better for querying and analysis
- More structured data storage
- Can integrate with other tools

---

## 📈 Monitoring & Alerts

### GitHub Actions:
- Built-in notifications
- Action logs in GitHub UI
- Email alerts on failures

### AWS Lambda:
- CloudWatch logs
- SNS notifications
- Custom dashboards

### Google Cloud:
- Cloud Logging
- Error reporting
- Monitoring dashboards

---

## 🛡️ Security Considerations

### API Keys:
- Store sensitive data in environment variables
- Use cloud secret management services
- Never commit secrets to git

### Data Privacy:
- Consider data retention policies
- Encrypt sensitive data
- Regular security audits

---

## 💰 Cost Comparison

| Service | Free Tier | Paid Tier | Best For |
|---------|-----------|-----------|----------|
| GitHub Actions | ✅ 2000 min/month | $0.008/min | Small projects, open source |
| AWS Lambda | ✅ 1M requests/month | $0.20/1M requests | Enterprise, AWS ecosystem |
| Google Cloud Functions | ✅ 2M requests/month | $0.40/1M requests | Google ecosystem |
| Heroku Scheduler | ✅ 550 hours/month | $25/month | Simple deployments |
| Cloud Run | ✅ 2M requests/month | $0.40/1M requests | Containerized apps |

---

## 🚀 Quick Start: GitHub Actions

1. **Push your code to GitHub**
2. **Go to Actions tab** in your repository
3. **Enable the workflow** if prompted
4. **Test manually** by clicking "Run workflow"
5. **Monitor execution** in the Actions tab

The workflow will automatically:
- Run daily at 9 AM UTC
- Install dependencies
- Execute your script
- Store data as artifacts
- Commit data back to your repo

---

## 🔧 Troubleshooting

### Common Issues:
1. **Import errors**: Make sure all `__init__.py` files exist
2. **Dependency issues**: Check `requirements.txt` is complete
3. **Permission errors**: Verify file paths and permissions
4. **API rate limits**: Add delays between requests if needed

### Debugging:
- Check action logs in GitHub
- Test locally first
- Use `workflow_dispatch` for manual testing 