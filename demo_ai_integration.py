"""
Demo: Connect Your AI Model to AURORA
This example shows how to integrate any AI model with AURORA monitoring
"""
import time
import requests
import random
from datetime import datetime

# AURORA API endpoint
AURORA_API = "http://localhost:3000/api/aurora/record"

class DemoAIModel:
    """
    Example AI model with AURORA integration
    Replace this with your actual AI model
    """
    
    def __init__(self, model_name="demo-ai-model"):
        self.model_name = model_name
        self.predictions_count = 0
        print(f"🤖 Initializing {model_name} with AURORA monitoring...")
        print(f"📊 Metrics will be sent to: {AURORA_API}")
        print(f"📈 View dashboard at: http://localhost:5174/aurora-monitor\n")
    
    def predict(self, input_data):
        """
        Make a prediction with automatic AURORA tracking
        
        Args:
            input_data: Your model input (text, image, etc.)
            
        Returns:
            Prediction result
        """
        self.predictions_count += 1
        start_time = time.time()
        
        try:
            # ============================================
            # YOUR MODEL PREDICTION GOES HERE
            # ============================================
            
            # Simulate model inference (replace with your model)
            processing_time = random.uniform(0.1, 0.4)
            time.sleep(processing_time)
            
            # Simulate prediction result (replace with your model output)
            sentiment = "positive" if random.random() > 0.5 else "negative"
            confidence = random.uniform(0.85, 0.99)
            
            result = {
                "input": input_data,
                "prediction": sentiment,
                "confidence": confidence,
                "model": self.model_name
            }
            
            # ============================================
            # END OF MODEL PREDICTION
            # ============================================
            
            # Calculate metrics
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            accuracy = confidence  # Use your accuracy metric
            
            # Send to AURORA for monitoring
            self._send_to_aurora(
                response_time=response_time,
                accuracy=accuracy,
                error=False
            )
            
            print(f"✅ Prediction #{self.predictions_count}:")
            print(f"   Input: {input_data}")
            print(f"   Result: {sentiment} ({confidence:.2%})")
            print(f"   Time: {response_time:.0f}ms")
            print(f"   📊 Tracked by AURORA\n")
            
            return result
            
        except Exception as e:
            # Track errors to AURORA
            response_time = (time.time() - start_time) * 1000
            self._send_to_aurora(
                response_time=response_time,
                accuracy=0.0,
                error=True
            )
            
            print(f"❌ Prediction #{self.predictions_count} failed: {e}\n")
            raise e
    
    def _send_to_aurora(self, response_time, accuracy, error):
        """
        Send performance metrics to AURORA
        
        AURORA will:
        1. Monitor these metrics in real-time
        2. Detect performance issues
        3. Automatically optimize if needed
        4. Alert you proactively
        """
        try:
            payload = {
                "response_time": response_time,
                "accuracy": accuracy,
                "error": error,
                "model_name": self.model_name,
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                AURORA_API,
                json=payload,
                timeout=2
            )
            
            if response.status_code == 200:
                print(f"   ✓ Metrics sent to AURORA")
            else:
                print(f"   ⚠️  AURORA returned status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️  AURORA not available (is backend running on port 3000?)")
        except Exception as e:
            print(f"   ⚠️  Failed to send to AURORA: {e}")


def demo_basic_usage():
    """Demo 1: Basic usage"""
    print("=" * 60)
    print("DEMO 1: Basic AI Model Integration")
    print("=" * 60 + "\n")
    
    # Initialize your model
    model = DemoAIModel("sentiment-analyzer")
    
    # Make predictions - AURORA automatically tracks each one
    texts = [
        "I love this product!",
        "This is terrible",
        "Amazing experience",
        "Not good at all",
        "Absolutely fantastic!"
    ]
    
    for text in texts:
        model.predict(text)
        time.sleep(0.5)  # Small delay between predictions
    
    print("✅ Demo 1 complete!")
    print(f"📊 View metrics at: http://localhost:5174/aurora-monitor\n")


def demo_batch_predictions():
    """Demo 2: Batch predictions"""
    print("=" * 60)
    print("DEMO 2: Batch Predictions with AURORA Monitoring")
    print("=" * 60 + "\n")
    
    model = DemoAIModel("batch-classifier")
    
    # Simulate batch processing
    print("Processing batch of 10 predictions...\n")
    
    for i in range(10):
        input_text = f"Sample text {i+1}"
        model.predict(input_text)
        time.sleep(0.2)
    
    print("✅ Demo 2 complete!")
    print(f"📊 AURORA tracked all {model.predictions_count} predictions\n")


def demo_performance_simulation():
    """Demo 3: Simulate performance degradation"""
    print("=" * 60)
    print("DEMO 3: Simulating Performance Issues")
    print("=" * 60 + "\n")
    
    model = DemoAIModel("performance-test")
    
    print("Simulating gradual performance degradation...")
    print("Watch AURORA detect and respond to the issue!\n")
    
    for i in range(5):
        # Simulate increasing response time
        delay = 0.1 + (i * 0.1)
        
        print(f"Prediction {i+1} (simulated delay: {delay:.1f}s)")
        
        start = time.time()
        time.sleep(delay)
        
        # Simulate decreasing accuracy
        accuracy = 0.95 - (i * 0.05)
        
        model._send_to_aurora(
            response_time=(time.time() - start) * 1000,
            accuracy=accuracy,
            error=False
        )
        
        print(f"   Response time: {delay*1000:.0f}ms")
        print(f"   Accuracy: {accuracy:.2%}\n")
        
        time.sleep(0.5)
    
    print("✅ Demo 3 complete!")
    print("📊 Check AURORA Monitor to see how it detected the degradation!")
    print(f"🔗 http://localhost:5174/aurora-monitor\n")


def main():
    """Run all demos"""
    print("\n" + "=" * 60)
    print("🤖 AURORA AI Model Integration Demo")
    print("=" * 60 + "\n")
    
    print("This demo shows how to connect any AI model to AURORA")
    print("for real-time monitoring and automatic optimization.\n")
    
    print("Choose a demo:")
    print("1. Basic usage (5 predictions)")
    print("2. Batch predictions (10 predictions)")
    print("3. Performance simulation (shows AURORA detecting issues)")
    print("4. Run all demos")
    print("0. Exit\n")
    
    try:
        choice = input("Enter your choice (0-4): ").strip()
        print()
        
        if choice == "1":
            demo_basic_usage()
        elif choice == "2":
            demo_batch_predictions()
        elif choice == "3":
            demo_performance_simulation()
        elif choice == "4":
            demo_basic_usage()
            time.sleep(2)
            demo_batch_predictions()
            time.sleep(2)
            demo_performance_simulation()
        elif choice == "0":
            print("👋 Goodbye!")
            return
        else:
            print("Invalid choice. Please run again.")
            return
        
        print("\n" + "=" * 60)
        print("🎉 Demo Complete!")
        print("=" * 60)
        print("\n📊 View your metrics at:")
        print("   http://localhost:5174/aurora-monitor")
        print("\n💡 What AURORA is doing:")
        print("   ✓ Monitoring response times")
        print("   ✓ Tracking accuracy trends")
        print("   ✓ Detecting performance issues")
        print("   ✓ Preparing automatic optimizations")
        print("\n📚 For integration guide, see:")
        print("   HOW_TO_CONNECT_AI_MODEL.md\n")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
