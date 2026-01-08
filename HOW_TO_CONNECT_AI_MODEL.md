# 🤖 How to Connect AURORA with Your AI Model

## 📋 Overview

AURORA can monitor and optimize any AI model by tracking its performance metrics and automatically implementing improvements. Here's how to integrate it.

---

## 🎯 Integration Methods

### Method 1: Direct Integration (Recommended)
Wrap your AI model calls with AURORA monitoring

### Method 2: Decorator Pattern
Use Python decorators to automatically track model usage

### Method 3: API Wrapper
Route all model requests through AURORA's API

---

## 🚀 Method 1: Direct Integration

### Step 1: Import AURORA Monitor

```python
# your_model.py
import time
import requests
from datetime import datetime

# AURORA monitoring endpoint
AURORA_API = "http://localhost:3000/api/aurora/record"

class YourAIModel:
    def __init__(self):
        # Your model initialization
        self.model = self.load_model()
    
    def predict(self, input_data):
        # Start timing
        start_time = time.time()
        
        try:
            # Your model prediction
            result = self.model.predict(input_data)
            
            # Calculate metrics
            response_time = (time.time() - start_time) * 1000  # ms
            accuracy = self.calculate_accuracy(result, input_data)
            
            # Send metrics to AURORA
            self.send_to_aurora(
                response_time=response_time,
                accuracy=accuracy,
                error=False
            )
            
            return result
            
        except Exception as e:
            # Track errors
            response_time = (time.time() - start_time) * 1000
            self.send_to_aurora(
                response_time=response_time,
                accuracy=0.0,
                error=True
            )
            raise e
    
    def send_to_aurora(self, response_time, accuracy, error):
        """Send metrics to AURORA for monitoring and optimization"""
        try:
            payload = {
                "response_time": response_time,
                "accuracy": accuracy,
                "error": error
            }
            requests.post(AURORA_API, json=payload, timeout=1)
        except:
            # Don't fail if AURORA is unavailable
            pass
    
    def calculate_accuracy(self, result, input_data):
        # Your accuracy calculation logic
        # Return a value between 0.0 and 1.0
        return 0.95  # Example
```

### Step 2: Use Your Model

```python
# main.py
from your_model import YourAIModel

model = YourAIModel()

# Every prediction is automatically tracked by AURORA
result = model.predict({"text": "Sample input"})

# AURORA will:
# 1. Monitor response time
# 2. Track accuracy
# 3. Detect performance issues
# 4. Automatically optimize if needed
```

---

## 🎨 Method 2: Decorator Pattern (Elegant)

### Step 1: Create AURORA Decorator

```python
# aurora_decorator.py
import time
import requests
from functools import wraps

AURORA_API = "http://localhost:3000/api/aurora/record"

def aurora_monitor(accuracy_func=None):
    """
    Decorator to automatically monitor AI model performance
    
    Usage:
        @aurora_monitor(accuracy_func=calculate_accuracy)
        def predict(input_data):
            return model.predict(input_data)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            error = False
            accuracy = 0.0
            
            try:
                # Execute the model prediction
                result = func(*args, **kwargs)
                
                # Calculate accuracy if function provided
                if accuracy_func:
                    accuracy = accuracy_func(result, *args, **kwargs)
                else:
                    accuracy = 0.95  # Default
                
                return result
                
            except Exception as e:
                error = True
                raise e
                
            finally:
                # Always send metrics to AURORA
                response_time = (time.time() - start_time) * 1000
                send_to_aurora(response_time, accuracy, error)
        
        return wrapper
    return decorator

def send_to_aurora(response_time, accuracy, error):
    """Send metrics to AURORA"""
    try:
        payload = {
            "response_time": response_time,
            "accuracy": accuracy,
            "error": error
        }
        requests.post(AURORA_API, json=payload, timeout=1)
    except:
        pass
```

### Step 2: Use the Decorator

```python
# your_model.py
from aurora_decorator import aurora_monitor

class YourAIModel:
    def __init__(self):
        self.model = self.load_model()
    
    @aurora_monitor(accuracy_func=lambda result, input_data: 0.95)
    def predict(self, input_data):
        """This method is now automatically monitored by AURORA"""
        return self.model.predict(input_data)
    
    @aurora_monitor()
    def generate_text(self, prompt):
        """This too!"""
        return self.model.generate(prompt)
```

---

## 🔧 Method 3: Complete Example with Real AI Model

### Example: Monitoring a Sentiment Analysis Model

```python
# sentiment_model.py
import time
import requests
from transformers import pipeline

AURORA_API = "http://localhost:3000/api/aurora/record"

class SentimentAnalyzer:
    def __init__(self):
        # Load your AI model (example: HuggingFace)
        self.model = pipeline("sentiment-analysis")
        self.baseline_accuracy = 0.95
    
    def analyze(self, text):
        """Analyze sentiment with AURORA monitoring"""
        start_time = time.time()
        
        try:
            # Run model inference
            result = self.model(text)[0]
            
            # Calculate metrics
            response_time = (time.time() - start_time) * 1000
            confidence = result['score']
            
            # Send to AURORA
            self._track_performance(
                response_time=response_time,
                accuracy=confidence,
                error=False
            )
            
            return result
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            self._track_performance(
                response_time=response_time,
                accuracy=0.0,
                error=True
            )
            raise e
    
    def _track_performance(self, response_time, accuracy, error):
        """Send metrics to AURORA for monitoring"""
        try:
            payload = {
                "response_time": response_time,
                "accuracy": accuracy,
                "error": error,
                "model_name": "sentiment-analyzer",
                "timestamp": time.time()
            }
            
            # Send to AURORA
            response = requests.post(
                AURORA_API,
                json=payload,
                timeout=1
            )
            
            if response.status_code == 200:
                print(f"✅ Metrics sent to AURORA: {response_time:.0f}ms, {accuracy:.2%}")
            
        except Exception as e:
            # Don't fail the main prediction if AURORA is down
            print(f"⚠️  AURORA tracking failed: {e}")

# Usage
analyzer = SentimentAnalyzer()
result = analyzer.analyze("I love this product!")
print(result)
# Output: {'label': 'POSITIVE', 'score': 0.9998}
# AURORA automatically tracks this prediction!
```

---

## 🎯 Real-World Example: Expense Tracker AI

Here's how the expense tracker currently uses AURORA:

```python
# From backend/expense_api.py (already implemented)

from backend.agents.planner_agent import PlannerAgent
from backend.rag.memory_store import MemoryStore

# Initialize AURORA components
memory_store = MemoryStore(use_pinecone=False)
planner_agent = PlannerAgent(memory_store)

@router.post("/api/expenses")
async def create_expense(expense_data: Dict[str, Any]):
    # Prepare context for AI
    ai_context = {
        "expense": {
            "amount": expense.amount,
            "category": expense.category,
            "description": expense.description
        },
        "task": "analyze_expense"
    }
    
    # AURORA planner agent analyzes the expense
    # This is automatically monitored!
    ai_decision = await planner_agent.execute(ai_context)
    
    # Store AI suggestion
    expense.ai_suggestion = ai_decision.reasoning[:200]
    
    return {"success": True, "expense": expense}
```

---

## 📊 What AURORA Tracks

### Automatic Metrics

When you integrate AURORA, it automatically tracks:

1. **Response Time** (ms)
   - How long each prediction takes
   - Trends over time
   - Alerts if too slow

2. **Accuracy** (0.0 to 1.0)
   - Model confidence scores
   - Prediction quality
   - Alerts if degrading

3. **Error Rate** (%)
   - Failed predictions
   - Exception tracking
   - Alerts if too high

4. **Throughput** (requests/sec)
   - How many predictions per second
   - Load patterns
   - Capacity planning

---

## 🤖 What AURORA Does Automatically

### 1. **Detects Performance Issues**

```python
# AURORA monitors every prediction
result = model.predict(input_data)

# If response time > 375ms (1.5x baseline):
# AURORA automatically:
# - Implements response caching
# - Optimizes inference pipeline
# - Adjusts batch processing
```

### 2. **Improves Accuracy**

```python
# If accuracy drops below 90%:
# AURORA automatically:
# - Triggers model retraining
# - Updates feature engineering
# - Validates new model
# - Deploys if better
```

### 3. **Handles Errors**

```python
# If error rate > 5%:
# AURORA automatically:
# - Implements fallback strategies
# - Adds input validation
# - Improves error handling
# - Logs for analysis
```

---

## 🔍 Advanced Integration

### Track Multiple Models

```python
# model_registry.py
class ModelRegistry:
    def __init__(self):
        self.models = {
            "sentiment": SentimentModel(),
            "classification": ClassificationModel(),
            "generation": GenerationModel()
        }
    
    def predict(self, model_name, input_data):
        start_time = time.time()
        
        try:
            model = self.models[model_name]
            result = model.predict(input_data)
            
            # Track with model-specific metrics
            self.track_to_aurora(
                model_name=model_name,
                response_time=(time.time() - start_time) * 1000,
                accuracy=result.get('confidence', 0.95),
                error=False
            )
            
            return result
            
        except Exception as e:
            self.track_to_aurora(
                model_name=model_name,
                response_time=(time.time() - start_time) * 1000,
                accuracy=0.0,
                error=True
            )
            raise e
```

### Custom Metrics

```python
def track_custom_metrics(model_name, metrics):
    """Track custom metrics beyond the defaults"""
    payload = {
        "model_name": model_name,
        "response_time": metrics.get("response_time"),
        "accuracy": metrics.get("accuracy"),
        "error": metrics.get("error", False),
        
        # Custom metrics
        "custom": {
            "tokens_used": metrics.get("tokens"),
            "cost": metrics.get("cost"),
            "user_feedback": metrics.get("feedback"),
            "cache_hit": metrics.get("cache_hit", False)
        }
    }
    
    requests.post(AURORA_API, json=payload)
```

---

## 🎨 Integration Checklist

### ✅ Step-by-Step Integration

1. **Identify Your Model**
   - [ ] Locate your model prediction function
   - [ ] Understand input/output format
   - [ ] Identify accuracy metric

2. **Add Timing**
   - [ ] Add `start_time = time.time()` before prediction
   - [ ] Calculate `response_time` after prediction
   - [ ] Handle exceptions

3. **Calculate Accuracy**
   - [ ] Define accuracy metric (confidence, F1, etc.)
   - [ ] Implement calculation function
   - [ ] Return value between 0.0 and 1.0

4. **Send to AURORA**
   - [ ] Import requests library
   - [ ] Create payload with metrics
   - [ ] POST to `http://localhost:3000/api/aurora/record`
   - [ ] Handle failures gracefully

5. **Test Integration**
   - [ ] Run a prediction
   - [ ] Check AURORA monitor: http://localhost:5174/aurora-monitor
   - [ ] Verify metrics appear
   - [ ] Test error handling

---

## 🚀 Quick Start Template

Copy and paste this template:

```python
import time
import requests

AURORA_API = "http://localhost:3000/api/aurora/record"

class YourModel:
    def __init__(self):
        # Initialize your model here
        self.model = None  # Your model
    
    def predict(self, input_data):
        """Your prediction function with AURORA monitoring"""
        start_time = time.time()
        
        try:
            # YOUR MODEL PREDICTION HERE
            result = self.model.predict(input_data)
            
            # Calculate metrics
            response_time = (time.time() - start_time) * 1000
            accuracy = 0.95  # Replace with your accuracy calculation
            
            # Send to AURORA
            self._send_to_aurora(response_time, accuracy, False)
            
            return result
            
        except Exception as e:
            # Track errors
            response_time = (time.time() - start_time) * 1000
            self._send_to_aurora(response_time, 0.0, True)
            raise e
    
    def _send_to_aurora(self, response_time, accuracy, error):
        try:
            requests.post(AURORA_API, json={
                "response_time": response_time,
                "accuracy": accuracy,
                "error": error
            }, timeout=1)
        except:
            pass  # Don't fail if AURORA is down
```

---

## 📊 Viewing Your Metrics

After integration, visit:

```
http://localhost:5174/aurora-monitor
```

You'll see:
- Real-time response times
- Accuracy trends
- Error rates
- Automatic optimizations AURORA has applied

---

## 🎯 Example: Complete Integration

Let me create a working example for you:

```python
# example_integration.py
import time
import requests
import random

AURORA_API = "http://localhost:3000/api/aurora/record"

class DemoAIModel:
    """Demo AI model with AURORA integration"""
    
    def __init__(self):
        print("🤖 Initializing AI Model with AURORA monitoring...")
        self.predictions_count = 0
    
    def predict(self, text):
        """Predict sentiment with AURORA tracking"""
        self.predictions_count += 1
        start_time = time.time()
        
        try:
            # Simulate model inference
            time.sleep(random.uniform(0.1, 0.3))  # Simulate processing
            
            # Simulate prediction
            sentiment = "positive" if random.random() > 0.5 else "negative"
            confidence = random.uniform(0.85, 0.99)
            
            result = {
                "text": text,
                "sentiment": sentiment,
                "confidence": confidence
            }
            
            # Calculate metrics
            response_time = (time.time() - start_time) * 1000
            
            # Send to AURORA
            self._track_to_aurora(response_time, confidence, False)
            
            print(f"✅ Prediction #{self.predictions_count}: {sentiment} ({confidence:.2%}) - {response_time:.0f}ms")
            
            return result
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            self._track_to_aurora(response_time, 0.0, True)
            print(f"❌ Prediction failed: {e}")
            raise e
    
    def _track_to_aurora(self, response_time, accuracy, error):
        """Send metrics to AURORA"""
        try:
            payload = {
                "response_time": response_time,
                "accuracy": accuracy,
                "error": error
            }
            
            response = requests.post(AURORA_API, json=payload, timeout=1)
            
            if response.status_code == 200:
                print(f"   📊 Sent to AURORA: {response_time:.0f}ms, {accuracy:.2%}")
            
        except Exception as e:
            print(f"   ⚠️  AURORA unavailable: {e}")

# Demo usage
if __name__ == "__main__":
    model = DemoAIModel()
    
    # Make some predictions
    texts = [
        "I love this product!",
        "This is terrible",
        "Amazing experience",
        "Not good at all",
        "Absolutely fantastic!"
    ]
    
    for text in texts:
        result = model.predict(text)
        time.sleep(0.5)
    
    print("\n🎉 Done! Check AURORA Monitor at: http://localhost:5174/aurora-monitor")
```

---

## 🎊 Summary

### To Connect AURORA with Your AI Model:

1. **Wrap your model calls** with timing and metrics
2. **Send metrics to AURORA** via POST request
3. **Visit the monitor** to see real-time tracking
4. **Let AURORA optimize** automatically

### AURORA Will:
- ✅ Monitor every prediction
- ✅ Track performance trends
- ✅ Detect issues early
- ✅ **Automatically optimize** when needed
- ✅ Alert you proactively
- ✅ Learn and improve over time

---

**Ready to integrate?** Use the quick start template above and start monitoring your AI model with AURORA! 🚀

