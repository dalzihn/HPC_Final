import pandas as pd
import numpy as np
from tensorflow import keras
import joblib


# Global vars
features = ["Close"]
CLOSE_IDX = features.index("Close")
SEQ_LEN = 60

def preprocess_api(
    ticker: str,
    data: pd.DataFrame,
    scaler_path: str,    
) -> np.array:
    """
    Preprocess the data for prediction

    Args:
        ticker (str): The ticker of the stock
        data (pd.DataFrame): The data to preprocess
        scaler (joblib): The scaler to use for normalisation
    
    Returns:
        tuple[np.array, np.array]: The preprocessed data 
    """
    scaler = joblib.load(scaler_path)
    data = data[features].values
    normalised_data = scaler.transform(data)
    predict_data = create_sequences_api(normalised_data, SEQ_LEN)
    predict_data = predict_data.reshape((predict_data.shape[0], SEQ_LEN, len(features)))
    return predict_data
    

def predict_price(
    model_path: str,
    scaler_path: str,
    data: np.array,
) -> np.array:
    """
    Predict the price of the stock

    Args:
        model_path (str): The path to the model
        scaler_path (str): The path to the scaler
        data (np.array): The data to predict
    
    Returns:
        np.array: The predicted price
    """
    scaler = joblib.load(scaler_path)
    model = keras.models.load_model(model_path)
    predict_data = model.predict(data)
    predict_data = scaler.inverse_transform(predict_data)   
    return predict_data
