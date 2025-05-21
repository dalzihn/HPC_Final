import reflex as rx
import numpy as np
import pandas as pd
import os

from .frontend.forms import stock_input_form
from .frontend.plot_pred import line_pred
from .frontend.table_pred import table_pred
from .frontend.navbar import navbar
from .frontend.footer import footer

from fastapi import FastAPI
from pydantic import BaseModel
from assets.helper.data_helper import crawl_data
from assets.helper.predict_helper import preprocess_api, predict_price
from datetime import datetime, timedelta

OUTPUT_LEN = 7

# Initialize FastAPI app
api = FastAPI()

# Data model for GET request body
class DataOutput(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    
    ticker: str
    raw_data: dict  # Will store the DataFrame as a dictionary
    
    @classmethod
    def from_dataframe(cls, ticker: str, df: pd.DataFrame):
        # Convert DataFrame to dict with orient = 'list' to ensure JSON serialization
        return cls(
            ticker=ticker,
            raw_data=df.reset_index().to_dict(orient='list')  
        )

# Pydantic model for POST request body
class PredictionOutput(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    
    ticker: str
    predicted_price: list[float]
    timestamp: list[str]
    
    @classmethod
    def from_prediction(cls, ticker: str, prediction: np.ndarray):
        return cls(
            ticker=ticker,
            predicted_price=prediction.flatten().tolist(),  # Convert numpy array to list
            timestamp=[(datetime.now() + timedelta(days=i)).strftime('%m-%d') for i in range(OUTPUT_LEN)]
        )

# API endpoint
@api.post("/predict/{ticker}")
def post_prediction(
    ticker: str
):
    """
    POST: /predict/AAPL?seq_len=60
    """
    # Handle POST request
    ## Crawl data
    ticker = ticker.strip().upper()
    df = crawl_data(ticker)

    ## Preprocess data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scaler_path = os.path.join(base_dir, "assets", "scaler", f"GRU_{ticker}_scaler.pkl")
    model_path = os.path.join(base_dir, "assets", "model", f"GRU_{ticker}_model.keras")


    # Special case for NVDA
    if ticker == "NVDA":
        scaler_path = os.path.join(base_dir, "assets", "scaler", "LSTM_NVDA_scaler.pkl")
        model_path = os.path.join(base_dir, "assets", "model", "LSTM_NVDA_model.keras")

    ## Preprocess
    df_preprocess = preprocess_api(ticker, df, scaler_path)

    ## Predict
    prediction = predict_price(model_path, scaler_path, df_preprocess)

    return PredictionOutput.from_prediction(ticker, prediction)

@api.get("/crawl/{ticker}")
def get_rawdata(
    ticker: str
):
    """
    GET: /crawl/AAPL
    """
    # Handle GET request
    ## Crawl data
    ticker = ticker.strip().upper()
    df = crawl_data(ticker, drop_date=False)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return DataOutput.from_dataframe(ticker=ticker, df=df)



## UI Page
def index():
    return rx.el.div(
        rx.el.div(
            navbar(),
            rx.el.div(
                stock_input_form(),
                rx.el.div(
                    rx.el.div(
                        line_pred(),
                        table_pred(),
                        class_name="mt-12 w-full grid grid-cols-2 gap-8 items-start"
                    ),
                ),
                class_name="container mx-auto p-6"
            ),
            footer(),
        ),
        class_name="justify-start items-center",
    )


app = rx.App(
    theme=rx.theme(
        appearance="light",
        panel_background="solid",
        accent_color="gold", #"gold", #teal
        radius="large"
    ),
    api_transformer=api
)

app.add_page(index, 
            route="/")

app.add_page(index, 
            route="/predict/AAPL")

app.add_page(index, 
            route="/predict/MSFT")

app.add_page(index, 
            route="/predict/NVDA")

app.add_page(index, 
            route="/predict/TSLA")

app.add_page(index, 
            route="/predict/QBTS")
