import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Momentum Scanner",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Momentum Trading Scanner")

st.caption("Watchlist pullback + momentum signals")

df = pd.read_csv("scan_results.csv")

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
