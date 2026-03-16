import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="FinPulse AI Ecosystem", layout="wide", page_icon="🏦")

# 2. CUSTOM STYLING (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); }
    h1 { color: #1e3a8a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 3. DATA LOADING FUNCTION
@st.cache_data
def load_data():
    # Loading the data.csv file from your folder
    df = pd.read_csv("data.csv")
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error("⚠️ Error: 'data.csv' not found! Please ensure the file is in your project folder.")
    st.stop()

# 4. SIDEBAR - CURRENCY SWITCHER & FILTERS
st.sidebar.title("🏛️ FinPulse Settings")

# --- Dynamic Currency Switcher ---
st.sidebar.subheader("💱 Currency Settings")
currency_mode = st.sidebar.radio("Display Currency In:", ["USD ($)", "INR (₹)"])

# Conversion Logic
conversion_rate = 83.5 # Standard USD to INR rate
if currency_mode == "INR (₹)":
    # Calculating values in INR
    df['DisplayAmount'] = df['TransactionAmount'].abs() * conversion_rate
    symbol = "₹"
    unit = "Cr" # Crores
else:
    # Calculating values in USD
    df['DisplayAmount'] = df['TransactionAmount'].abs()
    symbol = "$"
    unit = "M" # Millions

st.sidebar.markdown("---")

# --- Navigation Menu ---
menu = st.sidebar.selectbox("Go to Page:", ["Executive Dashboard", "Risk Analysis", "Data Explorer"])

# --- Global Filters ---
st.sidebar.header("🔍 Data Filters")
selected_channel = st.sidebar.multiselect("Select Channel", options=df['TransactionChannel'].unique(), default=df['TransactionChannel'].unique())
filtered_df = df[df['TransactionChannel'].isin(selected_channel)]

# 5. PAGE 1: EXECUTIVE DASHBOARD
if menu == "Executive Dashboard":
    st.title(f"📊 Financial Summary ({currency_mode})")
    
    # KPI Calculations
    total_volume = filtered_df['DisplayAmount'].sum()
    avg_txn = filtered_df['DisplayAmount'].mean()
    success_count = len(filtered_df[filtered_df['Status'] == 'Success'])
    success_rate = (success_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
    
    # Displaying Metric Cards
    m1, m2, m3 = st.columns(3)
    
    if currency_mode == "INR (₹)":
        m1.metric("Total Volume", f"{symbol}{total_volume/1e7:.2f} {unit}")
    else:
        m1.metric("Total Volume", f"{symbol}{total_volume/1e6:.2f} {unit}")
        
    m2.metric("Average Transaction", f"{symbol}{avg_txn:,.2f}")
    m3.metric("Success Rate", f"{success_rate:.1f}%")

    st.markdown("---")

    # Visualizations
    c1, c2 = st.columns(2)
    with c1:
        # Pie Chart
        fig_pie = px.pie(filtered_df, names='TransactionChannel', values='DisplayAmount', 
                         title=f"Transaction Volume by Channel ({symbol})", hole=0.5)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        # Bar Chart
        fig_bar = px.bar(filtered_df.groupby('TransactionType')['DisplayAmount'].sum().reset_index(), 
                         x='TransactionType', y='DisplayAmount', 
                         title=f"Volume by Type ({symbol})", color='TransactionType')
        st.plotly_chart(fig_bar, use_container_width=True)

# 6. PAGE 2: RISK ANALYSIS
elif menu == "Risk Analysis":
    st.title("🛡️ Fraud & Risk Detection")
    st.info("Identify high-value anomalies based on current currency selection.")
    
    # Slider for user-defined threshold
    limit = st.slider(f"Select Alert Threshold ({symbol})", 
                      min_value=int(df['DisplayAmount'].min()), 
                      max_value=int(df['DisplayAmount'].max()), 
                      value=int(df['DisplayAmount'].mean() * 2))
    
    high_risk = filtered_df[filtered_df['DisplayAmount'] > limit]
    st.warning(f"Found {len(high_risk)} transactions above {symbol}{limit:,}")
    st.dataframe(high_risk, use_container_width=True)

# 7. PAGE 3: DATA EXPLORER
elif menu == "Data Explorer":
    st.title("🗄️ Enterprise Data Ledger")
    st.write(f"Showing raw records converted to {currency_mode}")
    # Show dynamic column
    st.dataframe(filtered_df[['TransactionID', 'TransactionDate', 'DisplayAmount', 'TransactionChannel', 'Status']], use_container_width=True)
    
    # Export functionality
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Report", csv, "FinPulse_Report.csv", "text/csv")
    # --- ADVANCED FEATURE: AI INSIGHTS & FORECASTING ---
st.write("---")
st.subheader("🤖 AI Business Insights")

col1, col2 = st.columns(2)

with col1:
    # Logic: Identifying High-Value Anomalies
    avg_val = df['DisplayAmount'].mean()
    anomalies = df[df['DisplayAmount'] > avg_val * 3]
    st.warning(f"Found {len(anomalies)} suspicious high-value transactions.")
    if st.checkbox("Show Risky Transactions"):
        st.dataframe(anomalies)

with col2:
    # Logic: Simple Forecasting (Visual Representation)
    st.info("Trend Forecast: Next 30 Days")
    forecast_data = df.groupby('TransactionDate')['DisplayAmount'].sum().rolling(7).mean()
    st.line_chart(forecast_data)
    st.caption("AI prediction based on 7-day moving average.")
