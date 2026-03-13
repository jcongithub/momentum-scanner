import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from streamlit_javascript import st_javascript
import pytz

st.set_page_config(
    page_title="Momentum Scanner",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Momentum Trading Scanner")
st.caption("Watchlist pullback + momentum signals")

# --- Load CSV ---
csv_file = "scan_results.csv"
df = pd.read_csv(csv_file)

# --- Get CSV last update time in UTC ---
if os.path.exists(csv_file):
    last_updated = os.path.getmtime(csv_file)
    last_updated_utc = datetime.utcfromtimestamp(last_updated).replace(tzinfo=pytz.UTC)
else:
    last_updated_utc = None

# --- Get viewer's timezone offset in minutes using JS ---
offset_minutes = st_javascript("new Date().getTimezoneOffset();", key="tz_offset")  # offset in minutes

# --- Convert offset to approximate timezone code ---
# mapping JS offsets (in minutes) to short codes
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

if last_updated_utc and offset_minutes is not None:
    # JS offset is minutes *behind* UTC, we need -offset to get correct local time
    local_time = last_updated_utc - timedelta(minutes=offset_minutes)
    tz_code = offset_map.get(-offset_minutes, f"UTC{(-offset_minutes)//60:+}")
    last_updated_str = local_time.strftime("%Y-%m-%d %H:%M:%S")
else:
    last_updated_str = "N/A"
    tz_code = ""

st.markdown(f"**Last Updated ({tz_code}):** {last_updated_str}")

# --- Separate strong buys and watch list ---
strong = df[df["signal"] == "STRONG BUY"]
watch = df[df["signal"] == "WATCH"]

st.subheader("🔥 Strong Buy Signals")
st.dataframe(strong if not strong.empty else pd.DataFrame(["No strong signals today"]))

st.subheader("👀 Watch List")
st.dataframe(watch)

st.subheader("📊 Full Scan")
st.dataframe(df)
