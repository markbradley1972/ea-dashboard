import pandas as pd
import streamlit as st
from supabase import create_client, Client

# Page Setup
st.set_page_config(page_title="T-HOUSE CAPITAL Portfolio Dashboard", layout="wide")

# Custom Dark Theme Styling
st.markdown("""
    <style>
    .main { background-color: #0b0f15; color: #c9d1d9; }
    h1, h2, h3 { color: #ffffff !important; }
    .card-box { background-color: #121820; border-radius: 8px; padding: 16px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# Connect to Supabase
SUPABASE_URL = "https://rlfgzxmgzfiqrafblwgr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsZmd6eG1nemZpcXJhZmJsd2dyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgxODM5MjgsImV4cCI6MjEwMzc1OTkyOH0.s3EzgC0P6bI6NmBFhwbWPgE7KSjsl9Z9P7mx3y8XJOo"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_data(ttl=3)
def fetch_live_data():
    try:
        response = supabase.table("portfolio_updates").select("*").execute()
        df = pd.DataFrame(response.data)
        if not df.empty and 'magic' in df.columns:
            # Sort by ID descending to get the latest update per Magic Number
            df = df.sort_values(by="id", ascending=False)
            df = df.drop_duplicates(subset=["magic"], keep="first")
        return df
    except Exception as e:
        return pd.DataFrame()

df = fetch_live_data()

# Header
st.markdown("### T-HOUSE CAPITAL &nbsp;&nbsp;&nbsp; <span style='font-size:14px; color:#8b949e;'>Portfolio Dashboard</span>", unsafe_allow_html=True)
st.markdown("---")

if not df.empty and 'net_pnl' in df.columns:
    df['net_pnl'] = pd.to_numeric(df['net_pnl'], errors='coerce').fillna(0)
    df_sorted = df.sort_values(by="net_pnl", ascending=False).reset_index(drop=True)

    # --- TOP SPOTLIGHT CARDS ---
    col_carry, col_back = st.columns(2)
    
    # Top Performer
    top_ea = df_sorted.iloc[0]
    pnl_top = top_ea['net_pnl']
    top_color = "#3fb950" if pnl_top >= 0 else "#f85149"
    top_sign = "+" if pnl_top >= 0 else "-"
    
    with col_carry:
        st.markdown(f"""
            <div class="card-box" style="border: 1px solid #1f6feb;">
                <p style="color:#3fb950; font-size:12px; font-weight:bold; margin-bottom:4px;">▲ CARRYING THE PORTFOLIO</p>
                <h3 style="margin:4px 0;">{top_ea.get('strategy', 'N/A')} <span style="font-size:13px; color:#8b949e;">(Magic {top_ea.get('magic', '')})</span></h3>
                <h2 style="color:{top_color}; margin:4px 0;">{top_sign}£{abs(pnl_top):,.2f}</h2>
                <p style="color:#8b949e; font-size:12px; margin-top:6px;">Broker: {top_ea.get('broker', 'N/A')} &nbsp;|&nbsp; Status: Active</p>
            </div>
        """, unsafe_allow_html=True)

    # Worst Performer
    bottom_ea = df_sorted.iloc[-1]
    pnl_bot = bottom_ea['net_pnl']
    bot_color = "#3fb950" if pnl_bot >= 0 else "#f85149"
    bot_sign = "+" if pnl_bot >= 0 else "-"

    with col_back:
        st.markdown(f"""
            <div class="card-box" style="border: 1px solid #da3633;">
                <p style="color:#f85149; font-size:12px; font-weight:bold; margin-bottom:4px;">▼ HOLDING YOU BACK</p>
                <h3 style="margin:4px 0;">{bottom_ea.get('strategy', 'N/A')} <span style="font-size:13px; color:#8b949e;">(Magic {bottom_ea.get('magic', '')})</span></h3>
                <h2 style="color:{bot_color}; margin:4px 0;">{bot_sign}£{abs(pnl_bot):,.2f}</h2>
                <p style="color:#8b949e; font-size:12px; margin-top:6px;">Broker: {bottom_ea.get('broker', 'N/A')} &nbsp;|&nbsp; Status: Active</p>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("### CONTRIBUTION WATERFALL — EVERY INSTANCE, RANKED")

    # Waterfall Table View
    max_pnl = max(abs(df_sorted['net_pnl'].max()), 1)
    
    for idx, row in df_sorted.iterrows():
        cols = st.columns([3, 1, 3, 2, 2])
        pnl = row['net_pnl']
        color = "#3fb950" if pnl >= 0 else "#f85149"
        sign = "+" if pnl >= 0 else "-"

        with cols[0]:
            st.write(f"**{row.get('strategy', 'Unknown')}**")
        with cols[1]:
            st.write(f"`{row.get('magic', '')}`")
        with cols[2]:
            st.write(row.get('broker', ''))
        with cols[3]:
            st.markdown(f"<span style='color:{color}; font-weight:bold;'>{sign}£{abs(pnl):,.2f}</span>", unsafe_allow_html=True)
        with cols[4]:
            progress_val = int(min(max((abs(pnl) / max_pnl) * 100, 5), 100))
            st.progress(progress_val)
else:
    st.info("Waiting for live account data feed...")
