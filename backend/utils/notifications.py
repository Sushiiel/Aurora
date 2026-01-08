import os
import httpx
from datetime import datetime

# Use the production URL provided by the user
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://aurora123.app.n8n.cloud/webhook/expense-alert")
DEFAULT_ALERT_EMAIL = "sushiielanand8@gmail.com"

async def send_system_alert(title: str, message: str, category: str = "System Alert", email: str = None):
    """
    Send a system alert via the n8n webhook (reusing the budget alert workflow).
    """
    target_email = email or DEFAULT_ALERT_EMAIL
    
    payload = {
        "to": target_email,
        "subject": f"🚨 AURORA System Alert: {title}",
        "category": category,
        "spent": 0,  # Placeholder for budget workflow
        "limit": 0,  # Placeholder for budget workflow
        "percentage": 0, # Placeholder
        "timestamp": datetime.utcnow().isoformat(),
        "message": message
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                N8N_WEBHOOK_URL,
                json=payload,
                timeout=5.0
            )
            if response.status_code == 200:
                print(f"✅ Alert sent to {target_email}: {title}")
            else:
                print(f"❌ Failed to send alert: {response.text}")
    except Exception as e:
        print(f"⚠️ Error sending alert: {e}")
