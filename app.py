import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="FinPulse AI Ecosystem", layout="wide")

st.title("🏦 FinPulse AI: Financial Intelligence Ecosystem")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df.columns = df.columns.str.strip().str.lower() # Clean names
    if 'transactiondate' in df.columns:
        df['transactiondate'] = pd.to_datetime(df['transactiondate'])
    return df

try:
    df = load_data()

    # --- DEBUGGING SECTION: Ise check karke error pakdenge ---
    if 'channel' not in df.columns:
        st.error(f"❌ Error: Column 'channel' nahi mila! Aapki file mein ye columns hain: {list(df.columns)}")
        st.info("💡 Tip: Apni CSV file check karein ki usme 'Channel' naam ka column hai ya nahi.")
        st.stop() # App yahi ruk jayegi jab tak sahi column nahi milta

    # 1. CURRENCY ENGINE
    currency_mode = st.sidebar.radio("Select Currency Base:", ["USD ($)", "INR (₹)"])
    conversion_rate = 83.5 

    if currency_mode == "INR (₹)":
        df['displayamount'] = df['transactionamount'].abs() * conversion_rate
        symbol, unit = "₹", "Cr"
    else:
        df['displayamount'] = df['transactionamount'].abs()
        symbol, unit = "$", "M"

    # 2. SIDEBAR FILTERS
    available_channels = df['channel'].unique()
    selected_channels = st.sidebar.multiselect("Select Channels:", options=available_channels, default=available_channels)
    filtered_df = df[df['channel'].isin(selected_channels)]

    # --- MAIN DASHBOARD ---
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
        # Check for transactiontype column
        type_col = 'transactiontype' if 'transactiontype' in df.columns else df.columns[0]
        fig1 = px.pie(filtered_df, names=type_col, values='displayamount', hole=0.4)
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("Channel Performance")
        fig2 = px.bar(filtered_df, x='channel', y='displayamount', color='channel')
        st.plotly_chart(fig2, use_container_width=True)

    # --- AI INSIGHTS ---
    st.write("---")
    st.subheader("🤖 AI Business Insights & Forecasting")
    
    # Anomaly Detection
    threshold = avg_val * 3
    anomalies = filtered_df[filtered_df['displayamount'] > threshold]
    if not anomalies.empty:
        st.warning(f"Alert: {len(anomalies)} High-Risk transactions detected!")
    
    # Simple Trend
    df_daily = filtered_df.set_index('transactiondate').resample('D')['displayamount'].sum().fillna(0)
    st.line_chart(df_daily.rolling(window=7).mean())

except Exception as e:
    st.error(f"Ek unexpected error aaya hai: {e}")

st.write("---")
st.caption("Developed by Aarti | v2.3 Debug Mode")
