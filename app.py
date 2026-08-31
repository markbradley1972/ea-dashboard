import streamlit as pd
import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Page Setup
st.set_page_config(page_title="T-HOUSE CAPITAL Portfolio Dashboard", layout="wide")

# Connect to Supabase (Replace with your actual Supabase URL and Anon Key)
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_data(ttl=5)
def fetch_live_data():
    response = supabase.table("portfolio_updates").select("*").execute()
    return pd.DataFrame(response.data)

df = fetch_live_data()

# Dark Theme UI Layout
st.markdown("""
    <style>
    .main { background-color: #0b0f15; color: #c9d1d9; }
    h1, h2, h3 { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("### T-HOUSE CAPITAL &nbsp;&nbsp;&nbsp; <span style='font-size:14px; color:#8b949e;'>Portfolio Dashboard</span>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("### CONTRIBUTION WATERFALL — EVERY INSTANCE, RANKED")

if not df.empty and 'net_pnl' in df.columns:
    df_sorted = df.sort_values(by="net_pnl", ascending=False)
    for idx, row in df_sorted.iterrows():
        cols = st.columns([3, 1, 2, 2, 1])
        with cols[0]:
            st.write(f"**{row.get('strategy', 'Unknown')}**")
        with cols[1]:
            st.write(str(row.get('magic', '')))
        with cols[2]:
            st.write(row.get('broker', ''))
        with cols[3]:
            pnl = row.get('net_pnl', 0)
            color = "#3fb950" if pnl >= 0 else "#f85149"
            st.markdown(f"<span style='color:{color}; font-weight:bold;'>+£{pnl:,.2f}</span>", unsafe_allow_html=True)
        with cols[4]:
            st.progress(min(max(int(row.get('growth', 0)), 0), 100))
else:
    st.info("Waiting for live account data feed...")