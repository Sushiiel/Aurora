# 📘 n8n Configuration Guide for AURORA

## What is n8n?

n8n is a free, open-source workflow automation tool that AURORA uses for:
- Event-driven alerts
- Automated notifications
- Integration with external services
- Scheduled monitoring tasks

## Installation Options

### Option 1: Docker (Recommended)

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Option 2: NPM

```bash
npm install -g n8n
n8n start
```

### Option 3: Docker Compose (Integrated)

Add to your `docker-compose.yml`:

```yaml
n8n:
  image: n8nio/n8n
  ports:
    - "5678:5678"
  environment:
    - N8N_BASIC_AUTH_ACTIVE=true
    - N8N_BASIC_AUTH_USER=admin
    - N8N_BASIC_AUTH_PASSWORD=your_password
  volumes:
    - n8n_data:/home/node/.n8n
  restart: unless-stopped

volumes:
  n8n_data:
```

## Access n8n

After starting, open: **http://localhost:5678**

## AURORA Workflows

### Workflow 1: Alert on Model Degradation

**Purpose**: Send alerts when model performance drops

**Setup**:

1. **Create New Workflow**
   - Click "+" to create new workflow
   - Name it "AURORA Model Degradation Alert"

2. **Add Webhook Trigger**
   - Add node: Webhook
   - Method: POST
   - Path: `aurora/model-alert`
   - Click "Listen for Test Event"

3. **Add Condition Node**
   - Add node: IF
   - Connect from Webhook
   - Condition: `{{ $json["accuracy"] }} < 0.75`

4. **Add Slack/Email Notification** (True branch)
   - Add node: Slack / Send Email
   - Configure your credentials
   - Message template:
     ```
     🚨 AURORA Alert: Model Degradation Detected
     
     Model: {{ $json["model_name"] }}
     Accuracy: {{ $json["accuracy"] }}%
     Drift Score: {{ $json["drift_score"] }}
     
     Action Required: Review model performance
     ```

5. **Add HTTP Request** (Log back to AURORA)
   - Add node: HTTP Request
   - Method: POST
   - URL: `http://aurora:8000/api/metrics`
   - Body: `{{ $json }}`

6. **Activate Workflow**
   - Click "Active" toggle
   - Copy webhook URL

7. **Update AURORA .env**
   ```env
   N8N_WEBHOOK_URL=http://localhost:5678/webhook/aurora/model-alert
   ```

### Workflow 2: Scheduled Health Check

**Purpose**: Periodically check AURORA system health

**Setup**:

1. **Add Cron Trigger**
   - Add node: Cron
   - Schedule: `*/5 * * * *` (every 5 minutes)

2. **Add HTTP Request** (Check Health)
   - Add node: HTTP Request
   - Method: GET
   - URL: `http://aurora:8000/health`

3. **Add IF Condition**
   - Condition: `{{ $json["status"] }} !== "healthy"`

4. **Add Alert** (True branch)
   - Send notification if unhealthy

5. **Activate Workflow**

### Workflow 3: Auto-Retraining Trigger

**Purpose**: Automatically trigger retraining when conditions are met

**Setup**:

1. **Add Webhook**
   - Path: `aurora/trigger-retrain`

2. **Add HTTP Request** (Analyze System)
   - URL: `http://aurora:8000/api/analyze`
   - Method: POST
   - Body:
     ```json
     {
       "model_metrics": {{ $json["metrics"] }},
       "data_drift": {{ $json["drift"] }},
       "system_load": {{ $json["load"] }}
     }
     ```

3. **Add IF Condition**
   - Check if decision is "retrain"

4. **Add GCP Vertex AI Node** (True branch)
   - Trigger training job
   - Or use HTTP Request to Vertex AI API

5. **Add Notification**
   - Notify team of retraining

## Example: Testing Webhook

### From Terminal:

```bash
curl -X POST http://localhost:5678/webhook/aurora/model-alert \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "recommendation-model",
    "accuracy": 0.72,
    "drift_score": 0.65,
    "timestamp": "2026-01-07T20:00:00Z"
  }'
```

### From AURORA Code:

```python
import requests

def send_alert(model_name, accuracy, drift_score):
    webhook_url = "http://localhost:5678/webhook/aurora/model-alert"
    
    payload = {
        "model_name": model_name,
        "accuracy": accuracy,
        "drift_score": drift_score,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200
```

## Integration with AURORA

### Add to `backend/main.py`:

```python
import httpx

async def send_n8n_alert(alert_data: dict):
    """Send alert to n8n webhook"""
    if settings.n8n_webhook_url:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    settings.n8n_webhook_url,
                    json=alert_data,
                    timeout=10
                )
        except Exception as e:
            logger.error(f"Failed to send n8n alert: {e}")

# Use in analysis endpoint
@app.post("/api/analyze")
async def analyze_system(context: Dict[str, Any]):
    # ... existing code ...
    
    # Send alert if critical
    if critic_decision.decision_type == AgentDecisionType.RETRAIN:
        await send_n8n_alert({
            "type": "critical",
            "decision": critic_decision.to_dict(),
            "context": context
        })
```

## Advanced Workflows

### Multi-Step Approval Process

```
Webhook (Alert)
  → IF (Critical?)
    → True: Send to Slack for approval
    → Wait for response
    → IF (Approved?)
      → True: Execute action
      → False: Log rejection
```

### Data Pipeline Monitoring

```
Cron (Every hour)
  → HTTP Request (Get metrics)
  → Loop through models
    → Check each model
    → IF (Degraded?)
      → Send alert
      → Log to database
```

## n8n Credentials Setup

### Slack

1. Create Slack App: https://api.slack.com/apps
2. Add OAuth scope: `chat:write`
3. Install to workspace
4. Copy OAuth token
5. In n8n: Credentials → Slack → Add token

### Gmail

1. Enable 2FA on Google Account
2. Generate App Password
3. In n8n: Credentials → Gmail → Add credentials

### GCP

1. Use service account JSON
2. In n8n: Credentials → Google Cloud → Upload JSON

## Monitoring n8n

### Check Workflow Executions

- Go to "Executions" tab
- View success/failure logs
- Debug failed workflows

### Logs

```bash
# Docker logs
docker logs n8n

# NPM logs
~/.n8n/logs/
```

## Production Tips

1. **Use Environment Variables**
   - Store sensitive data in env vars
   - Reference in n8n: `{{ $env.VARIABLE_NAME }}`

2. **Error Handling**
   - Add error workflows
   - Set up retry logic
   - Log all failures

3. **Security**
   - Enable basic auth
   - Use HTTPS in production
   - Restrict webhook access

4. **Backup**
   - Export workflows regularly
   - Backup n8n data volume

## Free Alternatives to n8n

If you prefer other tools:

- **Zapier** (limited free tier)
- **Make (Integromat)** (free tier available)
- **Apache Airflow** (self-hosted, free)
- **Prefect** (self-hosted, free)

## Troubleshooting

### Webhook not receiving data

- Check n8n is running: `curl http://localhost:5678`
- Verify webhook path
- Check n8n logs
- Test with curl first

### Workflow not executing

- Ensure workflow is "Active"
- Check execution logs
- Verify node connections
- Test each node individually

### Can't connect to AURORA

- If using Docker, use service name: `http://aurora:8000`
- If local, use: `http://host.docker.internal:8000`
- Check network connectivity

## Next Steps

1. Create your first workflow
2. Test with sample data
3. Integrate with AURORA
4. Set up notifications
5. Monitor and iterate

---

**n8n Resources**:
- Documentation: https://docs.n8n.io
- Community: https://community.n8n.io
- Templates: https://n8n.io/workflows
