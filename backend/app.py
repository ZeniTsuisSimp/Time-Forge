from flask import Flask, request, jsonify
import numpy as np
import joblib
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or scaler is None:
        return jsonify({'error': 'Model or scaler not loaded'}), 500

    try:
        # Get JSON data from the frontend
        data = request.get_json()

        # Extract inputs
        stock_symbol = data['stock_symbol']
        number_of_shares = int(data['number_of_shares'])  # Number of shares instead of investment amount
        prediction_period = data['prediction_period']

        # Fetch live stock data for the given ticker
        try:
            stock_data = yf.Ticker(stock_symbol)
            latest_data = stock_data.history(period="1d")  # Fetch latest trading day's data
            if latest_data.empty:
                return jsonify({'error': f"No data found for ticker: {stock_symbol}"}), 400
        except Exception as e:
            return jsonify({'error': f"Failed to fetch data for ticker: {stock_symbol}. Error: {str(e)}"}), 400

        # Extract features from the latest data
        open_price = latest_data['Open'].iloc[-1]
        high_price = latest_data['High'].iloc[-1]
        low_price = latest_data['Low'].iloc[-1]
        close_price = latest_data['Close'].iloc[-1]
        volume = latest_data['Volume'].iloc[-1]

        # Detect currency based on the stock's exchange
        stock_info = stock_data.info
        exchange = stock_info.get('exchange', '').upper()
        currency = 'INR' if exchange in ['NSE', 'BSE'] else 'USD'

        # Create input for the model
        sample_input = [[open_price, high_price, low_price, close_price, volume]]
        scaled_input = scaler.transform(sample_input)

        # Use the model to make a raw prediction
        predicted_price = model.predict(scaled_input)[0]

        # Cap unrealistic predictions
        MAX_PRICE_CHANGE = 100  # Limit to 100% price change
        price_change_percentage = ((predicted_price - close_price) / close_price) * 100
        if price_change_percentage > MAX_PRICE_CHANGE:
            price_change_percentage = MAX_PRICE_CHANGE
            predicted_price = close_price * (1 + (MAX_PRICE_CHANGE / 100))

        # Calculate total cost and final value based on the number of shares
        total_cost = close_price * number_of_shares
        final_value = predicted_price * number_of_shares
        profit = final_value - total_cost

        # Generate recommendation based on price change percentage
        recommendation = ""
        pros = []
        cons = []

        if price_change_percentage > 10:
            recommendation = "Strong Buy"
            pros.append("The stock is predicted to grow significantly.")
            pros.append("Historical performance indicates upward trends.")
            cons.append("Market volatility may still pose risks.")
        elif price_change_percentage > 5:
            recommendation = "Buy"
            pros.append("The stock is expected to grow steadily.")
            pros.append("Moderate risk with potential for good returns.")
            cons.append("Short-term fluctuations could impact gains.")
        elif price_change_percentage > 0:
            recommendation = "Hold"
            pros.append("The stock is expected to maintain its value.")
            cons.append("Limited growth potential in the short term.")
        else:
            recommendation = "Avoid"
            cons.append("The stock is predicted to decline in value.")
            cons.append("Market conditions suggest higher risk.")
            pros.append("Selling now might help avoid future losses.")

        # Return the prediction as JSON
        return jsonify({
            'stock_symbol': stock_symbol,
            'currency': currency,  # Display currency based on exchange
            'current_price': round(close_price, 2),
            'predicted_price': round(predicted_price, 2),
            'price_change_percentage': round(price_change_percentage, 2),
            'recommendation': recommendation,
            'number_of_shares': number_of_shares,
            'total_cost': round(total_cost, 2),
            'profit': round(profit, 2),
            'final_value': round(final_value, 2),
            'analysis': {
                'pros': pros,
                'cons': cons
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)