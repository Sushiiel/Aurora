# 🎯 AURORA - Quick Reference Guide

## 🚀 Quick Start Commands

### Start AURORA
```bash
./start.sh
```

### Access Points
- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Stop Services
```bash
# Press Ctrl+C in the terminal running start.sh
```

## 📋 Common Tasks

### 1. Generate Test Data

```bash
# Activate virtual environment first
source venv/bin/activate

# Run data generator
python scripts/generate_data.py
```

Options:
1. Generate batch data (20 samples)
2. Simulate model degradation (60s)
3. Continuous monitoring (10s interval)
4. Single analysis test

### 2. Initialize/Reset Database

```bash
# Delete existing database
rm aurora.db

# Re-initialize
python scripts/init_db.py
```

### 3. Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Trigger analysis
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "model_metrics": {"accuracy": 0.72, "latency_ms": 650},
    "data_drift": {"detected": true, "score": 0.65},
    "system_load": {"cpu_usage": 0.7}
  }'

# Get recent metrics
curl http://localhost:8000/api/metrics/latest?limit=10

# Get decisions
curl http://localhost:8000/api/decisions?limit=10
```

### 4. View Logs

```bash
# Backend logs
tail -f backend.log

# Frontend logs
tail -f frontend.log

# Both
tail -f backend.log frontend.log
```

## 🐳 Docker Commands

### Start with Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f aurora

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build
```

### Access Docker Services

- Dashboard: http://localhost:8501
- API: http://localhost:8000
- PostgreSQL: localhost:5432

## 🧪 Testing Scenarios

### Scenario 1: Model Degradation

```python
# In Python or use the dashboard
import requests

response = requests.post("http://localhost:8000/api/analyze", json={
    "model_metrics": {
        "accuracy": 0.68,  # Low accuracy
        "latency_ms": 450
    },
    "data_drift": {
        "detected": True,
        "score": 0.75  # High drift
    },
    "system_load": {
        "cpu_usage": 0.5,
        "memory_usage": 0.4,
        "gpu_usage": 0.3
    }
})

print(response.json())
# Expected: Planner recommends RETRAIN, Critic approves, Executor submits job
```

### Scenario 2: High Latency

```python
response = requests.post("http://localhost:8000/api/analyze", json={
    "model_metrics": {
        "accuracy": 0.85,  # Good accuracy
        "latency_ms": 1200  # High latency
    },
    "data_drift": {
        "detected": False,
        "score": 0.1
    },
    "system_load": {
        "cpu_usage": 0.6,
        "memory_usage": 0.5,
        "gpu_usage": 0.4
    }
})

print(response.json())
# Expected: Planner recommends CACHE, Critic approves, Executor enables caching
```

### Scenario 3: Healthy System

```python
response = requests.post("http://localhost:8000/api/analyze", json={
    "model_metrics": {
        "accuracy": 0.92,  # Excellent
        "latency_ms": 350  # Fast
    },
    "data_drift": {
        "detected": False,
        "score": 0.05
    },
    "system_load": {
        "cpu_usage": 0.4,
        "memory_usage": 0.3,
        "gpu_usage": 0.2
    }
})

print(response.json())
# Expected: NO_ACTION - system healthy
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Minimal setup (SQLite)
DATABASE_URL=sqlite:///./aurora.db
GCP_PROJECT_ID=your-project-id
PINECONE_API_KEY=not-required-for-faiss

# Production setup (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/aurora
GCP_PROJECT_ID=aurora-ml-system
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
PINECONE_API_KEY=your-pinecone-key
```

### Agent Thresholds

Edit `backend/config.py`:

```python
critic_threshold: float = 0.85  # Minimum confidence for approval
max_retries: int = 3  # Max retry attempts
```

## 📊 Dashboard Features

### Overview Tab
- System health metrics
- Active models count
- Average accuracy and latency
- Recent decisions summary
- Performance trends
- Latency distribution

### Agents Tab
- Manual analysis trigger
- Adjust model parameters
- View agent decisions
- See reasoning and confidence
- Execution results

### Metrics Tab
- Detailed metrics table
- Model selector
- Drift analysis charts
- Historical performance

### Memory Tab
- Search system memory
- View similar past cases
- Memory statistics
- RAG retrieval testing

## 🔍 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 8501
lsof -ti:8501 | xargs kill -9
```

### Database Locked

```bash
# Stop all services
# Delete database
rm aurora.db
# Restart
./start.sh
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Dashboard Not Loading

```bash
# Check if backend is running
curl http://localhost:8000/health

# Restart frontend only
streamlit run frontend/dashboard.py
```

## 📦 Project Structure

```
AURORA/
├── backend/
│   ├── agents/           # Planner, Critic, Executor
│   ├── database/         # Models, connections
│   ├── rag/             # Memory store
│   ├── config.py        # Settings
│   └── main.py          # FastAPI app
├── frontend/
│   └── dashboard.py     # Streamlit UI
├── scripts/
│   ├── init_db.py       # Database setup
│   └── generate_data.py # Test data
├── docs/
│   ├── GCP_SETUP.md
│   ├── N8N_SETUP.md
│   └── PROJECT_DOCUMENTATION.md
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── start.sh            # Quick start script
└── .env               # Configuration
```

## 🎓 Next Steps

### For Development
1. ✅ Run `./start.sh`
2. ✅ Generate test data
3. ✅ Explore dashboard
4. ✅ Test API endpoints
5. ⬜ Integrate real models
6. ⬜ Configure GCP
7. ⬜ Set up n8n workflows

### For Research
1. ⬜ Design experiments
2. ⬜ Collect baseline metrics
3. ⬜ Run AURORA experiments
4. ⬜ Analyze results
5. ⬜ Write paper

### For Production
1. ⬜ Configure PostgreSQL
2. ⬜ Set up GCP Vertex AI
3. ⬜ Deploy to Cloud Run
4. ⬜ Configure monitoring
5. ⬜ Set up alerts

## 📚 Documentation

- [Setup Guide](../SETUP.md)
- [GCP Configuration](./GCP_SETUP.md)
- [n8n Workflows](./N8N_SETUP.md)
- [Full Documentation](./PROJECT_DOCUMENTATION.md)

## 🆘 Getting Help

1. Check logs: `tail -f backend.log frontend.log`
2. Review documentation in `docs/`
3. Test with curl commands
4. Check GCP/Pinecone credentials
5. Verify Python version (3.10+)

---

**Quick Tip**: Use the data generator to create realistic test scenarios and see AURORA in action!
