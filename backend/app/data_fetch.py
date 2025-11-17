# data_fetch.py
import yfinance as yf
import pandas as pd
from pathlib import Path

def fetch_sp500(ticker='SPY', start='2000-01-01', end=None, save_path='spy.csv'):
    """
    Fetch S&P 500 historical data and save to CSV.
    Handles yfinance changes (Adj Close may be missing).
    """
    # Download data with auto_adjust=False to keep 'Adj Close'
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=False)

    # Ensure only the columns that exist are selected
    expected_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    available_columns = [col for col in expected_columns if col in df.columns]
    df = df[available_columns]

    # Save to CSV
    path = Path(save_path)
    df.to_csv(path)
    print(f"Data saved to {path.resolve()}")

if __name__ == "__main__":
    fetch_sp500()

