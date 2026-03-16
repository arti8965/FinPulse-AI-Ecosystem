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

# Title
st.title("🏦 FinPulse AI: Financial Intelligence Ecosystem")
st.sidebar.header("Control Panel")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    # Step 1: Force all column names to lowercase and remove spaces
    df.columns = df.columns.str.strip().str.lower()
    
    # Step 2: Convert date (column name will now be 'transactiondate' in lowercase)
    if 'transactiondate' in df.columns:
        df['transactiondate'] = pd.to_datetime(df['transactiondate'])
    return df

df = load_data()

# 1. CURRENCY ENGINE
currency_mode = st.sidebar.radio("Select Currency Base:", ["USD ($)", "INR (₹)"])
conversion_rate = 83.5 

# Currency Logic using lower-case column names
if currency_mode == "INR (₹)":
    df['displayamount'] = df['transactionamount'].abs() * conversion_rate
    symbol, unit = "₹", "Cr"
else:
    df['displayamount'] = df['transactionamount'].abs()
    symbol, unit = "$", "M"

# 2. SIDEBAR FILTERS
# Using lowercase 'channel'
available_channels = df['channel'].unique()
selected_channels = st.sidebar.multiselect("Select Channels:", options=available_channels, default=available_channels)
filtered_df = df[df['channel'].isin(selected_channels)]

# --- MAIN DASHBOARD (KPIs) ---
m1, m2, m3 = st.columns(3)
total_vol = filtered_df['displayamount'].sum()
avg_val = filtered_df['displayamount'].mean()

with m1:
    st.metric("Total Transaction Volume", f"{symbol}{total_vol/1e6:.2f} {unit}")
with m2:
    st.metric("Average Ticket Size", f"{symbol}{avg_val:,.0f}")
with m3:
    st.metric("Active Channels", len(selected_channels))

# --- VISUALIZATIONS ---
st.write("---")
c1, c2 = st.columns(2)

with c1:
    st.subheader("Transaction Distribution")
    fig1 = px.pie(filtered_df, names='transactiontype', values='displayamount', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Channel Performance")
    fig2 = px.bar(filtered_df, x='channel', y='displayamount', color='channel')
    st.plotly_chart(fig2, use_container_width=True)

# --- ADVANCED AI INSIGHTS ---
st.write("---")
st.subheader("🤖 AI Business Insights & Forecasting")
ai_col1, ai_col2 = st.columns([1, 2])

with ai_col1:
    st.markdown("#### 🚩 Anomaly Detection")
    threshold = avg_val * 3
    anomalies = filtered_df[filtered_df['displayamount'] > threshold]
    if not anomalies.empty:
        st.error(f"Alert: {len(anomalies)} High-Risk transactions detected!")
        if st.checkbox("View Risk Logs"):
            st.dataframe(anomalies[['transactionid', 'displayamount', 'channel']].head(10))
    else:
        st.success("Financial patterns look stable.")

with ai_col2:
    st.markdown("#### 📈 7-Day Trend Analysis")
    df_daily = filtered_df.set_index('transactiondate').resample('D')['displayamount'].sum().fillna(0)
    forecast = df_daily.rolling(window=7).mean()
    st.line_chart(forecast)

st.write("---")
st.caption("Developed by Aarti | FinPulse AI Ecosystem v2.2")
