"""
AURORA Configuration Module
Centralized configuration management for the entire system
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    environment: str = "development"
    log_level: str = "INFO"
    api_port: int = int(os.getenv("API_PORT", os.getenv("PORT", "8000")))
    streamlit_port: int = 8501
    
    # GCP Configuration (Optional)
    gcp_project_id: Optional[str] = None
    gcp_region: str = "us-central1"
    google_application_credentials: Optional[str] = None
    
    # Vertex AI
    vertex_ai_endpoint: Optional[str] = None
    vertex_ai_model: str = "gemini-pro"
    
    # Database
    database_url: str = "sqlite:///./aurora.db"
    postgres_user: str = "aurora_user"
    postgres_password: Optional[str] = None
    postgres_db: str = "aurora"
    
    # Pinecone (Optional)
    pinecone_api_key: Optional[str] = None
    pinecone_environment: str = "us-west1-gcp"
    pinecone_index_name: str = "aurora-memory"
    
    # n8n
    n8n_webhook_url: Optional[str] = None
    
    # Agent Configuration
    planner_model: str = "gemini-pro"
    critic_threshold: float = 0.85
    max_retries: int = 3
    
    # Optional API Keys
    openai_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Export settings instance
settings = get_settings()
