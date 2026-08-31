import pandas as pd
import streamlit as st
from supabase import create_client, Client

# Page Configuration
st.set_page_config(page_title="T-HOUSE CAPITAL — Portfolio Dashboard", layout="wide")

# Custom Dark Theme Styling matching Screenshot
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #c9d1d9; }
    h1, h2, h3, h4 { color: #ffffff !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #0d121c; border-right: 1px solid #1a2332; }
    .sidebar-card { background-color: #121926; border: 1px solid #1e293b; border-radius: 6px; padding: 14px; margin-bottom: 15px; }
    
    /* Metric Cards */
    .spotlight-card { background-color: #121926; border-radius: 8px; padding: 18px; margin-bottom: 20px; }
    .card-carry { border: 1px solid #1d4ed8; }
    .card-back { border: 1px solid #991b1b; }
    
    /* Sub-text styles */
    .metric-subtext { color: #94a3b8; font-size: 13px; font-weight: 500; }
    .badge-green { color: #22c55e; font-weight: bold; }
    .badge-red { color: #ef4444; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Supabase Connection
SUPABASE_URL = "https://rlfgzxmgzfiqrafblwgr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsZmd6eG1nemZpcXJhZmJsd2dyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgxODM5MjgsImV4cCI6MjEwMzc1OTkyOH0.s3EzgC0P6bI6NmBFhwbWPgE7KSjsl9Z9P7mx3y8XJOo"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_data(ttl=3)
def fetch_data():
    try:
        response = supabase.table("portfolio_updates").select("*").execute()
        df = pd.DataFrame(response.data)
        if not df.empty and 'magic' in df.columns:
            df = df.sort_values(by="id", ascending=False)
            df = df.drop_duplicates(subset=["magic"], keep="first")
        return df
    except:
        return pd.DataFrame()

df = fetch_data()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## **T-HOUSE CAPITAL**")
    st.markdown("<p style='color:#64748b; font-size:12px; margin-top:-15px;'>Portfolio Dashboard</p>", unsafe_allow_html=True)
    
    # Portfolio Balance Card
    tot_equity = df['net_pnl'].sum() if not df.empty and 'net_pnl' in df.columns else 0.0
    total_strategies = len(df) if not df.empty else 0
    
    st.markdown(f"""
        <div class="sidebar-card">
            <p style="color:#64748b; font-size:11px; font-weight:bold; letter-spacing:1px; margin-bottom:2px;">TOTAL PORTFOLIO</p>
            <h2 style="margin:0; font-size:24px;">£{9257.60 + tot_equity:,.2f}</h2>
            <p style="color:#64748b; font-size:12px; margin-top:4px;">6 accounts · {total_strategies} strategies</p>
            <hr style="border-color:#1e293b; margin:8px 0;">
            <div style="display:flex; justify-content:space-between; font-size:12px; color:#94a3b8;">
                <span>5x GBP</span><span>£8,328.87</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:12px; color:#94a3b8;">
                <span>1x USD</span><span>$1,266.20</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation Views
    st.markdown("<p style='color:#64748b; font-size:11px; font-weight:bold; letter-spacing:1px;'>VIEWS</p>", unsafe_allow_html=True)
    st.markdown("""
        • Overview  
        • **Live Trades** `13`  
        • Calendar  
        • **Strategies** `105`  
        • Accounts  
        • Recovery  
        • Slippage  
        • Risk & Drawdown  
        • Deposits  
    """)
    
    st.markdown("<br><p style='color:#475569; font-size:11px;'>Dashboard v3.27<br>EA v2.20</p>", unsafe_allow_html=True)

# --- MAIN CONTENT ---
if not df.empty and 'net_pnl' in df.columns:
    df['net_pnl'] = pd.to_numeric(df['net_pnl'], errors='coerce').fillna(0)
    df['growth'] = pd.to_numeric(df.get('growth', 0), errors='coerce').fillna(0)
    df['pf'] = pd.to_numeric(df.get('pf', 1.0), errors='coerce').fillna(1.0)
    df['wr'] = pd.to_numeric(df.get('wr', 50.0), errors='coerce').fillna(50.0)
    df['trades'] = pd.to_numeric(df.get('trades', 1), errors='coerce').fillna(1)
    
    df_sorted = df.sort_values(by="net_pnl", ascending=False).reset_index(drop=True)

    # Top Spotlight Cards
    col_carry, col_back = st.columns(2)
    
    top = df_sorted.iloc[0]
    bot = df_sorted.iloc[-1]
    
    with col_carry:
        st.markdown(f"""
            <div class="spotlight-card card-carry">
                <p style="color:#22c55e; font-size:11px; font-weight:bold; letter-spacing:1px; margin-bottom:4px;">▲ CARRYING THE PORTFOLIO</p>
                <h3 style="margin:2px 0;">{top.get('strategy', 'Gold_Scalp_C')} <span style="font-size:13px; color:#64748b;">Magic {top.get('magic', '2103')}</span></h3>
                <p style="color:#64748b; font-size:12px; margin-top:-2px;">{top.get('broker', 'Vantage Markets (Pty) Ltd')}</p>
                <h2 style="color:#22c55e; margin:6px 0; font-size:28px;">+£{abs(top['net_pnl']):,.2f} <span style="font-size:16px;">(+{top['growth']:.2f}% of capital)</span></h2>
                <p class="metric-subtext"><b style="color:#e2e8f0;">PF</b> <span class="badge-green">{top['pf']:.2f}</span> &nbsp;&nbsp; <b style="color:#e2e8f0;">WR</b> <span style="color:#e2e8f0;">{top['wr']:.1f}%</span> &nbsp;&nbsp; {int(top['trades'])} trades &nbsp;&nbsp; XAUUSD+</p>
                <hr style="border-color:#1e293b; margin:10px 0;">
                <p style="color:#64748b; font-size:12px; margin:0;">Accounts for <b>16.1%</b> of all gains across the portfolio</p>
            </div>
        """, unsafe_allow_html=True)

    with col_back:
        st.markdown(f"""
            <div class="spotlight-card card-back">
                <p style="color:#ef4444; font-size:11px; font-weight:bold; letter-spacing:1px; margin-bottom:4px;">▼ HOLDING YOU BACK</p>
                <h3 style="margin:2px 0;">{bot.get('strategy', 'ScalpH1_B')} <span style="font-size:13px; color:#64748b;">Magic {bot.get('magic', '2102')}</span></h3>
                <p style="color:#64748b; font-size:12px; margin-top:-2px;">{bot.get('broker', 'Vantage Markets (Pty) Ltd')}</p>
                <h2 style="color:#ef4444; margin:6px 0; font-size:28px;">-£{abs(bot['net_pnl']):,.2f} <span style="font-size:16px;">({bot['growth']:.2f}% of capital)</span></h2>
                <p class="metric-subtext"><b style="color:#e2e8f0;">PF</b> <span class="badge-red">{bot['pf']:.2f}</span> &nbsp;&nbsp; <b style="color:#e2e8f0;">WR</b> <span style="color:#e2e8f0;">{bot['wr']:.1f}%</span> &nbsp;&nbsp; {int(bot['trades'])} trades &nbsp;&nbsp; XAUUSD+</p>
                <hr style="border-color:#1e293b; margin:10px 0;">
                <p style="color:#64748b; font-size:12px; margin:0;">Killing this alone would lift net P&L by <b style="color:#22c55e;">+£{abs(bot['net_pnl']):,.2f}</b> (12.5%)</p>
            </div>
        """, unsafe_allow_html=True)

    # Sort Bar & Table Header
    st.markdown("### CONTRIBUTION WATERFALL — EVERY INSTANCE, RANKED")
    st.markdown("<p style='color:#64748b; font-size:12px; margin-top:-10px;'>Each row is one running instance. The same strategy on different accounts or brokers appears as separate rows.</p>", unsafe_allow_html=True)

    # Waterfall Table Rows
    max_pnl = max(abs(df_sorted['net_pnl'].max()), 1)

    for idx, row in df_sorted.iterrows():
        cols = st.columns([2.5, 1, 2, 3, 1.5, 1])
        pnl = row['net_pnl']
        color = "#22c55e" if pnl >= 0 else "#ef4444"
        sign = "+" if pnl >= 0 else "-"

        with cols[0]:
            st.write(f"**{row.get('strategy', 'Unknown')}**")
        with cols[1]:
            st.write(f"<span style='color:#64748b;'>{row.get('magic', '')}</span>", unsafe_allow_html=True)
        with cols[2]:
            st.write(f"<span style='color:#64748b;'>{row.get('broker', '')}</span>", unsafe_allow_html=True)
        with cols[3]:
            progress_val = int(min(max((abs(pnl) / max_pnl) * 100, 3), 100))
            st.progress(progress_val)
        with cols[4]:
            st.markdown(f"<span style='color:{color}; font-weight:bold;'>{sign}£{abs(pnl):,.2f}</span> <span style='color:{color}; font-size:12px;'>({sign}{abs(row['growth']):.2f}%)</span>", unsafe_allow_html=True)
        with cols[5]:
            st.write(f"<span style='color:#64748b;'>{int(row['trades'])}t</span>", unsafe_allow_html=True)
else:
    st.info("Waiting for live account data feed...")
