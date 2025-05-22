# This will utilisem model to predict price
# Define an API endpoint for prediction
# Define prediction data structure for prediction
# Define a function predict price using trained models
# Define a class for stock state which is responsbile for storing input from the form and displaying line chart and table
# api/app/states/stock_state.py
# import reflex as rx
# import yfinance as yf
# from datetime import datetime, timedelta
# import pandas as pd
# import numpy as np
# from fastapi import FastAPI, HTTPException, Request, Query
# from pydantic import BaseModel
# from typing import Optional

# # Initialize FastAPI app for API endpoints
# api = FastAPI()

# # Pydantic model for POST request body
# class PredictionRequest(BaseModel):
#     ticker: str
#     days_ahead: Optional[int] = 1

       
# class StockState(rx.State):
#     """State for stock price prediction."""
    
#     # Store the predicted price
#     predicted_price: float = 0.0
#     stock_code: str = ""
#     loading: bool = False
#     error_message: str = ""
#     historical_data: list[dict] = []
#     table_data: list[dict] = []

#     @rx.var
#     def prediction_result(self) -> str:
#         """Return formatted prediction result."""
#         if self.error_message:
#             return self.error_message
#         if self.predicted_price > 0:
#             return f"Predicted price for {self.stock_code.upper()}: ${self.predicted_price:.2f}"
#         return ""

#     def set_stock_code(self, value: str):
#         """Update stock code when input changes."""
#         self.stock_code = value.upper()

#     async def fetch_historical_data(self, ticker: str, days: int = 30):
#         """Fetch historical stock data for the given ticker."""
#         try:
#             end_date = datetime.now()
#             start_date = end_date - timedelta(days=days)
#             df = yf.download(ticker, start=start_date, end=end_date)
            
#             if df.empty:
#                 raise ValueError("No data found for this ticker")
            
#             # Format data for the line chart
#             self.historical_data = [
#                 {
#                     "date": date.strftime("%Y-%m-%d"),
#                     "close": row["Close"],
#                     "open": row["Open"],
#                     "high": row["High"],
#                     "low": row["Low"],
#                     "volume": int(row["Volume"])
#                 }
#                 for date, row in df.iterrows()
#             ]
            
#             # Format data for the table (last 5 days)
#             self.table_data = [
#                 {
#                     "Date": date.strftime("%Y-%m-%d"),
#                     "Open": f"${row['Open']:.2f}",
#                     "High": f"${row['High']:.2f}",
#                     "Low": f"${row['Low']:.2f}",
#                     "Close": f"${row['Close']:.2f}",
#                     "Volume": f"{int(row['Volume']):,}"
#                 }
#                 for date, row in df.tail(5).iterrows()
#             ][::-1]  # Reverse to show latest first
            
#             return True
#         except Exception as e:
#             self.error_message = f"Error fetching historical data: {str(e)}"
#             return False
            
#     async def handle_submit(self, form_data: dict):
#         """Handle form submission and call the prediction API."""
#         ticker = form_data.get("stock_code", "").strip().upper()
#         if not ticker:
#             self.error_message = "Please enter a stock ticker"
#             return

#         self.loading = True
#         self.stock_code = ticker
#         self.error_message = ""

#         try:
#             # Call the prediction method
#             response = await self.get_prediction(ticker)
#             self.predicted_price = response["predicted_price"]
#         except Exception as e:
#             self.error_message = f"Error: {str(e)}"
#             self.predicted_price = 0.0
#         finally:
#             self.loading = False

#     async def get_prediction(self, ticker: str, days_ahead: int = 1):
#         """Get stock price prediction for the given ticker."""
#         self.loading = True
#         self.stock_code = ticker.upper()
#         self.error_message = ""
        
#         try:
#             # Get historical data
#             end_date = datetime.now()
#             start_date = end_date - timedelta(days=365)
#             df = yf.download(ticker, start=start_date, end=end_date)
            
#             if df.empty:
#                 raise ValueError("No data found for this ticker")
            
#             # Simple prediction logic
#             last_price = df['Close'].iloc[-1]
#             prediction = last_price * (1 + np.random.uniform(-0.02, 0.02) * days_ahead)
#             self.predicted_price = round(prediction, 2)
            
#         except Exception as e:
#             self.error_message = f"Error predicting price: {str(e)}"
#             self.predicted_price = 0.0
#             raise
        
#         self.loading = False
#         return {
#             "ticker": self.stock_code,
#             "predicted_price": self.predicted_price,
#             "currency": "USD",
#             "prediction_horizon_days": days_ahead,
#             "timestamp": datetime.now().isoformat()
#         }

# # API endpoint
# @api.api_route("/predict/{ticker}", methods=["GET", "POST"])
# async def predict_price(
#     request: Request,
#     ticker: str,
#     days_ahead: int = Query(1, description="Prediction horizon in days")
# ):
#     """
#     Combined GET and POST endpoint for stock price prediction.
#     GET: /predict/?days_ahead=5
#     POST: /predict/ with JSON body: {"ticker": "AAPL", "days_ahead": 5}
#     """
#     state = StockState()
    
#     # Handle POST request
#     if request.method == "POST":
#         try:
#             data = await request.json()
#             req = PredictionRequest(**data)
#             ticker = req.ticker
#             days_ahead = req.days_ahead
#         except Exception as e:
#             raise HTTPException(status_code=400, detail="Invalid request body")
    
#     # Handle GET request or use POST parameters
#     if not ticker:
#         raise HTTPException(status_code=400, detail="Ticker parameter is required")
    
#     try:
#         return await state.get_prediction(ticker=ticker, days_ahead=days_ahead)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
# backend/stock_api.py
# from fastapi import FastAPI, HTTPException, Request, Query
# from pydantic import BaseModel
# from typing import Optional
# from .stock_service import StockService

# # Initialize FastAPI app
# api = FastAPI()

# # Pydantic model for POST request body
# class PredictionRequest(BaseModel):
#     ticker: str
#     days_ahead: Optional[int] = 1

# # API endpoint
# @api.api_route("/predict/{ticker}", methods=["GET", "POST"])
# async def predict_price(
#     request: Request,
#     ticker: str,
#     days_ahead: int = Query(1, description="Prediction horizon in days")
# ):
#     """
#     Combined GET and POST endpoint for stock price prediction.
#     GET: /predict/AAPL?days_ahead=5
#     POST: /predict/DUMMY with JSON body: {"ticker": "AAPL", "days_ahead": 5}
#     """
#     # Handle POST request
#     if request.method == "POST":
#         try:
#             data = await request.json()
#             req = PredictionRequest(**data)
#             ticker = req.ticker
#             days_ahead = req.days_ahead
#         except Exception as e:
#             raise HTTPException(status_code=400, detail="Invalid request body")
    
#     # Handle GET request or use POST parameters
#     if not ticker:
#         raise HTTPException(status_code=400, detail="Ticker parameter is required")
    
#     try:
#         return await StockService.get_prediction(ticker=ticker, days_ahead=days_ahead)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))