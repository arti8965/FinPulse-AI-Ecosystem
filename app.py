import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE CONFIGURATION (Theme & Layout)
st.set_page_config(page_title="FinPulse AI Ecosystem", layout="wide", initial_sidebar_state="expanded")

# 2. PREMIUM CSS (Custom Styling for Cards)
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #1E3A8A; }
    .main { background-color: #F8FAFC; }
    .chart-container {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #0F172A; font-family: 'Inter', sans-serif; }
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

try:
    df = load_data()

    # SIDEBAR
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=80)
        st.title("Settings")
        currency_mode = st.radio("Reporting Currency", ["USD ($)", "INR (₹)"])
        selected_channels = st.multiselect("Select Channels", options=df['transactionchannel'].unique(), default=df['transactionchannel'].unique())
    
    conversion_rate = 83.5 
    if currency_mode == "INR (₹)":
        df['displayamount'] = df['transactionamount'].abs() * conversion_rate
        symbol, unit = "₹", "Cr"
    else:
        df['displayamount'] = df['transactionamount'].abs()
        symbol, unit = "$", "M"

    filtered_df = df[df['transactionchannel'].isin(selected_channels)]

    # --- HEADER SECTION ---
    st.title("🏦 FinPulse AI Ecosystem")
    st.markdown("#### Real-time Financial Intelligence & Risk Monitoring")
    
    # --- KPI SECTION (Modern Metrics) ---
    st.write("")
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("Total Volume", f"{symbol}{filtered_df['displayamount'].sum()/1e6:.2f} {unit}")
    with kpi2:
        st.metric("Avg Transaction", f"{symbol}{filtered_df['displayamount'].mean():,.0f}")
    with kpi3:
        st.metric("Total Records", f"{len(filtered_df):,}")
    st.write("---")

    # --- MAIN CHARTS (Visual Cleanup) ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Transaction Distribution")
        fig1 = px.pie(filtered_df, names='transactiontype', values='displayamount', hole=0.5,
                      color_discrete_sequence=['#1E3A8A', '#3B82F6', '#93C5FD'])
        fig1.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=350)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Channel Performance")
        fig2 = px.bar(filtered_df, x='transactionchannel', y='displayamount', 
                      color_discrete_sequence=['#10B981'])
        fig2.update_layout(margin=dict(t=20, b=0, l=0, r=0), height=350, xaxis_title="", yaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- AI & TREND SECTION ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🤖 AI Intelligence & Market Trends")
    
    ai_col1, ai_col2 = st.columns([1, 2])
    
    with ai_col1:
        st.info("**Anomaly Insights**")
        threshold = filtered_df['displayamount'].mean() * 3
        anomalies = filtered_df[filtered_df['displayamount'] > threshold]
        if not anomalies.empty:
            st.warning(f"⚠️ {len(anomalies)} High-Risk entries detected.")
            if st.button("Download Risk Report"):
                st.toast("Report generated successfully!")
        else:
            st.success("Patterns are within safe limits.")

    with ai_col2:
        df_daily = filtered_df.set_index('transactiondate').resample('D')['displayamount'].sum().fillna(0)
        fig_trend = px.line(df_daily.rolling(7).mean(), labels={'value': 'Volume'})
        fig_trend.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
        st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"System Error: {e}")

st.markdown("<p style='text-align: center; color: #64748B;'>FinPulse AI v2.6 | Developed by Aarti</p>", unsafe_allow_html=True)
