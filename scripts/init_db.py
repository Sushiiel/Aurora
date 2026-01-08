"""
Initialize AURORA database with empty tables
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database.connection import init_db
import asyncio

async def initialize_database():
    """Initialize database with empty tables for new users"""
    print("🔧 Initializing database...")
    
    # Initialize database tables
    init_db()
    
    print("✅ Database initialized successfully")
    print("📊 Dashboard is ready for your first model connection")
    print("\n🚀 AURORA is ready!")
    print("\n💡 Tip: Connect your first model using the 'Connect Model' page")

if __name__ == "__main__":
    asyncio.run(initialize_database())
