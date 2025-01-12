# trading_bot.py
import os
import requests
import pandas as pd
import pandas_ta as ta
from dotenv import load_dotenv
import numpy as np
import time

# Load environment variables
load_dotenv()
API_KEY = os.getenv('TRADING212_API_KEY')

# Trading212 API Base URL
BASE_URL = 'https://api.trading212.com'

# Headers for authentication
HEADERS = {'Authorization': f'Bearer {API_KEY}'}

def fetch_stock_data(symbol):
    """Fetch historical stock data for the given symbol."""
    url = f"{BASE_URL}/markets/price/{symbol}"  # Replace with the correct endpoint for historical data
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)  # Convert the response into a DataFrame
    else:
        print(f"Failed to fetch stock data: {response.status_code}")
        return pd.DataFrame()

def calculate_indicators(data):
    """Add technical indicators to the stock data."""
    data['RSI'] = ta.rsi(data['close'], length=14).fillna(np.nan)
    data['MACD'] = ta.macd(data['close']).macd.fillna(np.nan)
    data['MFI'] = ta.mfi(data['high'], data['low'], data['close'], data['volume']).fillna(np.nan)
    return data

def generate_signal(data):
    """Generate buy/sell signals based on indicators."""
    if data['RSI'].iloc[-1] < 30 and data['MACD'].iloc[-1] > 0:
        return 'BUY'
    elif data['RSI'].iloc[-1] > 70 and data['MACD'].iloc[-1] < 0:
        return 'SELL'
    return 'HOLD'

def execute_trade(symbol, action, quantity):
    """Execute a trade via the Trading212 API."""
    trade_data = {
        "instrument": symbol,
        "quantity": quantity,
        "orderType": "Market",
        "direction": action
    }
    response = requests.post(f"{BASE_URL}/orders", headers=HEADERS, json=trade_data)
    if response.status_code == 200:
        print(f"Trade executed: {response.json()}")
    else:
        print(f"Failed to execute trade: {response.status_code}")

def main():
    # Example: Trade Apple stock
    symbol = "AAPL"  # Replace with your desired symbol
    data = fetch_stock_data(symbol)
    if data.empty:
        print("No data fetched, skipping...")
        return

    data = calculate_indicators(data)

    signal = generate_signal(data)
    print(f"Generated Signal: {signal}")

    if signal in ['BUY', 'SELL']:
        execute_trade(symbol, signal, quantity=1)  # Example quantity
    else:
        print("No action taken.")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(300)  # Run every 5 minutes
