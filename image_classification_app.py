import requests
import time
import random
import logging

# --- CONFIGURATION ---
AURORA_API_URL = "https://sacreddevil2-aurora.hf.space"
APP_NAME = "Smart-Camera-v1"
ENV = "edge-device-001"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageClassifier:
    def __init__(self):
        self.current_model = "MobileNet-v2 (Standard)"
        self.lighting_condition = "Daylight"
        self.accuracy_base = 0.92
        self.steps = 0
        self.optimized = False

    def process_frame(self):
        self.steps += 1
        
        # 1. Simulate Environmental Change (Failure Mode)
        if self.steps > 15 and not self.optimized:
            self.lighting_condition = "Low Light (Night)"
            if self.current_model == "MobileNet-v2 (Standard)":
                self.accuracy_base = 0.55  # DRAMATIC DROP due to bad lighting
                logger.warning(f"📉 LIGHTING CHANGED to {self.lighting_condition}. Accuracy dropping!")
        
        # 2. Generate Metrics
        accuracy = max(0, min(1, random.normalvariate(self.accuracy_base, 0.05)))
        latency = random.normalvariate(45, 5) # 45ms inference
        
        drift_score = 0.0
        if self.lighting_condition != "Daylight" and not self.optimized:
            drift_score = 0.85 # High drift detected
            
        return {
            "model_name": self.current_model,
            "accuracy": accuracy,
            "latency_ms": latency,
            "data_drift_score": drift_score,
            "metadata": {
                "lighting": self.lighting_condition,
                "optimized": self.optimized
            }
        }

    def apply_optimization(self, action):
        """React to AURORA's Command"""
        logger.info(f"🤖 RECEIVED COMMAND FROM AURORA: {action}")
        
        if "switch_model" in action or "optimize" in action:
            logger.info("⚡ SWITCHING MODEL to ResNet-50 (Night Vision)...")
            time.sleep(1) # Simulate switch time
            self.current_model = "ResNet-50 (Night Vision)"
            self.accuracy_base = 0.96 # Recovered accuracy
            self.optimized = True
            logger.info("✅ Model Switched! System Optimized.")

def main():
    print(f"📷 Starting {APP_NAME}")
    print(f"📡 Connecting to AURORA: {AURORA_API_URL}")
    print("--------------------------------------------------")
    
    classifier = ImageClassifier()
    
    while True:
        # 1. Run inference simulation
        metrics = classifier.process_frame()
        
        try:
            # 2. Report to AURORA
            response = requests.post(
                f"{AURORA_API_URL}/api/metrics", 
                json=metrics,
                timeout=5
            )
            
            if response.status_code == 200:
                logger.info(f"Report: {metrics['model_name']} | Acc: {metrics['accuracy']:.2f} | Light: {metrics['metadata']['lighting']}")
                
                # 3. CHECK FOR ACTIVE CONTROL (Self-Healing)
                # In a real scenario, AURORA analyzes the drop and sends a command back.
                # Here we simulate the logic: if we report bad accuracy, we look for the fix.
                
                # For this demo, let's simulate receiving the command if we are failing
                if metrics['accuracy'] < 0.60 and not classifier.optimized:
                     logger.info("⚠️ Performance Critical! Waiting for AURORA decision...")
                     time.sleep(2)
                     # Simulate AURORA deciding to switch model
                     classifier.apply_optimization("switch_model:resnet_night")
                     
            elif response.status_code == 404:
                logger.warning("⏳ Waiting for AURORA server...")
            else:
                logger.error(f"❌ Server Error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Connection Error: {e}")
            
        time.sleep(2)

if __name__ == "__main__":
    main()
