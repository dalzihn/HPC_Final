import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def crawl_data(
    ticker: str,
    previous_days: int = 120,
    drop_date: bool = True,
) -> pd.DataFrame:
    """Crawling data from yfinance from a specified number of previous days to the current time
    
    Args:
        ticker (str): Ticker symbol of the stock
        previous_days (int, optional): Number of previous days to crawl data. Defaults to 7.
        drop_date (bool, optional): Whether to drop the date column. Defaults to True.
    
    Returns:
        pd.DataFrame: DataFrame containing the crawled data
    """
    current = datetime.now()
    previous = current - timedelta(days=previous_days)
    data = yf.Ticker(ticker)
    history = data.history(start=previous, end=current)
    if drop_date:
        history = history.reset_index().drop(["Date", "Dividends", "Stock Splits"], axis=1)
        return history
    history = history.reset_index().drop(["Dividends", "Stock Splits"], axis=1)
    history['Date'] = history['Date'].dt.strftime('%Y-%m-%d')
    return history
    