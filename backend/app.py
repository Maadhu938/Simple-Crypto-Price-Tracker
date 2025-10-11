from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import requests
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)
CORS(app)

LOOKBACK = 60
MODEL_PATH = "models/lstm_weights.h5"

# Load once at startup
model = load_model(MODEL_PATH)

def fetch_bitcoin_prices(days=LOOKBACK):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    r = requests.get(url, params=params)
    data = r.json()
    prices = [p[1] for p in data['prices']]
    return np.array(prices)

@app.route("/predict", methods=["POST"])
def predict():
    prices = fetch_bitcoin_prices(days=LOOKBACK+1)
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled = scaler.fit_transform(prices.reshape(-1,1))
    input_window = scaled[-LOOKBACK:].reshape(1, LOOKBACK, 1)
    predicted_norm = model.predict(input_window)
    predicted_price = scaler.inverse_transform(predicted_norm)[0,0]
    return jsonify({"predicted_price": round(float(predicted_price),2)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
