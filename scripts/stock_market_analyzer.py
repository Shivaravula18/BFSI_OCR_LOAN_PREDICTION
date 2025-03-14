import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf  # ✅ Yahoo Finance for stock data

# ✅ Stock Market Analyzer (Live Data)
def compare_stocks():
    st.header("📈 Live Stock Market Analyzer")

    # 🔹 Time periods for comparison
    time_periods = {
        "1 Week": "7d",
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "5 Years": "5y",
        "All Time": "max"
    }

    # 🔹 User input for stocks
    stock1 = st.text_input("🔹 Enter First Stock Symbol (e.g., AAPL for Apple)", "AAPL").upper()
    stock2 = st.text_input("🔹 Enter Second Stock Symbol (e.g., TSLA for Tesla)", "TSLA").upper()
    time_period = st.selectbox("📊 Select Time Period", list(time_periods.keys()))

    if st.button("Compare Stocks"):
        try:
            # ✅ Get the selected period
            period = time_periods[time_period]

            # ✅ Fetch stock data from Yahoo Finance
            stock1_data = yf.download(stock1, period=period, interval="1d")["Close"]
            stock2_data = yf.download(stock2, period=period, interval="1d")["Close"]

            # ✅ Check if data is available
            if stock1_data.empty or stock2_data.empty:
                st.error("⚠️ No stock data available. Try selecting another stock or period.")
                return

            # ✅ Create DataFrame with proper structure
            df = pd.DataFrame({
                stock1: stock1_data.squeeze(),  # ✅ Ensure 1D array
                stock2: stock2_data.squeeze()   # ✅ Ensure 1D array
            })

            df.index = pd.to_datetime(df.index)  # ✅ Set Date index

            # ✅ Plot Stock Comparison
            plt.figure(figsize=(10, 5))
            sns.lineplot(data=df, linewidth=2.5)
            plt.title(f"Stock Comparison: {stock1} vs {stock2}")
            plt.xlabel("Date")
            plt.ylabel("Stock Price (USD)")
            plt.legend([stock1, stock2])
            st.pyplot(plt)

        except Exception as e:
            st.error(f"⚠️ Error fetching stock data: {e}")
