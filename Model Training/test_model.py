import numpy as np
import joblib
import yfinance as yf
import matplotlib.pyplot as plt

# Load the trained model and scaler
MODEL_PATH = r'D:\Time Forge\project\public\linear_regression_model.pkl'
SCALER_PATH = r'D:\Time Forge\project\public\scaler.pkl'

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    model = None
    scaler = None

def predict_future_price(stock_symbol, future_days=14):
    if model is None or scaler is None:
        print("Model or scaler not loaded.")
        return

    # Fetch live stock data for the given ticker
    try:
        stock_data = yf.Ticker(stock_symbol)
        latest_data = stock_data.history(period="1mo")  # Fetch recent 1 month of data
        if latest_data.empty:
            print(f"No data found for ticker: {stock_symbol}")
            return
    except Exception as e:
        print(f"Failed to fetch data for ticker: {stock_symbol}. Error: {str(e)}")
        return

    # Extract the latest day's features
    open_price = latest_data['Open'].iloc[-1]
    high_price = latest_data['High'].iloc[-1]
    low_price = latest_data['Low'].iloc[-1]
    close_price = latest_data['Close'].iloc[-1]
    volume = latest_data['Volume'].iloc[-1]

    # Create input for the model
    sample_input = [[open_price, high_price, low_price, close_price, volume]]
    scaled_input = scaler.transform(sample_input)

    # Predict future prices iteratively
    predicted_prices = [close_price]  # Start with the latest closing price
    for _ in range(future_days):
        # Predict the next day's price
        next_day_price = model.predict(scaled_input)[0]
        predicted_prices.append(next_day_price)

        # Update the input features for the next prediction
        open_price = close_price
        high_price = max(high_price, next_day_price)
        low_price = min(low_price, next_day_price)
        close_price = next_day_price
        volume = volume * 1.01  # Simulate slight increase in volume over time
        sample_input = [[open_price, high_price, low_price, close_price, volume]]
        scaled_input = scaler.transform(sample_input)

    # Plot actual vs predicted future prices
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(predicted_prices)), predicted_prices, label='Predicted Prices', color='orange', linestyle='--')
    plt.scatter(0, predicted_prices[0], color='blue', label='Current Price', zorder=5)
    plt.title(f'Predicted Stock Price for {stock_symbol} (Next {future_days} Days)')
    plt.xlabel('Days Ahead')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    # Stock symbol to predict (e.g., TCS.NS, AAPL)
    STOCK_SYMBOL = "TCS.NS"

    # Number of days to predict into the future
    FUTURE_DAYS = 14  # Predict 2 weeks ahead

    # Predict future prices
    predict_future_price(STOCK_SYMBOL, FUTURE_DAYS)