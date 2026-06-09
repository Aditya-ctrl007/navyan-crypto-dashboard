"""
Real-Time Cryptocurrency Data Fetcher
Navyan Data Analytics Internship - Project 3
Author: Singh Aditya Manoj Kumar
"""

import requests
import pandas as pd


def get_crypto_prices():
    """
    Fetches live prices for top 10 cryptocurrencies from CoinGecko.
    No API key needed — completely free!
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data)
        df = df[[
            "name", "symbol", "current_price",
            "market_cap", "price_change_percentage_24h",
            "total_volume", "high_24h", "low_24h"
        ]]

        df.columns = [
            "Name", "Symbol", "Price (USD)",
            "Market Cap", "24h Change (%)",
            "Volume (24h)", "24h High", "24h Low"
        ]

        df["Symbol"] = df["Symbol"].str.upper()
        return df

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


# Test: run this file directly to check API works
if __name__ == "__main__":
    print("Fetching live crypto data from CoinGecko...")
    df = get_crypto_prices()
    if df is not None:
        print("Data fetched successfully!")
        print(df[["Name", "Price (USD)", "24h Change (%)"]].to_string())
    else:
        print("Failed to fetch data. Check your internet connection.")
