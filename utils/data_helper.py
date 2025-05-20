import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def crawl_data(
    ticker: str,
    previous_days: int = 120
) -> pd.DataFrame:
    """Crawling data from yfinance from a specified number of previous days to the current time
    
    Args:
        ticker (str): Ticker symbol of the stock
        previous_days (int, optional): Number of previous days to crawl data. Defaults to 7.
    
    Returns:
        pd.DataFrame: DataFrame containing the crawled data
    """
    current = datetime.now()
    previous = current - timedelta(days=previous_days)
    data = yf.Ticker(ticker)
    history = data.history(start=previous, end=current)
    history = history.reset_index().drop(["Date", "Dividends", "Stock Splits"], axis=1)
    return history
    