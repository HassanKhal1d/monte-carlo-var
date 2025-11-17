import yfinance as yf
import pandas as pd
from pathlib import Path

def fetch_sp500(ticker='SPY', start='2000-01-01', end=None, save_path=None):
    """
    Fetch S&P 500 historical data and save to CSV.
    Handles yfinance changes (Adj Close may be missing).
    """
    # If no save_path provided, save to backend/app/data/spy.csv relative to this file
    if save_path is None:
        base_dir = Path(__file__).parent       # backend/app
        data_dir = base_dir / "data"
        data_dir.mkdir(exist_ok=True)          # create folder if missing
        save_path = data_dir / "spy.csv"

    # Download data with auto_adjust=False to keep 'Adj Close'
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=False)

    # Ensure only the columns that exist are selected
    expected_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    available_columns = [col for col in expected_columns if col in df.columns]
    df = df[available_columns]

    # Save to CSV
    df.to_csv(save_path)
    print(f"Data saved to {save_path.resolve()}")

if __name__ == "__main__":
    fetch_sp500()
