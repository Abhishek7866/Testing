import streamlit as st
from apd_azure_priceprediction import get_prediction

st.title("📈 Stock Price Predictor (LSTM + Indicators)")
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):")

if st.button("Predict"):
    if ticker:
        try:
            prediction = get_prediction(ticker.upper())
            st.success(f"Predicted Closing Price: ${prediction:.2f}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
    else:
        st.warning("Please enter a valid stock ticker.")