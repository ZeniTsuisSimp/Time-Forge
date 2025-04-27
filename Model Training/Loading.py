import joblib

# Load the model and scaler
model = joblib.load('linear_regression_model.pkl')
scaler = joblib.load('scaler.pkl')

# Example input (replace with actual data)
sample_input = [[150]][[152]][[149]][[151]][[1000000]]  # [Open, High, Low, Close, Volume]

# Scale the input
scaled_input = scaler.transform(sample_input)

# Make a prediction
predicted_price = model.predict(scaled_input)[0]
print(f"Predicted Price: {predicted_price}")