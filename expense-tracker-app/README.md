# 💰 AURORA Expense Tracker

> Smart expense tracking with AI-powered insights and real-time budget alerts

## 🌟 Features

- ✅ **AI-Powered Analysis**: Get intelligent suggestions for every expense
- ✅ **Real-Time Budget Alerts**: Email notifications when budgets are exceeded
- ✅ **Beautiful Dashboard**: Visual insights with charts and graphs
- ✅ **Firebase Authentication**: Secure login and signup
- ✅ **AURORA Monitoring**: See how AURORA optimizes AI model performance

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ installed
- Backend running on port 8000
- Firebase account (for authentication)

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at **http://localhost:5174**

### Using the Startup Script

```bash
./start-expense-tracker.sh
```

## 📱 Application Pages

### 1. Login (`/`)
- Firebase authentication
- Sign in / Sign up
- Beautiful gradient UI

### 2. Expense Tracker (`/expenses`)
- Add expenses with AI suggestions
- View spending by category
- Track budget usage
- Real-time notifications

### 3. AURORA Monitor (`/aurora-monitor`)
- Real-time model performance metrics
- Automatic optimization insights
- Performance charts and trends
- Learn how AURORA solves problems

## 🔧 Configuration

### Firebase Setup

Edit `src/config/firebase.ts`:

```typescript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

### Backend API

The app connects to the backend at `http://localhost:8000` via Vite proxy.

Endpoints used:
- `POST /api/expenses` - Create expense
- `GET /api/expenses` - Get expenses
- `GET /api/budgets` - Get budgets
- `GET /api/aurora/metrics` - Get model metrics

## 🎨 Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Recharts** - Data visualization
- **Firebase** - Authentication
- **Lucide React** - Icons

## 📊 Features in Detail

### Expense Tracking
- Add expenses with amount, category, and description
- AI generates smart suggestions for each expense
- Delete expenses with budget recalculation
- Real-time budget monitoring

### Budget Management
- Set limits for 7 categories:
  - Food & Dining
  - Transportation
  - Shopping
  - Entertainment
  - Bills & Utilities
  - Healthcare
  - Other
- Visual progress bars
- Color-coded alerts (green/red)

### AI Insights
- Powered by AURORA planner agent
- Contextual suggestions based on spending patterns
- Smart categorization
- Personalized recommendations

### Email Notifications
- Automatic alerts when budgets exceeded
- Sent to user's login email
- Powered by n8n workflow automation
- Beautiful HTML email templates

### AURORA Monitor
- Real-time performance metrics
- Response time tracking
- Model accuracy monitoring
- Automatic optimization actions
- Performance charts and trends

## 🏗️ Project Structure

```
expense-tracker-app/
├── src/
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point
│   ├── index.css            # Global styles
│   ├── pages/
│   │   ├── Login.tsx        # Authentication page
│   │   ├── ExpenseTracker.tsx  # Main expense tracker
│   │   └── AuroraMonitor.tsx   # AURORA monitoring dashboard
│   ├── utils/
│   │   └── api.ts           # API utilities
│   └── config/
│       └── firebase.ts      # Firebase configuration
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── start-expense-tracker.sh
```

## 🔐 Environment Variables

No environment variables needed for the frontend. All configuration is in:
- `src/config/firebase.ts` - Firebase credentials
- `vite.config.ts` - API proxy settings

## 🚀 Building for Production

```bash
# Build the app
npm run build

# Preview production build
npm run preview
```

The built files will be in the `dist/` directory.

## 🎯 How AURORA Enhances This App

### Traditional Expense Tracker:
- Tracks expenses ✅
- Shows budgets ✅
- Sends alerts ✅

### AURORA-Powered Expense Tracker:
- Tracks expenses ✅
- Shows budgets ✅
- Sends alerts ✅
- **AI-powered suggestions** ⭐
- **Automatic performance optimization** ⭐
- **Real-time model monitoring** ⭐
- **Predictive issue detection** ⭐
- **Self-healing AI models** ⭐

## 📈 Performance

- **First Load**: < 2s
- **Route Changes**: < 100ms
- **API Calls**: < 300ms
- **AI Suggestions**: < 500ms (with AURORA optimization)

## 🤝 Contributing

This is part of the AURORA project. See the main AURORA repository for contribution guidelines.

## 📄 License

Part of the AURORA project.

## 🆘 Support

For issues or questions:
1. Check the main AURORA documentation
2. Review `EXPENSE_TRACKER_SEPARATION_GUIDE.md`
3. Visit the AURORA Monitor page for performance insights

## 🎉 What Makes This Special

This isn't just an expense tracker - it's a demonstration of how AURORA's intelligent automation can enhance any application:

- **Self-Optimizing**: AI models improve themselves
- **Self-Healing**: Performance issues are fixed automatically
- **Self-Learning**: Gets better with every use

**Traditional apps require constant maintenance.**  
**AURORA-powered apps maintain themselves.**

---

Built with ❤️ using AURORA - Intelligent AI Optimization
