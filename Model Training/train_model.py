import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import joblib
import os

# Step 1: Load raw data
data = pd.read_csv(r"D:\Time Forge\project\Model Training\Stock Data\TCS.NS_historical_data.csv")

# Step 2: Preprocess the data
data['Target'] = data['Close'].shift(-1)  # Predict the next day's closing price
data.dropna(inplace=True)

X = data[['Open', 'High', 'Low', 'Close', 'Volume']]  # Input features
y = data['Target']  # Target variable

# Normalize the data
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 3: Train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 4: Evaluate the model
y_pred = model.predict(X_test)

# Calculate evaluation metrics
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"Mean Absolute Error (MAE): {mae}")

# Step 5: Save the trained model and scaler in the current directory
model_path = 'linear_regression_model.pkl'  # Saved in the current directory
scaler_path = 'scaler.pkl'  # Saved in the current directory

joblib.dump(model, model_path)
joblib.dump(scaler, scaler_path)

# Print the file paths
print(f"Model saved at: {os.path.abspath(model_path)}")
print(f"Scaler saved at: {os.path.abspath(scaler_path)}")