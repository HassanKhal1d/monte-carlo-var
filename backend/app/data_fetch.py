# backend/app/data_fetch.py
import yfinance as yf
import os

OUT = "backend/app/data"
os.makedirs(OUT, exist_ok=True)

def fetch_sp500(start="1995-08-01", end="2025-08-31", ticker="^GSPC", out_csv="backend/app/data/spy.csv"):
    df = yf.download(ticker, start=start, end=end, progress=False)
    df = df[['Open','High','Low','Close','Adj Close','Volume']]
    df.to_csv(out_csv)
    print(f"Saved {out_csv}")
    return df

if __name__ == "__main__":
    fetch_sp500()

