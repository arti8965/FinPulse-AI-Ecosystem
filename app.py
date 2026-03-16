import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="FinPulse AI Ecosystem", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# Title and Sidebar
st.title("🏦 FinPulse AI: Financial Intelligence Ecosystem")
st.sidebar.header("Control Panel")

# 1. CURRENCY ENGINE
currency_mode = st.sidebar.radio("Select Currency Base:", ["USD ($)", "INR (₹)"])
conversion_rate = 83.5  # Standard Rate

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
    return df

df = load_data()

# Apply Currency Logic
if currency_mode == "INR (₹)":
    df['DisplayAmount'] = df['TransactionAmount'].abs() * conversion_rate
    symbol, unit = "₹", "Cr"
else:
    df['DisplayAmount'] = df['TransactionAmount'].abs()
    symbol, unit = "$", "M"

# Sidebar Filters
channels = st.sidebar.multiselect("Select Channels:", options=df['Channel'].unique(), default=df['Channel'].unique())
filtered_df = df[df['Channel'].isin(channels)]

# --- MAIN DASHBOARD (KPIs) ---
m1, m2, m3 = st.columns(3)
total_vol = filtered_df['DisplayAmount'].sum()
avg_val = filtered_df['DisplayAmount'].mean()

with m1:
    st.metric("Total Transaction Volume", f"{symbol}{total_vol/1e6:.2f} {unit}")
with m2:
    st.metric("Average Ticket Size", f"{symbol}{avg_val:,.0f}")
with m3:
    st.metric("Active Channels", len(channels))

# --- VISUALIZATIONS ---
st.write("---")
c1, c2 = st.columns(2)

with c1:
    st.subheader("Transaction Distribution")
    fig1 = px.pie(filtered_df, names='TransactionType', values='DisplayAmount', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Channel Performance")
    fig2 = px.bar(filtered_df, x='Channel', y='DisplayAmount', color='Channel', barmode='group')
    st.plotly_chart(fig2, use_container_width=True)

# --- ADVANCED AI INSIGHTS & FORECASTING ---
st.write("---")
st.subheader("🤖 AI Business Insights & Forecasting")

ai_col1, ai_col2 = st.columns([1, 2])

with ai_col1:
    st.markdown("#### 🚩 Anomaly Detection")
    # AI Logic: Flagging transactions 3x higher than average
    threshold = avg_val * 3
    anomalies = filtered_df[filtered_df['DisplayAmount'] > threshold]
    
    if not anomalies.empty:
        st.error(f"Alert: {len(anomalies)} High-Risk transactions detected!")
        if st.checkbox("View Risk Logs"):
            st.dataframe(anomalies[['TransactionID', 'DisplayAmount', 'Channel']].head(10))
    else:
        st.success("Financial patterns look stable. No anomalies detected.")

with ai_col2:
    st.markdown("#### 📈 7-Day Trend Analysis")
    # Grouping data by date for clean forecasting trend
    df_daily = filtered_df.set_index('TransactionDate').resample('D')['DisplayAmount'].sum().fillna(0)
    forecast = df_daily.rolling(window=7).mean()
    
    st.line_chart(forecast)
    st.caption("AI Note: Moving average trend used to predict future liquidity requirements.")

# Footer
st.write("---")
st.caption("Developed by Aarti | FinPulse AI Ecosystem v2.0 | Confidential Data Strategy")
