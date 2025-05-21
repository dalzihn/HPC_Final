# backend/stock_service.py
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

class StockService:
    @staticmethod
    async def get_prediction(ticker: str, days_ahead: int = 1) -> dict:
        """Get stock price prediction for the given ticker."""
        try:
            # Get historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            df = yf.download(ticker, start=start_date, end=end_date)
            
            if df.empty:
                raise ValueError("No data found for this ticker")
            
            # Simple prediction logic
            last_price = df['Close'].iloc[-1]
            predicted_price = round(last_price * (1 + np.random.uniform(-0.02, 0.02) * days_ahead), 2)
            
            # Get historical data for chart
            historical_data = [
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "close": float(row["Close"]),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "volume": int(row["Volume"])
                }
                for date, row in df.tail(30).iterrows()
            ][::-1]  # Reverse to show latest first
            
            # Format data for the table (last 5 days)
            table_data = [
                {
                    "Date": date.strftime("%Y-%m-%d"),
                    "Open": f"${row['Open']:.2f}",
                    "High": f"${row['High']:.2f}",
                    "Low": f"${row['Low']:.2f}",
                    "Close": f"${row['Close']:.2f}",
                    "Volume": f"{int(row['Volume']):,}"
                }
                for date, row in df.tail(5).iterrows()
            ][::-1]  # Reverse to show latest first
            
            return {
                "ticker": ticker.upper(),
                "predicted_price": predicted_price,
                "historical_data": historical_data,
                "table_data": table_data,
                "currency": "USD",
                "prediction_horizon_days": days_ahead,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise ValueError(f"Error predicting price: {str(e)}")