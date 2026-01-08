import requests
import time

# n8n default webhook URL
# If you are testing in the n8n UI, you might need to use 'webhook-test' instead of 'webhook'
WEBHOOK_URL = "https://aurora123.app.n8n.cloud/webhook/expense-alert"
TEST_WEBHOOK_URL = "https://aurora123.app.n8n.cloud/webhook-test/expense-alert"

print("🚀 Testing n8n Budget Alert Connection...")

payload = {
    "to": "sushiielanand8@gmail.com",
    "subject": "🔔 Test Alert from Aurora",
    "category": "Testing",
    "spent": 150.00,
    "limit": 100.00,
    "percentage": 150.0,
    "timestamp": "2026-01-08T12:00:00",
    "message": "This is a test message to verify n8n connectivity."
}

def try_webhook(url, name):
    print(f"\n📡 Trying {name} URL: {url}...")
    try:
        response = requests.post(url, json=payload, timeout=2)
        if response.status_code == 200:
            print(f"   ✅ SUCCESS! n8n received the data.")
            print(f"   Response: {response.text}")
            return True
        else:
            print(f"   ❌ Connected, but n8n returned error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Refused. Is n8n running?")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

# Try Production URL first
if not try_webhook(WEBHOOK_URL, "Production"):
    # Try Test URL (common when editing workflow)
    print("   (Tip: If you are in the n8n Editor, click 'Execute Node' on the Webhook and use the Test URL)")
    try_webhook(TEST_WEBHOOK_URL, "Test Mode")

print("\n📋 Next Steps:")
print("1. Ensure n8n is running: 'npx n8n'")
print("2. Import 'n8n-workflow-budget-alert.json'")
print("3. Ensure the Webhook path is set to 'expense-alert'")
print("4. Click 'Activate' (top right) in n8n")
