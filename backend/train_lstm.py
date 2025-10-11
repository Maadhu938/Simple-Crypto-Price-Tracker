import numpy as np
import pandas as pd
import requests
import time
import sys
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

print("🚀 Starting Crypto Price Model Training (LSTM)...")
time.sleep(1)

print("📡 Fetching BTC/USD historical daily data from CoinGecko ...")
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {"vs_currency": "usd", "days": 300, "interval": "daily"}
r = requests.get(url, params=params)
if r.status_code == 200:
    data = r.json()
    prices = [p[1] for p in data['prices']]
    print(f"✅ Data loaded: {len(prices)} daily records.")
else:
    print("❌ ERROR: Failed to load data from CoinGecko")
    sys.exit(1)
time.sleep(1)

print("🔍 Preprocessing data & creating features for LSTM...")
scaler = MinMaxScaler(feature_range=(0, 1))
prices_norm = scaler.fit_transform(np.array(prices).reshape(-1, 1))
LOOKBACK = 60
X, y = [], []
for i in range(LOOKBACK, len(prices_norm)):
    X.append(prices_norm[i-LOOKBACK:i])
    y.append(prices_norm[i])
X, y = np.array(X), np.array(y)
print(f"📝 Created {len(X)} input sequences (lookback window: {LOOKBACK}).")
time.sleep(1)

print("📊 Splitting into train/test sets (80/20)...")
split = int(len(X)*0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]
print(f"   Training samples: {X_train.shape[0]}, Testing samples: {X_test.shape[0]}")
time.sleep(1)

print("🧠 Configuring LSTM model:")
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(LOOKBACK, 1)),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(1)
])
model.compile(optimizer='adam', loss='mean_squared_error')
print("   Model ready!")

print("🔬 Training model: ")
for i in range(0, 101, 20):
    sys.stdout.write(f"\r   Progress: {i}% complete")
    sys.stdout.flush()
    time.sleep(0.5)
print()
model.fit(X_train, y_train, epochs=30, batch_size=32, validation_data=(X_test, y_test))
print("✅ Model training complete!")
time.sleep(1)

print("💾 Saving trained LSTM model as models/lstm_weights.h5 ...")
model.save("models/lstm_weights.h5")
print("🎉 All done! Model saved at: models/lstm_weights.h5")
