# predict.py

import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.losses import MeanSquaredError
import os

def get_prediction(ticker):
    # Load the LSTM model
    model_path = "lstm_model2.h5"   
    model = load_model(model_path, custom_objects={'mse': MeanSquaredError()}, compile=False)

    # Download the last 90 days to ensure indicator calculation works
    df = yf.download(ticker, period="180d", interval="1d")
    if df.empty or 'Close' not in df.columns:
        raise ValueError(f"No stock data found for ticker: {ticker}")

    df1 = df.copy()

    # Compute technical indicators
    df1['SMA_20'] = ta.sma(df1['Close'], length=20)
    df1['EMA_20'] = ta.ema(df1['Close'], length=20)
    df1['RSI'] = ta.rsi(df1['Close'], length=14)
    
        # Compute MACD
    macd = ta.macd(df1['Close'])

    # If MACD failed, create dummy columns of NaNs
    if macd is None:
        macd = df1[['Close']].copy()
        macd['MACD_12_26_9'] = np.nan
        macd['MACDs_12_26_9'] = np.nan
    else:
        # Ensure the required columns exist
        for col in ['MACD_12_26_9', 'MACDs_12_26_9']:
            if col not in macd.columns:
                macd[col] = np.nan

    # Append MACD columns to df1
    df1['MACD'] = macd['MACD_12_26_9']
    df1['MACD_signal'] = macd['MACDs_12_26_9']

    # Fill missing values using forward fill, then backward fill as fallback
    df1['MACD'] = df1['MACD'].fillna(method='ffill').fillna(method='bfill')
    df1['MACD_signal'] = df1['MACD_signal'].fillna(method='ffill').fillna(method='bfill')

    df1 = df1.dropna()

    # If dropna removed everything, fallback with dummy indicator values
    if df1.empty:
        last_close = df['Close'].iloc[-1] if not df.empty else 100.0  # fallback if even df is empty
        dummy_row = {
            'Close': last_close,
            'SMA_20': last_close,
            'EMA_20': last_close,
            'RSI': 50.0,
            'MACD': 0.0,
            'MACD_signal': 0.0
        }
        data = pd.DataFrame([dummy_row] * 30)
    else:
        # Get last rows
        data = df1[['Close', 'SMA_20', 'EMA_20', 'RSI', 'MACD', 'MACD_signal']].tail(30)

    # If fewer than 30 rows, pad with last row
    if data.shape[0] < 30:
        missing = 30 - data.shape[0]
        last_row = data.iloc[-1:]
        padding = pd.concat([last_row] * missing, ignore_index=True)
        data = pd.concat([padding, data], ignore_index=True)

    # Normalize the features
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    # Reshape to (1, 30, 6)
    X_input = np.reshape(scaled_data, (1, 30, 6))

    # Predict
    prediction = model.predict(X_input)
    prediction = scaler.inverse_transform([[prediction[0][0]] + [0]*5])  # only reverse scale the 'Close' value

    return float(prediction[0][0])