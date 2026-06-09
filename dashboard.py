"""
Real-Time Cryptocurrency Dashboard
Navyan Data Analytics Internship - Project 3
Author: Singh Aditya Manoj Kumar
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import time
from fetch_data import get_crypto_prices

# ── Page configuration ───────────────────────────────────────────
st.set_page_config(
    page_title="Crypto Dashboard | Singh Aditya Manoj Kumar",
    page_icon="📈",
    layout="wide"
)

# ── Header ───────────────────────────────────────────────────────
st.title("📈 Real-Time Cryptocurrency Dashboard")
st.caption("Navyan Data Analytics Internship — Project 3 | Singh Aditya Manoj Kumar | Data: CoinGecko API")

# ── Sidebar controls ─────────────────────────────────────────────
st.sidebar.header("⚙️ Controls")

alert_coin = st.sidebar.selectbox(
    "Set price alert for:",
    ["Bitcoin", "Ethereum", "Tether", "BNB", "Solana",
     "XRP", "USDC", "Cardano", "Avalanche", "Dogecoin"]
)

alert_threshold = st.sidebar.number_input(
    "Alert when price goes above ($):",
    min_value=0.0,
    value=50000.0,
    step=100.0
)

auto_refresh = st.sidebar.checkbox("Auto-refresh every 60 seconds", value=True)

st.sidebar.divider()
st.sidebar.markdown("**About**")
st.sidebar.markdown("Built by **Singh Aditya Manoj Kumar**")
st.sidebar.markdown("Navyan Data Analytics Internship")

# ── Fetch live data ──────────────────────────────────────────────
with st.spinner("Fetching live data from CoinGecko..."):
    df = get_crypto_prices()

if df is None:
    st.error("Could not fetch data. Check your internet connection and try again.")
    st.stop()

# ── Key metrics row ──────────────────────────────────────────────
st.subheader("📊 Market Overview")
col1, col2, col3, col4 = st.columns(4)

top_coin   = df.iloc[0]
gainers    = df[df["24h Change (%)"] > 0]
losers     = df[df["24h Change (%)"] < 0]
best       = df.loc[df["24h Change (%)"].idxmax()]
worst      = df.loc[df["24h Change (%)"].idxmin()]

col1.metric(
    label="Top Coin by Market Cap",
    value=top_coin["Name"],
    delta=f"${top_coin['Price (USD)']:,.2f}"
)
col2.metric(
    label="Coins Gaining (24h)",
    value=f"{len(gainers)} / 10"
)
col3.metric(
    label="Best Performer (24h)",
    value=best["Symbol"],
    delta=f"{best['24h Change (%)']:.2f}%"
)
col4.metric(
    label="Worst Performer (24h)",
    value=worst["Symbol"],
    delta=f"{worst['24h Change (%)']:.2f}%",
    delta_color="inverse"
)

st.divider()

# ── Price alert ──────────────────────────────────────────────────
alert_row = df[df["Name"] == alert_coin]
if not alert_row.empty:
    current_price = alert_row["Price (USD)"].values[0]
    if current_price > alert_threshold:
        st.warning(
            f"🔔 **Price Alert!** {alert_coin} is currently at **${current_price:,.2f}** "
            f"— above your threshold of **${alert_threshold:,.2f}**"
        )
    else:
        st.info(
            f"✅ {alert_coin} is at **${current_price:,.2f}** — below your alert threshold of ${alert_threshold:,.2f}"
        )

# ── Charts row 1 ─────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("💰 Current Prices (USD)")
    fig_bar = px.bar(
        df,
        x="Symbol",
        y="Price (USD)",
        color="24h Change (%)",
        color_continuous_scale=["#e74c3c", "#95a5a6", "#27ae60"],
        text_auto=".2s",
        title="Top 10 Cryptocurrencies by Price"
    )
    fig_bar.update_layout(height=380, showlegend=False)
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("📉 24h Price Change (%)")
    df_sorted = df.sort_values("24h Change (%)")
    colors = ["#e74c3c" if x < 0 else "#27ae60"
              for x in df_sorted["24h Change (%)"]]
    fig_change = go.Figure(go.Bar(
        x=df_sorted["24h Change (%)"],
        y=df_sorted["Symbol"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:.2f}%" for v in df_sorted["24h Change (%)"]],
        textposition="outside"
    ))
    fig_change.update_layout(
        height=380,
        xaxis_title="% Change (24h)",
        title="Gainers vs Losers"
    )
    st.plotly_chart(fig_change, use_container_width=True)

# ── Charts row 2 ─────────────────────────────────────────────────
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("🥧 Market Cap Distribution")
    fig_pie = px.pie(
        df,
        names="Symbol",
        values="Market Cap",
        title="Market Cap Share (Top 10)",
        hole=0.4
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right2:
    st.subheader("🔵 Market Cap vs Volume")
    fig_bubble = px.scatter(
        df,
        x="Market Cap",
        y="Volume (24h)",
        size="Price (USD)",
        color="24h Change (%)",
        hover_name="Name",
        color_continuous_scale=["#e74c3c", "#95a5a6", "#27ae60"],
        text="Symbol",
        title="Bubble size = Price | Color = 24h Change"
    )
    fig_bubble.update_traces(textposition="top center")
    fig_bubble.update_layout(height=400)
    st.plotly_chart(fig_bubble, use_container_width=True)

# ── 24h High vs Low comparison ───────────────────────────────────
st.subheader("📊 24h High vs Low Price Range")
fig_range = go.Figure()
fig_range.add_trace(go.Bar(
    name="24h High",
    x=df["Symbol"],
    y=df["24h High"],
    marker_color="#27ae60"
))
fig_range.add_trace(go.Bar(
    name="24h Low",
    x=df["Symbol"],
    y=df["24h Low"],
    marker_color="#e74c3c"
))
fig_range.update_layout(
    barmode="group",
    height=380,
    title="Daily Price Range per Coin",
    yaxis_title="Price (USD)"
)
st.plotly_chart(fig_range, use_container_width=True)

# ── Full data table ──────────────────────────────────────────────
st.subheader("📋 Full Data Table")
st.dataframe(
    df.style.format({
        "Price (USD)":    "${:,.2f}",
        "Market Cap":     "${:,.0f}",
        "Volume (24h)":   "${:,.0f}",
        "24h High":       "${:,.2f}",
        "24h Low":        "${:,.2f}",
        "24h Change (%)": "{:.2f}%"
    }).background_gradient(
        subset=["24h Change (%)"],
        cmap="RdYlGn"
    ),
    use_container_width=True,
    hide_index=True
)

# ── Auto-refresh ─────────────────────────────────────────────────
if auto_refresh:
    time.sleep(60)
    st.rerun()
