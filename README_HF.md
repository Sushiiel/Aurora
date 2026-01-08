---
title: AURORA AI System
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: apache-2.0
---

# AURORA - Agentic Unified Reasoning & Optimization Runtime for AI

AURORA is an autonomous AI system that monitors, analyzes, and optimizes machine learning models in production using multi-agent architecture powered by Google's Gemini AI.

## 🌟 Features

- **Multi-Agent Architecture**: Planner, Critic, and Executor agents work together
- **Real-time Monitoring**: Track model performance, accuracy, and latency
- **Drift Detection**: Automatic data and concept drift detection
- **RAG Memory**: Vector-based memory store for learning from past decisions
- **Beautiful Dashboard**: Modern, responsive UI built with React and Tailwind CSS
- **RESTful API**: Complete FastAPI backend with automatic documentation

## 🚀 Quick Start

This Space is running AURORA with:
- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI + SQLite
- **AI**: Google Gemini Pro (Vertex AI)

### Using the Application

1. **Dashboard**: View real-time metrics and agent decisions
2. **Connect Model**: Integrate your ML models using the provided Python code
3. **Memory Search**: Query the RAG system for past incidents and decisions

### API Access

- **API Documentation**: Visit `/docs` for interactive API documentation
- **Health Check**: `/health` endpoint for monitoring
- **Metrics**: POST to `/api/metrics` to send model metrics

## 🔧 Configuration

Set these environment variables in your Space settings:

```bash
# Required
GCP_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS_JSON=<your-service-account-json>

# Optional
VERTEX_AI_MODEL=gemini-pro
LOG_LEVEL=INFO
ENVIRONMENT=production
```

## 📊 Architecture

```
┌─────────────────────────────────────┐
│   Hugging Face Space Container      │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │   Nginx      │  │   FastAPI   │ │
│  │   (Port 7860)│──│   Backend   │ │
│  │              │  │             │ │
│  │   Serves:    │  └─────────────┘ │
│  │   - Frontend │                  │
│  │   - API Proxy│                  │
│  └──────────────┘                  │
└─────────────────────────────────────┘
```

## 🛠️ Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd aurora

# Run the quick start script
chmod +x start.sh
./start.sh
```

Access locally at:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📚 Documentation

- [Setup Guide](SETUP.md)
- [Deployment Guide](README_HF_DEPLOYMENT.md)
- [Project Summary](PROJECT_SUMMARY.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

Apache 2.0 - See LICENSE file for details

## 🔗 Links

- [GitHub Repository](#)
- [Documentation](#)
- [Report Issues](#)

---

Built with ❤️ using Google Gemini AI, FastAPI, and React
