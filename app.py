import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="FinPulse AI Ecosystem", layout="wide", initial_sidebar_state="expanded")

# 2. PREMIUM UI STYLING
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .main { background-color: #f8fafc; }
    h1 { color: #1e3a8a; font-weight: 800; font-family: 'Inter', sans-serif; }
    h3 { color: #334155; font-weight: 600; }
    span[data-baseweb="tag"] {
        background-color: #1e3a8a !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. DATA ENGINE
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df.columns = df.columns.str.strip().str.lower()
    if 'transactiondate' in df.columns:
        df['transactiondate'] = pd.to_datetime(df['transactiondate'])
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=80)
    st.title("Control Panel")
    st.write("---")
    
    currency_mode = st.radio("Reporting Currency:", ["USD ($)", "INR (₹)"], index=0)
    
    st.write("---")
    st.subheader("Filter by Channel")
    available_channels = df['transactionchannel'].unique()
    selected_channels = st.multiselect(
        "Select specific channels:",
        options=available_channels, 
        default=available_channels
    )
    st.write("---")
    st.caption("FinPulse AI v2.7")

# --- CURRENCY CALCULATIONS ---
conversion_rate = 83.5 
if currency_mode == "INR (₹)":
    df['displayamount'] = df['transactionamount'].abs() * conversion_rate
    symbol, unit = "₹", "Cr"
else:
    df['displayamount'] = df['transactionamount'].abs()
    symbol, unit = "$", "M"

filtered_df = df[df['transactionchannel'].isin(selected_channels)]

# --- MAIN DASHBOARD ---
st.title("🏦 FinPulse AI: Financial Intelligence Ecosystem")
st.markdown("#### Real-time Liquidity and Risk Monitoring")

# KPI Metrics
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Volume", f"{symbol}{filtered_df['displayamount'].sum()/1e6:.2f} {unit}")
with m2:
    st.metric("Avg Transaction", f"{symbol}{filtered_df['displayamount'].mean():,.0f}")
with m3:
    st.metric("Active Channels", len(selected_channels))

# --- ANALYTICS SECTION ---
st.write("")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Transaction Distribution")
    fig1 = px.pie(filtered_df, names='transactiontype', values='displayamount', hole=0.5,
                  color_discrete_sequence=['#1e3a8a', '#3b82f6', '#93c5fd', '#cbd5e1'])
    fig1.update_layout(height=400, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    st.subheader("Volume by Channel")
    fig2 = px.bar(filtered_df, x='transactionchannel', y='displayamount', 
                  color='transactionchannel', color_discrete_sequence=px.colors.qualitative.Prism)
    fig2.update_layout(height=400, showlegend=False, xaxis_title="", yaxis_title="Volume")
    st.plotly_chart(fig2, use_container_width=True)

# --- AI INSIGHTS & TREND FORECASTING ---
st.write("---")
st.subheader("🤖 AI Business Intelligence & Forecasting")

ai_col1, ai_col2 = st.columns([1, 2])

with ai_col1:
    st.markdown("#### 🚩 Anomaly Engine")
    threshold = filtered_df['displayamount'].mean() * 3
    anomalies = filtered_df[filtered_df['displayamount'] > threshold]
    
    if not anomalies.empty:
        st.error(f"Alert: {len(anomalies)} High-Risk entries detected!")
        st.info("Large value spikes flagged for review.")
    else:
        st.success("Financial patterns are stable.")

with ai_col2:
    # Smooth trend line logic
    df_daily = filtered_df.set_index('transactiondate').resample('D')['displayamount'].sum().fillna(0)
    smooth_trend = df_daily.rolling(window=7).mean()
    
    fig_line = px.line(smooth_trend, title="7-Day Market Volume Trend", labels={'value': 'Volume'})
    fig_line.update_traces(line_color='#1e3a8a', line_width=4)
    fig_line.update_layout(height=300)
    st.plotly_chart(fig_line, use_container_width=True)

st.write("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>Developed by Aarti | FinPulse AI Ecosystem v2.7</p>", unsafe_allow_html=True)
