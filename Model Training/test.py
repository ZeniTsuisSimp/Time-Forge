import yfinance as yf
import pandas as pd

# Fetch live stock data for the given ticker
stock_symbol = "AAPL"
stock_data = yf.download(stock_symbol, period="1d")  # Fetch latest data

# Extract features from the latest data
latest_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']].iloc[-1].values.reshape(1, -1)

# Define feature names
feature_names = ['Open', 'High', 'Low', 'Close', 'Volume']

# Convert to DataFrame with feature names
latest_data_df = pd.DataFrame(latest_data, columns=feature_names)

from sklearn.preprocessing import StandardScaler

# Initialize and fit the scaler with dummy data (replace with actual training data)
scaler = StandardScaler()
dummy_data = [[1, 1, 1, 1, 1]]  # Replace with actual data for fitting
scaler.fit(dummy_data)

# Scale the input
scaled_input = scaler.transform(latest_data_df)
print("Scaled Input:", scaled_input)