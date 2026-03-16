import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE SETUP
st.set_page_config(page_title="FinPulse AI Ecosystem", layout="wide")

# 2. ADVANCED UI STYLING
st.markdown("""
    <style>
    .stMetric {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .main { background-color: #f8f9fa; }
    h1 { color: #1e3a8a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
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

# SIDEBAR CUSTOMIZATION
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=70)
    st.markdown("## Control Center")
    currency_mode = st.radio("Reporting Currency:", ["USD ($)", "INR (₹)"])
    selected_channels = st.multiselect("Select Channels:", options=df['transactionchannel'].unique(), default=df['transactionchannel'].unique())

# CURRENCY LOGIC
conversion_rate = 83.5 
if currency_mode == "INR (₹)":
    df['displayamount'] = df['transactionamount'].abs() * conversion_rate
    symbol, unit = "₹", "Cr"
else:
    df['displayamount'] = df['transactionamount'].abs()
    symbol, unit = "$", "M"

filtered_df = df[df['transactionchannel'].isin(selected_channels)]

# --- DASHBOARD HEADER ---
st.title("🏦 FinPulse AI Ecosystem")
st.markdown("#### High-Fidelity Financial Intelligence")

# --- TOP METRICS ---
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Volume", f"{symbol}{filtered_df['displayamount'].sum()/1e6:.2f} {unit}")
with m2:
    st.metric("Avg Ticket Size", f"{symbol}{filtered_df['displayamount'].mean():,.0f}")
with m3:
    st.metric("Total Transactions", f"{len(filtered_df):,}")

# --- ANALYTICS SECTION ---
st.write("---")
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("Transaction Distribution")
    fig1 = px.pie(filtered_df, names='transactiontype', values='displayamount', hole=0.5,
                  color_discrete_sequence=['#1e3a8a', '#3b82f6', '#93c5fd'])
    fig1.update_layout(height=350, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Volume by Channel")
    fig2 = px.bar(filtered_df, x='transactionchannel', y='displayamount', 
                  color='transactionchannel', color_discrete_sequence=px.colors.qualitative.Safe)
    fig2.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# --- AI INSIGHTS & TRENDS (FIXED LOOK) ---
st.write("---")
st.subheader("🤖 AI Intelligence & Trend Forecasting")
col_ai1, col_ai2 = st.columns([1, 2])

with col_ai1:
    st.info("**Anomaly Detection Summary**")
    threshold = filtered_df['displayamount'].mean() * 3
    anomalies = filtered_df[filtered_df['displayamount'] > threshold]
    if not anomalies.empty:
        st.warning(f"Detected {len(anomalies)} high-risk anomalies.")
        st.button("Download Forensic Report", use_container_width=True)
    else:
        st.success("No anomalies detected.")

with col_ai2:
    # SMOOTHING THE GRAPH (Moving Average)
    df_daily = filtered_df.set_index('transactiondate').resample('D')['displayamount'].sum().fillna(0)
    smooth_df = df_daily.rolling(window=7).mean()
    
    fig_line = px.line(smooth_df, title="7-Day Moving Average Trend", labels={'value': 'Volume'})
    fig_line.update_traces(line_color='#1e3a8a', line_width=3)
    fig_line.update_layout(height=300, margin=dict(t=30, b=0, l=0, r=0))
    st.plotly_chart(fig_line, use_container_width=True)

st.write("---")
st.caption("FinPulse AI v2.6 | Developed by Aarti | Financial Data Intelligence Portfolio")
