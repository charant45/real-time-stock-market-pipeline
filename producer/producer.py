import yfinance as yf
import pandas as pd
from datetime import datetime

stocks = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN"]

data = []

for stock in stocks:
    ticker = yf.Ticker(stock)

    # Fetch 5 days of 1-minute interval data (~390 unique rows per trading day)
    hist = ticker.history(period="5d", interval="1m")

    if hist.empty:
        print(f"Skipping {stock}: no data returned")
        continue

    # Take the most recent 100 rows — each row is a unique minute
    hist = hist.tail(100).reset_index()

    hist["symbol"] = stock
    hist = hist.rename(columns={
        "Datetime": "timestamp",
        "Open":     "open_price",
        "High":     "high_price",
        "Low":      "low_price",
        "Close":    "close_price",
        "Volume":   "volume",
    })

    hist = hist[[
        "symbol", "timestamp",
        "open_price", "high_price", "low_price", "close_price",
        "volume"
    ]]

    data.append(hist)
    print(f"{stock}: {len(hist)} unique records fetched")

if not data:
    print("No data collected. Check your internet connection or ticker symbols.")
else:
    df = pd.concat(data, ignore_index=True)

    filename = f"stock_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)

    print(f"\nCreated {len(df)} total records across {df['symbol'].nunique()} stocks")
    print(f"Unique close prices per stock:")
    print(df.groupby("symbol")["close_price"].nunique().to_string())
    print(f"\nSaved to: {filename}")