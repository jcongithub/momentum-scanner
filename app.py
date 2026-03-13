import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_javascript import st_javascript
import pytz
from scanner import scan_all

st.set_page_config(
    page_title="Momentum Scanner",
    page_icon="📈",
    layout="wide"
)

DEFAULT_SYMBOLS = [
    "NVDA","AMZN","MSFT","META",
    "ASML","TSLA","SMCI","NFLX",
    "LULU","SHOP"
]

st.title("📈 Momentum Trading Scanner")
st.caption("Watchlist pullback + momentum signals")

# --- Watchlist input + Run button on same row ---
col1, col2 = st.columns([8,1])

with col1:
    symbols_input = st.text_area(
        "Edit Watchlist (comma separated)",
        value=",".join(DEFAULT_SYMBOLS),
        height=80
    )

with col2:
    run_scan = st.button("Run Scan")

symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]

# --- Initialize session state ---
if "df" not in st.session_state:
    st.session_state.df = None

if "last_updated_utc" not in st.session_state:
    st.session_state.last_updated_utc = None


# --- Get viewer timezone offset ---
offset_minutes = st_javascript("new Date().getTimezoneOffset();", key="tz_offset")

offset_map = {
    0: "GMT",
    60: "CET",
    120: "EET",
    -60: "AST",
    -120: "EST",
    -180: "CST",
    -240: "EDT",
    -300: "CDT",
    -330: "IST",
    -480: "PST",
    -420: "PDT"
}

# --- Run scan ---
if run_scan:

    results = scan_all(symbols=symbols)
    st.session_state.df = pd.DataFrame(results)

    st.session_state.last_updated_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)


# --- Show last updated time ---
if st.session_state.last_updated_utc and offset_minutes is not None:

    local_time = st.session_state.last_updated_utc - timedelta(minutes=offset_minutes)
    tz_code = offset_map.get(-offset_minutes, f"UTC{(-offset_minutes)//60:+}")

    last_updated_str = local_time.strftime("%Y-%m-%d %H:%M:%S")

    st.markdown(f"**Last Updated ({tz_code}):** {last_updated_str}")


# --- Show results ---
if st.session_state.df is not None:

    df = st.session_state.df

    strong = df[df["signal"] == "STRONG BUY"]
    watch = df[df["signal"] == "WATCH"]

    st.subheader("🔥 Strong Buy Signals")

    if strong.empty:
        st.info("No strong signals today")
    else:
        st.dataframe(strong)

    st.subheader("👀 Watch List")
    st.dataframe(watch)

    st.subheader("📊 Full Scan")
    st.dataframe(df)