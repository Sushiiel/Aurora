"""
AURORA FastAPI Backend
Main API server for the AURORA system
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import logging
from datetime import datetime

from backend.config import settings
from backend.database.connection import get_db_session, init_db
from backend.database.models import ModelMetrics, AgentDecision as AgentDecisionModel, SystemState
from backend.agents.planner_agent import PlannerAgent
from backend.agents.critic_agent import CriticAgent
from backend.agents.executor_agent import ExecutorAgent
from backend.agents.base_agent import AgentDecisionType
from backend.rag.memory_store import MemoryStore

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AURORA API",
    description="Agentic Unified Reasoning & Optimization Runtime for AI Systems",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
memory_store = MemoryStore(use_pinecone=False)  # Use FAISS for free tier
planner_agent = PlannerAgent(memory_store)
critic_agent = CriticAgent()
executor_agent = ExecutorAgent()


@app.on_event("startup")
async def startup_event():
    """Initialize database and components on startup"""
    logger.info("Starting AURORA API...")
    init_db()
    logger.info("Database initialized")
    
    # Store initial system knowledge
    await memory_store.store(
        "System initialization: AURORA started successfully",
        {"type": "system", "event": "startup"}
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AURORA",
        "version": "1.0.0",
        "status": "operational",
        "description": "Agentic Unified Reasoning & Optimization Runtime for AI Systems"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "database": "operational",
            "memory_store": "operational",
            "agents": "operational"
        }
    }


@app.post("/api/analyze")
async def analyze_system(
    context: Dict[str, Any],
    db: Session = Depends(get_db_session)
):
    """
    Analyze system state and get agent recommendations
    
    Request body should include:
    - model_metrics: Current model performance
    - data_drift: Drift detection results
    - system_load: Resource utilization
    """
    try:
        logger.info("Received analysis request")
        
        # Step 1: Planner analyzes and proposes action
        planner_decision = await planner_agent.execute(context)
        
        # Step 2: Critic evaluates the proposal
        critic_context = {
            "proposed_decision": planner_decision,
            "current_state": context
        }
        critic_decision = await critic_agent.execute(critic_context)
        
        # Step 3: If approved, executor can execute (optional auto-execution)
        execution_result = None
        if critic_decision.decision_type != AgentDecisionType.NO_ACTION:
            executor_context = {
                "approved_decision": critic_decision,
                "execution_params": context.get("execution_params", {})
            }
            execution_result = await executor_agent.execute(executor_context)
        
        # Log decision to database
        decision_record = AgentDecisionModel(
            agent_type="orchestrator",
            decision_type=critic_decision.decision_type.value,
            reasoning=critic_decision.reasoning,
            confidence_score=critic_decision.confidence,
            approved=critic_decision.decision_type != AgentDecisionType.NO_ACTION,
            executed=execution_result is not None,
            context=context,
            outcome=execution_result.to_dict() if execution_result else None
        )
        db.add(decision_record)
        db.commit()
        
        # Store in memory for future RAG
        await memory_store.store_decision(
            decision_type=critic_decision.decision_type.value,
            reasoning=critic_decision.reasoning,
            outcome=execution_result.to_dict() if execution_result else {}
        )
        
        return {
            "planner_decision": planner_decision.to_dict(),
            "critic_decision": critic_decision.to_dict(),
            "execution_result": execution_result.to_dict() if execution_result else None,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/metrics")
async def log_metrics(
    metrics: Dict[str, Any],
    db: Session = Depends(get_db_session)
):
    """Log model metrics"""
    try:
        metric_record = ModelMetrics(
            model_name=metrics.get("model_name", "unknown"),
            model_version=metrics.get("model_version", "1.0"),
            accuracy=metrics.get("accuracy"),
            precision=metrics.get("precision"),
            recall=metrics.get("recall"),
            f1_score=metrics.get("f1_score"),
            latency_ms=metrics.get("latency_ms"),
            data_drift_score=metrics.get("data_drift_score"),
            concept_drift_detected=metrics.get("concept_drift_detected", False),
            meta_data=metrics.get("metadata", {})
        )
        db.add(metric_record)
        db.commit()
        
        return {"status": "success", "id": metric_record.id}
        
    except Exception as e:
        logger.error(f"Failed to log metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics/latest")
async def get_latest_metrics(
    model_name: str = None,
    limit: int = 10,
    db: Session = Depends(get_db_session)
):
    """Get latest metrics"""
    try:
        query = db.query(ModelMetrics)
        
        if model_name:
            query = query.filter(ModelMetrics.model_name == model_name)
        
        metrics = query.order_by(ModelMetrics.timestamp.desc()).limit(limit).all()
        
        return {
            "metrics": [
                {
                    "id": m.id,
                    "model_name": m.model_name,
                    "model_version": m.model_version,
                    "timestamp": m.timestamp.isoformat(),
                    "accuracy": m.accuracy,
                    "latency_ms": m.latency_ms,
                    "data_drift_score": m.data_drift_score
                }
                for m in metrics
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/decisions")
async def get_decisions(
    limit: int = 20,
    db: Session = Depends(get_db_session)
):
    """Get recent agent decisions"""
    try:
        decisions = db.query(AgentDecisionModel)\
            .order_by(AgentDecisionModel.timestamp.desc())\
            .limit(limit)\
            .all()
        
        return {
            "decisions": [
                {
                    "id": d.id,
                    "timestamp": d.timestamp.isoformat(),
                    "agent_type": d.agent_type,
                    "decision_type": d.decision_type,
                    "reasoning": d.reasoning,
                    "confidence": d.confidence_score,
                    "approved": d.approved,
                    "executed": d.executed
                }
                for d in decisions
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch decisions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/memory/stats")
async def get_memory_stats():
    """Get memory store statistics"""
    return memory_store.get_stats()


@app.post("/api/memory/search")
async def search_memory(query: Dict[str, Any]):
    """Search memory store"""
    try:
        results = await memory_store.search(
            query.get("query", ""),
            top_k=query.get("top_k", 5)
        )
        return {"results": results}
        
    except Exception as e:
        logger.error(f"Memory search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=settings.environment == "development"
    )
