from flask import Flask, render_template, request, jsonify
import requests
import time
import random

app = Flask(__name__)

# AURORA Config
AURORA_URL = "https://sacreddevil2-aurora.hf.space"
MODEL_NAME = "Smart-Cam-X1"

# State
current_model = "MobileNet-v2 (Standard)"
lighting = "Daylight"
accuracy_base = 0.95

@app.route('/')
def home():
    return render_template('camera.html')

@app.route('/classify', methods=['POST'])
def classify():
    global current_model, lighting, accuracy_base
    
    # Simulate processing
    time.sleep(random.uniform(0.1, 0.3))
    
    # Simulate Logic: If lighting is bad and model is weak -> fail
    lighting = request.json.get('lighting', 'Daylight')
    
    if lighting == "Low Light" and current_model == "MobileNet-v2 (Standard)":
        accuracy = random.uniform(0.40, 0.60) # Fail
        drift = 0.8
    else:
        accuracy = random.uniform(0.85, 0.99) # Good
        drift = 0.1
        
    latency = random.uniform(80, 150)

    # REPORT TO AURORA
    metrics = {
        "model_name": current_model,
        "accuracy": accuracy,
        "latency_ms": latency,
        "data_drift_score": drift,
        "metadata": {"lighting": lighting, "env": "prod"}
    }
    
    aurora_status = "Not Connected"
    try:
        requests.post(f"{AURORA_URL}/api/metrics", json=metrics, timeout=1)
        aurora_status = "Metrics Sent to AURORA 🟢"
        
        # Simulate Optimization (Self-Healing)
        if accuracy < 0.65:
            # In real life, Aurora sends this back. We simulate it here.
            time.sleep(1)
            current_model = "ResNet-50 (Night Vision)"
            aurora_status += " | ⚡ OPTIMIZATION TRIGGERED: Switched Model!"
            
    except:
        aurora_status = "AURORA Offline 🔴"

    return jsonify({
        "class": "Person",
        "confidence": accuracy,
        "model": current_model,
        "aurora_message": aurora_status
    })

@app.route('/reset', methods=['POST'])
def reset():
    global current_model
    current_model = "MobileNet-v2 (Standard)"
    return jsonify({"status": "Reset"})

if __name__ == '__main__':
    print("📷 Camera UI running on http://localhost:5002")
    app.run(port=5002, debug=True)
