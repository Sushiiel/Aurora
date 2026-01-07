# ☁️ Google Cloud Platform (GCP) Setup Guide for AURORA

## Overview

AURORA uses GCP for:
- **Vertex AI**: Model training and deployment
- **BigQuery**: Large-scale data analytics (optional)
- **Cloud Storage**: Model artifacts and data
- **Cloud Run**: Deployment (optional)

## Free Tier Benefits

Google Cloud offers **$300 credit** for 90 days for new users, plus always-free tier:

- Vertex AI: Limited free predictions
- Cloud Storage: 5 GB free
- BigQuery: 1 TB queries/month free
- Cloud Run: 2 million requests/month free

## Step-by-Step Setup

### 1. Create GCP Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with Google account
3. Accept terms and activate free trial ($300 credit)
4. Add billing information (required but won't charge during trial)

### 2. Create Project

```bash
# Via Console:
# 1. Click "Select a project" → "New Project"
# 2. Name: "aurora-ml-system"
# 3. Click "Create"

# Via gcloud CLI:
gcloud projects create aurora-ml-system --name="AURORA ML System"
gcloud config set project aurora-ml-system
```

### 3. Enable Required APIs

```bash
# Enable Vertex AI
gcloud services enable aiplatform.googleapis.com

# Enable BigQuery (optional)
gcloud services enable bigquery.googleapis.com

# Enable Cloud Storage
gcloud services enable storage.googleapis.com

# Enable Cloud Run (for deployment)
gcloud services enable run.googleapis.com
```

### 4. Create Service Account

```bash
# Create service account
gcloud iam service-accounts create aurora-service \
  --display-name="AURORA Service Account" \
  --description="Service account for AURORA ML system"

# Grant necessary roles
gcloud projects add-iam-policy-binding aurora-ml-system \
  --member="serviceAccount:aurora-service@aurora-ml-system.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding aurora-ml-system \
  --member="serviceAccount:aurora-service@aurora-ml-system.iam.gserviceaccount.com" \
  --role="roles/bigquery.user"

gcloud projects add-iam-policy-binding aurora-ml-system \
  --member="serviceAccount:aurora-service@aurora-ml-system.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

# Create and download key
gcloud iam service-accounts keys create ~/aurora-service-account.json \
  --iam-account=aurora-service@aurora-ml-system.iam.gserviceaccount.com
```

### 5. Configure AURORA

Update `.env`:

```env
GCP_PROJECT_ID=aurora-ml-system
GCP_REGION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/aurora-service-account.json
VERTEX_AI_MODEL=gemini-pro
```

## Vertex AI Setup

### 1. Initialize Vertex AI

```python
from google.cloud import aiplatform

aiplatform.init(
    project="aurora-ml-system",
    location="us-central1"
)
```

### 2. Create Model Training Job

```python
from google.cloud import aiplatform

def create_training_job(model_name: str):
    """Create a custom training job on Vertex AI"""
    
    job = aiplatform.CustomTrainingJob(
        display_name=f"aurora-{model_name}-training",
        script_path="train.py",
        container_uri="gcr.io/cloud-aiplatform/training/pytorch-gpu.1-13:latest",
        requirements=["torch", "transformers"],
        model_serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/pytorch-gpu.1-13:latest"
    )
    
    model = job.run(
        replica_count=1,
        machine_type="n1-standard-4",
        accelerator_type="NVIDIA_TESLA_T4",
        accelerator_count=1
    )
    
    return model
```

### 3. Deploy Model Endpoint

```python
def deploy_model(model):
    """Deploy model to endpoint"""
    
    endpoint = model.deploy(
        deployed_model_display_name="aurora-model-v1",
        machine_type="n1-standard-2",
        min_replica_count=1,
        max_replica_count=3,
        traffic_percentage=100
    )
    
    return endpoint
```

### 4. Make Predictions

```python
def predict(endpoint, instances):
    """Make predictions using deployed model"""
    
    predictions = endpoint.predict(instances=instances)
    return predictions
```

## Using Gemini API (Free Tier)

### 1. Enable Gemini

```bash
gcloud services enable generativelanguage.googleapis.com
```

### 2. Use in AURORA

```python
import google.generativeai as genai
from backend.config import settings

genai.configure(api_key=settings.google_api_key)

def generate_analysis(context: str):
    """Use Gemini for analysis"""
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Analyze this ML system state and recommend actions:
    
    {context}
    
    Provide:
    1. Issue analysis
    2. Recommended action
    3. Confidence level
    """
    
    response = model.generate_content(prompt)
    return response.text
```

## BigQuery Setup (Optional)

### 1. Create Dataset

```bash
bq mk --dataset \
  --location=US \
  aurora-ml-system:aurora_metrics
```

### 2. Create Table

```bash
bq mk --table \
  aurora-ml-system:aurora_metrics.model_metrics \
  schema.json
```

### 3. Query from AURORA

```python
from google.cloud import bigquery

def query_metrics():
    """Query metrics from BigQuery"""
    
    client = bigquery.Client()
    
    query = """
        SELECT 
            model_name,
            AVG(accuracy) as avg_accuracy,
            AVG(latency_ms) as avg_latency
        FROM `aurora-ml-system.aurora_metrics.model_metrics`
        WHERE timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
        GROUP BY model_name
    """
    
    results = client.query(query).result()
    return list(results)
```

## Cloud Storage Setup

### 1. Create Bucket

```bash
gsutil mb -l us-central1 gs://aurora-ml-artifacts
```

### 2. Upload Model Artifacts

```python
from google.cloud import storage

def upload_model(local_path: str, blob_name: str):
    """Upload model to Cloud Storage"""
    
    client = storage.Client()
    bucket = client.bucket("aurora-ml-artifacts")
    blob = bucket.blob(blob_name)
    
    blob.upload_from_filename(local_path)
    return f"gs://aurora-ml-artifacts/{blob_name}"
```

## Monitoring & Logging

### 1. Enable Cloud Logging

```python
import google.cloud.logging

def setup_logging():
    """Setup Cloud Logging"""
    
    client = google.cloud.logging.Client()
    client.setup_logging()
```

### 2. View Logs

```bash
# View recent logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# Stream logs
gcloud logging tail "resource.type=cloud_run_revision"
```

## Cost Optimization

### 1. Use Preemptible VMs

```python
job = aiplatform.CustomTrainingJob(
    # ... other params ...
    base_output_dir="gs://aurora-ml-artifacts/training"
)

model = job.run(
    replica_count=1,
    machine_type="n1-standard-4",
    accelerator_type="NVIDIA_TESLA_T4",
    accelerator_count=1,
    use_preemptible_workers=True  # Save up to 80%
)
```

### 2. Set Budget Alerts

```bash
# Via Console:
# 1. Go to Billing → Budgets & alerts
# 2. Create budget: $50/month
# 3. Set alerts at 50%, 90%, 100%
```

### 3. Auto-shutdown

```python
# Add to training script
import signal
import sys

def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    # Save checkpoint
    # Clean up resources
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
```

## Deployment to Cloud Run

### 1. Build Container

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/aurora-ml-system/aurora:latest
```

### 2. Deploy to Cloud Run

```bash
gcloud run deploy aurora \
  --image gcr.io/aurora-ml-system/aurora:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=$DATABASE_URL,GCP_PROJECT_ID=aurora-ml-system
```

### 3. Get URL

```bash
gcloud run services describe aurora --region us-central1 --format 'value(status.url)'
```

## Security Best Practices

1. **Never commit service account keys**
   ```bash
   echo "*.json" >> .gitignore
   ```

2. **Use Secret Manager**
   ```bash
   # Store secrets
   echo -n "my-secret-value" | gcloud secrets create aurora-db-password --data-file=-
   
   # Access in code
   from google.cloud import secretmanager
   
   client = secretmanager.SecretManagerServiceClient()
   name = "projects/aurora-ml-system/secrets/aurora-db-password/versions/latest"
   response = client.access_secret_version(request={"name": name})
   secret = response.payload.data.decode("UTF-8")
   ```

3. **Use IAM roles properly**
   - Principle of least privilege
   - Separate service accounts for different services

## Troubleshooting

### Authentication Error

```bash
# Set credentials
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Verify
gcloud auth application-default print-access-token
```

### API Not Enabled

```bash
# Check enabled APIs
gcloud services list --enabled

# Enable missing API
gcloud services enable <api-name>
```

### Quota Exceeded

- Check quotas: Console → IAM & Admin → Quotas
- Request increase if needed
- Use preemptible resources

## Free Tier Limits

| Service | Free Tier | Notes |
|---------|-----------|-------|
| Vertex AI | Limited predictions | Pay per use after |
| Cloud Storage | 5 GB | US region |
| BigQuery | 1 TB queries/month | 10 GB storage |
| Cloud Run | 2M requests/month | 360k GB-seconds |
| Gemini API | 60 requests/minute | Free tier |

## Next Steps

1. ✅ Create GCP project
2. ✅ Enable APIs
3. ✅ Create service account
4. ✅ Download credentials
5. ✅ Update AURORA .env
6. Test Vertex AI connection
7. Deploy first model
8. Set up monitoring

## Resources

- [GCP Free Tier](https://cloud.google.com/free)
- [Vertex AI Docs](https://cloud.google.com/vertex-ai/docs)
- [Gemini API](https://ai.google.dev/)
- [Cloud Run Docs](https://cloud.google.com/run/docs)

---

**Need Help?** Check GCP documentation or AURORA issues on GitHub.
