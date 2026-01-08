# 🚀 Quick Start Guide - Smart Expense Tracker

## ⚡ 5-Minute Setup

Follow these steps to get the Smart Expense Tracker running with n8n email notifications!

---

## Step 1: Initialize the Database

```bash
cd /Users/mymac/Desktop/AURORA
python3 scripts/init_expense_db.py
```

**Expected Output:**
```
✅ Tables created successfully!
✅ Budgets created successfully!
✅ Sample expenses created successfully!
📊 EXPENSE TRACKER DATABASE SUMMARY
```

---

## Step 2: Start the Application

The application is already running! Check:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173

If not running, start it:
```bash
./start.sh
```

---

## Step 3: Access the Expense Tracker

Open your browser and go to:
```
http://localhost:5173/expenses
```

You should see:
- ✅ Dashboard with sample expenses
- ✅ Budget status for 7 categories
- ✅ Pie chart showing spending breakdown
- ✅ Recent expenses list

---

## Step 4: Set Up n8n (Email Notifications)

### 4.1 Install n8n

```bash
npm install -g n8n
```

### 4.2 Start n8n

```bash
n8n start
```

Access n8n at: **http://localhost:5678**

### 4.3 Create Workflow

1. Click **"New Workflow"**
2. Name it: `AURORA Budget Alert`

### 4.4 Add Webhook Node

1. Add **Webhook** node
2. Set **Path**: `expense-alert`
3. Set **HTTP Method**: `POST`
4. **Copy the webhook URL**: `http://localhost:5678/webhook/expense-alert`

### 4.5 Add Gmail Node

1. Add **Gmail** node (or **Send Email** for SMTP)
2. Connect Gmail account via OAuth2
3. Configure:
   - **To**: `{{ $json.to }}`  ← **This is the key expression!**
   - **Subject**: `{{ $json.subject }}`
   - **Email Type**: HTML
   - **Message**: Copy from `docs/N8N_EMAIL_SETUP.md`

### 4.6 Connect Nodes

Drag from **Webhook** → **Gmail**

### 4.7 Activate Workflow

Toggle the **Active** switch in the top-right

---

## Step 5: Configure AURORA Backend

Add the n8n webhook URL to your `.env` file:

```bash
echo "N8N_WEBHOOK_URL=http://localhost:5678/webhook/expense-alert" >> .env
```

**Restart the backend** (the start.sh script will pick up the new env variable automatically).

---

## Step 6: Test the Integration

### Test 1: Manual Webhook Test

```bash
curl -X POST http://localhost:5678/webhook/expense-alert \
  -H "Content-Type: application/json" \
  -d '{
    "to": "YOUR_EMAIL@example.com",
    "subject": "⚠️ Budget Alert: Food & Dining Limit Exceeded",
    "category": "Food & Dining",
    "spent": 550.00,
    "limit": 500.00,
    "percentage": 110.0,
    "timestamp": "2026-01-08T10:00:00Z",
    "message": "You have exceeded your Food & Dining budget!"
  }'
```

**Replace `YOUR_EMAIL@example.com` with your actual email!**

✅ You should receive an email within seconds!

### Test 2: Full Application Test

1. Go to http://localhost:5173/expenses
2. Click **"Add Expense"**
3. Enter:
   - **Amount**: `600`
   - **Category**: `Food & Dining`
   - **Description**: `Expensive dinner`
4. Click **"Add Expense"**

✅ You should see a notification in the app  
✅ You should receive an email alert!

---

## 📧 Key n8n Expression

In the Gmail/Email node, use this expression for the **"To Email"** field:

```
{{ $json.to }}
```

**Why?** This pulls the `to` field from the webhook payload, which contains the user's login email from Firebase!

---

## 🎯 How the Email Flow Works

```
User adds expense
    ↓
Backend checks if budget exceeded
    ↓
If YES → Trigger n8n webhook with user email
    ↓
n8n receives payload: { "to": "user@example.com", ... }
    ↓
Gmail node uses: {{ $json.to }}
    ↓
Email sent to user's login email!
```

---

## 🔍 Troubleshooting

### Backend not starting?

```bash
# Check if ports are in use
lsof -i :8000
lsof -i :5173

# Kill processes if needed
kill -9 <PID>

# Restart
./start.sh
```

### n8n webhook not triggering?

1. Check n8n is running: http://localhost:5678
2. Verify workflow is **Active** (toggle in top-right)
3. Check backend logs: `tail -f backend.log`
4. Verify `.env` has correct `N8N_WEBHOOK_URL`

### Email not sending?

1. Check n8n execution log (click "Executions" in sidebar)
2. Verify Gmail OAuth credentials
3. Check spam folder
4. Try SMTP instead of Gmail

### Database issues?

```bash
# Re-initialize database
rm aurora.db
python3 scripts/init_expense_db.py
```

---

## 📚 Additional Resources

- **Full Setup Guide**: `EXPENSE_TRACKER_README.md`
- **n8n Email Setup**: `docs/N8N_EMAIL_SETUP.md`
- **API Documentation**: http://localhost:8000/docs

---

## 🎉 You're All Set!

You now have:
- ✅ Smart Expense Tracker running locally
- ✅ AI-powered insights from AURORA agents
- ✅ Email notifications via n8n
- ✅ Dynamic user email handling

**Next Steps:**
1. Add more expenses
2. Test budget alerts
3. Customize email templates
4. Explore AI insights

---

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| Expense Tracker | http://localhost:5173/expenses |
| API Docs | http://localhost:8000/docs |
| n8n Dashboard | http://localhost:5678 |
| AURORA Dashboard | http://localhost:5173/dashboard |

---

**Built with ❤️ using AURORA, React, FastAPI, and n8n**
