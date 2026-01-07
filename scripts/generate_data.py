"""
Sample data generator for testing AURORA
Generates realistic model metrics and system states
"""
import random
import asyncio
import requests
from datetime import datetime, timedelta
import time

API_URL = "http://localhost:8000"

def generate_model_metrics(model_name: str, base_accuracy: float = 0.85):
    """Generate realistic model metrics"""
    
    # Add some variance
    accuracy = base_accuracy + random.uniform(-0.1, 0.05)
    accuracy = max(0.5, min(1.0, accuracy))
    
    # Latency varies
    latency = random.uniform(200, 800)
    
    # Drift score
    drift_score = random.uniform(0.0, 0.5)
    drift_detected = drift_score > 0.4
    
    return {
        "model_name": model_name,
        "model_version": "1.0",
        "accuracy": accuracy,
        "precision": accuracy + random.uniform(-0.05, 0.05),
        "recall": accuracy + random.uniform(-0.05, 0.05),
        "f1_score": accuracy,
        "latency_ms": latency,
        "data_drift_score": drift_score,
        "concept_drift_detected": drift_detected,
        "meta_data": {
            "timestamp": datetime.utcnow().isoformat(),
            "environment": "production"
        }
    }

def generate_system_context(model_name: str):
    """Generate system context for analysis"""
    
    metrics = generate_model_metrics(model_name)
    
    return {
        "model_metrics": {
            "accuracy": metrics["accuracy"],
            "latency_ms": metrics["latency_ms"]
        },
        "data_drift": {
            "detected": metrics["concept_drift_detected"],
            "score": metrics["data_drift_score"]
        },
        "system_load": {
            "cpu_usage": random.uniform(0.3, 0.9),
            "memory_usage": random.uniform(0.4, 0.8),
            "gpu_usage": random.uniform(0.2, 0.7)
        }
    }

def send_metrics(metrics):
    """Send metrics to AURORA API"""
    try:
        response = requests.post(f"{API_URL}/api/metrics", json=metrics, timeout=5)
        if response.status_code == 200:
            print(f"✅ Sent metrics for {metrics['model_name']}: accuracy={metrics['accuracy']:.2%}")
            return True
        else:
            print(f"❌ Failed to send metrics: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending metrics: {e}")
        return False

def trigger_analysis(context):
    """Trigger system analysis"""
    try:
        response = requests.post(f"{API_URL}/api/analyze", json=context, timeout=30)
        if response.status_code == 200:
            result = response.json()
            decision = result.get("critic_decision", {})
            print(f"🤖 Analysis complete: {decision.get('decision_type')} (confidence: {decision.get('confidence', 0):.2%})")
            print(f"   Reasoning: {decision.get('reasoning', '')[:100]}...")
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return False

def simulate_degradation(model_name: str, duration_seconds: int = 60):
    """Simulate model degradation over time"""
    print(f"\n🔄 Simulating degradation for {model_name} over {duration_seconds}s\n")
    
    start_accuracy = 0.90
    end_accuracy = 0.65
    
    steps = duration_seconds // 5
    accuracy_drop = (start_accuracy - end_accuracy) / steps
    
    for i in range(steps):
        current_accuracy = start_accuracy - (accuracy_drop * i)
        
        # Generate and send metrics
        metrics = generate_model_metrics(model_name, current_accuracy)
        send_metrics(metrics)
        
        # Every 3rd step, trigger analysis
        if i % 3 == 0:
            context = generate_system_context(model_name)
            context["model_metrics"]["accuracy"] = current_accuracy
            trigger_analysis(context)
        
        time.sleep(5)
    
    print(f"\n✅ Simulation complete for {model_name}\n")

def generate_batch_data(num_samples: int = 20):
    """Generate batch of sample data"""
    print(f"\n📊 Generating {num_samples} sample metrics\n")
    
    models = ["recommendation-model", "classification-model", "nlp-model"]
    
    for i in range(num_samples):
        model = random.choice(models)
        metrics = generate_model_metrics(model)
        send_metrics(metrics)
        time.sleep(0.5)
    
    print(f"\n✅ Generated {num_samples} samples\n")

def run_continuous_monitoring(interval_seconds: int = 10):
    """Run continuous monitoring simulation"""
    print(f"\n🔄 Starting continuous monitoring (interval: {interval_seconds}s)\n")
    print("Press Ctrl+C to stop\n")
    
    models = ["recommendation-model", "classification-model"]
    
    try:
        while True:
            for model in models:
                # Send metrics
                metrics = generate_model_metrics(model)
                send_metrics(metrics)
                
                # Occasionally trigger analysis
                if random.random() < 0.3:
                    context = generate_system_context(model)
                    trigger_analysis(context)
            
            time.sleep(interval_seconds)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring stopped\n")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 AURORA Data Generator")
    print("=" * 60)
    
    print("\nOptions:")
    print("1. Generate batch data (20 samples)")
    print("2. Simulate model degradation (60s)")
    print("3. Continuous monitoring (10s interval)")
    print("4. Single analysis test")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        generate_batch_data(20)
    
    elif choice == "2":
        simulate_degradation("recommendation-model", 60)
    
    elif choice == "3":
        run_continuous_monitoring(10)
    
    elif choice == "4":
        print("\n🧪 Running single analysis test\n")
        context = {
            "model_metrics": {"accuracy": 0.72, "latency_ms": 650},
            "data_drift": {"detected": True, "score": 0.65},
            "system_load": {"cpu_usage": 0.7, "memory_usage": 0.6, "gpu_usage": 0.5}
        }
        trigger_analysis(context)
    
    else:
        print("Invalid option")
