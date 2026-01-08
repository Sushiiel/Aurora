import requests
import time
import random
import logging

# --- CONFIGURATION ---
AURORA_API_URL = "https://sacreddevil2-aurora.hf.space"  # Your Deployment
MODEL_NAME = "Sentiment-Analyzer-v1"
ENV = "local-dev"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def simulate_inference():
    """Simulates a model making predictions and calculating its own metrics"""
    
    # 1. Simulate Latency (random processing time)
    latency = random.normalvariate(120, 20)  # ms
    time.sleep(latency / 1000) 
    
    # 2. Simulate Accuracy (sometimes it dips, triggering Aurora)
    # Most of the time good (0.95), sometimes bad (0.75)
    base_accuracy = 0.95
    if random.random() < 0.1: # 10% chance of performance drop
        base_accuracy = 0.75
        drift_score = 0.4 # High drift
    else:
        drift_score = 0.05 # Low drift

    accuracy = max(0, min(1, random.normalvariate(base_accuracy, 0.05)))
    
    return {
        "accuracy": accuracy,
        "latency_ms": latency,
        "data_drift_score": drift_score
    }

def send_metrics(metrics):
    """Sends metrics to AURORA"""
    try:
        payload = {
            "model_name": MODEL_NAME,
            "accuracy": metrics["accuracy"],
            "latency_ms": metrics["latency_ms"],
            "data_drift_score": metrics["data_drift_score"],
            "metadata": {
                "version": "1.0.2",
                "env": ENV,
                "host": "mac-local"
            }
        }
        
        response = requests.post(f"{AURORA_API_URL}/api/metrics", json=payload)
        
        if response.status_code == 200:
            logger.info(f"✅ Sent metrics: Acc={metrics['accuracy']:.2f}, Latency={metrics['latency_ms']:.0f}ms")
            
            # Check if AURORA sent back any optimization commands (Active Control)
            try:
                data = response.json()
                if data.get("optimization_triggered"):
                     logger.warning(f"⚠️ AURORA TRIGGERED OPTIMIZATION: {data.get('action')}")
            except:
                pass
                 
        elif response.status_code in [404, 502, 503]:
            logger.warning(f"⏳ Waiting for AURORA deployment to finish... (Status: {response.status_code})")
        else:
            logger.error(f"❌ Failed to send metrics: {response.status_code} - {response.text[:200]}")
            
    except Exception as e:
        logger.error(f"Connection error: {e}")

def main():
    print(f"🚀 Starting Local AI Model: {MODEL_NAME}")
    print(f"📡 Connecting to AURORA at: {AURORA_API_URL}")
    print("--------------------------------------------------")
    
    while True:
        # Simulate processing one batch of data
        metrics = simulate_inference()
        
        # Report to AURORA
        send_metrics(metrics)
        
        # Wait a bit before next batch
        time.sleep(2)

if __name__ == "__main__":
    main()
