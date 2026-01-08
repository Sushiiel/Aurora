import requests
import random
import time

API_URL = "https://sacreddevil2-aurora.hf.space"

models = [
    "Smart-Cam-X1", 
    "ResNet-50 (Night Vision)"
]

print("🚀 Forcing data into Aurora to populate Dashboard Dropdown...")

for model in models:
    try:
        print(f"  Sending metric for {model}...")
        requests.post(f"{API_URL}/api/metrics", json={
            "model_name": model,
            "accuracy": 0.95,
            "latency_ms": 150,
            "data_drift_score": 0.0,
            "metadata": {"env": "demo_populate"}
        }, timeout=5)
    except Exception as e:
        print(f"  Failed: {e}")

print("✅ Done! Refresh your Dashboard now.")
