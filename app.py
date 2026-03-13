import streamlit as st
import pandas as pd
import os
from datetime import datetime
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
    last_updated_utc = datetime.utcfromtimestamp(last_updated)
else:
    last_updated_utc = None

# --- Viewer timezone selection ---
timezones = pytz.all_timezones
viewer_tz = st.selectbox("Select your timezone", timezones, index=timezones.index("America/New_York"))

if last_updated_utc:
    tz = pytz.timezone(viewer_tz)
    last_updated_local = pytz.utc.localize(last_updated_utc).astimezone(tz)
    last_updated_str = last_updated_local.strftime("%Y-%m-%d %H:%M:%S")
else:
    last_updated_str = "N/A"

st.markdown(f"**Last Updated ({viewer_tz}):** {last_updated_str}")

# --- Separate strong buys and watch list ---
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
