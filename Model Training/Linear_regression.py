import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


STOCK_TICKER = "GOOG"  
data = yf.download(STOCK_TICKER, period="6mo")  


data['Target'] = data['Close'].shift(-1)  


data.dropna(inplace=True)

X = data[['Open', 'High', 'Low', 'Volume']] 
y = data['Target']  


split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]


model = LinearRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"\nModel Performance:")
print(f"Mean Squared Error: {mse:.4f}")
print(f"R² Score: {r2:.4f}")


dates = data.index[split:]  

plt.figure(figsize=(14, 6), dpi=150)
plt.plot(dates, y_test.values, label='Actual Price', color='blue', linewidth=2)
plt.plot(dates, y_pred, label='Predicted Price (Linear Reg)', color='red', linestyle='--', linewidth=2)

plt.title(f"{STOCK_TICKER} Actual vs Predicted Prices (Linear Regression)", fontsize=14)
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()