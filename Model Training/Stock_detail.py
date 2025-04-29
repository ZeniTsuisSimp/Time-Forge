import yfinance as yf

# Download historical data for a stock (e.g., Apple Inc.)
ticker = "Googl"
data = yf.download(ticker, start="2015-01-01", end="2025-01-01")

# Save the data to a CSV file
data.to_csv(f"{ticker}_historical_data.csv")