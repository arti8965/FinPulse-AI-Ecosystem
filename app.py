import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE SETUP
st.set_page_config(page_title="FinPulse AI Ecosystem", layout="wide")

# 2. EXECUTIVE STYLING
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .main { background-color: #f8fafc; }
    h1 { color: #1e3a8a; font-weight: 800; }
    .sidebar .sidebar-content { background-color: #f1f5f9; }
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

# --- SIDEBAR (Executive Style) ---
with st.sidebar:
    st.title("🏦 FinPulse Settings")
    
    # A. CURRENCY SETTINGS
    st.subheader("🌐 Currency Settings")
    currency_mode = st.radio("Display Currency In:", ["USD ($)", "INR (₹)"])
    
    st.write("---")
    
    # B. PAGE NAVIGATION (The "Go to Page" thing you wanted!)
    st.subheader("📍 Go to Page:")
    page_selection = st.selectbox("Select View:", 
                                 ["Executive Dashboard", "Risk & AI Analytics", "Raw Transaction Data"])
    
    st.write("---")
    
    # C. DATA FILTERS
    st.subheader("🔍 Data Filters")
    available_channels = df['transactionchannel'].unique()
    selected_channels = st.multiselect("Select Channels:", options=available_channels, default=available_channels)
    
    available_types = df['transactiontype'].unique()
    selected_types = st.multiselect("Transaction Types:", options=available_types, default=available_types)

# --- CALCULATIONS ---
conversion_rate = 83.5 
if currency_mode == "INR (₹)":
    df['displayamount'] = df['transactionamount'].abs() * conversion_rate
    symbol, unit = "₹", "Cr"
else:
    df['displayamount'] = df['transactionamount'].abs()
    symbol, unit = "$", "M"

# Apply Filters
mask = (df['transactionchannel'].isin(selected_channels)) & (df['transactiontype'].isin(selected_types))
filtered_df = df[mask]

# --- MAIN PAGE LOGIC (Based on Page Selection) ---

if page_selection == "Executive Dashboard":
    st.title(f"📊 Financial Summary ({currency_mode})")
    
    # Top KPI Row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Volume", f"{symbol}{filtered_df['displayamount'].sum()/1e6:.2f} {unit}")
    with m2:
        st.metric("Average Transaction", f"{symbol}{filtered_df['displayamount'].mean():,.2f}")
    with m3:
        st.metric("Success Rate", "95.3%") # Static example for UI
        
    st.write("---")
    
    # Charts Row
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(f"Transaction Volume by Channel ({symbol})")
        fig1 = px.donut(filtered_df, names='transactionchannel', values='displayamount', hole=0.5)
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.subheader(f"Volume by Type ({symbol})")
        fig2 = px.bar(filtered_df, x='transactiontype', y='displayamount', color='transactiontype')
        st.plotly_chart(fig2, use_container_width=True)

elif page_selection == "Risk & AI Analytics":
    st.title("🤖 AI Intelligence & Market Trends")
    
    ai_col1, ai_col2 = st.columns([1, 2])
    with ai_col1:
        st.info("**Anomaly Detection Summary**")
        avg = filtered_df['displayamount'].mean()
        anomalies = filtered_df[filtered_df['displayamount'] > avg * 3]
        if not anomalies.empty:
            st.warning(f"Detected {len(anomalies)} high-risk anomalies.")
            st.button("Download Forensic Report")
        else:
            st.success("No anomalies detected.")
            
    with ai_col2:
        st.subheader("7-Day Moving Average Trend")
        df_daily = filtered_df.set_index('transactiondate').resample('D')['displayamount'].sum().fillna(0)
        fig_line = px.line(df_daily.rolling(7).mean())
        st.plotly_chart(fig_line, use_container_width=True)

elif page_selection == "Raw Transaction Data":
    st.title("📑 Transaction Logs")
    st.write("Full filtered dataset:")
    st.dataframe(filtered_df, use_container_width=True)

# Footer
st.write("---")
st.caption(f"FinPulse AI v2.9 | View: {page_selection} | Developed by Aarti")
