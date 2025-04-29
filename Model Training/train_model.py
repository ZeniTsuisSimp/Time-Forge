import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import os

# Step 1: Load raw data
data = pd.read_csv(r"F:\Time Forge\Time Forge\project\Model Training\Stock Data\Googl_historical_data.csv")

# Step 2: Preprocess the data
data['Target'] = data['Close'].shift(-1)  # Predict next day's closing price
data.dropna(inplace=True)

# Features and target
features = ['Open', 'High', 'Low', 'Close', 'Volume']
X = data[features].values
y = data['Target'].values

# Normalize features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Define time step for sequences
time_step = 60  # Use 60 days of history to predict next day's Close price

def create_sequences(features, target, time_step):
    X_seq, y_seq = [], []
    for i in range(len(features) - time_step):
        X_seq.append(features[i:i + time_step])
        y_seq.append(target[i + time_step])
    return np.array(X_seq), np.array(y_seq)

X_seq, y_seq = create_sequences(X_scaled, y, time_step)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42, shuffle=False)

# Step 3: Build the LSTM model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(1)  # Predicting next day closing price
])

model.compile(optimizer='adam', loss='mse')

# Add early stopping to prevent overfitting
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Step 4: Train the model
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.1,
    callbacks=[early_stop],
    verbose=1
)

# Step 5: Evaluate the model
train_loss = model.evaluate(X_train, y_train, verbose=0)
test_loss = model.evaluate(X_test, y_test, verbose=0)

print(f"Training Loss (MSE): {train_loss}")
print(f"Testing Loss (MSE): {test_loss}")

# Step 6: Save the trained model and scaler
model_path = 'Googl_lstm_model.h5'  # HDF5 format for Keras models
scaler_path = 'Googl_scaler.pkl'

model.save(model_path)
joblib.dump(scaler, scaler_path)

# Print file paths
print(f"LSTM Model saved at: {os.path.abspath(model_path)}")
print(f"Scaler saved at: {os.path.abspath(scaler_path)}")