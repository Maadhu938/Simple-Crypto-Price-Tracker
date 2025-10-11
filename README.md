Crypto Price Tracker & LSTM Predictor
A full-stack project to fetch, display, and predict real-time cryptocurrency prices using CoinGecko API (frontend) and advanced LSTM machine learning (Python backend).

🚀 Features
Real-time crypto prices: Fetches live prices for top cryptocurrencies from the CoinGecko API.

Modern frontend: Interactive UI built with HTML, CSS, and JavaScript (see /frontend).

ML backend: Python Flask API with LSTM model for price prediction (see /backend)

🛠 Getting Started
1. Frontend (User Interface)
Open frontend/index.html in your browser.

For real API-demo: ensure backend server is running.

2. Backend (Python LSTM API)
Go to the backend folder:

bash
cd backend
pip install -r requirements.txt
python app.py
The backend will run at http://localhost:5000 by default.

🧠 How Predictions Work
Input: Recent historical prices for a specific coin (e.g., Bitcoin).

LSTM neural network predicts future prices based on past data.

The backend returns predicted price to the frontend.

📝 Credits
Built with CoinGecko API for realtime data.

LSTM implementation powered by TensorFlow/Keras.

UI inspired by CoinGecko and popular crypto dashboards.

📄 License
MIT License
