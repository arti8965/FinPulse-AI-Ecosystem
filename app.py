import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="FinPulse AI Ecosystem", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# Application Header
st.title("🏦 FinPulse AI: Financial Intelligence Ecosystem")
st.sidebar.header("Global Filters")

# Data Loading with Cache for performance
@st.cache_data
def load_data():
    # Loading the dataset
    df = pd.read_csv("data.csv")
    # Standardizing column names to lowercase for consistency
    df.columns = df.columns.str.strip().str.lower()
    
    # Converting date column to datetime objects
    if 'transactiondate' in df.columns:
        df['transactiondate'] = pd.to_datetime(df['transactiondate'])
    return df

# Initialize Data
try:
    df = load_data()

    # 1. CURRENCY CONVERSION ENGINE
    currency_mode = st.sidebar.radio("Select Reporting Currency:", ["USD ($)", "INR (₹)"])
    conversion_rate = 83.5 

    if currency_mode == "INR (₹)":
        df['displayamount'] = df['transactionamount'].abs() * conversion_rate
        symbol, unit = "₹", "Cr"
    else:
        df['displayamount'] = df['transactionamount'].abs()
        symbol, unit = "$", "M"

    # 2. MULTI-SELECT FILTERS
    # Using 'transactionchannel' as identified in your CSV
    available_channels = df['transactionchannel'].unique()
    selected_channels = st.sidebar.multiselect("Filter by Channel:", options=available_channels, default=available_channels)
    
    # Filtered Dataframe for all visualizations
    filtered_df = df[df['transactionchannel'].isin(selected_channels)]

    # --- KEY PERFORMANCE INDICATORS (KPIs) ---
    m1, m2, m3 = st.columns(3)
    total_vol = filtered_df['displayamount'].sum()
    avg_val = filtered_df['displayamount'].mean()

    with m1:
        st.metric("Total Transaction Volume", f"{symbol}{total_vol/1e6:.2f} {unit}")
    with m2:
        st.metric("Average Transaction Value", f"{symbol}{avg_val:,.0f}")
    with m3:
        st.metric("Active Transaction Channels", len(selected_channels))

    # --- GRAPHICAL ANALYSIS ---
    st.write("---")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Transaction Type Distribution")
        fig1 = px.pie(filtered_df, names='transactiontype', values='displayamount', hole=0.4, 
                      color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("Revenue by Channel")
        fig2 = px.bar(filtered_df, x='transactionchannel', y='displayamount', 
                      color='transactionchannel', labels={'displayamount': 'Amount', 'transactionchannel': 'Channel'})
        st.plotly_chart(fig2, use_container_width=True)

    # --- ADVANCED AI INSIGHTS & FORECASTING ---
    st.write("---")
    st.subheader("🤖 AI Business Insights & Forecasting")
    
    ai_col1, ai_col2 = st.columns([1, 2])

    with ai_col1:
        st.markdown("#### 🚩 Automated Anomaly Detection")
        # Logic: Flagging transactions 3x higher than average as potential risks
        threshold = avg_val * 3
        anomalies = filtered_df[filtered_df['displayamount'] > threshold]
        
        if not anomalies.empty:
            st.error(f"Alert: {len(anomalies)} High-Risk transactions flagged!")
            if st.checkbox("Show Risk Details"):
                st.dataframe(anomalies[['transactionid', 'displayamount', 'transactionchannel']].head(10))
        else:
            st.success("Stable patterns detected. No financial anomalies found.")

    with ai_col2:
        st.markdown("#### 📈 7-Day Moving Trend")
        # Aggregating data by date for trend forecasting
        df_daily = filtered_df.set_index('transactiondate').resample('D')['displayamount'].sum().fillna(0)
        forecast = df_daily.rolling(window=7).mean()
        
        st.line_chart(forecast)
        st.caption("AI Note: Using a 7-day rolling window to forecast liquidity trends.")

except Exception as e:
    st.error(f"Critical System Error: {e}")

# Footer section
st.write("---")
st.caption("System Developed by Aarti | FinPulse AI Ecosystem v2.5 | End-to-End Financial Intelligence")
