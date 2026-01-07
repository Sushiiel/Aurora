"""
Initialize AURORA database and seed with sample data
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database.connection import init_db, get_db
from backend.database.models import ModelMetrics, SystemState, ExperimentLog
from backend.rag.memory_store import MemoryStore
from datetime import datetime, timedelta
import asyncio

async def seed_database():
    """Seed database with initial data"""
    print("🌱 Seeding database...")
    
    # Initialize database
    init_db()
    
    # Seed sample metrics
    with get_db() as db:
        # Add sample model metrics
        for i in range(10):
            metric = ModelMetrics(
                model_name="recommendation-model",
                model_version="1.0",
                accuracy=0.85 + (i * 0.01),
                precision=0.83,
                recall=0.87,
                f1_score=0.85,
                latency_ms=400 + (i * 10),
                data_drift_score=0.1 + (i * 0.02),
                concept_drift_detected=False,
                meta_data={"environment": "production"}
            )
            db.add(metric)
        
        # Add system state
        state = SystemState(
            active_models=2,
            total_requests=10000,
            avg_latency_ms=420,
            error_rate=0.01,
            cpu_usage=0.6,
            memory_usage=0.5,
            gpu_usage=0.4,
            state_data={"status": "healthy"}
        )
        db.add(state)
        
        db.commit()
    
    print("✅ Database seeded successfully")
    
    # Seed memory store
    print("🧠 Seeding memory store...")
    memory_store = MemoryStore(use_pinecone=False)
    
    # Add sample memories
    await memory_store.store_experiment(
        experiment_type="retraining",
        description="Retrained recommendation model due to data drift",
        results={"accuracy_improvement": 0.05, "training_time": "2h"},
        success=True
    )
    
    await memory_store.store_experiment(
        experiment_type="fine_tuning",
        description="Fine-tuned classification model with new data",
        results={"accuracy_improvement": 0.02, "training_time": "30m"},
        success=True
    )
    
    await memory_store.store_decision(
        decision_type="cache",
        reasoning="Enabled caching due to high latency",
        outcome={"latency_reduction": "40%", "cache_hit_rate": 0.75}
    )
    
    print("✅ Memory store seeded successfully")
    print("\n🚀 AURORA is ready!")

if __name__ == "__main__":
    asyncio.run(seed_database())
