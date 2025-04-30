import numpy as np
import joblib
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Load the trained model and scaler
MODEL_PATH = r'D:\Time Forge1\Time Forge\Time Forge\project\Model Training\Models\Googl_model.pkl'
SCALER_PATH = r'D:\Time Forge1\Time Forge\Time Forge\project\Model Training\Scaler\Googl_scaler.pkl'

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    model = None
    scaler = None

def predict_future_price(stock_symbol, historical_period="6mo", future_days=14):
    if model is None or scaler is None:
        print("Model or scaler not loaded.")
        return

    # Fetch historical stock data for the specified period
    try:
        stock_data = yf.Ticker(stock_symbol)
        historical_data = stock_data.history(period=historical_period)  # Fetch data for the given period
        if historical_data.empty:
            print(f"No data found for ticker: {stock_symbol}")
            return
    except Exception as e:
        print(f"Failed to fetch data for ticker: {stock_symbol}. Error: {str(e)}")
        return

    # Extract the latest day's features
    open_price = historical_data['Open'].iloc[-1]
    high_price = historical_data['High'].iloc[-1]
    low_price = historical_data['Low'].iloc[-1]
    close_price = historical_data['Close'].iloc[-1]
    volume = historical_data['Volume'].iloc[-1]

    # Create input for the model
    sample_input = [[open_price, high_price, low_price, close_price, volume]]
    scaled_input = scaler.transform(sample_input)

    # Predict future prices iteratively with simulated fluctuations
    predicted_prices = [close_price]  # Start with the latest closing price
    for _ in range(future_days):
        # Predict the next day's price
        next_day_price = model.predict(scaled_input)[0]

        # Add random fluctuations to simulate volatility
        fluctuation = np.random.normal(0, 0.01) * next_day_price  # ±1% fluctuation
        next_day_price += fluctuation

        # Ensure the price doesn't go negative
        next_day_price = max(next_day_price, 0)

        predicted_prices.append(next_day_price)

        # Update the input features for the next prediction
        open_price = close_price
        high_price = max(high_price, next_day_price)
        low_price = min(low_price, next_day_price)
        close_price = next_day_price
        volume = volume * 1.01  # Simulate slight increase in volume over time
        sample_input = [[open_price, high_price, low_price, close_price, volume]]
        scaled_input = scaler.transform(sample_input)

    # Prepare historical prices
    historical_prices = historical_data['Close'].values

    # Combine historical and future dates
    total_days = len(historical_prices) + future_days
    historical_dates = historical_data.index
    future_dates = pd.date_range(start=historical_dates[-1], periods=future_days + 1, freq='D')[1:]

    # Plot historical and predicted prices
    plt.figure(figsize=(14, 7), dpi=150)  # Increase resolution with dpi
    plt.plot(historical_dates, historical_prices, label='Historical Prices', color='blue', linewidth=2)
    plt.plot(future_dates, predicted_prices[1:], label='Predicted Prices', color='orange', linestyle='--', linewidth=2)
    
    # Highlight key points
    plt.scatter(historical_dates[-1], historical_prices[-1], color='green', label='Latest Price', zorder=5, s=100)
    plt.scatter(future_dates[-1], predicted_prices[-1], color='red', label='Final Predicted Price', zorder=5, s=100)
    
    # Add vertical line to separate historical and predicted data
    plt.axvline(x=historical_dates[-1], color='gray', linestyle='--', alpha=0.7)
    plt.text(historical_dates[-1], max(historical_prices), ' Prediction Start ', rotation=90, verticalalignment='top')

    # Add gridlines and formatting
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.title(f'Historical and Predicted Stock Price for {stock_symbol}', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Stock Price', fontsize=14)
    plt.legend(fontsize=12)
    plt.tight_layout()

    # Show the plot
    plt.show()

if __name__ == '__main__':
    # Stock symbol to predict (e.g., TCS.NS, AAPL)
    STOCK_SYMBOL = "Googl"

    # Historical period (e.g., "1y" for 1 year, "6mo" for 6 months, "3mo" for 3 months)
    HISTORICAL_PERIOD = "6mo"

    # Number of days to predict into the future
    FUTURE_DAYS = 14  # Predict 2 weeks ahead

    # Predict future prices
    predict_future_price(STOCK_SYMBOL, HISTORICAL_PERIOD, FUTURE_DAYS)