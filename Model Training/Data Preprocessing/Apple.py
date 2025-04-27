import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import os
import joblib

# Step 1: Load raw data
data = pd.read_csv(r"D:\Time Forge\project\Model Training\Stock Data\AAPL_historical_data.csv")

# Step 2: Preprocess the data
data['Target'] = data['Close'].shift(-1)  # Predict the next day's closing price
data.dropna(inplace=True)

X = data[['Open', 'High', 'Low', 'Close', 'Volume']]  # Input features
y = data['Target']  # Target variable

# Normalize the data
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Scale the target variable
y_scaler = MinMaxScaler()
y_scaled = y_scaler.fit_transform(np.array(y).reshape(-1, 1))

# Split the data
X_train, X_test, y_train_scaled, y_test_scaled = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Step 3: Save the preprocessed data and scaler
os.makedirs("preprocessed_data", exist_ok=True)
np.save('preprocessed_data/X_train.npy', X_train)
np.save('preprocessed_data/X_test.npy', X_test)
np.save('preprocessed_data/y_train.npy', y_train_scaled)
np.save('preprocessed_data/y_test.npy', y_test_scaled)
joblib.dump(y_scaler, 'preprocessed_data/y_scaler.pkl')

# Step 4: Train the model
model = LinearRegression()
model.fit(X_train, y_train_scaled.ravel())

# Step 5: Evaluate the model
y_pred_scaled = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test_scaled, y_pred_scaled))
mae = mean_absolute_error(y_test_scaled, y_pred_scaled)

print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"Mean Absolute Error (MAE): {mae}")

# Step 6: Save the model
joblib.dump(model, 'preprocessed_data/linear_regression_model.pkl')

# Step 7: Inverse transform predictions (if needed)
y_pred_actual = y_scaler.inverse_transform(y_pred_scaled.reshape(-1, 1))
y_test_actual = y_scaler.inverse_transform(y_test_scaled)