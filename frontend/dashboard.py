"""
AURORA Streamlit Dashboard
Modern, interactive UI for monitoring and controlling the AURORA system
"""
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="AURORA - AI Systems Control",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for black and blue theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00d4ff !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00d4ff;
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #8b9dc3;
        font-size: 0.9rem;
    }
    
    /* Cards */
    .css-1r6slb0 {
        background: rgba(26, 31, 58, 0.6);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1429 0%, #1a1f3a 100%);
        border-right: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0066ff 0%, #00d4ff 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 212, 255, 0.3);
    }
    
    /* Text */
    p, span, label {
        color: #c5d0e6;
    }
    
    /* Dataframe */
    .dataframe {
        background: rgba(26, 31, 58, 0.6);
        color: #c5d0e6;
    }
    
    /* Success/Error boxes */
    .stSuccess {
        background: rgba(0, 255, 136, 0.1);
        border-left: 4px solid #00ff88;
    }
    
    .stError {
        background: rgba(255, 68, 68, 0.1);
        border-left: 4px solid #ff4444;
    }
    
    .stWarning {
        background: rgba(255, 187, 0, 0.1);
        border-left: 4px solid #ffbb00;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(26, 31, 58, 0.6);
        border-radius: 8px 8px 0 0;
        color: #8b9dc3;
        border: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0066ff 0%, #00d4ff 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = "http://localhost:8000"

# Helper functions
def get_health_status():
    """Get system health status"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def get_latest_metrics():
    """Get latest model metrics"""
    try:
        response = requests.get(f"{API_URL}/api/metrics/latest?limit=50", timeout=5)
        return response.json().get("metrics", []) if response.status_code == 200 else []
    except:
        return []

def get_recent_decisions():
    """Get recent agent decisions"""
    try:
        response = requests.get(f"{API_URL}/api/decisions?limit=20", timeout=5)
        return response.json().get("decisions", []) if response.status_code == 200 else []
    except:
        return []

def trigger_analysis(context):
    """Trigger system analysis"""
    try:
        response = requests.post(f"{API_URL}/api/analyze", json=context, timeout=30)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        return {"error": str(e)}

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 🚀 AURORA")
    st.markdown("### Agentic Unified Reasoning & Optimization Runtime")
with col2:
    health = get_health_status()
    if health and health.get("status") == "healthy":
        st.success("🟢 System Operational")
    else:
        st.error("🔴 System Offline")

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    
    st.markdown("### Quick Actions")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### System Info")
    if health:
        st.json(health.get("components", {}))
    
    st.markdown("---")
    
    st.markdown("### Agent Configuration")
    auto_execute = st.checkbox("Auto-execute approved actions", value=False)
    confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.85, 0.05)

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🤖 Agents", "📈 Metrics", "🧠 Memory"])

with tab1:
    st.markdown("## System Overview")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = get_latest_metrics()
    decisions = get_recent_decisions()
    
    with col1:
        st.metric(
            label="Active Models",
            value=len(set(m.get("model_name") for m in metrics)) if metrics else 0,
            delta="Operational"
        )
    
    with col2:
        avg_accuracy = sum(m.get("accuracy", 0) for m in metrics[:10]) / max(len(metrics[:10]), 1)
        st.metric(
            label="Avg Accuracy",
            value=f"{avg_accuracy:.2%}",
            delta="+2.3%" if avg_accuracy > 0.85 else "-1.2%"
        )
    
    with col3:
        avg_latency = sum(m.get("latency_ms", 0) for m in metrics[:10]) / max(len(metrics[:10]), 1)
        st.metric(
            label="Avg Latency",
            value=f"{avg_latency:.0f}ms",
            delta="-15ms" if avg_latency < 500 else "+25ms"
        )
    
    with col4:
        approved_decisions = sum(1 for d in decisions if d.get("approved"))
        st.metric(
            label="Decisions (24h)",
            value=len(decisions),
            delta=f"{approved_decisions} approved"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Model Performance Trend")
        if metrics:
            df = pd.DataFrame(metrics)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(len(df))),
                y=df['accuracy'],
                mode='lines+markers',
                name='Accuracy',
                line=dict(color='#00d4ff', width=3),
                marker=dict(size=8)
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#c5d0e6'),
                xaxis=dict(gridcolor='rgba(139, 157, 195, 0.1)'),
                yaxis=dict(gridcolor='rgba(139, 157, 195, 0.1)', range=[0, 1]),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No metrics data available")
    
    with col2:
        st.markdown("### ⚡ Latency Distribution")
        if metrics:
            df = pd.DataFrame(metrics)
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=list(range(len(df))),
                y=df['latency_ms'],
                marker=dict(
                    color=df['latency_ms'],
                    colorscale='Blues',
                    showscale=False
                )
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#c5d0e6'),
                xaxis=dict(gridcolor='rgba(139, 157, 195, 0.1)'),
                yaxis=dict(gridcolor='rgba(139, 157, 195, 0.1)'),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No latency data available")

with tab2:
    st.markdown("## 🤖 Agent Activity")
    
    # Manual trigger
    st.markdown("### Trigger Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        model_accuracy = st.slider("Model Accuracy", 0.0, 1.0, 0.75, 0.01)
        latency_ms = st.number_input("Latency (ms)", 0, 5000, 450)
    
    with col2:
        drift_detected = st.checkbox("Data Drift Detected", value=False)
        drift_score = st.slider("Drift Score", 0.0, 1.0, 0.3, 0.01)
    
    if st.button("🚀 Run Analysis", use_container_width=True):
        with st.spinner("Analyzing system state..."):
            context = {
                "model_metrics": {
                    "accuracy": model_accuracy,
                    "latency_ms": latency_ms
                },
                "data_drift": {
                    "detected": drift_detected,
                    "score": drift_score
                },
                "system_load": {
                    "cpu_usage": 0.6,
                    "memory_usage": 0.5,
                    "gpu_usage": 0.4
                }
            }
            
            result = trigger_analysis(context)
            
            if result and "error" not in result:
                st.success("✅ Analysis completed successfully!")
                
                # Display results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("#### 📋 Planner Decision")
                    planner = result.get("planner_decision", {})
                    st.json(planner)
                
                with col2:
                    st.markdown("#### ✅ Critic Evaluation")
                    critic = result.get("critic_decision", {})
                    st.json(critic)
                
                with col3:
                    st.markdown("#### ⚡ Execution Result")
                    execution = result.get("execution_result")
                    if execution:
                        st.json(execution)
                    else:
                        st.info("No action executed")
            else:
                st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
    
    st.markdown("---")
    
    # Recent decisions
    st.markdown("### Recent Decisions")
    if decisions:
        df = pd.DataFrame(decisions)
        st.dataframe(
            df[['timestamp', 'agent_type', 'decision_type', 'confidence', 'approved', 'executed']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No recent decisions")

with tab3:
    st.markdown("## 📈 Detailed Metrics")
    
    if metrics:
        df = pd.DataFrame(metrics)
        
        # Model selector
        models = df['model_name'].unique()
        selected_model = st.selectbox("Select Model", models)
        
        model_df = df[df['model_name'] == selected_model]
        
        # Metrics table
        st.dataframe(
            model_df[['timestamp', 'model_version', 'accuracy', 'latency_ms', 'data_drift_score']],
            use_container_width=True,
            hide_index=True
        )
        
        # Drift analysis
        st.markdown("### Drift Analysis")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(model_df))),
            y=model_df['data_drift_score'],
            mode='lines+markers',
            name='Drift Score',
            line=dict(color='#ff6b6b', width=3),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.2)'
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c5d0e6'),
            xaxis=dict(gridcolor='rgba(139, 157, 195, 0.1)'),
            yaxis=dict(gridcolor='rgba(139, 157, 195, 0.1)', range=[0, 1]),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No metrics data available")

with tab4:
    st.markdown("## 🧠 Memory & RAG")
    
    st.markdown("### Search System Memory")
    
    query = st.text_input("Enter search query", placeholder="e.g., 'model retraining with high drift'")
    
    if st.button("🔍 Search", use_container_width=True):
        if query:
            with st.spinner("Searching memory..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/memory/search",
                        json={"query": query, "top_k": 5},
                        timeout=10
                    )
                    if response.status_code == 200:
                        results = response.json().get("results", [])
                        if results:
                            st.success(f"Found {len(results)} relevant memories")
                            for i, result in enumerate(results):
                                with st.expander(f"Result {i+1} (Score: {result.get('score', 0):.2f})"):
                                    st.json(result)
                        else:
                            st.info("No results found")
                    else:
                        st.error("Search failed")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a search query")
    
    st.markdown("---")
    
    # Memory stats
    st.markdown("### Memory Statistics")
    try:
        response = requests.get(f"{API_URL}/api/memory/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Backend", stats.get("backend", "unknown").upper())
            with col2:
                st.metric("Total Memories", stats.get("total_memories", 0))
            with col3:
                st.metric("Dimension", stats.get("dimension", 0))
    except:
        st.error("Failed to fetch memory stats")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #8b9dc3; padding: 2rem;'>"
    "AURORA v1.0.0 | Agentic AI Systems Engineering | "
    "<a href='#' style='color: #00d4ff;'>Documentation</a>"
    "</div>",
    unsafe_allow_html=True
)
