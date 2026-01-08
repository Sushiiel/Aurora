import time
import random
import requests
import sys

# Configuration
AURORA_API = "http://localhost:8000/api/metrics"
MODEL_NAME = "sentiment-classifier-pro"
VERSION = "v2.0.1"

def print_status(status, msg):
    color = "\033[92m" if status == "OK" else "\033[91m"
    reset = "\033[0m"
    print(f"{color}[{status}] {msg}{reset}")

def simulate_inference():
    print("\n🚀 Starting Sample AI Model: " + MODEL_NAME)
    print(f"📡 Connected to AURORA Monitor at {AURORA_API}")
    print("------------------------------------------------")
    
    # 1. Normal Operation Phase
    print("Phase 1: Normal Operation (High Accuracy)")
    for i in range(10):
        accuracy = random.uniform(0.92, 0.98)
        latency = random.uniform(100, 200)
        
        payload = {
            "model_name": MODEL_NAME,
            "accuracy": accuracy,
            "latency_ms": latency,
            "data_drift_score": 0.02,
            "metadata": {"env": "production", "version": VERSION}
        }
        
        try:
            requests.post(AURORA_API, json=payload)
            print_status("OK", f"Processed Batch #{i+1} | Acc: {accuracy:.1%} | Latency: {latency:.0f}ms")
        except:
            print_status("ERR", "Failed to connect to AURORA")
        
        time.sleep(2)

    # 2. Concept Drift Phase
    print("\n⚠️  Simulating Data Drift Event (Concept Shift)...")
    time.sleep(1)
    
    for i in range(15):
        # Accuracy drops gradually
        accuracy = max(0.60, 0.90 - (i * 0.03)) 
        latency = random.uniform(200, 400)
        drift_score = 0.1 + (i * 0.05)
        
        payload = {
            "model_name": MODEL_NAME,
            "accuracy": accuracy,
            "latency_ms": latency,
            "data_drift_score": drift_score,
            "metadata": {"env": "production", "version": VERSION}
        }
        
        try:
            requests.post(AURORA_API, json=payload)
            if accuracy < 0.8:
                 print_status("WARN", f"Processed Batch #{i+11} | Acc: {accuracy:.1%} | Drift: {drift_score:.2f}")
            else:
                 print_status("OK", f"Processed Batch #{i+11} | Acc: {accuracy:.1%} | Drift: {drift_score:.2f}")
        except:
            print_status("ERR", "Connection Failed")
            
        time.sleep(2)
        
    print("\n✅ Simulation Complete. Check AURORA Dashboard for Agent Actions.")

if __name__ == "__main__":
    try:
        simulate_inference()
    except KeyboardInterrupt:
        print("\nStopped.")
