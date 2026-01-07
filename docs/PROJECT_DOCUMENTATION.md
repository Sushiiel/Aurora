# 📊 AURORA Project Documentation

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Key Features](#key-features)
4. [Technology Stack](#technology-stack)
5. [Research Contributions](#research-contributions)
6. [Getting Started](#getting-started)
7. [API Reference](#api-reference)
8. [Agent System](#agent-system)
9. [Deployment](#deployment)
10. [Publications](#publications)

## Overview

**AURORA** (Agentic Unified Reasoning & Optimization Runtime for AI Systems) is a novel autonomous ML infrastructure management system that uses multi-agent AI to continuously monitor, reason about, and optimize machine learning pipelines in real-time.

### What Makes AURORA Unique?

Unlike traditional static ML pipelines, AURORA introduces:

- **Self-Observing**: Continuous monitoring of model performance, data drift, and system health
- **Self-Reasoning**: RAG-powered decision making based on historical experiments and best practices
- **Self-Optimizing**: Autonomous execution of optimization actions (retraining, caching, routing)

### Problem Statement

**Current ML Infrastructure:**
- ❌ Static pipelines that require manual intervention
- ❌ Reactive approach to model degradation
- ❌ Lost knowledge from past experiments
- ❌ Manual retraining and optimization decisions

**AURORA's Solution:**
- ✅ Autonomous decision-making agents
- ✅ Proactive optimization based on real-time analysis
- ✅ RAG-based memory of all system states and decisions
- ✅ Automated retraining, routing, and resource management

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Data Sources                          │
│  (Model Metrics, Logs, Performance Data, Drift Signals) │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              AURORA Control Plane                        │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Planner    │→ │    Critic    │→ │   Executor   │  │
│  │    Agent     │  │    Agent     │  │    Agent     │  │
│  └──────┬───────┘  └──────────────┘  └──────┬───────┘  │
│         │                                     │          │
│         ▼                                     ▼          │
│  ┌─────────────────────────────────────────────────┐   │
│  │         RAG Memory Store (FAISS/Pinecone)       │   │
│  │  (Past Experiments, Decisions, Best Practices)  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 Execution Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ Vertex AI│  │PostgreSQL│  │  Cache   │  │  n8n    │ │
│  │ Training │  │   State  │  │  Layer   │  │ Alerts  │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. Planner Agent
- **Role**: Analyzes system state and proposes actions
- **Input**: Model metrics, drift signals, system load
- **Process**: 
  - Queries RAG memory for similar past situations
  - Evaluates current state against historical patterns
  - Proposes optimal action (retrain, cache, route, etc.)
- **Output**: Decision with reasoning and confidence score

#### 2. Critic Agent
- **Role**: Safety layer that evaluates proposed actions
- **Input**: Planner's proposed decision
- **Process**:
  - Validates confidence threshold
  - Assesses risk level
  - Checks system constraints (resources, load)
- **Output**: Approved/rejected decision

#### 3. Executor Agent
- **Role**: Executes approved actions
- **Input**: Approved decision from Critic
- **Process**:
  - Interfaces with Vertex AI for training
  - Updates cache configurations
  - Modifies routing rules
  - Sends alerts via n8n
- **Output**: Execution result and status

#### 4. RAG Memory Store
- **Technology**: FAISS (local) or Pinecone (cloud)
- **Storage**: 
  - Past experiment results
  - Agent decisions and outcomes
  - System state snapshots
  - Error cases and resolutions
- **Retrieval**: Semantic search for similar situations

## Key Features

### 1. Autonomous Decision Making

```python
# Example: System detects drift and autonomously decides
context = {
    "model_metrics": {"accuracy": 0.72, "latency_ms": 650},
    "data_drift": {"detected": True, "score": 0.65}
}

# Planner analyzes
planner_decision = await planner_agent.execute(context)
# → Proposes: RETRAIN (confidence: 0.95)

# Critic evaluates
critic_decision = await critic_agent.execute({"proposed_decision": planner_decision})
# → Approves: RETRAIN (risk: medium, resources: available)

# Executor acts
execution_result = await executor_agent.execute({"approved_decision": critic_decision})
# → Submits training job to Vertex AI
```

### 2. RAG-Powered Reasoning

```python
# Agent queries past similar situations
similar_cases = await memory_store.search(
    "model accuracy dropped with data drift",
    top_k=5
)

# Returns:
# - Previous retraining that improved accuracy by 8%
# - Fine-tuning that took 30 minutes
# - Caching that reduced latency by 40%
```

### 3. Real-Time Monitoring

- Continuous metric collection
- Drift detection (data and concept drift)
- Latency tracking
- Resource utilization monitoring

### 4. Interactive Dashboard

- System health overview
- Agent decision history
- Performance metrics visualization
- Manual analysis triggers
- Memory search interface

## Technology Stack

### Backend
- **FastAPI**: REST API server
- **SQLAlchemy**: ORM for PostgreSQL
- **Sentence Transformers**: Text embeddings
- **FAISS**: Vector similarity search
- **Pydantic**: Data validation

### Frontend
- **Streamlit**: Interactive dashboard
- **Plotly**: Data visualization
- **Pandas**: Data manipulation

### ML/AI
- **PyTorch**: Model training
- **Transformers**: LLM integration
- **Scikit-learn**: ML utilities

### Infrastructure
- **GCP Vertex AI**: Model training and deployment
- **PostgreSQL**: System state storage
- **Pinecone**: Cloud vector database (optional)
- **n8n**: Workflow automation
- **Docker**: Containerization

## Research Contributions

### 1. Agentic ML Infrastructure Control

**Novelty**: First system to use autonomous agents for ML infrastructure decisions

**Key Innovation**:
- Multi-agent architecture (Planner-Critic-Executor)
- Agents reason about system-level decisions, not just model predictions
- Closed-loop optimization without human intervention

**Publishable Claims**:
- Novel agent orchestration pattern for ML systems
- Demonstrated improvement in system reliability
- Reduced time-to-recovery from degradation

### 2. RAG for System Memory

**Novelty**: Application of RAG to system states rather than documents

**Key Innovation**:
- Vector embeddings of system states and decisions
- Semantic retrieval of similar past situations
- Learning from historical experiments

**Publishable Claims**:
- Novel application of RAG beyond QA systems
- Improved decision quality through historical context
- Reduced repeated mistakes

### 3. Autonomous Retraining Under Uncertainty

**Novelty**: Automated decision-making for model lifecycle management

**Key Innovation**:
- Confidence-based decision thresholds
- Risk assessment for automated actions
- Multi-criteria optimization (accuracy, latency, cost)

**Publishable Claims**:
- Framework for safe autonomous ML operations
- Cost-performance tradeoff optimization
- Reduced manual intervention by X%

## Getting Started

### Quick Start (5 minutes)

```bash
# Clone and navigate
cd /Users/mymac/Desktop/AURORA

# Run quick start script
./start.sh
```

This will:
1. Create virtual environment
2. Install dependencies
3. Initialize database
4. Start backend (port 8000)
5. Start dashboard (port 8501)

### Manual Setup

See [SETUP.md](./SETUP.md) for detailed instructions.

### Docker Setup

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## API Reference

### Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-07T20:00:00Z",
  "components": {
    "database": "operational",
    "memory_store": "operational",
    "agents": "operational"
  }
}
```

### Trigger Analysis

```bash
POST /api/analyze
```

**Request:**
```json
{
  "model_metrics": {
    "accuracy": 0.75,
    "latency_ms": 450
  },
  "data_drift": {
    "detected": true,
    "score": 0.6
  },
  "system_load": {
    "cpu_usage": 0.7,
    "memory_usage": 0.6,
    "gpu_usage": 0.5
  }
}
```

**Response:**
```json
{
  "planner_decision": {
    "decision_type": "retrain",
    "reasoning": "Model accuracy below threshold with drift detected",
    "confidence": 0.95
  },
  "critic_decision": {
    "decision_type": "retrain",
    "reasoning": "Approved: High confidence, acceptable risk",
    "confidence": 0.95
  },
  "execution_result": {
    "decision_type": "retrain",
    "reasoning": "Training job submitted successfully",
    "context": {
      "training_job_id": "training-20260107-200000"
    }
  }
}
```

### Log Metrics

```bash
POST /api/metrics
```

**Request:**
```json
{
  "model_name": "recommendation-model",
  "model_version": "1.0",
  "accuracy": 0.85,
  "latency_ms": 420,
  "data_drift_score": 0.15
}
```

### Get Recent Decisions

```bash
GET /api/decisions?limit=20
```

### Search Memory

```bash
POST /api/memory/search
```

**Request:**
```json
{
  "query": "model retraining with high drift",
  "top_k": 5
}
```

## Agent System

### Agent Lifecycle

```
1. Monitor → 2. Analyze → 3. Decide → 4. Evaluate → 5. Execute → 6. Learn
    ↑                                                                  │
    └──────────────────────────────────────────────────────────────────┘
```

### Decision Types

| Type | Description | Trigger Conditions |
|------|-------------|-------------------|
| `RETRAIN` | Full model retraining | Accuracy < 70% AND drift detected |
| `FINE_TUNE` | Incremental tuning | Moderate drift (score > 0.5) |
| `CACHE` | Enable caching | Latency > 1000ms |
| `ROUTE` | Traffic routing | Load imbalance |
| `SCALE` | Resource scaling | High resource usage |
| `ALERT` | Send notification | Critical issues |
| `NO_ACTION` | No change needed | System healthy |

### Confidence Thresholds

- **High Confidence** (>0.9): Auto-execute safe actions
- **Medium Confidence** (0.7-0.9): Execute with monitoring
- **Low Confidence** (<0.7): Alert only, require approval

## Deployment

### Local Development

```bash
./start.sh
```

### Docker Production

```bash
docker-compose up -d
```

### GCP Cloud Run

```bash
gcloud run deploy aurora \
  --image gcr.io/aurora-ml-system/aurora:latest \
  --platform managed \
  --region us-central1
```

See [docs/GCP_SETUP.md](./docs/GCP_SETUP.md) for details.

## Publications

### Target Venues

**Journals:**
- Springer Nature Computer Science
- Journal of Big Data
- Applied AI (Springer)
- IEEE Transactions on Systems

**Conferences:**
- MLSys
- SysML
- ICML (Workshop track)
- NeurIPS (Systems track)

### Paper Structure

**Title**: "AURORA: Autonomous Agentic Reasoning for ML Infrastructure Optimization"

**Abstract**: Present the three key contributions

**Sections**:
1. Introduction & Motivation
2. Related Work (RAG, AutoML, MLOps)
3. System Architecture
4. Agent Design & Implementation
5. Experiments & Results
6. Discussion & Future Work

### Experiments to Run

1. **Performance Improvement**
   - Baseline: Manual intervention
   - AURORA: Autonomous optimization
   - Metrics: Time-to-recovery, accuracy improvement

2. **Cost Analysis**
   - Resource utilization before/after
   - Training job efficiency
   - Total cost of ownership

3. **Decision Quality**
   - Agent decision accuracy
   - False positive rate
   - User satisfaction

## Contributing

This is a research project. Contributions welcome!

## License

MIT License

## Contact

For questions or collaboration: [Your contact info]

---

**AURORA** - Making ML Infrastructure Self-Optimizing
