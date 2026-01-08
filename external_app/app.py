from flask import Flask, render_template, request, jsonify
import requests
import time
import random

app = Flask(__name__)

# AURORA Configuration
AURORA_URL = "https://sacreddevil2-aurora.hf.space"
MODEL_NAME = "Sentiment-v2-Pro"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.json.get('text', '')
    
    # Simulate AI Model Processing
    start_time = time.time()
    
    # Fake sentiment analysis logic
    sentiment = "Positive" if "good" in text or "great" in text else "Negative"
    confidence = random.uniform(0.8, 0.99)
    
    # Simulate latency
    process_time = random.uniform(0.05, 0.2) # 50-200ms
    time.sleep(process_time)
    
    latency_ms = (time.time() - start_time) * 1000
    
    # REPORT TO AURORA
    try:
        metrics = {
            "model_name": MODEL_NAME,
            "accuracy": confidence,
            "latency_ms": latency_ms,
            "data_drift_score": 0.0,
            "metadata": {"input_length": len(text)}
        }
        # Fire and forget (getting 404 is fine if Aurora is down)
        try:
             requests.post(f"{AURORA_URL}/api/metrics", json=metrics, timeout=1)
        except:
             pass 
             
    except Exception as e:
        print(f"Failed to report to Aurora: {e}")

    return jsonify({
        "sentiment": sentiment,
        "confidence": confidence,
        "aurora_status": "Metrics sent to Aurora"
    })

if __name__ == '__main__':
    print("🚀 Starting External AI App on http://localhost:5001")
    app.run(port=5001, debug=True)
