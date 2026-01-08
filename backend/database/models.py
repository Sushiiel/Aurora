"""
Database models for AURORA system state tracking
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class ModelMetrics(Base):
    """Track model performance metrics over time"""
    __tablename__ = "model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(255), index=True, nullable=False)
    model_version = Column(String(100), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Performance metrics
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    latency_ms = Column(Float)
    
    # Drift detection
    data_drift_score = Column(Float)
    concept_drift_detected = Column(Boolean, default=False)
    
    # Metadata (renamed to avoid SQLAlchemy reserved keyword)
    meta_data = Column(JSON)


class AgentDecision(Base):
    """Log all agent decisions for audit and learning"""
    __tablename__ = "agent_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Agent information
    agent_type = Column(String(50), nullable=False)  # planner, critic, executor
    decision_type = Column(String(100), nullable=False)  # retrain, route, cache, etc.
    
    # Decision details
    reasoning = Column(Text)
    confidence_score = Column(Float)
    approved = Column(Boolean, default=False)
    executed = Column(Boolean, default=False)
    
    # Context
    context = Column(JSON)
    outcome = Column(JSON)


class SystemState(Base):
    """Track overall system state snapshots"""
    __tablename__ = "system_state"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # System health
    active_models = Column(Integer)
    total_requests = Column(Integer)
    avg_latency_ms = Column(Float)
    error_rate = Column(Float)
    
    # Resource utilization
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    gpu_usage = Column(Float)
    
    # State snapshot
    state_data = Column(JSON)


class ExperimentLog(Base):
    """Store experiment results for RAG retrieval"""
    __tablename__ = "experiment_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(String(255), unique=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Experiment details
    experiment_type = Column(String(100))  # training, tuning, routing, etc.
    model_name = Column(String(255))
    hyperparameters = Column(JSON)
    
    # Results
    metrics = Column(JSON)
    success = Column(Boolean)
    error_message = Column(Text, nullable=True)
    
    # For RAG
    description = Column(Text)
    embedding_id = Column(String(255), index=True)  # Reference to vector DB


class DataStream(Base):
    """Monitor data streams and quality"""
    __tablename__ = "data_streams"
    
    id = Column(Integer, primary_key=True, index=True)
    stream_name = Column(String(255), index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Data quality metrics
    record_count = Column(Integer)
    null_percentage = Column(Float)
    schema_version = Column(String(50))
    
    # Drift detection
    distribution_shift = Column(Float)
    anomaly_detected = Column(Boolean, default=False)
    
    # Metadata (renamed to avoid SQLAlchemy reserved keyword)
    meta_data = Column(JSON)


class Expense(Base):
    """Track user expenses for the Smart Expense Tracker"""
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    description = Column(String(500), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    user_email = Column(String(255), index=True)  # User's login email from Firebase
    ai_suggestion = Column(Text, nullable=True)  # AI-generated insights
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Budget(Base):
    """Track budget limits per category"""
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), unique=True, nullable=False, index=True)
    limit = Column(Float, nullable=False)
    spent = Column(Float, default=0.0)
    percentage = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
