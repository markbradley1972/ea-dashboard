import json
import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(page_title="T-HOUSE CAPITAL Portfolio Dashboard", layout="wide")

# Custom Dark Theme Styling
st.markdown("""
    <style>
    .main { background-color: #0b0f15; color: #c9d1d9; }
    h1, h2, h3 { color: #ffffff !important; }
    .stMetric { background-color: #121820; border: 1px solid #21262d; padding: 15px; border-radius: 6px; }
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data(ttl=5)
def load_data():
    try:
        with open("dashboard.json", "r") as f:
            return json.load(f)
    except:
        return {"accounts": {}}

data = load_data()
accounts_list = list(data["accounts"].values())
df = pd.DataFrame(accounts_list)

# Top Bar / Portfolio Summary Header
st.markdown("### T-HOUSE CAPITAL &nbsp;&nbsp;&nbsp; <span style='font-size:14px; color:#8b949e;'>Portfolio Dashboard</span>", unsafe_allow_html=True)
st.markdown("---")

# Top Spotlight Cards (Carrying vs Holding Back)
col_carry, col_back = st.columns(2)

with col_carry:
    st.markdown("""
        <div style="background-color:#121820; border: 1px solid #1f6feb; padding:15px; border-radius:8px;">
            <p style="color:#3fb950; font-size:12px; font-weight:bold; margin-bottom:0;">▲ CARRYING THE PORTFOLIO</p>
            <h3 style="margin:5px 0; color:#fff;">Gold_Scalp_C <span style="font-size:14px; color:#8b949e;">(Magic 2103)</span></h3>
            <h2 style="color:#3fb950; margin:0;">+£898.26 <span style="font-size:16px;">(+89.83% of capital)</span></h2>
            <p style="color:#8b949e; font-size:13px; margin-top:8px;">PF 10.04 &nbsp;&nbsp;|&nbsp;&nbsp; WR 84.2% &nbsp;&nbsp;|&nbsp;&nbsp; 19 trades &nbsp;&nbsp;|&nbsp;&nbsp; XAUUSD+</p>
        </div>
    """, unsafe_allow_html=True)

with col_back:
    st.markdown("""
        <div style="background-color:#121820; border: 1px solid #da3633; padding:15px; border-radius:8px;">
            <p style="color:#f85149; font-size:12px; font-weight:bold; margin-bottom:0;">▼ HOLDING YOU BACK</p>
            <h3 style="margin:5px 0; color:#fff;">ScalpH1_B <span style="font-size:14px; color:#8b949e;">(Magic 2102)</span></h3>
            <h2 style="color:#f85149; margin:0;">-£451.31 <span style="font-size:16px;">(-45.13% of capital)</span></h2>
            <p style="color:#8b949e; font-size:13px; margin-top:8px;">PF 0.50 &nbsp;&nbsp;|&nbsp;&nbsp; WR 47.7% &nbsp;&nbsp;|&nbsp;&nbsp; 44 trades &nbsp;&nbsp;|&nbsp;&nbsp; XAUUSD+</p>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# Contribution Waterfall Ranked View
st.markdown("### CONTRIBUTION WATERFALL — EVERY INSTANCE, RANKED")
st.markdown("<p style='color:#8b949e; font-size:12px;'>Each row is one running instance. The same strategy on different accounts or brokers appears as separate rows.</p>", unsafe_allow_html=True)

if not df.empty:
    df_sorted = df.sort_values(by="net_pnl", ascending=False)
    
    for idx, row in df_sorted.iterrows():
        cols = st.columns([3, 1, 2, 2, 1])
        with cols[0]:
            st.write(f"**{row['strategy']}**")
        with cols[1]:
            st.write(str(row['magic']))
        with cols[2]:
            st.write(row['broker'])
        with cols[3]:
            color = "#3fb950" if row['net_pnl'] >= 0 else "#f85149"
            st.markdown(f"<span style='color:{color}; font-weight:bold;'>+£{row['net_pnl']:,.2f} (+{row['growth']}%)</span>", unsafe_allow_html=True)
        with cols[4]:
            st.progress(min(max(int(row['growth']), 0), 100))
else:
    st.info("No trading data reported yet.")