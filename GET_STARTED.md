# ⚡ AURORA - Getting Started

## 🎯 What You Have

A **production-ready Agentic AI System** with a modern web interface.

### The Stack
- **Frontend**: React + Vite + Tailwind CSS + Framer Motion
- **Backend**: FastAPI + Python Agents
- **Memory**: RAG with FAISS
- **Database**: SQLite (Local) / PostgreSQL (Prod)

## 🚀 Start in 1 Step

```bash
cd /Users/mymac/Desktop/AURORA
./start.sh
```

This will automatically:
- Install Python dependencies
- Initialize the Database
- Install Node.js dependencies (Frontend)
- Start Backend (Port 8000)
- Start Frontend (Port 5173)

## 🖥️ Using the System

1. **Open Web App**: Go to **http://localhost:5173**
2. **Login**: Click "Sign In" (Demo mode active)
3. **Initialize**: Click "Initialize System" on the landing page
4. **Monitor**: Watch real-time metrics and agent decisions

## 🧪 Quick Test

To see the system react to changes:

```bash
# In a new terminal
source venv/bin/activate
python scripts/generate_data.py
```
Select option **2** to simulate model degradation. Watch the dashboard update!

## 🔧 Requirements
- Python 3.8+
- Node.js & npm (for the React frontend)

## 📚 Links
- **Web App**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Project Structure**: [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)
