import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator

pd.options.display.width = 120

WATCHLIST = [
"NVDA","AMZN","MSFT","META","ASML",
"TSLA","SMCI","NFLX","LULU","SHOP"
]

def scan_all(symbols):
    data = download_data(symbols)

    results = []
    for symbol in symbols:

        df = data[symbol]

        close = df["Close"].squeeze()
        high = df["High"].squeeze()

        volume = df["Volume"].squeeze()
        avg_volume = volume.tail(20).mean()
        today_volume = volume.iloc[-1]
        volume_surge = today_volume > avg_volume * 1.5

        open_price = df["Open"].squeeze().iloc[-1]
        prev_close = close.iloc[-2]
        gap_percent = (open_price - prev_close) / prev_close
        gap_up = gap_percent > 0.02

        rsi = RSIIndicator(close=close, window=14).rsi()

        price = float(close.iloc[-1])
        rsi_value = float(rsi.iloc[-1])

        high20 = float(high.tail(20).max())
        pullback = (high20 - price) / high20

        score = 0

        if rsi_value < 40:
            score += 1
        if pullback > 0.07:
            score += 1
        if volume_surge:
            score += 1
        if gap_up:
            score += 1

        if score >= 3:
            signal = "STRONG BUY"
        elif score == 2:
            signal = "WATCH"
        else:
            signal = "HOLD"

        results.append({
            "symbol": symbol,
            "price": round(price,2),
            "rsi": round(rsi_value,1),
            "pullback%": round(pullback*100,1),
            "gap%": round(gap_percent*100,1),
            "vol_surge": volume_surge,
            "score": score,
            "signal": signal
        })

    return results

def download_data(symbols):
    tickers = " ".join(symbols)

    df = yf.download(
        tickers,
        period="3mo",
        interval="1d",
        group_by="ticker",
        progress=False
    )
    return df

results = scan_all(symbols=WATCHLIST)

df = pd.DataFrame(results)
print("\nMomentum Pullback Scanner\n")

if df.empty:
    print("No data returned")
else:
    df = df.sort_values("pullback%", ascending=False)
    print(df)
    print("\nBUY SIGNALS\n")
    buys = df[df["signal"] == "BUY"]

    if buys.empty:
        print("No buy signals today")
    else:
        for _, row in buys.iterrows():
            print(
                f"🔥 BUY {row['symbol']}  "
                f"Price:{row['price']}  "
                f"RSI:{row['rsi']}  "
                f"Pullback:{row['pullback%']}%"
            )

df.to_csv("scan_results.csv", index=False)
print("\nScan results saved to scan_results.csv")