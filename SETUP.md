# 🚀 AURORA Setup Guide

## Prerequisites

- Python 3.10+
- PostgreSQL (or use Docker)
- GCP Account (free tier)
- Pinecone Account (optional, free tier available)

## Quick Start

### 1. Clone and Setup

```bash
cd /Users/mymac/Desktop/AURORA
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

**Required configurations:**

```env
# For local development with SQLite (easiest)
DATABASE_URL=sqlite:///./aurora.db

# GCP (use free tier)
GCP_PROJECT_ID=your-project-id
GCP_REGION=us-central1

# Pinecone (optional - will use FAISS if not configured)
PINECONE_API_KEY=your-key-here
```

### 3. Run with Docker (Recommended)

```bash
docker-compose up -d
```

Access:
- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. Run Locally (Development)

Terminal 1 - Start Backend:
```bash
python -m backend.main
```

Terminal 2 - Start Dashboard:
```bash
streamlit run frontend/dashboard.py
```

## GCP Setup (Free Tier)

### 1. Create GCP Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable free tier ($300 credit for 90 days)

### 2. Enable Required APIs

```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable bigquery.googleapis.com
```

### 3. Create Service Account

1. Go to IAM & Admin > Service Accounts
2. Create service account with roles:
   - Vertex AI User
   - BigQuery User
3. Download JSON key
4. Set in `.env`:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
   ```

### 4. Vertex AI Setup

- **Free tier includes**: 
  - Gemini API calls (limited)
  - Model training credits
  - Prediction endpoints

## n8n Setup (Free)

### 1. Install n8n

```bash
npm install -g n8n
# or use Docker
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
```

### 2. Create Webhook Workflow

1. Open n8n: http://localhost:5678
2. Create new workflow
3. Add **Webhook** node:
   - Method: POST
   - Path: `aurora-alert`
4. Add **HTTP Request** node to forward to AURORA API
5. Activate workflow
6. Copy webhook URL to `.env`:
   ```
   N8N_WEBHOOK_URL=http://localhost:5678/webhook/aurora-alert
   ```

### 3. Example Alert Workflow

```
Webhook (Trigger) 
  → Filter (Check severity)
  → Email/Slack (Send notification)
  → HTTP Request (Log to AURORA)
```

## Pinecone Setup (Optional - Free Tier)

1. Sign up at [Pinecone](https://www.pinecone.io/)
2. Create index:
   - Name: `aurora-memory`
   - Dimensions: 384
   - Metric: cosine
3. Get API key and environment
4. Add to `.env`

**Note**: If not configured, AURORA will automatically use FAISS (local, free).

## Database Options

### Option 1: SQLite (Easiest - No setup)
```env
DATABASE_URL=sqlite:///./aurora.db
```

### Option 2: PostgreSQL (Recommended for production)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/aurora
```

### Option 3: Docker PostgreSQL
```bash
docker-compose up postgres -d
```

## Testing the System

### 1. Check Health

```bash
curl http://localhost:8000/health
```

### 2. Trigger Analysis

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "model_metrics": {"accuracy": 0.75, "latency_ms": 450},
    "data_drift": {"detected": true, "score": 0.6},
    "system_load": {"cpu_usage": 0.6}
  }'
```

### 3. View Dashboard

Open http://localhost:8501 and explore:
- System overview
- Agent decisions
- Metrics visualization
- Memory search

## Project Structure

```
AURORA/
├── backend/
│   ├── agents/          # Planner, Critic, Executor
│   ├── database/        # Models and connections
│   ├── rag/            # Memory store
│   ├── config.py       # Configuration
│   └── main.py         # FastAPI app
├── frontend/
│   └── dashboard.py    # Streamlit UI
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

## Free Tier Resources Summary

| Service | Free Tier | Usage |
|---------|-----------|-------|
| GCP Vertex AI | $300 credit | Model training, Gemini API |
| Pinecone | 1 index, 100k vectors | Optional (FAISS alternative) |
| PostgreSQL | Local/Docker | Free forever |
| n8n | Self-hosted | Free forever |
| Streamlit | Local hosting | Free forever |

## Troubleshooting

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 8501
lsof -ti:8501 | xargs kill -9
```

### Database connection error
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- For SQLite, ensure write permissions

### GCP authentication error
- Verify service account JSON path
- Check GOOGLE_APPLICATION_CREDENTIALS
- Ensure APIs are enabled

## Next Steps

1. **Add Real Models**: Integrate your actual ML models
2. **Configure Monitoring**: Set up real data streams
3. **Customize Agents**: Adjust decision thresholds
4. **Deploy**: Use GCP Cloud Run or Kubernetes

## Support

For issues or questions, check the documentation or create an issue.

---

**AURORA** - Agentic AI Systems Engineering
