import requests

# Paste this where your model runs inference
API_URL = "https://sacreddevil2-aurora.hf.space"

print(f"📡 Sending test metric to: {API_URL}...")

try:
    response = requests.post(f"{API_URL}/api/metrics", json={
        "model_name": "Test-Model-Manual",
        "accuracy": 0.95,        # Replace with real accuracy
        "latency_ms": 120,       # Replace with real latency
        "data_drift_score": 0.0, # Optional: Drift metric
        "metadata": {
            "version": "1.0",
            "env": "production"
        }
    })

    if response.status_code == 200:
        print("✅ SUCCESS! Metric sent.")
        print("Response:", response.json())
    else:
        print(f"❌ FAILED. Status Code: {response.status_code}")
        
        # Check if it's a Private Space redirecting to login
        if "Sign up" in response.text or "Log in" in response.text:
            print("\n⚠️  POSSIBLE CAUSE: The Space is PRIVATE.")
            print("👉  Please go to Settings > Make Public in your Hugging Face Space.")
            
        elif response.status_code == 404:
            print("\n⚠️  POSSIBLE CAUSE: The Space is still BUILDING or starting up.")
            print("👉  Please check the 'Logs' tab in your Space.")
            
        print("\nFull Response snippet:", response.text[:200])
        
except Exception as e:
    print(f"❌ Connection Error: {e}")
