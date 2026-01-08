# 📧 n8n Email Notification Setup for AURORA Expense Tracker

## Overview
This guide shows you how to set up **n8n** to send email notifications when users exceed their budget limits in the Smart Expense Tracker.

## 🎯 What This Solves
- **Automatic Email Alerts**: When a user exceeds their budget in any category, they receive an instant email
- **Dynamic User Emails**: Emails are sent to the user's login email (captured from Firebase authentication)
- **Real-time Integration**: The backend triggers n8n webhooks automatically

---

## 📋 Prerequisites
1. **n8n installed** (local or cloud)
2. **Email service** (Gmail, SendGrid, or any SMTP provider)
3. **AURORA backend running** on `http://localhost:8000`

---

## 🚀 Step-by-Step Setup

### Step 1: Install n8n (if not already installed)

```bash
# Using npm
npm install -g n8n

# Or using Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Step 2: Start n8n

```bash
n8n start
```

Access n8n at: **http://localhost:5678**

---

### Step 3: Create the Budget Alert Workflow

1. **Open n8n** in your browser
2. Click **"New Workflow"**
3. Name it: `AURORA Budget Alert Emailer`

---

### Step 4: Add Webhook Trigger

1. **Add Node** → Search for **"Webhook"**
2. Configure the webhook:
   - **HTTP Method**: `POST`
   - **Path**: `expense-alert`
   - **Authentication**: None (for testing)
   - **Response Mode**: Immediately
   - **Response Code**: 200

3. **Copy the Webhook URL** (e.g., `http://localhost:5678/webhook/expense-alert`)

4. **Save** the workflow

---

### Step 5: Add Email Node

1. **Add Node** → Search for **"Send Email"** or **"Gmail"**

#### Option A: Using Gmail

1. Select **Gmail** node
2. **Credentials**: 
   - Click "Create New Credentials"
   - Follow OAuth2 flow to connect your Gmail account
3. **Configure Email**:
   - **To**: `{{ $json.to }}` ← **This is the dynamic user email!**
   - **Subject**: `{{ $json.subject }}`
   - **Email Type**: HTML
   - **Message**: Use the template below

#### Option B: Using SMTP (SendGrid, etc.)

1. Select **Send Email** node
2. **Credentials**:
   - SMTP Host: `smtp.sendgrid.net` (or your provider)
   - SMTP Port: `587`
   - Username: Your SMTP username
   - Password: Your SMTP password
3. **Configure Email**:
   - **From Email**: `noreply@aurora.app`
   - **From Name**: `AURORA Expense Tracker`
   - **To Email**: `{{ $json.to }}` ← **Dynamic user email**
   - **Subject**: `{{ $json.subject }}`
   - **Email Type**: HTML
   - **Message**: Use the template below

---

### Step 6: Email Template (HTML)

Paste this in the **Message** field:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #0a0f1e;
            color: #ffffff;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: linear-gradient(135deg, #1a1f3a 0%, #0a0f1e 100%);
            border-radius: 16px;
            padding: 40px;
            border: 1px solid rgba(0, 212, 255, 0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo {
            font-size: 32px;
            font-weight: bold;
            background: linear-gradient(135deg, #00d4ff 0%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .alert-box {
            background: rgba(239, 68, 68, 0.1);
            border-left: 4px solid #ef4444;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
        }
        .stat {
            text-align: center;
        }
        .stat-value {
            font-size: 28px;
            font-weight: bold;
            color: #00d4ff;
        }
        .stat-label {
            font-size: 14px;
            color: #9ca3af;
            margin-top: 5px;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #6b7280;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🚀 AURORA</div>
            <p style="color: #9ca3af; margin-top: 10px;">Smart Expense Tracker</p>
        </div>
        
        <div class="alert-box">
            <h2 style="margin: 0 0 10px 0; color: #ef4444;">⚠️ Budget Alert!</h2>
            <p style="margin: 0; font-size: 16px;">{{ $json.message }}</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">${{ $json.spent }}</div>
                <div class="stat-label">Spent</div>
            </div>
            <div class="stat">
                <div class="stat-value">${{ $json.limit }}</div>
                <div class="stat-label">Budget Limit</div>
            </div>
            <div class="stat">
                <div class="stat-value">{{ $json.percentage }}%</div>
                <div class="stat-label">Usage</div>
            </div>
        </div>
        
        <p style="text-align: center; color: #9ca3af;">
            Category: <strong style="color: #00d4ff;">{{ $json.category }}</strong>
        </p>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="http://localhost:5173/expenses" 
               style="display: inline-block; background: linear-gradient(135deg, #00d4ff 0%, #a855f7 100%); 
                      color: white; padding: 12px 30px; text-decoration: none; 
                      border-radius: 8px; font-weight: bold;">
                View Expenses
            </a>
        </div>
        
        <div class="footer">
            <p>This is an automated message from AURORA Expense Tracker</p>
            <p>Sent at: {{ $json.timestamp }}</p>
        </div>
    </div>
</body>
</html>
```

---

### Step 7: Connect Nodes

1. **Drag** from the Webhook node to the Email node
2. **Activate** the workflow (toggle switch in top-right)

---

### Step 8: Update AURORA Backend

Add the n8n webhook URL to your `.env` file:

```bash
# n8n Webhook
N8N_WEBHOOK_URL=http://localhost:5678/webhook/expense-alert
```

**Restart your backend** to apply changes:

```bash
# Stop the current backend (Ctrl+C)
# Then restart
./start.sh
```

---

## 🧪 Testing the Integration

### Test 1: Manual Webhook Test

Use curl to test the n8n webhook:

```bash
curl -X POST http://localhost:5678/webhook/expense-alert \
  -H "Content-Type: application/json" \
  -d '{
    "to": "your-email@example.com",
    "subject": "⚠️ Budget Alert: Food & Dining Limit Exceeded",
    "category": "Food & Dining",
    "spent": 550.00,
    "limit": 500.00,
    "percentage": 110.0,
    "timestamp": "2026-01-08T10:00:00Z",
    "message": "You have exceeded your Food & Dining budget! You'\''ve spent $550.00 out of $500.00 (110.0%)"
  }'
```

**Expected Result**: You should receive an email at `your-email@example.com`

---

### Test 2: Full Application Test

1. **Open AURORA**: http://localhost:5173/expenses
2. **Login** with Firebase (email will be captured)
3. **Add an expense** that exceeds a budget:
   - Amount: `$600`
   - Category: `Food & Dining`
   - Description: `Expensive dinner`
4. **Check your email** (the one you used to login)

---

## 🔑 Key Expression for Dynamic User Email

### In the Backend (`expense_api.py`)

The user email is captured from the expense data:

```python
user_email=expense_data.get("userEmail", "user@example.com")
```

### In the Frontend (`ExpenseTracker.tsx`)

The user email is retrieved from localStorage (set during Firebase login):

```typescript
const email = localStorage.getItem('userEmail') || 'user@example.com';
setUserEmail(email);
```

And sent with each expense:

```typescript
const newExpense = {
    amount: parseFloat(amount),
    category,
    description,
    date: new Date().toISOString(),
    userEmail // ← Dynamic user email from login
};
```

### In n8n (Email Node)

Use this expression in the **"To Email"** field:

```
{{ $json.to }}
```

This pulls the `to` field from the webhook payload, which contains the user's login email.

---

## 🎨 Advanced: Multiple Recipients

If you want to send to multiple emails (e.g., user + admin):

### Backend Modification

```python
payload = {
    "to": [user_email, "admin@aurora.app"],  # List of emails
    "subject": f"⚠️ Budget Alert: {category} Limit Exceeded",
    # ... rest of payload
}
```

### n8n Expression

```
{{ $json.to.join(', ') }}
```

---

## 📊 Workflow Execution Log

In n8n, you can view all executions:

1. Click **"Executions"** in the left sidebar
2. See all triggered webhooks
3. Debug any failed emails

---

## 🔒 Production Considerations

### 1. Secure the Webhook

Add authentication to your n8n webhook:

```python
# In expense_api.py
headers = {
    "Authorization": f"Bearer {os.getenv('N8N_WEBHOOK_TOKEN')}"
}

response = await client.post(
    N8N_WEBHOOK_URL,
    json=payload,
    headers=headers,
    timeout=10.0
)
```

### 2. Use Environment Variables

```bash
# .env
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/expense-alert
N8N_WEBHOOK_TOKEN=your-secret-token
```

### 3. Rate Limiting

Add rate limiting to prevent spam:

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@router.post("/expenses")
@limiter.limit("10/minute")
async def create_expense(...):
    # ...
```

---

## 🎯 Summary

You now have a **fully functional email notification system** that:

✅ Sends emails to the **user's login email** (dynamic)  
✅ Triggers automatically when budgets are exceeded  
✅ Uses **n8n** for flexible workflow automation  
✅ Integrates seamlessly with **AURORA's AI agents**  

**Expression for Dynamic Email**: `{{ $json.to }}`

This pulls the email from the webhook payload, which is set to the user's Firebase login email!

---

## 📞 Troubleshooting

### Email not sending?

1. Check n8n execution log
2. Verify Gmail OAuth credentials
3. Check SMTP settings
4. Ensure webhook URL is correct in `.env`

### User email not captured?

1. Verify Firebase login sets `localStorage.setItem('userEmail', email)`
2. Check browser console for the email value
3. Inspect the API request payload

### Webhook not triggering?

1. Check backend logs for n8n request
2. Verify `N8N_WEBHOOK_URL` in `.env`
3. Ensure n8n workflow is activated

---

**Happy Budgeting! 💰**
