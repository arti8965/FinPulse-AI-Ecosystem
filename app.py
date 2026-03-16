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
conversion_rate = 83.5 

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    # Sabhi column names ke aage-piche se space hatana (Very Important)
    df.columns = df.columns.str.strip()
    
    # Date convert karna
    if 'TransactionDate' in df.columns:
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
    return df

df = load_data()

# --- ERROR CHECKING FOR COLUMNS ---
# Hum check kar rahe hain ki column ka sahi naam kya hai (Channel ya channel)
channel_col = 'Channel' if 'Channel' in df.columns else 'channel'
amount_col = 'TransactionAmount' if 'TransactionAmount' in df.columns else 'transactionamount'

# Apply Currency Logic
if currency_mode == "INR (₹)":
    df['DisplayAmount'] = df[amount_col].abs() * conversion_rate
    symbol, unit = "₹", "Cr"
else:
    df['DisplayAmount'] = df[amount_col].abs()
    symbol, unit = "$", "M"

# Sidebar Filters
# Ab ye error nahi dega kyunki humne 'channel_col' variable use kiya hai
available_channels = df[channel_col].unique()
channels = st.sidebar.multiselect("Select Channels:", options=available_channels, default=available_channels)
filtered_df = df[df[channel_col].isin(channels)]

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
    # Yahan bhi dynamic column name use kiya hai
    type_col = 'TransactionType' if 'TransactionType' in df.columns else 'transactiontype'
    fig1 = px.pie(filtered_df, names=type_col, values='DisplayAmount', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Channel Performance")
    fig2 = px.bar(filtered_df, x=channel_col, y='DisplayAmount', color=channel_col)
    st.plotly_chart(fig2, use_container_width=True)

# --- ADVANCED AI INSIGHTS ---
st.write("---")
st.subheader("🤖 AI Business Insights & Forecasting")
ai_col1, ai_col2 = st.columns([1, 2])

with ai_col1:
    st.markdown("#### 🚩 Anomaly Detection")
    threshold = avg_val * 3
    anomalies = filtered_df[filtered_df['DisplayAmount'] > threshold]
    if not anomalies.empty:
        st.error(f"Alert: {len(anomalies)} High-Risk transactions detected!")
        if st.checkbox("View Risk Logs"):
            # ID column check
            id_col = 'TransactionID' if 'TransactionID' in df.columns else df.columns[0]
            st.dataframe(anomalies[[id_col, 'DisplayAmount', channel_col]].head(10))
    else:
        st.success("Financial patterns look stable.")

with ai_col2:
    st.markdown("#### 📈 7-Day Trend Analysis")
    date_col = 'TransactionDate' if 'TransactionDate' in df.columns else df.columns[0]
    df_daily = filtered_df.set_index(date_col).resample('D')['DisplayAmount'].sum().fillna(0)
    forecast = df_daily.rolling(window=7).mean()
    st.line_chart(forecast)

st.write("---")
st.caption("Developed by Aarti | FinPulse AI Ecosystem v2.1")
