from fastapi import FastAPI, BackgroundTasks
import requests
import random
import time
import uvicorn

# This is a sample "E-Commerce Recommendation Engine"
# It runs separately from AURORA.

app = FastAPI(title="Acme E-Commerce API", version="1.0.0")

# Configuration for AURORA connection
AURORA_URL = "http://localhost:8000/api/metrics"
MODEL_NAME = "acme-recommender-v1"

def log_to_aurora(accuracy: float, latency: float):
    """
    Background task to send metrics to AURORA without blocking the user response.
    """
    try:
        payload = {
            "model_name": MODEL_NAME,
            "accuracy": accuracy,
            "latency_ms": latency,
            "data_drift_score": random.uniform(0.0, 0.1), # Simulated drift check
            "metadata": {
                "region": "us-west-1",
                "customer_tier": "premium"
            }
        }
        requests.post(AURORA_URL, json=payload)
        print(f"📡 Logged to AURORA: Acc={accuracy:.2f}, Lat={latency:.0f}ms")
    except Exception as e:
        print(f"⚠️ Failed to log to log to AURORA: {e}")

@app.get("/")
def home():
    return {"status": "Acme E-Commerce API is Running"}

@app.post("/recommend")
async def get_recommendations(user_id: int, background_tasks: BackgroundTasks):
    """
    Main endpoint that returns product recommendations.
    It simulates using an AI model.
    """
    start_time = time.time()
    
    # 1. Simulate AI Inference (fake delay)
    latency_ms = random.uniform(50, 200)
    time.sleep(latency_ms / 1000.0)
    
    # 2. Simulate AI Performance Impact
    # (Sometimes the model is confident/accurate, sometimes not)
    # We'll simulate a random "accuracy" score for this prediction
    simulated_accuracy = random.uniform(0.85, 0.99)
    
    # 3. Log to AURORA (Asynchronously!)
    # We use background_tasks so the user gets their response instantly
    background_tasks.add_task(log_to_aurora, simulated_accuracy, latency_ms)
    
    return {
        "user_id": user_id,
        "recommendations": ["Wireless Headphones", "Mechanical Keyboard", "Monitor Stand"],
        "confidence": simulated_accuracy
    }

if __name__ == "__main__":
    print(f"🚀 Acme E-Commerce API starting on Port 8001...")
    print(f"🔗 Connects to AURORA on {AURORA_URL}")
    uvicorn.run(app, host="0.0.0.0", port=8001)
