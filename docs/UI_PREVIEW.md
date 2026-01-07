# 🎨 AURORA UI Preview

This is a preview of the AURORA dashboard design.

## Dashboard Features

### Color Scheme
- **Background**: Deep space gradient (#0a0e27 → #1a1f3a)
- **Primary Accent**: Electric blue (#00d4ff)
- **Secondary**: Royal blue (#0066ff)
- **Text**: Light blue-gray (#c5d0e6)
- **Success**: Green (#00ff88)
- **Cards**: Glassmorphism with translucent backgrounds

### Layout Components

#### Header
- AURORA logo with rocket emoji
- System status indicator (green = operational)
- Navigation tabs (Dashboard, Agents, Metrics, Memory)

#### Sidebar
- Control panel with refresh button
- System uptime
- Resource usage (CPU, Memory)
- Quick actions

#### Main Dashboard
1. **Metrics Row** (4 cards)
   - Active Models
   - Average Accuracy
   - Average Latency
   - Recent Decisions

2. **Charts Section**
   - Model Performance Trend (line chart)
   - Latency Distribution (bar chart)

### Design Principles
✨ Modern glassmorphism effects
✨ Smooth gradients and transitions
✨ Interactive hover states
✨ Professional typography
✨ Clear data hierarchy
✨ Responsive layout

## Actual Implementation

The dashboard is built with Streamlit and includes:
- Real-time data updates
- Interactive Plotly charts
- Custom CSS styling
- Responsive design
- Dark theme optimized for long sessions

Run `./start.sh` and visit http://localhost:8501 to see it live!
