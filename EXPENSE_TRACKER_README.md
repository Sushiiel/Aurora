# 🎯 Smart Expense Tracker - Real-Time Problem-Solving Application

## 📌 What Problem Does This Solve?

**Problem**: People struggle to track their spending and often exceed their budgets without realizing it until it's too late.

**Solution**: A **Smart Expense Tracker** that:
- ✅ Tracks expenses in real-time
- ✅ Uses **AI (AURORA agents)** to provide intelligent insights
- ✅ Sends **instant email alerts** when budgets are exceeded
- ✅ Emails are sent to the **user's login email** (captured from Firebase authentication)
- ✅ Integrates with **n8n** for flexible workflow automation

---

## 🌟 Why This Application is Familiar

Everyone deals with expenses! This app solves a **universal problem**:
- 💰 **Personal Finance**: Track daily spending
- 🏢 **Business Expenses**: Monitor team budgets
- 👨‍👩‍👧‍👦 **Family Budgeting**: Manage household expenses
- 🎓 **Student Budgets**: Control limited funds

---

## 🚀 How We're Solving the Problem

### 1. **AI-Powered Expense Analysis**
- **AURORA Planner Agent** analyzes each expense
- Provides smart suggestions (e.g., "Consider cheaper alternatives")
- Learns from spending patterns

### 2. **Real-Time Budget Monitoring**
- Tracks spending across 7 categories:
  - Food & Dining
  - Transportation
  - Shopping
  - Entertainment
  - Bills & Utilities
  - Healthcare
  - Other

### 3. **Instant Email Notifications via n8n**
- When you exceed a budget, **n8n triggers an email**
- Email is sent to **your login email** (from Firebase)
- Beautiful HTML email with spending breakdown

### 4. **Visual Insights**
- Pie charts showing category breakdown
- Budget status bars with color-coded alerts
- Real-time expense feed

---

## 🏗️ Architecture

```
┌─────────────────┐
│  User Login     │ ← Firebase Auth (captures email)
│  (Firebase)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  React Frontend │ ← Expense Tracker UI
│  (Vite + React) │
└────────┬────────┘
         │ API Calls
         ▼
┌─────────────────┐
│  FastAPI Backend│ ← AURORA + Expense API
│  (Python)       │
└────────┬────────┘
         │
         ├──────────────┐
         │              │
         ▼              ▼
┌─────────────────┐  ┌─────────────────┐
│  AURORA Agents  │  │  n8n Webhook    │
│  (AI Analysis)  │  │  (Email Alerts) │
└─────────────────┘  └─────────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  User's Email   │
                     │  (Gmail/SMTP)   │
                     └─────────────────┘
```

---

## 🔑 Key Feature: Dynamic User Email

### How It Works

1. **User Logs In** (Firebase Authentication)
   ```typescript
   // In Login.tsx
   const email = user.email;
   localStorage.setItem('userEmail', email);
   ```

2. **Email is Captured** in Expense Tracker
   ```typescript
   // In ExpenseTracker.tsx
   const userEmail = localStorage.getItem('userEmail');
   ```

3. **Email is Sent with Each Expense**
   ```typescript
   const newExpense = {
       amount: 100,
       category: "Food & Dining",
       description: "Lunch",
       userEmail: userEmail  // ← Dynamic user email
   };
   ```

4. **Backend Triggers n8n Webhook**
   ```python
   # In expense_api.py
   payload = {
       "to": user_email,  # ← User's login email
       "subject": "Budget Alert!",
       "category": category,
       "spent": spent,
       "limit": limit
   }
   
   await client.post(N8N_WEBHOOK_URL, json=payload)
   ```

5. **n8n Sends Email to User**
   ```
   To Email: {{ $json.to }}  ← Expression pulls user email
   ```

---

## 📊 n8n Expression for Dynamic Email

### In the n8n Email Node:

**Field**: To Email  
**Expression**: `{{ $json.to }}`

This expression:
- Reads the `to` field from the webhook payload
- The `to` field contains the user's login email
- Email is sent to the correct user automatically

### Example Payload to n8n:

```json
{
  "to": "john.doe@example.com",  ← User's login email
  "subject": "⚠️ Budget Alert: Food & Dining Limit Exceeded",
  "category": "Food & Dining",
  "spent": 550.00,
  "limit": 500.00,
  "percentage": 110.0,
  "message": "You have exceeded your Food & Dining budget!"
}
```

---

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Recharts** - Data visualization
- **Firebase Auth** - User authentication

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database
- **AURORA Agents** - AI-powered insights
- **httpx** - Async HTTP client

### Integration
- **n8n** - Workflow automation
- **Gmail/SMTP** - Email delivery

---

## 🚀 Quick Start

### 1. Start the Application

```bash
cd /Users/mymac/Desktop/AURORA
./start.sh
```

This starts:
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:5173`

### 2. Set Up n8n

```bash
# Install n8n
npm install -g n8n

# Start n8n
n8n start
```

Access n8n: `http://localhost:5678`

### 3. Configure n8n Webhook

Follow the guide: [`docs/N8N_EMAIL_SETUP.md`](./N8N_EMAIL_SETUP.md)

### 4. Update Environment Variables

```bash
# Add to .env
N8N_WEBHOOK_URL=http://localhost:5678/webhook/expense-alert
```

### 5. Access the Expense Tracker

```
http://localhost:5173/expenses
```

---

## 🧪 Testing the Application

### Test 1: Add an Expense

1. Go to `http://localhost:5173/expenses`
2. Click **"Add Expense"**
3. Enter:
   - Amount: `$100`
   - Category: `Food & Dining`
   - Description: `Lunch at restaurant`
4. Click **"Add Expense"**

### Test 2: Trigger Budget Alert

1. Set a budget for "Food & Dining": `$500`
2. Add expenses totaling more than `$500`
3. **Check your email** (the one you used to login)
4. You should receive a budget alert email

### Test 3: View AI Insights

- Each expense shows an AI suggestion
- Example: "Consider meal prepping to save money"

---

## 📧 Email Notification Flow

```
User adds expense → Backend checks budget → Budget exceeded?
                                                    │
                                                    ▼ YES
                                          Trigger n8n webhook
                                                    │
                                                    ▼
                                          n8n receives payload
                                                    │
                                                    ▼
                                          Extract user email: {{ $json.to }}
                                                    │
                                                    ▼
                                          Send email via Gmail/SMTP
                                                    │
                                                    ▼
                                          User receives alert email
```

---

## 🎨 Features Showcase

### 1. **Dashboard Overview**
- Total spent this month
- Budget usage percentage
- Number of expenses tracked
- Email notification count

### 2. **Category Breakdown**
- Interactive pie chart
- Visual spending distribution
- Click to filter expenses

### 3. **Budget Status**
- Progress bars for each category
- Color-coded alerts (green/red)
- Real-time updates

### 4. **Recent Expenses**
- Chronological list
- AI suggestions per expense
- Quick delete option

### 5. **Email Notifications**
- Beautiful HTML emails
- Spending breakdown
- Direct link to app

---

## 🔧 Customization

### Change Budget Limits

```typescript
// In ExpenseTracker.tsx
const [monthlyBudget, setMonthlyBudget] = useState(5000);
```

### Add New Categories

```typescript
const CATEGORIES = [
    'Food & Dining',
    'Transportation',
    'Shopping',
    'Entertainment',
    'Bills & Utilities',
    'Healthcare',
    'Travel',  // ← Add new category
    'Other'
];
```

### Customize Email Template

Edit the HTML in `docs/N8N_EMAIL_SETUP.md`

---

## 📈 Future Enhancements

- [ ] **Recurring Expenses**: Auto-add monthly bills
- [ ] **Budget Recommendations**: AI suggests optimal budgets
- [ ] **Expense Forecasting**: Predict future spending
- [ ] **Multi-Currency Support**: Track expenses in different currencies
- [ ] **Receipt Scanning**: OCR to extract expense details
- [ ] **Shared Budgets**: Family/team expense tracking
- [ ] **Export Reports**: PDF/CSV expense reports

---

## 🎯 Why This Solution is Powerful

### 1. **Real-Time Problem Solving**
- Immediate feedback on spending
- Prevents budget overruns
- Actionable insights

### 2. **AI-Powered Intelligence**
- AURORA agents analyze patterns
- Smart categorization
- Personalized recommendations

### 3. **Seamless Integration**
- n8n for flexible workflows
- Firebase for authentication
- Easy to extend

### 4. **User-Centric Design**
- Beautiful, modern UI
- Intuitive interactions
- Mobile-responsive

---

## 📞 Support

For issues or questions:
1. Check `docs/N8N_EMAIL_SETUP.md` for n8n setup
2. Review backend logs: `backend.log`
3. Check browser console for frontend errors

---

## 🎉 Summary

You now have a **production-ready expense tracking application** that:

✅ Solves a **real, familiar problem** (expense management)  
✅ Uses **AI** for intelligent insights (AURORA agents)  
✅ Sends **email notifications** via n8n  
✅ Emails go to the **user's login email** (dynamic)  
✅ Runs **locally** for testing  
✅ Can be **deployed** to production  

**Key Expression**: `{{ $json.to }}` in n8n pulls the user's email from the webhook payload!

---

**Built with ❤️ using AURORA, React, FastAPI, and n8n**
